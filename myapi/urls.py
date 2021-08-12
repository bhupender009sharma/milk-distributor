from os import name
from django.urls import path
from myapi import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('hello/',views.Hello.as_view()),
    path('customers/',views.CustomersList.as_view()),
    path('customers/<int:pk>',views.CustomersUpdate.as_view()),
    path('customers/<int:pk>/archive',views.ArchiveCustomers.as_view()),
    path('customers/<int:pk>/active',views.UnarchiveCustomers.as_view()),
    path('customers/archived',views.ArchivedList.as_view()),    
    path('customers/<int:pk>/milk',views.MilkDistribution.as_view()),
    path('customers/<int:pk>/milk/<int:d>',views.UpdateDistribution.as_view()),
    path('reports/cow-vs-buffalo/<str:start_date>/<str:end_date>',views.CowVsBuffalo.as_view()),
    path('reports/total-earning/<str:start_date>/<str:end_date>',views.TotalEarning.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
