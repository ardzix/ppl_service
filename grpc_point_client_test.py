import grpc
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ppl.settings')
django.setup()

from django.conf import settings
from point.grpc import point_pb2, point_pb2_grpc
from point.models import Category

def test_add_activity(stub, name, point_impact, category_id, type):
    activity = point_pb2.AddActivityRequest(
        name=name,
        description=f"Points for {name}",
        point_impact=point_impact,
        category_id=category_id,
        type=type
    )
    response = stub.AddActivity(activity)
    print(f"Activity added with ID: {response.id} and Code: {response.code}")
    return response.id, response.code

def test_record_activity(stub, activity_code, user_hash, nonce):
    record = point_pb2.RecordActivityRequest(
        code=activity_code,
        user_hash=user_hash,
        nonce=nonce
    )
    response = stub.RecordActivity(record)
    return response

def test_get_user_points(stub, user_hash):
    user = point_pb2.GetUserPointsRequest(user_hash=user_hash)
    response = stub.GetUserPoints(user)
    return response.points

def cleanup(activity_ids):
    from point.models import Activity, UserPoint, ActivityLog
    # Delete test activities
    Activity.objects.filter(id__in=activity_ids).delete()
    # Delete test user points and logs
    user_points = UserPoint.objects.filter(user_hash="user12345")
    for user_point in user_points:
        ActivityLog.objects.filter(user=user_point).delete()
        user_point.delete()

def main():
    # Connect to gRPC server
    channel = grpc.insecure_channel(f'{settings.PROMO_SERVICE_HOST}:{settings.POINT_SERVICE_PORT}')
    stub = point_pb2_grpc.PointServiceStub(channel)

    # Ensure category exists
    category, created = Category.objects.get_or_create(name="Test Category")

    # Test add activities
    single_activity_id, single_activity_code = test_add_activity(stub, "Finish Registration", 10, category.id, "single")
    multiple_activity_id, multiple_activity_code = test_add_activity(stub, "Like Post", 5, category.id, "multiple")

    # Test record single occurrence activity
    try:
        response = test_record_activity(stub, single_activity_code, "user12345", "unique_nonce_single_1")
        print(f"User points after single occurrence activity: {response.points}")
        # Try to record the same single occurrence activity again
        response = test_record_activity(stub, single_activity_code, "user12345", "unique_nonce_single_2")
    except grpc.RpcError as e:
        print(f"Expected error for single occurrence activity: {e.details()}")

    # Test record multiple occurrence activity
    response = test_record_activity(stub, multiple_activity_code, "user12345", "unique_nonce_multiple_1")
    print(f"User points after first multiple occurrence activity: {response.points}")
    response = test_record_activity(stub, multiple_activity_code, "user12345", "unique_nonce_multiple_2")
    print(f"User points after second multiple occurrence activity: {response.points}")

    # Test get user points
    points = test_get_user_points(stub, "user12345")
    print(f"Final user points: {points}")

    # Cleanup test data
    cleanup([single_activity_id, multiple_activity_id])

if __name__ == '__main__':
    main()
