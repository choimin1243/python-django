from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.list, name='list'),
    path('create/', views.create, name='restaurant-create'),
    path('update/', views.update, name='restaurant-update'),
    path('restaurant/<int:id>/delete/', views.delete, name='restaurant-delete'),

    path('restaurant/<int:id>/', views.detail, name='restaurant-detail'),
    path('restaurant/<int:restaurant_id>/review/create/', views.review_create, name='review-create'),
]

