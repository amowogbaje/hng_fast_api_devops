# Number Classification API

This is a FastAPI-based microservice that classifies numbers based on various mathematical properties and provides a fun fact.

## Features
- Determines if a number is **prime** or **perfect**.
- Identifies number properties (e.g., **Armstrong number**, **even/odd**).
- Calculates the **sum of its digits**.
- Fetches a **fun fact** about the number.
- Supports **CORS** for cross-origin requests.

## API Specification

### **Endpoint:**
```plaintext
GET /api/classify-number?number=<integer>
```

### **Response Format:**
#### **200 OK**
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

#### **400 Bad Request** (Invalid Input)
```json
{
    "number": "alphabet",
    "error": true
}
```

## Setup & Installation

### **1. Clone Repository**
```sh
git clone https://github.com/your-username/number-classification-api.git
cd number-classification-api
```

### **2. Create Virtual Environment & Install Dependencies**
```sh
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Run the API Locally**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Deployment (NGINX + Systemd)

### **1. Configure Systemd Service**
Create `/etc/systemd/system/fastapi.service`:
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
Reload and start service:
```sh
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
sudo systemctl status fastapi
```

### **2. Configure Nginx Reverse Proxy**
Create `/etc/nginx/sites-available/fastapi`:
```nginx
server {
    listen 80;
    server_name your-server-ip;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Enable and restart Nginx:
```sh
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **3. Open Firewall Ports**
```sh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw reload
```

## Testing the API

### **Using cURL**
```sh
curl -X GET http://your-server-ip/api/classify-number?number=371
```

### **Using a Browser**
Visit:
```plaintext
http://your-server-ip/api/classify-number?number=371
```

## License
MIT License

