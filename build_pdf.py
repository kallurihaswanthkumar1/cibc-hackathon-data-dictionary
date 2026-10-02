import csv
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ss = getSampleStyleSheet()
cell = ParagraphStyle("cell", parent=ss["Normal"], fontSize=7, leading=9)
hdr = ParagraphStyle("hdr", parent=cell, textColor=colors.white, fontName="Helvetica-Bold")

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def tbl(path, widths):
    rows = list(csv.reader(open(path, encoding="utf-8")))
    data = [[Paragraph(esc(c), hdr) for c in rows[0]]] + [[Paragraph(esc(c), cell) for c in r] for r in rows[1:]]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#7a1f2b")),
        ("GRID",(0,0),(-1,-1),0.25,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f4f4f4")])]))
    return t

doc = SimpleDocTemplate("docs/CIBC_Hackathon_Data_Dictionary.pdf", pagesize=landscape(letter),
                        leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30,
                        title="CIBC Hackathon - Data Dictionary")
W = 732
s = [Paragraph("Collections Hackathon: Data Dictionary", ss["Title"]), Paragraph("Source: Google Sheet 'CIBC Hackathon - Data Dictionary' (read-only copy)", ss["Normal"]), Spacer(1,10),
     Paragraph("1. About", ss["Heading2"]), tbl("data/about.csv",[120,612]), PageBreak(),
     Paragraph("2. Tables (31)", ss["Heading2"]), tbl("data/tables.csv",[105,65,230,125,70,70,67]), PageBreak(),
     Paragraph("3. Relationships (48)", ss["Heading2"]), tbl("data/relationships.csv",[150,150,150,150]), PageBreak(),
     Paragraph("4. Columns (partial: first 51 of 1,421 rows, customers table)", ss["Heading2"]),
     tbl("data/columns_partial.csv",[70,105,65,30,215,120,127])]
doc.build(s)
