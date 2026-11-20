# GPU-LMStudio-Chat

A powerful, terminal-based Python application that allows you to interact with local Large Language Models (LLMs) via [LM Studio](https://lmstudio.ai/). Experience the power of local AI with customizable personalities and detailed interaction logging.

## 🚀 Key Features

### 🏠 Fully Local AI
Powered by **LM Studio**, this application connects to LM Studio's local OpenAI-compatible server. Your conversations stay on your machine, subject to the model and server settings you choose.

### 🎭 Immersive Personalities
Transform your AI interaction with four distinct personas. You can switch between them to change the tone and style of the response:

*   **Jeeves**: Your faithful and impeccable servant. Always ready to assist with utmost respect and precision.
*   **SageBrush**: The Mystic Sage of the mountain top. Ponders the imponderable, responding with cryptic and mystical language.
*   **Captain RedEye**: A ruthless and salty pirate. Expect aggressive, bold, and high-seas-inspired responses.
*   **The Dull Assistant**: The definition of boring. Provides the most basic, uninspired, and monotonous responses possible.

### 📊 Advanced AI Tracking
Never lose a thought. The application automatically logs every interaction to a local SQLite database (`PythonLogAI/`), tracking:
*   Question & Answer text
*   Model used
*   Tokens consumed (Input/Output)
*   Time taken for response
*   Word counts

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:

1.  **LM Studio**: The local model server. [Download here](https://lmstudio.ai/).
2.  **Python 3.x**: Ensure Python is installed and added to your system's PATH.

## ⚙️ Installation

1.  **Clone the repository** (if applicable).
2.  **Install the required Python libraries** using pip:

    ```bash
    pip install colorama openai pandas
    ```

3.  In LM Studio, download a model and start the local server with the OpenAI-compatible API enabled. The default endpoint is `http://127.0.0.1:1234/v1`. Set `LM_STUDIO_BASE_URL` or `LM_STUDIO_API_KEY` if your server uses different connection settings.

## 🚀 Usage

Once everything is set up, simply run the script:

```bash
python GPU-lmstudio-chat.py
```

**Follow the interactive menu to:**
1.  **Select your model**: Choose from the models reported by LM Studio.
2.  **Choose a personality**: Select the persona that fits your mood.
3.  **Chat**: Start typing your questions!

## 🛠️ Technical Details

*   **Logging**: Uses a dedicated `PythonLog` module to track application performance and interaction metrics.
*   **Database**: Data is stored in a local SQLite database. If the project database is read-only or unavailable, the application attempts to save logs under `~/.gpu-lmstudio-chat/PythonLogAI/`.
*   **Colors**: Uses `colorama` for a rich, readable terminal experience.

---
**Author:** Daniel Morvay
**License:** MIT
