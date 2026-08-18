# src/api/routers/documents.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/documents/tearsheet/{company_id}")
def get_tearsheet_path(company_id: str):
    return {
        "company_id": company_id,
        "tearsheet_pdf": f"reports/tearsheets/{company_id}_tearsheet.pdf",
        "status": "Available"
    }

@router.get("/documents/pros-cons/{company_id}")
def get_pros_cons(company_id: str):
    return {
        "company_id": company_id,
        "pros": ["Consistent revenue compounding over 5 years."],
        "cons": ["Higher valuation multiple relative to industry peers."]
    }