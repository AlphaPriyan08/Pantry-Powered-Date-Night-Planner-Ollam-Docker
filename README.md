# 🕯️ Pantry-Powered Date-Night Planner (Self-Hosted with Ollama)

An interactive AI agent that transforms your available pantry ingredients into a complete, personalized, and romantic date-night plan. This project demonstrates the power of Large Language Models (LLMs) and conversational AI frameworks to create a helpful and engaging user experience.

This version is fully self-hosted, running locally with Ollama and Docker, ensuring your data remains completely private.

The agent doesn't just give you a recipe; it acts as a "romance concierge," helping you plan the meal, the ambiance, and even a conversation starter, refining its suggestions based on your feedback.

---

## ✨ Features

-   **Conversational Planning:** Tell the agent what ingredients you have, and it will start the planning process.
-   **Holistic Experience:** Get suggestions for a main dish, ambiance (music & lighting), decor, and an icebreaker.
-   **Iterative Refinement:** The agent asks for your feedback and adjusts the plan until you say it's perfect. It remembers the context of the conversation.
-   **Interactive UI:** A simple and clean chat interface powered by Streamlit.
-   **100% Local & Private:** Runs entirely on your machine using Ollama and Docker. No data ever leaves your computer.

---

## 🛠️ Tech Stack

-   **LLM Framework:** LangChain – Used to orchestrate the agent's logic, manage memory, and chain prompts.
-   **Local LLM:** Ollama with Llama 3 – The local generative model that powers the agent's creativity.
-   **Web Framework:** Streamlit – Used to rapidly build the interactive chat-based user interface.
-   **Containerization:** Docker & Docker Compose – For creating a consistent, portable, and easy-to-run environment.

---

## 🚀 Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

-   [Git](https://git-scm.com/downloads)
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
-   [Ollama](https://ollama.com/) installed and running.

### Installation & Setup

1.  **Pull the LLM model:**
    Before starting the app, you need to download the AI model. Open your terminal and run:
    ```bash
    ollama pull llama3:8b
    ```

2.  **Clone the repository:**
    Get the project files onto your machine.
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
    *(Remember to replace `your-username` and `your-repo-name` with your actual GitHub details!)*

3.  **Build and run the application with Docker Compose:**
    This single command builds the container and starts the application.
    ```bash
    docker compose up --build
    ```

4.  **Open the application:**
    Once the build is complete, open your web browser and navigate to:
    **[http://localhost:8501](http://localhost:8501)**

You can now start planning your perfect date night!