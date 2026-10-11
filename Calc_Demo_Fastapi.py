from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Calculation(BaseModel):
    a: float
    operator: str
    b: float


@app.get("/")
def home():
    return {"message": "Calculator API is running"}


@app.post("/calculate")
def calculate(data: Calculation):
    if data.operator == "add":
        result = data.a + data.b

    elif data.operator == "subtract":
        result = data.a - data.b

    elif data.operator == "multiply":
        result = data.a * data.b

    elif data.operator == "divide":
        if data.b == 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot divide by zero",
            )
        result = data.a / data.b

    else:
        raise HTTPException(
            status_code=400,
            detail="Use add, subtract, multiply, or divide",
        )

    return {
        "a": data.a,
        "operator": data.operator,
        "b": data.b,
        "result": result,
    }