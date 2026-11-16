import csv
import json
import logging
from pathlib import Path
from typing import List, Optional, Union

import pymupdf
import openpyxl

logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).parent

CSV_FILE = BASE_DIR / "employees.csv"
JSON_FILE = BASE_DIR / "employees.json"
HIGH_EARNERS_FILE = BASE_DIR / "high_earners.csv"
EXCEL_FILE = BASE_DIR / "salary.xlsx"
PDF_FILE = BASE_DIR / "sample.pdf"


def read_employees(path: Path) -> List[dict]:

    employees: List[dict] = []

    try:
        with path.open(mode="r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:
                row["salary"] = int(row["salary"])
                employees.append(row)

    except FileNotFoundError:
        logger.error("File not found: %s", path.name)

    return employees


def write_employees_json(employees: List[dict], path: Path) -> None:

    with path.open(mode="w", encoding="utf-8") as file:

        json.dump(employees, file, indent=4)


def write_high_earners(employees: List[dict], path: Path) -> int:

    high_earners = [employee for employee in employees if employee["salary"] > 50000]

    fieldnames = ["name", "department", "salary"]

    with path.open(mode="w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(high_earners)

    return len(high_earners)


def create_salary_excel(employees: List[dict], path: Path) -> int:

    workbook = openpyxl.Workbook()

    sheet = workbook.active
    sheet.title = "Employee Salaries"

    headers = ["name", "department", "salary"]

    sheet.append(headers)

    for employee in employees:

        sheet.append([employee["name"], employee["department"], employee["salary"]])

    workbook.save(path)
    workbook.close()

    return len(employees)


def read_salary_excel(path: Path) -> List[dict]:

    workbook = openpyxl.load_workbook(path, data_only=True)

    sheet = workbook.active

    rows = list(sheet.iter_rows(values_only=True))

    headers = rows[0]

    employees = [dict(zip(headers, row)) for row in rows[1:]]

    workbook.close()

    return employees


def extract_pdf_text(path: Path) -> str:

    try:
        with pymupdf.open(path) as pdf:

            if len(pdf) == 0:
                return ""

            text = pdf[0].get_text()

            print("PDF First 100 Characters:")
            print(text[:100])

            return text

    except FileNotFoundError:
        logger.error("File not found: %s", path.name)

    return ""


def read_file(path: Union[str, Path]) -> Optional[dict]:

    try:
        file_path = Path(path)

        with file_path.open(mode="r", encoding="utf-8") as file:

            return json.load(file)

    except FileNotFoundError:
        logger.error("File not found: %s", Path(path).name)

    except json.JSONDecodeError as error:
        logger.error("Invalid JSON file: %s", error)

    return None


def find_employee(name: str, employees: List[dict]) -> Optional[dict]:

    for employee in employees:

        if employee["name"].lower() == name.lower():
            return employee

    return None


def get_employee_identifier(employee_id: Union[int, str]) -> Union[int, str]:

    return employee_id


def main() -> None:

    # Read CSV
    employees = read_employees(CSV_FILE)

    # Write JSON
    write_employees_json(employees, JSON_FILE)

    # Write High Earners CSV
    high_earners_count = write_high_earners(employees, HIGH_EARNERS_FILE)

    print(
        f"Rows read: {len(employees)} | " f"High earners written: {high_earners_count}"
    )

    # Create Excel
    create_salary_excel(employees, EXCEL_FILE)

    # Read Excel
    excel_employees = read_salary_excel(EXCEL_FILE)

    print(f"salary.xlsx created and read back: " f"{len(excel_employees)} rows")

    # Find Employee
    employee = find_employee("Rahul", employees)

    if employee:
        print("Employee found:", employee)

    read_file(BASE_DIR / "missing.txt")

    if PDF_FILE.exists():
        extract_pdf_text(PDF_FILE)


if __name__ == "__main__":
    main()
