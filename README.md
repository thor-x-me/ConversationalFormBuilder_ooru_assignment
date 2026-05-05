# ConversationalFormBuilder — Setup Guide

A conversational AI-powered form builder that uses a local LLM (via Ollama) as its inference backend and Form.io as the form engine.

---

## Prerequisites

- [Docker](https://www.docker.com/) installed and running
- [Git](https://git-scm.com/) installed
- Python 3.11+
- A modern web browser

---

## Step 1 — Run Form.io with Docker

Follow the official Form.io self-hosted setup using Docker:

👉 [https://github.com/formio/formio](https://github.com/formio/formio)

The quickest way to get Form.io running locally is via Docker Compose. Clone the Form.io repo and follow their Docker instructions to spin up the API server and MongoDB instance.

```bash
git clone https://github.com/formio/formio.git
cd formio
# Follow the Docker setup instructions in their README
```

Make sure Form.io is up and accessible (typically at `http://localhost:3001`) before proceeding.

---

## Step 2 — Clone This Repository

```bash
git clone https://github.com/thor-x-me/ConversationalFormBuilder_ooru_assignment.git
cd ConversationalFormBuilder_ooru_assignment
```

---

## Step 3 — Install Ollama

Download and install Ollama for your operating system:

👉 [https://ollama.com/download](https://ollama.com/download)

Follow the installer instructions for your platform (macOS, Linux, or Windows).

---

## Step 4 — Pull the Model & Verify Inference

Pull the `qwen3.5:latest` model and verify that inference is working:

```bash
ollama run qwen3.5:latest
```

Once the model loads, type a test prompt in the interactive session to confirm it responds correctly. Press `Ctrl+D` or type `/bye` to exit.

---

## Step 5 — Set Up Python Environment

Create a virtual environment and install all dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 6 — Run the Backend Server

Start the FastAPI backend using Uvicorn:

```bash
uvicorn app:app --reload
```

The server runs at **`http://localhost:8000`** by default.

> ⚠️ **Changing the port:** If you need to use a different port, update the port number in both the Uvicorn command **and** the frontend file to keep them in sync.

---

## Step 7 — Open the Frontend

Open the frontend HTML file directly in your browser:

```
frontend/index.html   (or whichever path applies in this repo)
```

You can simply double-click the file in your file explorer, or open it via your browser's **File → Open** menu.

Once open, you're all set — start building forms conversationally! 🎉

---

## Quick Reference

| Component     | Default URL                  |
|---------------|------------------------------|
| Form.io API   | `http://localhost:3001`      |
| Backend API   | `http://localhost:8000`      |
| Ollama        | `http://localhost:11434`     |
| Frontend      | Open `chatbot_frontend.html` in browser |

---

## Troubleshooting

- **Ollama not responding?** Make sure the Ollama service is running in the background (`ollama serve`).
- **Backend 500 errors?** Confirm the model name in your code matches exactly: `qwen3.5:latest`.
- **Form.io connection issues?** Ensure Docker containers are running (`docker ps`) and Form.io is healthy before starting the backend.
- **Port conflicts?** Change the port in both `uvicorn` startup command and the frontend's API base URL.
