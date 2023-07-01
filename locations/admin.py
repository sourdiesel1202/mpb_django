from django.contrib import admin
from locations.models import *
admin.site.register(LocationCity)
admin.site.register(LocationCountry)
admin.site.register(LocationState)
admin.site.register(Location)
