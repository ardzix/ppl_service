import grpc
from concurrent import futures
from ..models import Category, Activity, UserPoint, ActivityLog
from . import point_pb2, point_pb2_grpc  # Protobuf files

class PointService(point_pb2_grpc.PointServiceServicer):

    def AddActivity(self, request, context):
        try:
            category = Category.objects.get(id=request.category_id)
            activity = Activity.objects.create(
                name=request.name,
                description=request.description,
                point_impact=request.point_impact,
                category=category,
                type=request.type
            )
            return point_pb2.ActivityResponse(id=activity.id, code=activity.code)
        except Category.DoesNotExist:
            context.set_details('Category not found.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return point_pb2.ActivityResponse()

    def RecordActivity(self, request, context):
        try:
            activity = Activity.objects.get(code=request.code)
            user, created = UserPoint.objects.get_or_create(user_hash=request.user_hash)

            # Check if the activity is single occurrence and has already been done
            if activity.type == 'single':
                if ActivityLog.objects.filter(user=user, activity=activity).exists():
                    context.set_details('Activity already recorded for this user.')
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    return point_pb2.UserPointsResponse()

            ActivityLog.objects.create(user=user, activity=activity, nonce=request.nonce)
            user.points += activity.point_impact
            user.save()
            return point_pb2.UserPointsResponse(points=user.points)
        except Activity.DoesNotExist:
            context.set_details('Activity not found.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return point_pb2.UserPointsResponse()

    def GetUserPoints(self, request, context):
        try:
            user = UserPoint.objects.get(user_hash=request.user_hash)
            return point_pb2.UserPointsResponse(points=user.points)
        except UserPoint.DoesNotExist:
            context.set_details('User not found.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return point_pb2.UserPointsResponse()
