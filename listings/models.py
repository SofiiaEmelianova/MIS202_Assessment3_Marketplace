from django.db import models


# Main model - one product listing created by a seller.
# Covers all the fields required by the case study: title, description, price,
# discount, condition, availability, category, status workflow, and who's selling it.
class ProductListing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # optional, not every listing has a discount

    condition = models.CharField(
        max_length=20,
        choices=[('new', 'New'), ('second_hand', 'Second-Hand')]
    )

    availability = models.CharField(
        max_length=20,
        choices=[('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock')],
        default='in_stock'
    )

    category = models.CharField(max_length=50, default='Books')

    # status workflow required by the case study:
    # draft -> under_review -> approved / rejected -> hidden
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('hidden', 'Hidden'),
        ],
        default='draft'
    )

    # temporary field - there's no real Business model with login yet,
    # so we just store the seller's name as plain text for now
    seller_name = models.CharField(max_length=150, default='Demo Seller')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # shows the listing title instead of "ProductListing object" in the admin panel
        return self.title


# One product listing can have up to 5 images (case study requirement),
# so images are a separate model linked back to ProductListing with a ForeignKey.
class ProductImage(models.Model):
    listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')

    def __str__(self):
        return f"Image for {self.listing.title}"


# A public question a buyer asks about a listing.
# The seller can answer it later, and the answer is also public.
class Enquiry(models.Model):
    listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name='enquiries')
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)  # empty until the seller replies

    # temporary field, same reason as seller_name above - no login system yet
    asked_by = models.CharField(max_length=150, default='Anonymous Buyer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q on {self.listing.title}: {self.question[:30]}"


# A star rating + comment left for a business after a completed transaction.
# Used to calculate the business's average public rating.
class Rating(models.Model):
    business_name = models.CharField(max_length=150)  # matches ProductListing.seller_name for now
    stars = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(blank=True)
    rated_by = models.CharField(max_length=150, default='Anonymous Buyer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} - {self.stars} stars"


# A private message sent between a buyer and a seller about a specific listing.
class Message(models.Model):
    listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField(max_length=150, default='Buyer')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_name}: {self.text[:30]}"