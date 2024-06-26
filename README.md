# PPL (Point, Promo, and Loyalty) Service

## Overview

The PPL service handles functionalities for points collection, promo creation and redemption, and loyalty programs. It uses Django for the web framework and gRPC for communication between services.

## Features

- Points: Collect user points based on activities. Activities can be added and reduced.
- Promos: Marketing can create promos that can be redeemed based on points and other criteria.
- Loyalty: Manage loyalty programs.

## Technology Stack

- Backend: Django
- API: gRPC
- Database: PostgreSQL (or any other database supported by Django)
- Containerization: Docker

## Installation

### Prerequisites
- Docker
- Docker Compose (optional, but recommended)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

### Using Docker

1. Build the Docker image:

```bash
docker build -t your_project_name .
```

2. Run the Docker container:

```bash
docker run -p 8000:8000 -p 50051:50051 your_project_name
```

### Using Docker Compose

1. Build and start services:

```bash
docker-compose up --build
```

2. Stop services:

```bash
docker-compose down
```

## Usage

### Admin Panel

- Access the admin panel at http://localhost:8000/admin
- Use the admin panel to manage activities, promos, and loyalty programs.

### gRPC Services

- Add Activity: Add new activities that impact user points.
- Record Activity: Record an activity occurrence for a user.
- Get User Points: Retrieve the total points for a user.

### Testing

Run the gRPC test script:

```bash
python -m ppl.point.tests.grpc_client_test
```

### Cleanup Test Data

The test script includes a cleanup function to delete test data after execution.

## Protobuf Definition

The point.proto file defines the gRPC services and messages:

```proto
syntax = "proto3";

package point;

service PointService {
    rpc AddActivity (AddActivityRequest) returns (ActivityResponse);
    rpc RecordActivity (RecordActivityRequest) returns (UserPointsResponse);
    rpc GetUserPoints (GetUserPointsRequest) returns (UserPointsResponse);
}

message AddActivityRequest {
    string name = 1;
    string description = 2;
    int32 point_impact = 3;
    int32 category_id = 4;
    string type = 5;
}

message ActivityResponse {
    int32 id = 1;
    string code = 2;
}

message RecordActivityRequest {
    string code = 1;
    string user_hash = 2;
    string nonce = 3;
}

message UserPointsResponse {
    int32 points = 1;
}

message GetUserPointsRequest {
    string user_hash = 1;
}
```

## Environment Variables

- `DJANGO_SETTINGS_MODULE`: Set to masterdata.settings
- `PYTHONUNBUFFERED`: Set to 1 to ensure Python outputs everything directly to the terminal without buffering.

## Contributing

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature').
5. Push to the branch (git push origin feature-branch).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.