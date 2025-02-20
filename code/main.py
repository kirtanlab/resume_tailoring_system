from pdfminer.high_level import extract_text
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
import uuid
import logging

app = FastAPI()

# Temporary storage (only in memory)
class ResumeJDData(BaseModel):
    resume_text: str
    job_description: str

class JobDescriptionData(BaseModel):
    resume_id: str
    job_description: str

# Logging configuration to print to console
logging.basicConfig(level=logging.INFO)

@app.post("/process")
def process_resume(data: ResumeJDData):
    # Simulate AI processing
    tailored_resume = f"Processed Resume:\n\n{data.resume_text}\n\nMatched with:\n\n{data.job_description}"
    return {"tailored_resume": tailored_resume}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    # Generate a unique filename
    file_id = str(uuid.uuid4())
    file_path = f"/tmp/{file_id}.pdf"

    # Save the file temporarily
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"resume_id": file_id, "message": "Resume uploaded successfully"}

@app.post("/upload-jd")
async def upload_job_description(data: JobDescriptionData):
    # Print the job description to the console
    logging.info(f"Received Job Description for Resume ID {data.resume_id}:")
    logging.info(data.job_description)

    # For now, just returning the received job description
    return {"message": "Job description received and logged", "job_description": data.job_description}     

# pdf_path = "/home/kirtan/Documents/resume_tailoring_system/kirtan_latex_resume.pdf"  # Replace with your PDF file
# text = extract_text(pdf_path)


