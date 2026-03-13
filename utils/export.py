import os
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


async def export_to_excel(applications: list) -> str:
    export_dir = "exports"
    os.makedirs(export_dir, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Applications"

    headers = ["ID", "Name", "Phone", "Description", "Status", "Created at"]
    ws.append(headers)

    for col_num, _ in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    for app in applications:
        ws.append([
            app.id,
            app.name,
            app.phone,
            app.description,
            app.status,
            str(app.created_at),
        ])

    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 40
    ws.column_dimensions["E"].width = 15
    ws.column_dimensions["F"].width = 24

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(export_dir, f"applications_{timestamp}.xlsx")
    wb.save(filepath)
    return filepath