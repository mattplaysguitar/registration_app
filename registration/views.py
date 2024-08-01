from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import AttendeeForm
from .models import Product, Event, Registration
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.views import View
import json
from django.db.models import Sum
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.models import CustomUser


YOUR_DOMAIN = 'http://localhost:8000'

stripe.api_key = settings.STRIPE_SECRET_KEY


# Using Django
@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  event = None
  try:
    event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  # Handle the event
  if event.type == 'payment_intent.succeeded':
    payment_intent = event.data.object # contains a stripe.PaymentIntent
    # Then define and call a method to handle the successful payment intent.
    # handle_payment_intent_succeeded(payment_intent)
  elif event.type == 'payment_method.attached':
    payment_method = event.data.object # contains a stripe.PaymentMethod
    # Then define and call a method to handle the successful attachment of a PaymentMethod.
    # handle_payment_method_attached(payment_method)
  # ... handle other event types 
  else:
    print('Unhandled event type {}'.format(event.type))

  if event.type == 'charge.succeeded':
    charge = event.data.object
    billing_details =charge["billing_details"]
    email = billing_details["email"]
    user = CustomUser.objects.get(email=email)
    print(user)
    reg = Registration.objects.filter(user=user, is_paid=False)
    reg.update(is_paid=True)

  return HttpResponse(status=200)

 

class CheckoutView(TemplateView):
   template_name = "checkout.html"


class SuccessView(TemplateView):
   template_name = "success.html"


class IndexView(TemplateView):
   template_name = "index.html"
  

@csrf_exempt
def create_checkout_session(request):
    user = request.user
    line_items =[]
    item = Registration.objects.filter(user=user, is_paid=False)
    for i in item:
      new_item = {"price": i.event.stripe_price_id, 'quantity': 1,}
      line_items.append(new_item)
    print(line_items)
    try:
        session = stripe.checkout.Session.create(
            customer_email= user.email,
            ui_mode='embedded',
            line_items=line_items,
            mode='payment',
            return_url=YOUR_DOMAIN + '/return/?session_id={CHECKOUT_SESSION_ID}',
            automatic_tax={'enabled': True},
        )
        clientSecret = session.client_secret
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
    return JsonResponse({'clientSecret': clientSecret})


def session_status(self, session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    status=session.status
    customer_email=session.customer_details.email
    context = {
        "status":status,
        "customer_email":customer_email
    }
    return JsonResponse(context)


class ReturnView(TemplateView):
    template_name = "return.html"



def get_products(request):
    product = stripe.Product.list()
    for p in product:
        print(p.name)
        p_name = p.name
        p_descript = p.description
        p_id = p.id
        Product.objects.update_or_create(name=p_name, description=p_descript, stripe_product_id=p_id)
    return render(request, "products.html")



class EventView(ListView):
   model = Event
   template_name = "event_view.html"

@login_required
def event_detail_view(request, pk):
   user = request.user
   event = Event.objects.get(pk=pk)
   form = AttendeeForm()
   if request.method == "POST":
    form = AttendeeForm(request.POST)
    if form.is_valid():
          name = form.cleaned_data["name"]
          instrument = form.cleaned_data["instrument"]
          other_inst = form.cleaned_data["other_inst"]
          print(name)
          print(instrument)
          Registration.objects.update_or_create(user=user, attendee=name, event=event, is_paid=False, instrument=instrument, other_inst=other_inst)
          return HttpResponseRedirect("/cart/")
   context = {
      "event":event,
      "form":form
   }

   return render(request, "event_detail_view.html", context)

@login_required
def cart_view(request):
    user = request.user
    registration = Registration.objects.filter(user=user, is_paid=False)
     
    return render(request, "cart.html", {"registration":registration})


def event_delete(self, pk):
   reg = Registration.objects.get(pk=pk)
   reg.delete()
   return HttpResponseRedirect("/cart/")
   
   




