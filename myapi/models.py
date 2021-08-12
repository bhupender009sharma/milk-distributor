from django.db import models
from django.db.models.constraints import Deferrable
from datetime import date

# Create your models here.
class Customers(models.Model):
    user_id=models.CharField(max_length=32,blank=True)
    name= models.CharField(max_length=100, blank=True)
    mobile= models.CharField(max_length=10,blank=True)
    address = models.CharField(max_length=300,blank=True)
    pincode = models.CharField(max_length=10,blank=True)

    customer_type = (('individual','individual'),('professional','professional'),)
    type_of_customer = models.CharField(max_length=100,choices=customer_type,default='individual')

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural="Customers"

    def __str__(self):
        return self.user_id

class DistributionRequired(models.Model):
    customers =models.ForeignKey(Customers,on_delete=models.CASCADE)

    customer_id = models.PositiveIntegerField(default=1)  

    milk_type = (('cow','cow'),('buffalo','buffalo'),)
    type_of_milk = models.CharField(max_length=100,choices = milk_type,default='cow')
    
    price = models.FloatField(default=0)
    
    unit_type = (('litre','litre'),('kilogram','kilogram'),)
    unit = models.CharField(max_length=100, choices = unit_type,default='litre')

    delivery_type = (('morning','morning'),('evening','evening'),('both','both'))
    time_of_delivery = models.CharField(max_length=100, choices = delivery_type,default='morning')

    class Meta:
        verbose_name_plural="Distribution_Required"

    def __str__(self) -> str:
        return super().__str__()

class DailyDistribution(models.Model):
    customers =models.ForeignKey(Customers,on_delete=models.CASCADE)

    customer_id = models.PositiveIntegerField(default=1)  


    milk_type = (('cow','cow'),('buffalo','buffalo'),)
    type_of_milk = models.CharField(max_length=100,choices=milk_type,default='cow')

    quantity = models.FloatField(default=0)

    delivered_at= models.DateField(default=date.today)

    class Meta:
        verbose_name_plural="Daily_Distribution"

    def __str__(self) -> str:
        return super().__str__()
