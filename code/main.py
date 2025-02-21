from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import shutil
import os
import uuid
import logging
from resume_agent import ResumeAgent
from jd_agent import JD_agent

app = FastAPI()

# Logging configuration to print to console
logging.basicConfig(level=logging.INFO)

@app.post("/upload-resume-jd")
async def upload_resume_jd(file: UploadFile = File(...), job_description: str = Form(...)):
    # Generate a unique filename
    file_id = str(uuid.uuid4())
    file_path = f"/tmp/{file_id}.pdf"

    # Save the file temporarily
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Log the received job description
    if(job_description and file_id): 
        print("Content received")
    else: 
        return "No Content Received"

    # logging.info(f"Received Job Description for Resume ID {file_id}:")
    # logging.info(job_description)
    
    #------------------------RESUME AGENT----------------------------------------

    # Process resume with AI model 
    resume_agent = ResumeAgent(file_path)
    resume_content = resume_agent.analyze_resume()

    #------------------------JD AGENT----------------------------------------

    #process jd with AI model 
    jd_agent = JD_agent(job_description)
    jd_extract = jd_agent.analyze_jd()

    print("jd_extract: ",jd_extract)

    return {
        "resume_id": file_id,
        "message": "Resume and Job Description processed successfully",
        "tailored_resume": jd_extract['content']
    }
