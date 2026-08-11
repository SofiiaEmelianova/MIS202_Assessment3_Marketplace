from django.db import models

class ProductListing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
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
    seller_name = models.CharField(max_length=150, default='Demo Seller')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title