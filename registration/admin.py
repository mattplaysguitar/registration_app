from django.contrib import admin
from .models import Product, Price, Event, Registration, Instrument


admin.site.register(Event)
admin.site.register(Product)
admin.site.register(Price)
admin.site.register(Registration)
admin.site.register(Instrument)
