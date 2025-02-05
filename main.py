from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    response_data = {
        "number": number,
        "is_prime": False,
        "is_perfect": False,
        "properties": [],
        "digit_sum": 0,
        "fun_fact": "No fun fact available"
    }
    status_code = 200

    try:
        number_float = float(number)
    except ValueError:
        # Invalid input, calculate digit sum from the original string
        response_data["digit_sum"] = sum(int(c) for c in number if c.isdigit())
        try:
            fact_response = requests.get(f"http://numbersapi.com/{number}")
            if fact_response.status_code == 200:
                response_data["fun_fact"] = fact_response.text
        except:
            pass
        return JSONResponse(content=response_data, status_code=400)

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
        response_data.update({
            "is_prime": is_prime_val,
            "is_perfect": is_perfect_val,
            "properties": num_properties,
            "digit_sum": sum(int(d) for d in str(abs(number_int)))
        })
    else:
        response_data["digit_sum"] = sum(int(c) for c in number if c.isdigit())

    # Fetch fun fact for valid numbers
    try:
        fact_response = requests.get(f"http://numbersapi.com/{number_float}")
        if fact_response.status_code == 200:
            response_data["fun_fact"] = fact_response.text
    except:
        pass

    return JSONResponse(content=response_data, status_code=status_code)