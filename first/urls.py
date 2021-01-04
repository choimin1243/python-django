from django.urls import path

from first import views

urlpatterns=[
    path('',views.index,name='index'),
    path('select/',views.select,name="select"),
    path('result/',views.result,name="result"),
]

