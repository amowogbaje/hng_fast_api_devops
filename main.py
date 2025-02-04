from fastapi import FastAPI, Query
import requests

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
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
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="Number to classify")):
    try:
        num_properties = []
        if number % 2 == 0:
            num_properties.append("even")
        else:
            num_properties.append("odd")

        if is_prime(number):
            num_properties.append("prime")

        if is_perfect(number):
            num_properties.append("perfect")

        if is_armstrong(number):
            num_properties.append("armstrong")

        digit_sum = sum(int(d) for d in str(number))
        
        # Fetch a fun fact
        fun_fact = "No fun fact available"
        try:
            fact_response = requests.get(f"http://numbersapi.com/{number}")
            if fact_response.status_code == 200:
                fun_fact = fact_response.text
        except:
            pass  # Ignore errors from the external API
        
        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": num_properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }
    except:
        return {"number": number, "error": True}, 400
