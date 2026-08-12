from django.urls import path
from . import views

urlpatterns = [
    path('browse/', views.browse_listings, name='browse_listings'),
    path('create/', views.create_listing, name='create_listing'),
    path('product/<int:listing_id>/', views.product_details, name='product_details'),
    path('chat/<int:listing_id>/', views.chat, name='chat'),
    path('favourite/<int:listing_id>/', views.toggle_favourite, name='toggle_favourite'),
path('favourites/', views.favourites_list, name='favourites_list'),
path('messages/', views.messages_list, name='messages_list'),
path('reports/', views.reports_dashboard, name='reports_dashboard'),
path('', views.home, name='home'),
path('faq/', views.faq, name='faq'),
path('seller-enquiries/', views.seller_enquiries, name='seller_enquiries'),
]
