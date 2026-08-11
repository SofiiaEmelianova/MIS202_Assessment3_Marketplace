from django.shortcuts import render, redirect
from .models import ProductListing

def browse_listings(request):
    listings = ProductListing.objects.filter(status='approved')
    return render(request, 'browse-listings.html', {'listings': listings})


def create_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        availability = request.POST.get('availability')
        condition = request.POST.get('condition')
        category = request.POST.get('category')

        errors = []

        if not price or float(price) <= 0:
            errors.append('Price must be a positive number.')

        if not condition:
            errors.append('Please select a condition.')

        if not title:
            errors.append('Title is required.')

        if errors:
            return render(request, 'create-listing.html', {'errors': errors})

        new_listing = ProductListing(
            title=title,
            description=description,
            price=price,
            discount_price=discount_price if discount_price else None,
            availability=availability,
            condition=condition,
            category=category,
            status='under_review',
        )
        new_listing.save()

        return redirect('browse_listings')

    return render(request, 'create-listing.html')