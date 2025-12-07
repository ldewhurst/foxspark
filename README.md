# Foxspark

Foxspark is a Discord LLM integration powered by Ollama. It connects a Discord bot and a Twitch Application to a local large language model running on your machine to moderate your community.

## Prerequisites

- [Python 3.10+](https://www.python.org/)
- [Ollama](https://docs.ollama.com/quickstart): local LLM runtime (see quick setup below)

## Clone the Project

Choose a directory where you want the project stored and run:

```bash
git clone git@github.com:ldewhurst/foxspark.git
cd foxspark
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

## Configure Applications

You need to configure a [Discord](https://discord.com/developers/applications) and [Twitch](https://dev.twitch.tv/docs/authentication/register-app) application for Foxspark to interface with these platforms.

Configure Foxspark by creating a `.env` file in the project root containing:

- `OLLAMA_MODEL`: The Ollama model to use.
- `DISCORD_TOKEN`: **(Secret)** Your Discord bot token
- `TWITCH_CLIENT_ID`: Your Twitch application's client id.
- `TWITCH_CLIENT_SECRET`: **(Secret)** Your Twtich application's client secret.

**Do not reveal this file to anyone! Do not commit this file to the repository!** Anyone with secrets can connect to your applications.

### Template

```dotenv
OLLAMA_MODEL="gemma3:latest"
DISCORD_TOKEN="discord-bot-token"
TWITCH_CLIENT_ID="twitch-client-id"
TWITCH_CLIENT_SECRET="twitch-secret"
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
