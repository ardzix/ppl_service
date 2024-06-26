# server.py
import os
import grpc
from concurrent import futures
import time

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ppl.settings')

import django
django.setup()

from point.grpc import point_pb2_grpc
from point.grpc.grpc_service import PointService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    point_pb2_grpc.add_PointServiceServicer_to_server(PointService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("point gRPC server running on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
