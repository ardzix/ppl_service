import grpc
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ppl.settings')
django.setup()

from datetime import datetime, timedelta
from promo.models import Promo, DiscountPromo, BogoPromo, BuyXGetYPromo, BundlePromo, ThresholdPromo, PointPurchasePromo
from promo.grpc import promo_pb2, promo_pb2_grpc

def test_get_product_promos(stub, product_hash):
    request = promo_pb2.ProductPromoRequest(product_hash=product_hash)
    response = stub.GetProductPromos(request)
    print(f"Product {product_hash} Promos:")
    print(f"  Has Discount: {response.has_discount}")
    if response.has_discount:
        print(f"  Final Price: {response.final_price}")
    print(f"  Is BOGO: {response.is_bogo}")
    if response.buy_x_get_y_promos:
        for promo in response.buy_x_get_y_promos:
            print(f"  Buy X Get Y Promo - Required Product Hash: {promo.required_product_hash}, Discounted Product Hash: {promo.discounted_product_hash}, Discounted Price: {promo.discounted_price}")
    if response.bundle_product_hashes:
        print(f"  Bundle Product Hashes: {response.bundle_product_hashes}")
    print(f"  Can Purchase by Points: {response.can_purchase_by_points}")
    if response.can_purchase_by_points:
        print(f"  Points Required: {response.points_required}")

def test_check_threshold_promo(stub, subtotal):
    request = promo_pb2.ThresholdPromoRequest(subtotal=subtotal)
    response = stub.CheckThresholdPromo(request)
    print(f"Subtotal {subtotal} Threshold Promo:")
    print(f"  Has Threshold Promo: {response.has_threshold_promo}")
    if response.has_threshold_promo:
        print(f"  Discount Value: {response.discount_value}")

def cleanup_promos():
    Promo.objects.all().delete()
    DiscountPromo.objects.all().delete()
    BogoPromo.objects.all().delete()
    BuyXGetYPromo.objects.all().delete()
    BundlePromo.objects.all().delete()
    ThresholdPromo.objects.all().delete()
    PointPurchasePromo.objects.all().delete()

def create_test_data():
    # Create a Discount Promo
    promo = Promo.objects.create(
        name="Test Discount Promo",
        description="Test Discount Description",
        promo_type="discount",
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1),
        active=True
    )
    DiscountPromo.objects.create(
        promo=promo,
        discount_type="percentage",
        discount_value=10.0,
        product_hash="product1"  # Ensure product_hash matches the test
    )

    # Create a BOGO Promo
    promo = Promo.objects.create(
        name="Test BOGO Promo",
        description="Test BOGO Description",
        promo_type="bogo",
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1),
        active=True
    )
    BogoPromo.objects.create(
        promo=promo,
        required_product_hash="product1",
        free_product_hash="product2"
    )

    # Create a Buy X Get Y Promo
    promo = Promo.objects.create(
        name="Test Buy X Get Y Promo",
        description="Test Buy X Get Y Description",
        promo_type="buy_x_get_y",
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1),
        active=True
    )
    BuyXGetYPromo.objects.create(
        promo=promo,
        required_product_hash="product1",
        discounted_product_hash="product3",
        discounted_price=5.0
    )

    # Create a Bundle Promo
    promo = Promo.objects.create(
        name="Test Bundle Promo",
        description="Test Bundle Description",
        promo_type="bundle",
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1),
        active=True
    )
    BundlePromo.objects.create(
        promo=promo,
        product_hashes=["product1", "product4"],
        bundle_price=15.0
    )

    # Create a Threshold Promo
    promo = Promo.objects.create(
        name="Test Threshold Promo",
        description="Test Threshold Description",
        promo_type="threshold",
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1),
        active=True
    )
    ThresholdPromo.objects.create(
        promo=promo,
        threshold_amount=50.0,
        discount_value=5.0
    )

    # Create a Point Purchase Promo
    promo = Promo.objects.create(
        name="Test Point Purchase Promo",
        description="Test Point Purchase Description",
        promo_type="point_purchase",
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1),
        active=True
    )
    PointPurchasePromo.objects.create(
        promo=promo,
        product_hash="product5",
        points_required=100
    )

def main():
    # Set up the gRPC channel and stub
    channel = grpc.insecure_channel('localhost:50052')
    stub = promo_pb2_grpc.PromoServiceStub(channel)

    # Clean up any existing test data
    cleanup_promos()

    # Create test data
    create_test_data()

    # Test GetProductPromos
    test_get_product_promos(stub, "product1")  # This should have a discount and a BOGO promo
    test_get_product_promos(stub, "product5")  # This should have a point purchase promo

    # Test CheckThresholdPromo
    test_check_threshold_promo(stub, 60.0)
    test_check_threshold_promo(stub, 40.0)

    # Clean up test data
    cleanup_promos()

if __name__ == '__main__':
    main()
