from django.db import models
from accounts.models import CustomUser
from tinymce.models import HTMLField


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    stripe_product_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField()

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
    
    def __str__(self):
        return self.price
    

class Event(models.Model):
    name = models.CharField(max_length=100)
    short_descript = HTMLField(null=True)
    description = HTMLField()
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(null=True)

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    def get_absolute_url(self):
        return reverse("event-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Registration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attendee = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=20)
    other_inst = models. CharField(max_length=30, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.event.name
    

class Instrument(models.Model):
    inst_name = models.CharField(max_length=20)
    
    def __str__(self):
            return self.inst_name
