# infrastructure/statements/pdf_statement_adapter.py

#from reportlab.pdfgen import canvas

#class PDFStatementAdapter:
 #   def generate(self, account, transactions, filename="statement.pdf"):
 #       c = canvas.Canvas(filename)
#        c.drawString(100, 800, f"Statement for Account: {account.account_number}")

 #       y = 760
 #           c.drawString(100, y, f"{t.timestamp.date()} | {t.type.upper()} | ${t.amount}")
  #          y -= 20

  #      c.save()


# infrastructure/statements/csv_statement_adapter.py

import csv

class CSVStatementAdapter:
    def generate(self, account, transactions, filename="statement.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Amount"])
            for t in transactions:
                writer.writerow([t.timestamp.strftime("%Y-%m-%d"), t.type, t.amount])
