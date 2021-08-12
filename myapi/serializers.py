from rest_framework import response, serializers
from myapi import models
from .models import Customers,DistributionRequired,DailyDistribution
import json

class HelloSerializer(serializers.Serializer):
    name= serializers.CharField(max_length=100)

class CustomersSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customers
        fields = ['user_id','name','mobile','address','pincode','type_of_customer','is_active']
        extra_kwargs = {'is_active': {'write_only': True}}
        
    def create(self, validated_data):
        #obj = models.Customers.objects.create(**validated_data)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.name = validated_data.get('name', instance.name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.address = validated_data.get('address', instance.address)
        instance.pincode = validated_data.get('pincode',instance.pincode)
        instance.type_of_customer= validated_data.get('type_of_customer',instance.type_of_customer)
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return super().update(instance, validated_data)
    

class DistributionRequiredSerializer(serializers.Serializer):
    #cus = CustomersSerializer(many=True,required=False)
    customer_id =serializers.IntegerField()
    type_of_milk = serializers.CharField()
    price= serializers.FloatField()
    unit =serializers.CharField()
    time_of_delivery = serializers.CharField()

    class Meta:
        model = models.DistributionRequired
        fields = ('customer_id','type_of_milk','price','unit','time_of_delivery')
        #extra_kwargs = {'customerid': {'read_only': False, 'required': True}}

    def create(self, validated_data):

        #obj = models.DistributionRequired.objects.create(**validated_data)
        obj = models.Customers.objects.get(id=self.context.get("pk"))

        obj.distributionrequired_set.create(**validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):

        instance.customer_id = validated_data.get('customer_id',instance.customer_id)
        instance.type_of_milk = validated_data.get('type_of_milk',instance.type_of_milk)
        instance.price = validated_data.get('price',instance.price)
        instance.unit = validated_data.get('unit',instance.unit)
        instance.time_of_delivery = validated_data.get('time_of_delivery',instance.time_of_delivery)

        instance.save()
        return super().update(instance, validated_data)

class DailyDistributionSerializer(serializers.Serializer):
    
    customer_id =serializers.IntegerField()
    type_of_milk = serializers.CharField()
    quantity = serializers.FloatField()
    delivered_at= serializers.DateField()

    class Meta:
        model= models.DailyDistribution
        fields=('customer_id','time_period','quantity','delivered_at')


class milkSerializer(serializers.Serializer):
    
    class Meta:
        model = DistributionRequired
    
    def to_representation(self, instance):

        response_dict = {
            "type_of_milk": instance.type_of_milk,   
            "total_quantity":self.context.get("total_quantity"),  
            "cost": ""  
        }
        return response_dict

class TotalEarningSerializer(serializers.Serializer):
    '''{
            "customer_id": "",  2
            "total_earning": "",  2,3
            [{
            "type_of_milk": "",  2
            "total_quantity": "", 3
            "cost": ""  2
            }, {
            "type_of_milk": "",   2
            "total_quantity": "",  3 
            "cost": ""  2
            }]
        }'''
    
    class Meta:
        model = Customers
        fields =('customer_id','total_earning','response_dict')
        depth=1


    def to_representation(self, instance):
        start_date = self.context.get('start_date')
        end_date = self.context.get('end_date')

        tearning = 0
        cquantity = 0
        bquantity = 0
        cmilk=0
        bmilk=0

        for dis in instance.distributionrequired_set.all():
                if dis.type_of_milk == "cow":
                    cmilk = dis.price
                    for dai in instance.dailydistribution_set.all():
                        if dai.type_of_milk == "cow" and dai.delivered_at >= start_date and dai.delivered_at<= end_date:
                            tearning += cmilk*dai.quantity
                            cquantity+=dai.quantity
                
                elif dis.type_of_milk == "buffalo":
                    bmilk = dis.price
                    for dai in instance.dailydistribution_set.all():
                        if dai.type_of_milk == "buffalo" and dai.delivered_at >= start_date and dai.delivered_at<= end_date:
                            tearning += bmilk*dai.quantity
                            bquantity+=dai.quantity

        
        response_dict = [
            {
            "type_of_milk": "cow",   
            "total_quantity": cquantity,  
            "cost": cmilk
            },  
            {
            "type_of_milk": "buffalo",   
            "total_quantity": bquantity,  
            "cost": bmilk
            }
        ]
        
        result = "\"customer_id:\" %d ,\n\"total_earning:\" %d,\n %s" % (instance.id,tearning,response_dict)
        return json.dumps(result)