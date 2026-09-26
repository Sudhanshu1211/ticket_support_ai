# AI Support Ticket Analyzer

An AI-powered customer support intake and ticket analysis tool built with Python, LangChain, Google Gemini, Pydantic, and Streamlit.

The application accepts support requests in several formats and uses Gemini to classify each request by category, urgency, customer sentiment, summary, affected product or feature, confidence score, and suggested next action.

## Features

- Direct support query input
- Guided issue form with customer details
- Email-to-ticket conversion
- Urgent issue reporting
- Knowledge and feature explanation requests
- Structured AI output validated with Pydantic
- Ticket category classification
- Urgency and sentiment detection
- Suggested next action for support teams
- Recent analysis history during the current app session
- Navy-themed Streamlit interface

## Technology Stack

- Python
- Streamlit
- LangChain
- `langchain-google-genai`
- Google Gemini
- Pydantic
- python-dotenv

## Project Structure

```text
project1.1/
├── frontend.py   # Streamlit user interface
├── main.py       # Gemini analysis pipeline and data models
├── test.py       # API connectivity test
├── .env          # Local API key, not committed to Git
└── .gitignore    # Protects secrets and virtual environment files
```

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install streamlit langchain langchain-core langchain-google-genai pydantic python-dotenv
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Never commit `.env` or share your API key publicly.

## Run the Application

Start the Streamlit frontend:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Test API Connectivity

```powershell
.\.venv\Scripts\python.exe test.py
```

The test confirms that the API key loads and Gemini responds successfully.

## Command-Line Mode

The analyzer can also be used from the terminal:

```powershell
.\.venv\Scripts\python.exe main.py
```

Enter a support query when prompted. The result is printed as structured JSON.

## How It Works

1. A user submits a support request through the Streamlit interface.
2. The request is passed to a LangChain prompt template.
3. Gemini analyzes the request using the ticket analysis schema.
4. Pydantic validates the structured response.
5. The frontend displays the category, urgency, sentiment, summary, confidence, and recommended action.

## Current Limitations

- Analysis history is stored only in Streamlit session state.
- Tickets are not yet saved to a database.
- There is no authentication or support-agent dashboard.
- Email notifications and ticket assignment are not implemented.
- The confidence score is supplied by the model and is not independently calibrated.

## Future Improvements

- Add SQLite or PostgreSQL ticket storage
- Add ticket IDs and status tracking
- Add support-agent assignment and filtering
- Add email notifications
- Add automated tests with mocked Gemini responses
- Add input validation and human-review escalation
- Add a knowledge-base search system

## Security Notes

- Keep API keys in `.env` or a secure secrets manager.
- Do not commit `.env` to GitHub.
- Avoid sending unnecessary personal or confidential information to external AI services.
- Review AI-generated classifications before taking high-impact actions.
