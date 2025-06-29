import os
os.environ["PYDANTIC_SUPPRESS_DEPRECATION_WARNINGS"] = "1"

import warnings
warnings.filterwarnings("ignore", message=".*PydanticDeprecatedSince20.*")


from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import asyncio
from typing import Optional


from crewai import Crew, Process, Task
from agents import doctor, verifier

app = FastAPI(title="Blood Test Report Analyzer")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define tasks inline (since task.py might be missing)
verification = Task(
    description=(
        "Verify that the document at {file_path} is a valid blood test report with readable medical data. "
        "Check for the presence of key blood markers, laboratory values, and ensure the document structure "
        "is consistent with standard medical lab reports. Validate data quality and completeness before analysis."
    ),
    expected_output=(
        "A verification report confirming the document is a valid blood test with a summary of key sections found, "
        "including patient information, test parameters, reference ranges, and any quality issues identified."
    ),
    agent=verifier
)

help_patients = Task(
    description=(
        "Analyze the blood test report at {file_path} to answer the patient's query: '{query}'. "
        "Provide detailed medical insights, identify abnormal values, explain their significance, "
        "and offer evidence-based recommendations. Consider the patient's specific concerns and "
        "provide clear, understandable explanations of their blood work results."
    ),
    expected_output=(
        "A comprehensive medical analysis including: "
        "1. Summary of all blood markers and their values "
        "2. Identification of abnormal results with explanations "
        "3. Health implications and potential concerns "
        "4. Evidence-based recommendations for improvement "
        "5. Suggestions for follow-up care or lifestyle modifications "
        "6. Clear answers to the patient's specific query"
    ),
    agent=doctor,
    dependencies=[verification]  # This task depends on verification completing first
)

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the medical analysis crew"""
    try:
        medical_crew = Crew(
            agents=[verifier, doctor],
            tasks=[verification, help_patients],
            process=Process.sequential,
            verbose=True
        )
        
        inputs = {
            'query': query,
            'file_path': file_path
        }
        
        result = medical_crew.kickoff(inputs)
        return result
    except Exception as e:
        raise Exception(f"Error running crew: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Blood Test Report Analyzer API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "ai_agents": "ready",
            "file_system": "accessible"
        }
    }

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Please analyze my blood test report and provide a comprehensive summary")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"uploads/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure uploads directory exists
        os.makedirs("uploads", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            f.write(content)
        
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Please analyze my blood test report and provide a comprehensive summary"
        
        # Process the blood report with medical crew
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename,
            "timestamp": str(uuid.uuid4())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                print(f"Warning: Could not clean up file {file_path}: {cleanup_error}")

@app.post("/analyze-sample")
async def analyze_sample_report(
    query: str = Form(default="Please analyze the sample blood test report")
):
    """Analyze the sample blood test report"""
    
    sample_path = "data/sample.pdf"
    
    if not os.path.exists(sample_path):
        raise HTTPException(status_code=404, detail="Sample blood test report not found")
    
    try:
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Please analyze the sample blood test report"
        
        # Process the sample blood report
        response = run_crew(query=query.strip(), file_path=sample_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": "sample.pdf",
            "timestamp": str(uuid.uuid4())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sample report: {str(e)}")

# Don't use uvicorn.run() with reload=True in the main script
# This causes the warning you're seeing
