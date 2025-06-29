# Blood Test Analyzer API

A FastAPI microservice that:

- Takes as input PDF blood test reports
- Analyzes it via AI agents (CrewAI + LangChain + OpenAI)
- Gives medical analysis, nutrition, and exercise recommendations output

---

## ⚙️ **Original Project Description**

The project initially contained:

- A FastAPI backend that:
  - Takes blood test reports as PDF uploads
  - Passes the reports to a CrewAI pipeline of humorous and satirical “medical” agents
- Tools to:
  - Read PDF files
  - Analyze nutrition
  - Generate exercise plans
- Agents with personalities:
  - Doctor
  - Nutritionist
  - Exercise Specialist
  - Verifier
- Tasks describing how agents should respond

---

## ✅ **Bugs and Issues Fixed**

### 1. Pydantic Warnings

**Original Problem:**

Earlier, Pydantic `DeprecationWarnings` appeared during runtime because of version conflicts with Pydantic v2.

Original code tried suppressing warnings like this:

```python
warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)
```

✅ **Fixed By:**

Setting the environment variable:

```python
import os
os.environ["PYDANTIC_SUPPRESS_DEPRECATION_WARNINGS"] = "1"
```

---

### 2. Asynchronous Method Definitions

**Original Problem:**

Some tool methods were declared as `async` but never integrated into async workflows, e.g. in `BloodTestReportTool`:

```python
async def read_data_tool(path='data/sample.pdf'):
    ...
```

✅ **Fix:**

Refactored these tools to either:
- Become synchronous (if no async code is inside)
- Or properly integrate into the async event loop

---

### 3. Missing PDF Loader Import

**Original Problem:**

`BloodTestReportTool` used:

```python
docs = PDFLoader(file_path=path).load()
```

…but `PDFLoader` was never imported.

✅ **Fixed By:**

Added import:

```python
from langchain_community.document_loaders import PyPDFLoader as PDFLoader
```

---

### 4. Incorrect Tool Class Definitions

**Original Problem:**

- In the tools, methods were defined as static-like functions, e.g.:
  
  ```python
  class BloodTestReportTool:
      async def read_data_tool(...)
  ```
  
…but then referenced as:

```python
BloodTestReportTool.read_data_tool
```

This would give error because those were instance methods and needed either:
- Static methods
- Or instances created

✅ **Fix:**

Refactored tools to:
- Provide static methods for direct usage, e.g.:
  
  ```python
  class BloodTestReportTool:
      @staticmethod
      def read_data_tool(...)
  ```
  
- Or instantiate the tool properly.

---

### 5. Agent and Task Mismatches

**Original Problem:**

- Tasks assigned tools that did not exist or were incorrectly referenced.
- The `llm` variable was undefined in `agents.py`:

  ```python
  llm = llm
  ```

✅ **Fix:**

- Ensured `llm` is defined (e.g. via OpenAI integration).

---

### 6. Server Reload Issue

**Original Problem:**

Earlier code launched Uvicorn like this:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

This causes duplicate worker in some environments.

✅ **Fix:**

Recommend running Uvicorn via CLI instead:

```bash
uvicorn main:app --reload
```

---

### 7. File Cleanup Logic

**Original Problem:**

Earlier code saved uploaded files but failed to ensure cleanup if exceptions occurred.

✅ **Fix:**

Moved file cleanup into the `finally` block in `main.py`:

```python
finally:
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            pass
```

---

## 🚀 **Setup Instructions**

Clone the repo:

```bash
git clone https://github.com/<your-username>/blood-test-analyzer.git
cd blood-test-analyzer
```

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create your `.env` file:

```bash
cp .env.example .env
# Then edit .env to add your API keys
```

Run the server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📬 **API Usage**

### GET /**

Health check endpoint.

```
GET /
```

Response:

```json
{
  "message": "Blood Test Report Analyser API is running"
}
```

---

### POST /analyze

Upload a blood test PDF to generate a humorous medical analysis.

**Request:**

- `file` → PDF blood test report
- `query` → Text prompt (optional)

Example curl:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=Summarise my blood test report"
```

**Response:**

```json
{
  "status": "success",
  "query": "Summarise my blood test report",
  "analysis": "Some humorous or medical analysis...",
  "file_processed": "sample.pdf"
}
```

---

## 🚀 How to Run

```bash
# Install requirements
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Example Response

On sending a POST request to `/analyze`, we will get a JSON response like this:

```json
{
  "status": "success",
  "query": "Summarise my Blood Test Report",
  "analysis": "🩸 Iron & Hemoglobin:\n- Include iron-rich foods like spinach, lentils, and lean meats\n...",
  "file_processed": "my_blood_report.pdf"
}
```



## ✅ **Improvements Made**

- Added Redis/Celery for queued processing of large PDF files
- Connected a database for saving:
  - uploaded reports
  - user queries
  - generated analyses
- Implemented real nutrition and exercise logic
- Proper LLM configuration for production

---

## 🛑 **Disclaimer**

> This project’s agents produce fictional, comedic medical responses. **Not for real medical use.**

