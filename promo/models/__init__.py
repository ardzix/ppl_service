from django.utils.translation import gettext_lazy as _
from django.db import models

class Promo(models.Model):
    PROMO_TYPE_CHOICES = [
        ('discount', _('Discount')),
        ('bogo', _('Buy One Get One')),
        ('buy_x_get_y', _('Buy X Get Y')),
        ('bundle', _('Bundle')),
        ('threshold', _('Threshold')),
        ('point_purchase', _('Point Purchase'))
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    promo_type = models.CharField(max_length=20, choices=PROMO_TYPE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class DiscountPromo(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ]

    promo = models.OneToOneField(Promo, on_delete=models.CASCADE, related_name='discount_promo')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    product_hash = models.CharField(max_length=64)  # Add this field to store product hash

class BogoPromo(models.Model):
    promo = models.OneToOneField(Promo, on_delete=models.CASCADE, related_name='bogo_promo')
    required_product_hash = models.CharField(max_length=64)
    free_product_hash = models.CharField(max_length=64, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class BuyXGetYPromo(models.Model):
    promo = models.OneToOneField(Promo, on_delete=models.CASCADE, related_name='buy_x_get_y_promo')
    required_product_hash = models.CharField(max_length=64)
    discounted_product_hash = models.CharField(max_length=64)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class BundlePromo(models.Model):
    promo = models.OneToOneField(Promo, on_delete=models.CASCADE, related_name='bundle_promo')
    product_hashes = models.JSONField()  # Store a list of product hashes
    bundle_price = models.DecimalField(max_digits=10, decimal_places=2)

class ThresholdPromo(models.Model):
    promo = models.OneToOneField(Promo, on_delete=models.CASCADE, related_name='threshold_promo')
    threshold_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

class PointPurchasePromo(models.Model):
    promo = models.OneToOneField(Promo, on_delete=models.CASCADE, related_name='point_purchase_promo')
    product_hash = models.CharField(max_length=64)
    points_required = models.IntegerField()
