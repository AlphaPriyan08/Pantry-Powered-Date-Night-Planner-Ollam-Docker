import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from typing import List, Dict, Any, Optional

# Import the universal file processor
from file_processor import process_uploaded_files

# --- Configuration and Initialization ---
st.set_page_config(page_title="Pantry-Powered Date-Night Planner (Local)", page_icon="🏡")

# --- MODEL AND PROMPT SETUP ---
# Use a multimodal model like llava. The ":latest" tag is usually fine.
LOCAL_MODEL_NAME = "llava:7b" 
# This URL is crucial for Dockerized setups. It allows the Streamlit container
# to communicate with the Ollama service running on the host machine.
OLLAMA_BASE_URL = "http://host.docker.internal:11434"

# The prompt template can now be identical to the Gemini version.
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Act as a world-renowned, imaginative, and romantically intuitive date night planner with 20+ years of experience. You specialize in turning ordinary pantry items—whether shared through typed messages, PDFs, text files, or even image uploads—into extraordinary, intimate evenings.

            Your role is to be the user's magical behind-the-scenes designer, crafting every detail of their dream date night: the food, the ambiance, the connection, and the atmosphere. You take pride in making every moment feel bespoke and unforgettable.

            MULTIMODAL INTELLIGENCE:
            - Your input for a user's turn may contain a combination of text and images.
            - If the input contains text labeled "Content from uploaded file:", you MUST prioritize and base the plan on that content.
            - If the input contains an image, you must extract and analyze all visible ingredient labels or recognizable food items.
            - Always **combine** all sources (typed text, file text, images) into a unified ingredient list before planning.

            YOUR STEP-BY-STEP STRATEGY:
            1. Extract and synthesize all ingredients from every available source in the user's latest message.
            2. Identify the best romantic dish (or dishes) that can be made using these ingredients.
            3. If it elevates the recipe, suggest up to two optional but common pantry ingredients.
            4. Design the ambiance: lighting, music, and decor ideas tailored for a cozy, romantic home setting.
            5. Recommend a meaningful or playful icebreaker or activity that sparks conversation or intimacy.
            6. Present your full plan in the structured, emoji-enhanced Markdown format shown below.
            7. End your plan with the question: 
               **"How does this sound for your date night? Feel free to ask for changes to any part of the plan—the recipe, the music, anything at all!"**
            8. Wait for user feedback and improve the plan iteratively until the user replies with something like: **"Yes, this is perfect!"**
            9. Upon final confirmation, respond with a short, warm, celebratory closing—never generate a new plan at this point.

            MEMORY & INTERACTION RULES:
            - Use the chat history to track evolving preferences (e.g., dietary restrictions, spice levels, cheese preferences, lighting tone, etc.).
            - Ask thoughtful, open-ended questions to clarify or expand on vague user input.
            - Do NOT repeat suggestions unless explicitly requested.
            - Remember everything about the current session until it’s completed.

            FORMATTING & STYLE (ALWAYS USE THIS STRUCTURE):
            - 🍽️ **Recipe Suggestion**: [Name of the dish]
              • **Ingredients Identified**: 
                - [Ingredient 1 from any source]\n
                - [Ingredient 2...]\n
                - [Ingredient 3...]\n
              • **Optional Additions**: [Optional 1], [Optional 2]
              • **Preparation Steps**:
                1. [Step one]\n
                2. [Step two]\n
                3. [Step three]\n
                Each step should be in a new line, starting with a number and consistent formatting.
            - 🎶 **Ambiance**: [Music genre or playlist idea]
            - 🕯️ **Decor**: [Lighting mood, aesthetic details, props]
            - 💬 **Icebreaker**: [Fun game, meaningful prompt, or playful challenge]

            STYLE REQUIREMENTS:
            - Always use **Markdown** formatting with bold headers.
            - Start each preparation step on a **new line with a number**.
            - Maintain a **charming, inviting, poetic tone**—as if you’re designing a fairytale evening for two.

            Take a deep breath and work on this problem step-by-step.
            """
        ),
        MessagesPlaceholder(variable_name="chat_history"),
    ]
)

# Initialize the Ollama LLM
llm = ChatOllama(model=LOCAL_MODEL_NAME, temperature=0.7, base_url=OLLAMA_BASE_URL)
chain = prompt_template | llm | StrOutputParser()

# --- Session State Management ---
def initialize_session_state():
    """Initializes session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm your local date night planner. What ingredients do you have? Upload photos, text files, or PDFs!"),
        ]
    if "conversation_active" not in st.session_state:
        st.session_state.conversation_active = True

initialize_session_state()

# --- Core Response Generation Function (Now unified and robust) ---
def generate_ai_response(user_prompt: str, image_parts: Optional[List[Dict[str, Any]]] = None, extracted_text: str = ""):
    """
    Handles AI response generation by constructing a single multimodal message.
    This works seamlessly for both ChatOllama and other modern LLM providers.
    """
    with st.spinner("The local chef is thinking..."):
        user_message_content = []

        # Add text from files first
        if extracted_text:
            user_message_content.append({"type": "text", "text": f"Content from uploaded files:\n{extracted_text}"})

        # Add the user's typed prompt, including a nudge for VLMs
        prompt_with_nudge = user_prompt
        if image_parts:
            prompt_with_nudge += "\n\nPlease analyze the ingredients in the attached image(s) and use them in your plan."
        
        user_message_content.append({"type": "text", "text": prompt_with_nudge})

        # Add any image parts (already in the correct base64 format)
        if image_parts:
            user_message_content.extend(image_parts)

        # Create the multimodal HumanMessage
        human_message = HumanMessage(content=user_message_content)
        st.session_state.chat_history.append(human_message)

        # Invoke the chain
        ai_response = chain.invoke({
            "chat_history": st.session_state.chat_history
        })
        st.session_state.chat_history.append(AIMessage(content=ai_response))

# --- UI Rendering & Main Application Flow (Now robust for multimodal messages) ---
st.title("🕯️ Pantry-Powered Date-Night Planner (Local)")

# Display chat history
for message in st.session_state.chat_history:
    avatar = "🏡" if isinstance(message, AIMessage) else "👤"
    with st.chat_message(name="AI" if isinstance(message, AIMessage) else "Human", avatar=avatar):
        if isinstance(message.content, list):
            # Display text and image placeholders from multimodal messages
            text_parts = [part['text'] for part in message.content if part['type'] == 'text']
            st.markdown("\n\n".join(text_parts))
            
            num_images = sum(1 for part in message.content if part.get('type') == 'image_url')
            if num_images > 0:
                st.info(f"🖼️ *{num_images} image(s) were attached to this message.*")
        else:
            # Standard text content for AI messages
            st.markdown(message.content)

# Main Application Flow (Unchanged logic, but now interacts with the new response generator)
if st.session_state.conversation_active:
    if len(st.session_state.chat_history) > 1:
        st.write("---")
        st.write("Need some ideas?")
        cols = st.columns(3)
        suggestions = {
            "Yes, this is perfect!": {"is_conclusive": True},
            "Suggest a different recipe": {"is_conclusive": False},
            "Change the ambiance": {"is_conclusive": False},
        }
        
        button_prompts = list(suggestions.keys())
        buttons = [cols[i].button(prompt, use_container_width=True) for i, prompt in enumerate(button_prompts)]

        for i, (prompt, props) in enumerate(suggestions.items()):
            if buttons[i]:
                if props["is_conclusive"]:
                    st.session_state.conversation_active = False
                generate_ai_response(prompt)
                st.rerun()
                
    with st.form(key="input_form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Upload ingredients (images, txt, pdf)",
            type=["txt", "pdf", "png", "jpg", "jpeg"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        user_prompt = st.text_input("What would you like to do?", key="chat_input", placeholder="Tell me what you have, or ask for changes...")
        submit_button = st.form_submit_button(label="Plan my date!")

    if submit_button and (user_prompt or uploaded_files):
        text_from_files, image_data = process_uploaded_files(uploaded_files, st)
        prompt_for_ai = user_prompt or "Please create a plan based on the attached file(s)."
        generate_ai_response(prompt_for_ai, image_data, text_from_files)
        st.rerun()
else:
    st.success("Enjoy your magical date night! ✨")
    if st.button("Start a New Plan"):
        keys_to_clear = ["chat_history", "conversation_active"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()