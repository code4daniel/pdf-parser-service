import requests
from bs4 import BeautifulSoup
import pdfplumber
import re
import json
import os


# ---- step 1: find the latest cutoff pdf 
base_url = "https://mak.ac.ug"
cutoff_page_url = f"{base_url}/study-mak/cut-points"

response = requests.get(cutoff_page_url)
soup = BeautifulSoup(response.text, "html.parser")

pdf_links = [a['href'] for a in soup.find_all('a', href=True) 
              if a['href'].endswith('.pdf')]

if not pdf_links:
    raise Exception("No PDF links found on the page")


#  take the first (most recent  pdf)
pdf_url = pdf_links[0]
if not pdf_url.startswith("http"):
    pdf_url = base_url + pdf_url

print("Found PDF: ", pdf_url)



# step 2: Download pdf

pdf_filename = "latest_cutoffs.pdf"
with open(pdf_filename, "wb") as f:
    f.write(requests.get(pdf_url).content)

print("PDF Downloaded")


# STEP 3: Extract course cutoff

cutoffs = []

with pdfplumber.open(pdf_filename) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")


        for line in lines:
            if not line.strip() or "PROGRAMME" in line or "Page" in line:
                continue

            match = re.match(r"^\d+\s(.*?)\s+([A-Z]{2,3})\s+([\d.]+)(?:\s([\d.]+))?$", line.strip())
            if match:
                course_name = match.group(1).strip()
                course_code = match.group(2).strip()
                cutoff_all = float(match.group(3))
                cutoff_female = float(match.group(4)) if match.group(4) else None

                cutoffs.append({
                    "course_name": course_name,
                    "course_code": course_code,
                    "cutoff_all" : cutoff_all,
                    "cutoff_female": cutoff_female
                })




#  step 4: Save to JSON
output_path = "cutoffs_extracted.json"
with open(output_path, "w") as f:
    json.dump(cutoffs,f,indent=2)

print(f"Extracted {len(cutoffs)} courses and saved to {output_path}.")


# os.remove(pdf_filename)