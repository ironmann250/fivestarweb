from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(ACCOUNT)
admin.site.register(PACKAGE)
admin.site.register(PACKAGETEST)
admin.site.register(SEARCH)
admin.site.register(STATUS)
admin.site.register(PAYMENT_HOLDER)
admin.site.register(DEPARTURE_HOLDER)
admin.site.register(ARRIVED_HOLDER)
admin.site.register(PICKUP_HOLDER)