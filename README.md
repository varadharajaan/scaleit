# Technical Documentation for "ScaleIt" Project

## 1. Proper Description

The "ScaleIt" project is an auto-scaler designed to manipulate the number of replicas of a separate application based on CPU utilization metrics. The goal is to automatically adjust the replica count to maintain an average CPU usage of 0.80 (80%). The application communicates with a sample application provided by Vimeo, which starts on a user-defined port. The sample application's JSON/REST API allows monitoring the emulated CPU usage and changing the number of replicas. The reported CPU usage simulates real-world scenarios, rising and falling over time, and the APIs occasionally return errors to mimic real-life situations.

## 2. Architecture Explanation

The architecture of the "ScaleIt" project is based on the Flask framework, designed to interact with the Vimeo-provided sample application through its REST API. The auto-scaler continuously monitors the CPU utilization reported by the sample application and adjusts the replica count to maintain an average CPU usage of 0.80. The Flask app exposes endpoints to retrieve the current status and update the replica count based on the provided API specifications.

## 3. Steps to Download the Project from GitHub and Run the Flask App

To run the "ScaleIt" project locally, follow the steps mentioned earlier. Additionally, ensure that the Vimeo-provided sample application is running on the specified port.

### Clone the GitHub Repository

```bash
git clone https://github.com/varadharajaan/scaleit.git
cd scaleit
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Flask App

```bash
python app.py --port 8213
```

This command will start the Flask app, and it will be accessible at `http://localhost:8213`. To run the app on a different port, provide the desired port number using the `--port` flag.

### Access the Swagger UI

Open your web browser and navigate to `http://localhost:8213/apidocs` to explore the documentation and test the exposed APIs using the Swagger UI. The Swagger endpoint is also available at `http://localhost:8213/apidocs`.

Ensure that you have Python installed, and consider using a virtual environment for dependency isolation.

Note: If the repository is private, you might need to provide authentication credentials during the `git clone` step.

## 4. APIs Exposed

### 4.1 POST /login

Performs user authentication to access protected endpoints.

#### Request Sample

- HTTP Method: POST
- Endpoint: `/login`
- Content-Type: application/json

```json
{
  "username": "admin",
  "password": "admin"
}
```

#### Response Sample

```json
{
  "message": "Login successful. Access token generated.",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTYzOTU2NTQwMH0.lSdqTH_h9-B3a3f6BW7q_TLl1eGqvcmTKGhE7f4MWnA"
}
```

### 4.2 GET /app/status

Retrieves the current status of the application, including CPU utilization and the current number of replicas.

#### Request Sample

- HTTP Method: GET
- Endpoint: `/app/status`
- Authorization: Bearer \<Access Token\>

#### Response Sample

```json
{
  "cpu": {
    "highPriority": 0.68
  },
  "replicas": 10
}
```

### 4.3 PUT /app/replicas

Updates the replica count to adjust the application's scalability. Requires a JSON payload with the desired replica count.

#### Request Sample

- HTTP Method: PUT
- Endpoint: `/app/replicas`
- Content-Type: application/json
- Authorization: Bearer \<Access Token\>

```json
{
  "replicas": 60,
  "user": "name"
}
```

#### Response Sample

- HTTP Status: 400 Bad Request

```json
{
  "error": "Invalid request",
  "message": "Replica count must be a valid integer greater than one. If replicas exceed 50, a valid username is required."
}
```

## 5. Advanced Validation

Advanced validation is applied to the `/app/replicas` endpoint to ensure that the difference between the current replica count and the new replica count is not greater than 50. If the difference exceeds 50, the presence of a valid username in the request body is required for authentication.

### Request Sample

- HTTP Method: PUT
- Endpoint: `/app/replicas`
- Content-Type: application/json
- Authorization: Bearer \<Access Token\>

```json
{
  "replicas": 60,
  "user": "name"
}
```

### Response Sample (Success)

- HTTP Status: 200 OK

```json
{
  "message": "Replica count updated successfully"
}
```

### Response Sample (Failure)

- HTTP Status: 400 Bad Request

```json
{
  "error": "Invalid request",
  "message": "Replica count must be a valid integer greater than one. If the difference between the current and new replica counts exceeds 50, a valid username is required."
}
```

## 6. Swagger Page Integration

The Swagger UI provides documentation for the exposed APIs, allowing users to understand and test the functionality easily. Access the Swagger UI at `http://localhost:apidocs

## 7. Unit Testing and Integration Testing

Comprehensive unit tests and integration tests are included to ensure the functionality and reliability of the auto-scaler. Testing frameworks such as `pytest` can be used to execute the tests.

## 8. Dockerization and Publication

The "ScaleIt" project is Dockerized for easy deployment. It can be published as a Docker image with the tag `varadharajaan/scaleit`. To run the project in a Docker container, follow the provided Docker run command.

Feel free to explore and contribute to the project on GitHub: [https://github.com/varadharajaan/scaleit](https://github.com/varadharajaan/scaleit)

## 9. Production Deployment

This project is dockerized in Production standard already this can be deployed in any Kubernetes cluster or standlone instance and can be accessed using public IP.

# Note:

Ensure that the Vimeo-provided sample application is running and accessible on the specified port (defaulting to 8123) for accurate auto-scaling based on CPU utilization metrics.