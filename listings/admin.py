from django.contrib import admin
from .models import ProductListing, Enquiry, Rating, Message, ProductImage

admin.site.register(ProductListing)
admin.site.register(Enquiry)
admin.site.register(Rating)
admin.site.register(Message)
admin.site.register(ProductImage)