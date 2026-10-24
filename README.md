
# Small Business AI Operations Agent

A local AI-powered task management assistant built with Python, Streamlit, Ollama, and PostgreSQL.

## Features

- Conversational interface using Streamlit
- Local language model using Ollama and Qwen 2.5
- AI tool calling to manage tasks
- PostgreSQL persistence
- Add, list, complete, and delete tasks

## Tech Stack

- Python
- Streamlit
- Ollama
- Qwen 2.5 3B
- PostgreSQL
- Psycopg

## Prerequisites

- Python 3.11 or compatible version
- PostgreSQL
- Ollama

## Setup

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install Ollama and download the model:

   ```bash
   ollama pull qwen2.5:3b
   ```

5. Create a PostgreSQL database named `business_ai` and create the `tasks` table.
6. Create a `.env` file using the following variables:

   ```text
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=business_ai
   DB_USER=postgres
   DB_PASSWORD=your_local_password
   ```

7. Start the application:

   ```bash
   python -m streamlit run app.py
   ```

## Note

This is a learning project and prototype. The local database and AI model must be running for the application to work.
