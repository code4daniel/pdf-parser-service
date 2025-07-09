import pdfplumber
import re

def extract_cutoffs_from_pdf(pdf_path, university_name):
    cutoffs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")

            for line in lines:
                if not line.strip() or "PROGRAMME" in line or "Page" in line:
                    continue

                match = re.match(r"^\d+\s+(.*?)\s+([A-Z]{2,5})\s+([\d.]+)(?:\s+([\d.]+))?$", line.strip())
                if match:
                    course_name = match.group(1).strip()
                    course_code = match.group(2).strip()
                    cutoff_all = float(match.group(3))
                    cutoff_female = float(match.group(4)) if match.group(4) else None

                    cutoffs.append({
                        "university": university_name,
                        "course_name": course_name,
                        "course_code": course_code,
                        "cutoff_all": cutoff_all,
                        "cutoff_female": cutoff_female
                    })
    return cutoffs
