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
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="Number to classify")):
    try:
        number_float = float(number)
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail={"number": number, "error": "Invalid input. Please enter a valid number."}
        )

    if number_float.is_integer():
        number_int = int(number_float)
        num_properties = ["even" if number_int % 2 == 0 else "odd"]
        is_prime_val = is_prime(number_int)
        is_perfect_val = is_perfect(number_int)
        is_armstrong_val = is_armstrong(number_int)
        if is_prime_val:
            num_properties.append("prime")
        if is_perfect_val:
            num_properties.append("perfect")
        if is_armstrong_val:
            num_properties.append("armstrong")
        digit_sum = sum(int(d) for d in str(abs(number_int)))
    else:
        num_properties = []
        is_prime_val = False
        is_perfect_val = False
        is_armstrong_val = False
        digit_sum = sum(int(c) for c in number if c.isdigit())

    fun_fact = "No fun fact available"
    try:
        fact_response = requests.get(f"http://numbersapi.com/{number_float}")
        if fact_response.status_code == 200:
            fun_fact = fact_response.text
    except:
        pass  # Ignore API errors

    return {
        "number": number_float,
        "is_prime": is_prime_val,
        "is_perfect": is_perfect_val,
        "properties": num_properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
