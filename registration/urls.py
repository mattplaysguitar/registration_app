from django.urls import path
from .views import my_webhook_view, create_checkout_session, IndexView, session_status, ReturnView, get_products, CheckoutView, EventView, event_detail_view, cart_view, event_delete


urlpatterns = [
    path("stripe_webhooks/", my_webhook_view, name="stripe_webhooks"),
    path("create-checkout-session/", create_checkout_session, name="embed_checkout"),
    path("index/", IndexView.as_view(), name="index"),
    path("session-status/<session_id>/", session_status, name="session-status"),
    path("return/", ReturnView.as_view(), name="return"),   
    path("get-products/", get_products, name="products"),
    path("checkout/", CheckoutView.as_view(),name="checkout"),
    path("", EventView.as_view(), name="event-list"),
    path("event-detail/<int:pk>", event_detail_view, name="event-detail"),
    path("cart/", cart_view, name="cart"),
    path("event/delete/<int:pk>", event_delete, name="event-delete"),
]