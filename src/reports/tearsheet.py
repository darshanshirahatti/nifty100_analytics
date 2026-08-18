# src/reports/tearsheet.py

import os
import pandas as pd
import numpy as np

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String

def generate_tearsheet(ticker: str, output_pdf_path: str):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles with Word Wrap
    title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.whitesmoke,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'HeaderSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.whitesmoke
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyWrap',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor("#2D3748"),
        wordWrap='CJK'
    )
    
    pro_style = ParagraphStyle(
        'ProStyle',
        parent=body_style,
        textColor=colors.HexColor("#276749")
    )
    
    con_style = ParagraphStyle(
        'ConStyle',
        parent=body_style,
        textColor=colors.HexColor("#9B2C2C")
    )

    story = []

    # ================= PAGE 1 =================
    # 1. Header Bar (Navy)
    header_data = [[
        Paragraph(f"<b>Company Tearsheet: {ticker}</b>", title_style),
        Paragraph("<b>Nifty 100 Analytics Platform</b><br/>Financial & Valuation Report", subtitle_style)
    ]]
    header_table = Table(header_data, colWidths=[340, 200])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1A365D")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))

    # 2. KPI Tiles (2 rows of 3)
    kpi_data = [
        [Paragraph("<b>Market Cap</b><br/>₹ 2,45,000 Cr", body_style),
         Paragraph("<b>P/E Ratio</b><br/>28.5 x", body_style),
         Paragraph("<b>ROE (5Yr Avg)</b><br/>18.4 %", body_style)],
        [Paragraph("<b>ROCE (5Yr Avg)</b><br/>22.1 %", body_style),
         Paragraph("<b>Debt / Equity</b><br/>0.25", body_style),
         Paragraph("<b>Dividend Yield</b><br/>1.2 %", body_style)]
    ]
    kpi_table = Table(kpi_data, colWidths=[180, 180, 180])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.white),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 15))

    # 3. Charts Section (Revenue & Net Profit Bar Chart Placeholder Drawing)
    story.append(Paragraph("10-Year Revenue & Net Profit Trend", section_heading))
    d_bar = Drawing(540, 140)
    d_bar.add(Rect(0, 0, 540, 140, fillColor=colors.HexColor("#F7FAFC"), strokeColor=colors.HexColor("#E2E8F0")))
    d_bar.add(String(200, 65, "[ 10-Yr Revenue & Net Profit Bar Chart ]", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor("#4A5568")))
    story.append(d_bar)
    story.append(Spacer(1, 15))

    # 4. ROE and ROCE Line Chart Placeholder Drawing
    story.append(Paragraph("ROE & ROCE Dual-Axis Trend", section_heading))
    d_line = Drawing(540, 140)
    d_line.add(Rect(0, 0, 540, 140, fillColor=colors.HexColor("#F7FAFC"), strokeColor=colors.HexColor("#E2E8F0")))
    d_line.add(String(205, 65, "[ ROE vs ROCE Trend Chart ]", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor("#4A5568")))
    story.append(d_line)

    # Page Break for Page 2
    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph(f"<b>Financial Structure & Qualitative Analysis: {ticker}</b>", section_heading))
    story.append(Spacer(1, 8))

    # 1. Balance Sheet Composition Stacked Bar Placeholder
    story.append(Paragraph("Balance Sheet Composition (Equity, Borrowings, Other Liabilities)", section_heading))
    d_bs = Drawing(540, 120)
    d_bs.add(Rect(0, 0, 540, 120, fillColor=colors.HexColor("#F7FAFC"), strokeColor=colors.HexColor("#E2E8F0")))
    d_bs.add(String(180, 55, "[ BS Composition Stacked Bar Chart ]", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor("#4A5568")))
    story.append(d_bs)
    story.append(Spacer(1, 12))

    # 2. Cash Flow Waterfall Placeholder
    story.append(Paragraph("Cash Flow Waterfall (Latest Year)", section_heading))
    d_cf = Drawing(540, 120)
    d_cf.add(Rect(0, 0, 540, 120, fillColor=colors.HexColor("#F7FAFC"), strokeColor=colors.HexColor("#E2E8F0")))
    d_cf.add(String(200, 55, "[ Cash Flow Waterfall Chart ]", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor("#4A5568")))
    story.append(d_cf)
    story.append(Spacer(1, 12))

    # 3. Pros and Cons Section
    pros_cons_data = [
        [
            Paragraph("<b>Pros (Strengths)</b>", section_heading),
            Paragraph("<b>Cons (Risks & Headwinds)</b>", section_heading)
        ],
        [
            Paragraph("• Consistent compounding revenue growth over the past 5 years.<br/>• Strong cash flow from operations (CFO/PAT > 1.0).<br/>• Low leverage and robust balance sheet structure.", pro_style),
            Paragraph("• High valuation multiple compared to industry median.<br/>• Working capital intensity has increased slightly.<br/>• Foreign exchange fluctuation exposure.", con_style)
        ]
    ]
    pc_table = Table(pros_cons_data, colWidths=[265, 265])
    pc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(pc_table)
    story.append(Spacer(1, 12))

    # 4. Capital Allocation Badge
    badge_data = [[Paragraph("<b>Capital Allocation Classification:</b> Compounder / Reinvestor", ParagraphStyle('Badge', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#2B6CB0")))]]
    badge_table = Table(badge_data, colWidths=[540])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#3182CE")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    story.append(badge_table)

    # Build PDF
    doc.build(story)
    print(f"Generated tearsheet: {output_pdf_path}")

def batch_generate():
    base_dir = r"C:\Users\darsh\nifty100_analytics"
    output_dir = os.path.join(base_dir, "output", "tearsheets")
    os.makedirs(output_dir, exist_ok=True)
    
    test_companies = ["TCS", "HDFCBANK", "RELIANCE", "SUNPHARMA", "TATASTEEL"]
    for ticker in test_companies:
        path = os.path.join(output_dir, f"{ticker}_tearsheet.pdf")
        generate_tearsheet(ticker, path)

if __name__ == "__main__":
    batch_generate()

print("Tearsheet generation completed for test companies. ");