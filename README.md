# Foxspark

Foxspark is a Discord LLM integration powered by Ollama. It connects a Discord bot to a local large language model running on your machine.

## Prerequisites

- [Python 3.10+](https://www.python.org/)
- [Ollama](https://docs.ollama.com/quickstart): local LLM runtime (see quick setup below)
- [Discord Application](https://discord.com/developers/applications): Bot for frontend integration

## Clone the Project

Choose a directory where you want the project stored and run:

```bash
git clone <url>
cd <project>
```

## Create and Activate a Virtual Environment

Foxspark uses a Python virtual environment to sandbox dependencies ([learn more about venv](https://docs.python.org/3/library/venv.html)).

### Create the virtual environment

```bash
python3 -m venv .venv
```

### Activate it

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

## Install Dependencies

With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

## Configure .env File

Create a `.env` file in the project root containing:

- `TOKEN`: Your Discord bot token
- `MODEL`: The Ollama model to use (e.g. `gemma3:latest`)

### Template

```dotenv
TOKEN=<discord-bot-token>
MODEL=<model-name>
```

## Ollama Setup

Foxspark requires an Ollama instance running locally.

### 1. Install Ollama

[Follow the official guide](https://docs.ollama.com/quickstart)

### 2. Start the Ollama service

```bash
ollama serve
```

### 3. Download the model specified in your .env

```bash
ollama pull <model-name>
```

### 4. *(Optional)* Test the model manually

```bash
ollama run <model-name>
```

If you see a response, Ollama is working correctly.

## Run the Project

Once Ollama is running and your model is available:

```bash
python3 main.py
```

You should see a message indicating the bot has connected to Discord.
