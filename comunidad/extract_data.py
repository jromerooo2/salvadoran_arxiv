from email.message import EmailMessage
from string import Template
import smtplib, time, os
import pandas as pd
import json

# Public Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/1Hl-ufwePxMax_mmELmMGVEMVwUgeTWCUui49fe7RilI/edit?usp=sharing"

# Extract the sheet ID and build a CSV export URL
sheet_id = sheet_url.split("/d/")[1].split("/")[0]
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"


# Read into a DataFrame
df = pd.read_csv(csv_url)

recipients = [
    {
        "name": "" if pd.isna(row["Nombre y Apellido"]) else row["Nombre y Apellido"],
        "titulo_afiliacion": "" if pd.isna(row["Título y afiliación actual"]) else row["Título y afiliación actual"],
        "correo_institucional": "" if pd.isna(row["Correo electrónico institucional"]) else row["Correo electrónico institucional"],
    }
    for _, row in df.dropna(subset=["Nombre y Apellido"]).iterrows()
    if str(row["Nombre y Apellido"]).strip()
]

for i, rep in enumerate(recipients, start=1):
    print(f"{i}. {rep}")

    # After looping, save the recipients list as 'people.json'
    with open('people.json', 'w', encoding='utf-8') as f:
        json.dump(recipients, f, ensure_ascii=False, indent=2)