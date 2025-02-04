from fastapi import FastAPI, Query, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n < 2 or not float(n).is_integer():
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n < 1 or not float(n).is_integer():
        return False
    return sum(i for i in range(1, int(n)) if int(n) % i == 0) == int(n)

def is_armstrong(n: int) -> bool:
    if not float(n).is_integer():
        return False
    digits = [int(d) for d in str(int(n))]
    return sum(d ** len(digits) for d in digits) == int(n)

@app.get("/api/classify-number")
async def classify_number(number: float = Query(..., description="Number to classify")):
    if not float(number).is_integer():
        raise HTTPException(status_code=400, detail="Only integer values are allowed")

    number = int(number)
    num_properties = ["even" if number % 2 == 0 else "odd"]
    
    if is_prime(number):
        num_properties.append("prime")
    if is_perfect(number):
        num_properties.append("perfect")
    if is_armstrong(number):
        num_properties.append("armstrong")

    digit_sum = sum(int(d) for d in str(abs(number)))

    fun_fact = "No fun fact available"
    try:
        fact_response = requests.get(f"http://numbersapi.com/{number}")
        if fact_response.status_code == 200:
            fun_fact = fact_response.text
    except:
        pass  

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": num_properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
