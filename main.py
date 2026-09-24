import os
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

# 1. Load the API key from the .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: API key not found. Check your .env file.")
    exit()

# 2. Set up the Gemini Client
client = genai.Client(api_key=api_key)

# 3. Read the PDF
# (Put a resume PDF in your folder and change the name below)
pdf_filename = "resume.pdf" 
print(f"📄 Reading {pdf_filename}...")

reader = PdfReader(pdf_filename)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# 4. Send to Gemini
print("🤖 Asking the AI...\n")
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=f"List 5 skills from this resume:\n\n{full_text}"
)

# 5. Print the result
print("✅ AI Response:")
print(interaction.output_text)