# Smart Meter Gateway API
This project implements a Smart Meter Gateway system using Flask and MongoDB. 

## Installation

### 1. Create a virtual environment and activate it:
``` bash
python -m venv ./venv # This requires that the venv module is installed
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 2. Install the dependencies:
``` bash
pip install -r requirements.txt
```

### 3. Set up the environment variables:
Create a .env file in the root directory of the project and add the following:
```bash
MONGO_URI=<mongoUrl>
JWT_SECRET_KEY=<jwtKey>
...
```


### 2. Start the container
```bash
podman-compose up -d
```

### 3. Run the app
```bash
python run.py
```

## Configuration
The application uses environment variables for configuration. The following variables need to be set:
* MONGO_URI: The MongoDB connection string.
* JWT_SECRET_KEY: The secret key used for JWT authentication.
* WAN_HOST: Host to be used for WAN connection
* WAN_PORT: Port to be used for WAN connection
* LAN_HOST: Host to be used for LAN connection
* LAN_PORT: Port to be used for WAN connection 
* LAN_IP_RANGES: IP ranges can be defined individually

## Endpoints
### Register User
#### Request
* URL: /auth/register
* Method: POST
* Description: Registers a new user.
* Request Body:
``` json
{
  "username": "<username>",
  "password": "<password>",
  "role": "<role>"
}
```

#### Response
``` json
Success: 201 Created
{
  "message": "User created successfully",
  "id": "user_id"
}

-- or --

Error: 500 Internal Server Error
{
  "message": "An error occurred",
  "error": "error_message"
}
```
### Login User
#### Request
* URL: /auth/login
* Method: POST
* Description: Login an existing user.
* Request Body:
``` json
{
  "username": "<username>",
  "password": "<password>"
}
```

#### Response
``` json
Success: 200 OK
{
  "access_token": "<jwt_token>"
}

-- or --

Error: 401 Unauthorized
{
  "message": "Invalid credentials"
}
```
### Get Consumption Data
#### Request
* URL: /main/consumption
* Method: GET
* Description: Retrieves consumption data for the authenticated user.

#### Response
``` json
Success: 200 OK
[
  {
    "id": "consumption_id",
    "timestamp": "2024-06-30T12:36:22.810+00:00",
    "value": "100"
  }
]

-- or --

Error: 401 Unauthorized
{
  "message": "Invalid credentials"
}
```

### Add Consumption Data
#### Request
* URL: /main/consumption
* Method: POST
* Description: Adds consumption data for the authenticated user.
* Request Body:
``` json
{
  "value": "<some-value>"
}
```

#### Response
``` json
Success: 201 CREATED
{
  "message": "Consumption data added successfully",
  "id": "consumption_id"
}
```