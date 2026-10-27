
# RADIX Talent Check

## Project Overview

RADIX Talent Check is a web application that evaluates a candidate's skill readiness against company skill requirements. It calculates a readiness score and identifies skill gaps to help understand areas for improvement.

The project includes a Python backend API and a React frontend.

## Features

- Upload candidate skill profile and company requirement files.
- Calculate a skill readiness score.
- Identify skill gaps and shortfalls.
- Display evaluation results in a web interface.
- Download evaluation results as JSON.
- Handle invalid inputs and display error messages.
- Use synthetic benchmark data for demonstration.

## Technologies Used

- Python
- FastAPI
- React
- Vite
- JavaScript
- HTML and CSS
- Pytest

## Project Structure

```text
radix-talent-check/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── benchmarks.py
│   ├── scoring.py
│   ├── requirements.txt
│   ├── samples/
│   └── tests/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
├── .gitignore
└── README.md
```

## Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version
- Node.js and npm
- Git

## Backend Setup

From the project root, create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
py -m pip install -r backend/requirements.txt
```

Start the backend API:

```powershell
py -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## Frontend Setup

Open a second terminal at the project root and run:

```powershell
cd frontend
npm ci
npm.cmd run dev
```

Open the local frontend URL displayed in the terminal, usually:

http://localhost:5173/

## Running Tests

From the project root, run:

```powershell
py -m pytest backend/tests -q
```

## Sample Data

Sample input files are available in `backend/samples/`.

These files contain fictional demonstration data and should be used for testing the application.

## Benchmark Limitations

The current demonstration uses synthetic benchmark data. It does not represent verified industry-wide skill benchmarks.

A live or authorized benchmark source must be configured separately before real benchmark integration can be claimed.

## API Endpoints

- `POST /api/team/v1/talent-check/evaluate` — Evaluates a candidate profile against company requirements.
- `GET /api/team/v1/talent-check/benchmark-status` — Reports benchmark availability.

Evaluation requests use multipart form data with the fields `profile_file`, `company_file`, and `benchmark_mode`.

## Security and Data Handling

Do not commit passwords, API keys, environment secrets, private candidate profiles, or other confidential information to this repository.

## Current Status

This project is a development implementation intended for demonstration and testing. Final verification should include automated tests, frontend build checks, and testing from a fresh Git checkout.

