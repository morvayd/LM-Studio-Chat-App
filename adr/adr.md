# GPU-lmstudio-chat.py - Application Purpose

**Overall Purpose:**
This is an interactive command-line chatbot that connects to locally hosted language models through LM Studio's OpenAI-compatible API. It provides selectable models, multiple personality modes, streaming responses, and local conversation logging.

## Configuration and System Variables

- **`strModel`** - Model selected from the models reported by LM Studio
- **`strThink`** - Toggle for the detailed-response prompt mode ("Yes"/"No")
- **`strPirate`** - Toggle for pirate personality mode ("Yes"/"No")
- **`strJeeves`** - Toggle for Jeeves (butler) personality mode ("Yes"/"No")
- **`strMystic`** - Toggle for mystic personality mode ("Yes"/"No")
- **`strPythonScript`** - Script name recorded in Python logs: `GPU-LMStudio-chat.py`
- **`strModified`** - Last modification date recorded in Python logs
- **`strPC`**, **`strUser`**, **`strOS`** - Hostname, username, and operating system

## LM Studio Connection

- **`LM_STUDIO_BASE_URL`** - API base URL, defaulting to `http://127.0.0.1:1234/v1`; can be overridden with an environment variable
- **`LM_STUDIO_API_KEY`** - API key sent by the OpenAI client; defaults to `lm-studio` for the local server and can be overridden with an environment variable
- **`AIclient`** - OpenAI Python client configured for the LM Studio endpoint
- **`LMStudioModel(client)`** - Lists models available from the server and prompts the user to select one

The local server must be running in LM Studio with its OpenAI-compatible API enabled.

## Conversation and Tracking Variables

- **`strQuestion`** - User input or command
- **`strAnswer`** - Streamed response text
- **`dictToSend`** - Message payload sent to the selected model
- **`strRequest`** - Prompt with the selected role/personality instructions
- **`strInputTokens`**, **`strOutputTokens`** - Token counts reported by the streaming response; remain zero if usage is not provided
- **`strInputWords`**, **`strAnswerWords`** - Question and response word counts
- **`strTimeDelta`** - Response duration
- **`strDBFile`** - Primary SQLite log database at `PythonLogAI/<hostname>-AILog.db`

If the primary database is read-only or unavailable, the application attempts to save the interaction under `~/.gpu-lmstudio-chat/PythonLogAI/` and reports the fallback location.

## Core Functionality

1. Select from models reported by LM Studio.
2. Chat with streamed model responses.
3. Switch between standard, pirate, Jeeves, and mystic prompt styles.
4. Toggle detailed-response prompting.
5. Log conversations, model names, token counts, word counts, and response times to SQLite.
6. Display color-coded terminal output using Colorama.
