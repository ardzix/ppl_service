import os
import grpc
from concurrent import futures
import time

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ppl.settings')

import django
django.setup()

from django.conf import settings
from point.grpc import point_pb2_grpc
from point.grpc.grpc_service import PointService
from promo.grpc import promo_pb2_grpc
from promo.grpc.grpc_service import PromoService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add both PointService and PromoService to the same server instance
    point_pb2_grpc.add_PointServiceServicer_to_server(PointService(), server)
    promo_pb2_grpc.add_PromoServiceServicer_to_server(PromoService(), server)

    # Listen on two different ports
    server.add_insecure_port(f'[::]:{settings.POINT_SERVICE_PORT}')
    server.add_insecure_port(f'[::]:{settings.PROMO_SERVICE_PORT}')

    server.start()
    print(f'gRPC servers running on ports {settings.POINT_SERVICE_PORT} and {settings.PROMO_SERVICE_PORT}...')
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
