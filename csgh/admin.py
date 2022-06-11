from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(DocumentLogs)
admin.site.register(SalesQuoteLogs)
admin.site.register(RetailPrice)
admin.site.register(WHPrice)
admin.site.register(FacilityList)
admin.site.register(ApiDetail)
admin.site.register(SupplyData)

