from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import ProductListing, Enquiry, Rating, Message, ProductImage


# Shows all approved listings on the Browse page.
# Also handles search, filtering and sorting using data from the URL (GET request).
def browse_listings(request):
    listings = ProductListing.objects.filter(status='approved')

    # search by keyword in the title
    search_query = request.GET.get('search')
    if search_query:
        listings = listings.filter(title__icontains=search_query)

    # filter by condition (new / second-hand)
    # using __iexact so it doesn't matter if the letters are upper or lower case
    condition_filter = request.GET.get('condition')
    if condition_filter:
        listings = listings.filter(condition__iexact=condition_filter)

    # filter by category
    # using __iexact for the same reason - avoids "Electronics" vs "electronics" mismatches
    category_filter = request.GET.get('category')
    if category_filter:
        listings = listings.filter(category__iexact=category_filter)

    # sort by price, low to high or high to low
    sort_price = request.GET.get('sort_price')
    if sort_price == 'asc':
        listings = listings.order_by('price')
    elif sort_price == 'desc':
        listings = listings.order_by('-price')

    # sort by date, newest or oldest first
    sort_date = request.GET.get('sort_date')
    if sort_date == 'oldest':
        listings = listings.order_by('created_at')
    elif sort_date == 'newest':
        listings = listings.order_by('-created_at')

    return render(request, 'browse-listings.html', {'listings': listings})

# Handles the "create listing" form.
# GET request = just show the empty form.
# POST request = validate the data and save the new listing.
def create_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        availability = request.POST.get('availability')
        condition = request.POST.get('condition')
        category = request.POST.get('category')
        images = request.FILES.getlist('images')  # files come from request.FILES, not request.POST

        errors = []

        # price must be a positive number, this is a case study requirement
        if not price or float(price) <= 0:
            errors.append('Price must be a positive number.')

        if not condition:
            errors.append('Please select a condition.')

        if not title:
            errors.append('Title is required.')

        # case study says max 5 images per listing
        if len(images) > 5:
            errors.append('You can upload a maximum of 5 images.')

        # if something is wrong, show the form again with the errors, don't save anything
        if errors:
            return render(request, 'create-listing.html', {'errors': errors})

        # everything is valid, so create the listing
        # status is set to 'under_review' because it needs moderator approval before going live
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

        # save each uploaded image separately, linked to this listing
        for image_file in images:
            ProductImage.objects.create(listing=new_listing, image=image_file)

        return redirect('browse_listings')

    return render(request, 'create-listing.html')


# Shows one specific listing, plus handles two forms on the same page:
# asking a public question (Enquiry) and leaving a rating (Rating).
def product_details(request, listing_id):
    # get_object_or_404 shows a normal 404 page instead of crashing if the listing doesn't exist
    listing = get_object_or_404(ProductListing, id=listing_id, status='approved')

    if request.method == 'POST':
        # two different forms live on this page, so check which one was submitted
        if 'question' in request.POST:
            question_text = request.POST.get('question')
            if question_text:
                Enquiry.objects.create(listing=listing, question=question_text)

        elif 'stars' in request.POST:
            stars = request.POST.get('stars')
            comment = request.POST.get('comment')
            Rating.objects.create(
                business_name=listing.seller_name,
                stars=stars,
                comment=comment,
            )

        # reload the same page after submitting so the new question/rating shows up
        return redirect('product_details', listing_id=listing.id)

    # get all questions and ratings for this listing to display them
    enquiries = listing.enquiries.all()
    ratings = Rating.objects.filter(business_name=listing.seller_name)
    average_rating = ratings.aggregate(Avg('stars'))['stars__avg']

    # check if this listing is already in the user's favourites (stored in session)
    favourites = request.session.get('favourites', [])

    return render(request, 'product-details.html', {
        'listing': listing,
        'enquiries': enquiries,
        'ratings': ratings,
        'average_rating': average_rating,
        'favourites': favourites,
    })


# Shows the private chat for one listing and lets the user send a new message.
def chat(request, listing_id):
    listing = get_object_or_404(ProductListing, id=listing_id, status='approved')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(listing=listing, text=text)
        return redirect('chat', listing_id=listing.id)

    messages = listing.messages.all()
    return render(request, 'chat.html', {'listing': listing, 'messages': messages})


# Adds or removes a listing from favourites.
# No login system yet, so favourites are stored in the session (basically remembers the browser).
def toggle_favourite(request, listing_id):
    favourites = request.session.get('favourites', [])
    if listing_id in favourites:
        favourites.remove(listing_id)
    else:
        favourites.append(listing_id)
    request.session['favourites'] = favourites
    return redirect('product_details', listing_id=listing_id)


# Shows all listings the user has favourited.
def favourites_list(request):
    favourite_ids = request.session.get('favourites', [])
    listings = ProductListing.objects.filter(id__in=favourite_ids, status='approved')
    return render(request, 'favourites.html', {'listings': listings})


# Shows all conversations (one per listing that has at least one message).
def messages_list(request):
    listings_with_messages = ProductListing.objects.filter(messages__isnull=False).distinct()
    return render(request, 'messages.html', {'listings_with_messages': listings_with_messages})


# Admin reports page - shows the numbers required by the case study
# (total listings, new vs second-hand, approved vs pending, average rating, etc.)
def reports_dashboard(request):
    total_listings = ProductListing.objects.count()
    new_listings_count = ProductListing.objects.filter(condition='new').count()
    second_hand_count = ProductListing.objects.filter(condition='second_hand').count()
    approved_count = ProductListing.objects.filter(status='approved').count()
    pending_count = ProductListing.objects.filter(status='under_review').count()
    average_rating_overall = Rating.objects.aggregate(Avg('stars'))['stars__avg']
    total_ratings = Rating.objects.count()
    total_enquiries = Enquiry.objects.count()

    context = {
        'total_listings': total_listings,
        'new_listings_count': new_listings_count,
        'second_hand_count': second_hand_count,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'average_rating_overall': average_rating_overall,
        'total_ratings': total_ratings,
        'total_enquiries': total_enquiries,
    }
    return render(request, 'reports-dashboard.html', context)


# Homepage - shows the 8 most recent approved listings.
def home(request):
    listings = ProductListing.objects.filter(status='approved').order_by('-created_at')[:8]
    return render(request, 'index.html', {'listings': listings})


# Simple static FAQ page, no database needed.
def faq(request):
    return render(request, 'faq.html')


# Seller-facing page for answering public questions.
# Only shows questions that don't have an answer yet.
def seller_enquiries(request):
    enquiries = Enquiry.objects.filter(answer__isnull=True).order_by('-created_at')

    if request.method == 'POST':
        # find which question is being answered using the hidden enquiry_id field
        enquiry_id = request.POST.get('enquiry_id')
        answer_text = request.POST.get('answer')
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        enquiry.answer = answer_text
        enquiry.save()
        return redirect('seller_enquiries')

    return render(request, 'enquiries.html', {'enquiries': enquiries})