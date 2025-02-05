from fastapi import FastAPI, Query, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
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
async def classify_number(number: float = Query(..., description="Number to classify")):
    try:
        # Check if the input is valid (numeric values are acceptable)
        if not isinstance(number, (int, float)):
            raise HTTPException(status_code=400, detail="Invalid input. Please enter a valid number.")

        num_properties = ["even" if number % 2 == 0 else "odd"]

        if is_prime(int(number)):
            num_properties.append("prime")
        if is_perfect(int(number)):
            num_properties.append("perfect")
        if is_armstrong(int(number)):
            num_properties.append("armstrong")

        digit_sum = sum(int(d) for d in str(abs(int(number))))

        # Fetch fun fact
        fun_fact = "No fun fact available"
        try:
            fact_response = requests.get(f"http://numbersapi.com/{int(number)}")
            if fact_response.status_code == 200:
                fun_fact = fact_response.text
        except:
            pass  # Ignore API errors

        return {
            "number": number,
            "is_prime": is_prime(int(number)),
            "is_perfect": is_perfect(int(number)),
            "properties": num_properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input. Please enter a valid number.")
