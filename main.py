import os
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

# 1. Load the API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: API key not found. Check your .env file.")
    exit()

client = genai.Client(api_key=api_key)

# 2. Read the PDF Resume
pdf_filename = "resume.pdf" 
print(f"📄 Reading {pdf_filename}...")
reader = PdfReader(pdf_filename)
resume_text = ""
for page in reader.pages:
    resume_text += page.extract_text()

# 3. Define a sample Job Description (we will make this user input later)
job_description = """
We are looking for a Python Developer Intern.
Requirements:
- Strong Python skills
- Experience with SQL databases
- Knowledge of Machine Learning concepts
- Familiarity with Git and GitHub
- Good communication skills
"""

# 4. Create a powerful prompt
prompt = f"""
You are an expert HR recruiter. Compare the following resume to the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return the analysis in this exact format:
1. Match Score (0-100): [score]
2. Missing Skills: [list them]
3. Strengths: [list them]
"""

# 5. Send to Gemini
print("🤖 Analyzing resume against job description...\n")
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt
)

# 6. Print the result
print("✅ AI Analysis:")
print(interaction.output_text)