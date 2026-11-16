import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

DATA_FILE = Path(__file__).resolve().parent.parent / "config" / "employees.json"

app = FastAPI(title="Employee Service")


class Employee(BaseModel):
    name: str
    department: str
    salary: float

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be empty")
        return v

    @field_validator("salary")
    @classmethod
    def salary_above_zero(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("salary must be above 0")
        return v


def load_employees() -> List[dict]:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


employees: List[dict] = load_employees()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/employees")
def list_employees() -> List[dict]:
    return employees


@app.get("/employees/{name}")
def get_employee(name: str) -> dict:
    for emp in employees:
        if emp["name"].lower() == name.lower():
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(emp: Employee) -> dict:
    data = emp.model_dump()
    employees.append(data)
    return data
