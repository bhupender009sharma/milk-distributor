from rest_framework import response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from myapi import serializers,models
from .models import Customers,DistributionRequired
from datetime import date

class Hello(APIView):
    
    serializer_class = serializers.HelloSerializer

    def get(self,request,format=None):
        an_apiview = [
            'welcome',
            'Home Page',
        ]

        return Response({'message':'Hello', 'an_apiview':an_apiview})

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )    

class CustomersList(APIView):
    serializer_class = serializers.CustomersSerializer
    qs = models.Customers.objects.all()

    def get(self,request,format=None):
        '''Lists all customers'''
        customers = Customers.objects.all()
        serializer = serializers.CustomersSerializer(customers,many=True)
        return Response(serializer.data,status=200)

    def post(self,request):
        """Add Customers"""
        serializer = serializers.CustomersSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message":"Customer successfully added.", "errors":""},
                status=201
                )
        return Response(
                {"message":"", "errors":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
                )
            
    
class CustomersUpdate(APIView):
    serializer_class = serializers.CustomersSerializer
    def put(self, request, pk):

        obj = get_object_or_404(Customers.objects.all(), pk=pk)
        serializer = serializers.CustomersSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            return Response(
                            {"message":"Customer successfully updated.", "errors":""},
                            status=201
                            )
        return Response(
                        {"message":"", "errors":serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                        )
class ArchiveCustomers(APIView):
        
    def patch(self,request,pk):
        obj = get_object_or_404(Customers.objects.all(), pk=pk)
        data={'is_active':"False"}
        serializer = serializers.CustomersSerializer(instance=obj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            return Response(
                            {"message":"Customer successfully archived.", "errors":""},
                            status=200
                            )
        return Response(
                        {"message":"", "errors":serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                        )

class UnarchiveCustomers(APIView):
    def patch(self,request,pk):
        obj = get_object_or_404(Customers.objects.all(), pk=pk)
        data={'is_active':"True"}
        serializer = serializers.CustomersSerializer(instance=obj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            return Response(
                            {"message":"Customer successfully marked as active.", "errors":""},
                            status=200
                            )
        return Response(
                        {"message":"", "errors":serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                        )
class ArchivedList(APIView):
    def get(self,request,format=None):
        customers = Customers.objects.filter(is_active=False).values()
        serializer = serializers.CustomersSerializer(customers,many=True)
        return Response(serializer.data,status=200)

class MilkDistribution(APIView):
    serializer_class = serializers.DistributionRequiredSerializer
    def get(self,request,pk):
        customers = Customers.objects.get(id=pk)
        obj=customers.distributionrequired_set.all()
        serializer = serializers.DistributionRequiredSerializer(obj,many=True)
        return Response(serializer.data,status=200)

    def post(self,request,pk):

        #data=serializers.DistributionRequiredSerializer(data =request.data)
        
        '''customerid =pk
        type_of_milk= request.data.get('type_of_milk')
        price=request.data.get('price')
        unit=request.data.get('unit')
        time_of_delivery=request.data.get('time_of_delivery')

        data={
            'customerid' :customerid,
            'type_of_milk':type_of_milk,
            'price':price,
            'unit':unit,
            'time_of_delivery':time_of_delivery,
        }'''
        obj = get_object_or_404(Customers.objects.all(), pk=pk)
        
        #serializer = serializers.DistributionRequiredSerializer(data =request.data)
        serializer = serializers.DistributionRequiredSerializer(data =request.data,context={"pk":pk})


        

        if serializer.is_valid():
            serializer.save()
            errors = serializer.errors
            return Response(
                {"message":"Milk details successfully added.", "errors":""},
                status=200
                )
        return Response(
                        {"message":"", "errors":serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                        )
    
    def put(self, request, pk):

        obj = get_object_or_404(Customers.objects.all(), pk=pk)
        serializer = serializers.CustomersSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            return Response(
                            {"message":"Customer successfully updated.", "errors":""},
                            status=201
                            )
        return Response(
                        {"message":"", "errors":serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                        )

class UpdateDistribution(APIView):
    serializer_class = serializers.DistributionRequiredSerializer
    
    def put(self, request, pk,d):

        cus = get_object_or_404(Customers.objects.all(), pk=pk)
        obj = cus.distributionrequired_set.get(id=d)
        serializer = serializers.DistributionRequiredSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            return Response(
                            {"message":"Customer successfully updated.", "errors":""},
                            status=200
                            )
        return Response(
                        {"message":"", "errors":serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                        )

class CowVsBuffalo(APIView):

    def get(self,request,start_date,end_date):
        start_date =  date.fromisoformat(start_date)
        end_date =  date.fromisoformat(end_date)

        cmilk=0
        cearning=0
        bmilk=0
        bearning=0
        cquantity=0
        bquantity=0
        cus = Customers.objects.all()
        for c in cus:
            for dis in c.distributionrequired_set.all():
                if dis.type_of_milk == "cow":
                    cmilk = dis.price
                    for dai in c.dailydistribution_set.all():
                        if dai.type_of_milk == "cow" and dai.delivered_at >= start_date and dai.delivered_at<= end_date:
                            cearning += cmilk*dai.quantity
                            cquantity+=dai.quantity
                
                elif dis.type_of_milk == "buffalo":
                    bmilk = dis.price
                    for dai in c.dailydistribution_set.all():
                        if dai.type_of_milk == "buffalo" and dai.delivered_at >= start_date and dai.delivered_at<= end_date:
                            bearning += bmilk*dai.quantity
                            bquantity+=dai.quantity


        res=[
                {
                    "type_of_milk":"cow",
                    "total_quantity":cquantity,
                    "total_earning":cearning
                },
                {
                    "type_of_milk":"cow",
                    "total_quantity":bquantity,
                    "total_earning":bearning
                }
            ]
        return Response(res,status=200)

class TotalEarning(APIView):
    def get(self,request,start_date,end_date):
        start_date =  date.fromisoformat(start_date)
        end_date =  date.fromisoformat(end_date)

        '''{
            "customer_id": "",
            "total_earning": "",
            [{
            "type_of_milk": "",
            "total_quantity": "",
            "cost": ""
            }, {
            "type_of_milk": "",
            "total_quantity": "",
            "cost": ""
            }]
        }'''
        customers= Customers.objects.all()
        serializer = serializers.TotalEarningSerializer(customers,many=True,context={"start_date":start_date,"end_date":end_date})

        return Response(serializer.data,status=200)