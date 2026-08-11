from django.urls import path
from . import views

urlpatterns = [
    path('browse/', views.browse_listings, name='browse_listings'),
    path('create/', views.create_listing, name='create_listing'),
]
