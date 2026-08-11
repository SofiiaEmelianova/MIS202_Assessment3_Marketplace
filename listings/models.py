from django.db import models

# Create your models here.

class ProductListing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    condition = models.CharField(
        max_length=20,
        choices=[('new', 'New'), ('second_hand', 'Second-Hand')]
    )
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title