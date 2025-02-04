# Number Classification API

## Overview
This is a FastAPI-based API that classifies numbers by checking their mathematical properties and fetching a fun fact about them.

## Features
- Determines if a number is prime, perfect, or an Armstrong number.
- Identifies if a number is even or odd.
- Computes the digit sum.
- Fetches a fun fact using [NumbersAPI](http://numbersapi.com/).
- Returns responses in JSON format.
- Handles CORS for cross-origin requests.

## API Specification

### Endpoint
**GET** `/api/classify-number?number=371`

### Response Format
#### 200 OK
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```
#### 400 Bad Request
```json
{
    "number": "alphabet",
    "error": true
}
```

## Installation
### Prerequisites
- Python 3.8+
- Git
- Virtual Environment

### Setup
```sh
git clone <your-repo-url>
cd hng_fast_api_devops
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Locally
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Deployment with Nginx
### Configure Systemd Service
1. Create a service file:
   ```sh
   sudo nano /etc/systemd/system/fastapi.service
   ```
   Add the following:
   ```ini
   [Unit]
   Description=FastAPI Application
   After=network.target
   
   [Service]
   User=root
   Group=www-data
   WorkingDirectory=/var/www/hng_fast_api_devops
   ExecStart=/var/www/hng_fast_api_devops/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

2. Start and enable service:
   ```sh
   sudo systemctl daemon-reload
   sudo systemctl enable fastapi
   sudo systemctl start fastapi
   ```

### Configure Nginx
1. Create an Nginx config file:
   ```sh
   sudo nano /etc/nginx/sites-available/fastapi
   ```
   Add:
   ```nginx
   server {
       listen 80;
       server_name 164.92.218.181;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

2. Enable the site:
   ```sh
   sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Testing
```sh
curl -X GET http://164.92.218.181/api/classify-number?number=371
```

## License
This project is licensed under the MIT License.

