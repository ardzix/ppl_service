from django.contrib import admin
from ..models import Promo, DiscountPromo, BogoPromo, BuyXGetYPromo, BundlePromo, ThresholdPromo, PointPurchasePromo

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('name', 'promo_type', 'start_date', 'end_date', 'active')
    search_fields = ('name', 'promo_type')
    list_filter = ('promo_type', 'active')

@admin.register(DiscountPromo)
class DiscountPromoAdmin(admin.ModelAdmin):
    list_display = ('promo', 'discount_type', 'discount_value')
    search_fields = ('promo__name',)

@admin.register(BogoPromo)
class BogoPromoAdmin(admin.ModelAdmin):
    list_display = ('promo', 'required_product_hash', 'free_product_hash', 'discounted_price')
    search_fields = ('promo__name', 'required_product_hash', 'free_product_hash')

@admin.register(BuyXGetYPromo)
class BuyXGetYPromoAdmin(admin.ModelAdmin):
    list_display = ('promo', 'required_product_hash', 'discounted_product_hash', 'discounted_price')
    search_fields = ('promo__name', 'required_product_hash', 'discounted_product_hash')

@admin.register(BundlePromo)
class BundlePromoAdmin(admin.ModelAdmin):
    list_display = ('promo', 'bundle_price')
    search_fields = ('promo__name', 'product_hashes')

@admin.register(ThresholdPromo)
class ThresholdPromoAdmin(admin.ModelAdmin):
    list_display = ('promo', 'threshold_amount', 'discount_value')
    search_fields = ('promo__name',)

@admin.register(PointPurchasePromo)
class PointPurchasePromoAdmin(admin.ModelAdmin):
    list_display = ('promo', 'product_hash', 'points_required')
    search_fields = ('promo__name', 'product_hash')
