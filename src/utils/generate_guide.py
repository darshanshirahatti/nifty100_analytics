import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_analyst_guide():
    os.makedirs("docs", exist_ok=True)
    pdf_path = "docs/analyst_guide.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor("#1A365D"), spaceAfter=15)
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=15, textColor=colors.HexColor("#2B6CB0"), spaceBefore=12, spaceAfter=8)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor("#2D3748"), spaceAfter=8)
    
    story = []
    
    # Page 1-2: Title & Screener Guide
    story.append(Paragraph("Nifty 100 Financial Analytics: Analyst Guide", title_style))
    story.append(Paragraph("Comprehensive User Handbook for Streamlit Dashboards and FastAPI Endpoints", body_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("1. How to Use the Streamlit Screener", h2_style))
    story.append(Paragraph("The Streamlit Screener screen enables users to filter Nifty 100 companies dynamically based on fundamentals such as Return on Equity (ROE), Debt-to-Equity ratios, market capitalization bands, and annual revenue growth rates. Use the sidebar inputs to configure custom numeric ranges, then click 'Run Screener' to view filtered subsets instantly.", body_style))
    story.append(PageBreak())
    
    # Page 3-4: Dashboard Screens
    story.append(Paragraph("2. Navigating Dashboard Screens", h2_style))
    story.append(Paragraph("• **Executive Summary:** Provides macro market health indicators, top gainers/losers, and sector performance distributions.<br/>• **Company Profile View:** Deep-dive screen containing multi-year financial statements, balance sheets, and cash flow graphs.<br/>• **Valuation & Ratios:** Evaluates P/E ratios, EV/EBITDA, and proprietary stock scorecards.", body_style))
    story.append(PageBreak())
    
    # Page 5-6: PDF Tearsheets
    story.append(Paragraph("3. Generating PDF Tearsheets", h2_style))
    story.append(Paragraph("Each Company Profile view contains a 'Download PDF Tearsheet' button. When clicked, Reportlab dynamically compiles key financial metrics, ratios, and valuation scores into an institutional-grade, multi-page portfolio summary document ready for client distribution.", body_style))
    story.append(PageBreak())
    
    # Page 7-8: API curl Commands
    story.append(Paragraph("4. Calling the FastAPI Backend via cURL", h2_style))
    story.append(Paragraph("To query company profiles or execute programmatic screening calls directly against the REST API:", body_style))
    story.append(Paragraph("<b>Get Company Details:</b><br/><font face='Courier'>curl -X GET \"http://127.0.0.1:8000/api/v1/companies/COMP_001\" -H \"accept: application/json\"</font>", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Run Screener Query:</b><br/><font face='Courier'>curl -X GET \"http://127.0.0.1:8000/api/v1/screener?min_roe=15.0\" -H \"accept: application/json\"</font>", body_style))
    story.append(PageBreak())
    
    # Page 9-10: Troubleshooting
    story.append(Paragraph("5. Troubleshooting Common Issues", h2_style))
    story.append(Paragraph("• **Port Conflicts:** Ensure ports 8000 (FastAPI) and 8501 (Streamlit) are not occupied by stale python background processes.<br/>• **Database Not Found:** Verify that the `nifty100.db` file exists at the root path and is successfully seeded via `python -m src.etl.loader`.<br/>• **Slow Performance:** Confirm SQLite indexes are created using the optimization script if query times exceed standard limits.", body_style))
    
    doc.build(story)
    print("[Guide Generator] Analyst Guide PDF generated successfully at docs/analyst_guide.pdf")

if __name__ == "__main__":
    generate_analyst_guide()