from django.urls import path
from . import views

urlpatterns = [
    path('', views.apartment, name="apartment"),
    path('category/<slug:slug>/', views.apartmentListing, name='apartments_by_category'),
    path('category/<slug:slug>/<slug:apartment_slug>', views.apartment_view, name='apartment_view'),
    path('submit_review/<int:apartment_id>/', views.submit_review, name='submit_review'),
    path('search/', views.search, name='search'),
    path('apartment_add/', views.apartment_add, name="apartment_add"),
    path('manage_request', views.manage_request, name="manage_request"),
    path('update_status/<int:id>', views.update_status, name="update_status"),
]
