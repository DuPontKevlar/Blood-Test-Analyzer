"""
Celery worker setup for Blood Test Analyzer API.

This module defines a Celery app that could be used
for background tasks such as PDF processing, heavy analysis, etc.
"""

from celery import Celery

celery_app = Celery(
    "blood_test_analyzer",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

@celery_app.task
def analyze_pdf_task(file_path: str, query: str) -> str:
    """
    Dummy Celery task to simulate PDF analysis.

    Args:
        file_path (str): Path to the uploaded PDF file.
        query (str): The user query or prompt.

    Returns:
        str: Simulated analysis result.
    """
    # Invoke CrewAI logic or LLM calls
    return f"Simulated analysis for file {file_path} with query: {query}"
