from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:apartment_id>/', views.checkout, name="checkout"),
    path('transaction', views.transaction, name="transaction"),
    path('thankyou', views.thankyou, name="thankyou"),
]
