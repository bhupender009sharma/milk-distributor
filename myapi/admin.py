from django.contrib import admin
from myapi import models
# Register your models here.

admin.site.register(models.Customers)
admin.site.register(models.DistributionRequired)
admin.site.register(models.DailyDistribution)
'''
{
"type_of_milk": "cow",
"price": 44,
"unit": "litre",
"time_of_delivery": "morning"
}
'''
