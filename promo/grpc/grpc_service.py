from datetime import datetime
from decimal import Decimal
from ..models import DiscountPromo, BogoPromo, BuyXGetYPromo, BundlePromo, ThresholdPromo, PointPurchasePromo
from . import promo_pb2, promo_pb2_grpc

class PromoService(promo_pb2_grpc.PromoServiceServicer):

    def GetProductPromos(self, request, context):
        product_hash = request.product_hash
        response = promo_pb2.ProductPromoResponse()

        # Check for discount promo
        discount_promo = DiscountPromo.objects.filter(
            promo__active=True,
            promo__start_date__lte=datetime.now(),
            promo__end_date__gte=datetime.now(),
            product_hash=product_hash
        ).first()
        if discount_promo:
            response.has_discount = True
            response.final_price = float(self.calculate_final_price(product_hash, discount_promo))

        # Check for BOGO promo
        bogo_promo = BogoPromo.objects.filter(
            promo__active=True,
            promo__start_date__lte=datetime.now(),
            promo__end_date__gte=datetime.now(),
            required_product_hash=product_hash
        ).first()
        if bogo_promo:
            response.is_bogo = True

        # Check for Buy X Get Y and Bundle promo
        buy_x_get_y_promos = BuyXGetYPromo.objects.filter(
            promo__active=True,
            promo__start_date__lte=datetime.now(),
            promo__end_date__gte=datetime.now(),
            required_product_hash=product_hash
        )
        for promo in buy_x_get_y_promos:
            buy_x_get_y_info = promo_pb2.BuyXGetYInfo(
                required_product_hash=promo.required_product_hash,
                discounted_product_hash=promo.discounted_product_hash,
                discounted_price=float(promo.discounted_price)
            )
            response.buy_x_get_y_promos.append(buy_x_get_y_info)

        bundle_promos = BundlePromo.objects.filter(
            promo__active=True,
            promo__start_date__lte=datetime.now(),
            promo__end_date__gte=datetime.now()
        )
        for promo in bundle_promos:
            if product_hash in promo.product_hashes:
                response.bundle_product_hashes.extend(promo.product_hashes)

        # Check for point purchase promo
        point_purchase_promo = PointPurchasePromo.objects.filter(
            promo__active=True,
            promo__start_date__lte=datetime.now(),
            promo__end_date__gte=datetime.now(),
            product_hash=product_hash
        ).first()
        if point_purchase_promo:
            response.can_purchase_by_points = True
            response.points_required = point_purchase_promo.points_required

        return response

    def CheckThresholdPromo(self, request, context):
        subtotal = request.subtotal
        response = promo_pb2.ThresholdPromoResponse()

        threshold_promo = ThresholdPromo.objects.filter(
            promo__active=True,
            promo__start_date__lte=datetime.now(),
            promo__end_date__gte=datetime.now(),
            threshold_amount__lte=subtotal
        ).first()
        if threshold_promo:
            response.has_threshold_promo = True
            response.discount_value = float(threshold_promo.discount_value)

        return response

    def calculate_final_price(self, product_hash, discount_promo):
        # Placeholder function for calculating final price based on discount promo
        # Actual implementation will depend on your pricing logic
        original_price = self.get_original_price(product_hash)
        if discount_promo.discount_type == 'percentage':
            return original_price * (Decimal('1') - discount_promo.discount_value / Decimal('100'))
        else:
            return original_price - discount_promo.discount_value

    def get_original_price(self, product_hash):
        # Placeholder function for retrieving the original price of a product
        # Actual implementation will depend on your product pricing data
        return Decimal('100.0')  # Example fixed price for demonstration