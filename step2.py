import streamlit as st
import openai

# Set your OpenAI API key
from secrets import api_key

openai.api_key = api_key

st.title("Learn How to Use ChatGPT")
st.write("Let's learn how to write effective prompts!")

# User input
user_prompt = st.text_area("Enter your prompt:")


def evaluate_prompt(prompt):
    """Evaluates the quality of the prompt."""
    if len(prompt.split()) < 3:
        return "The prompt is too short and written like a Google search. Try to rewrite it with more details or a specific question."
    if "cat breeds" in prompt.lower() and len(prompt.split()) <= 5:
        return "The prompt could be more specific. Try asking for differences between specific breeds or details about their characteristics."
    return None

def evaluate_prompt_with_chatgpt(prompt):
    """Uses ChatGPT to evaluate the quality of the prompt."""
    evaluation_prompt = (
        "Please evaluate the quality of the following prompt for learning about cat breeds, "
        "and provide feedback on how to improve it:\n\n"
        f"Prompt: {prompt}\n\n"
        "Your feedback should include: "
        "1. Whether the prompt is too broad, too short, or too specific. "
        "2. Suggestions for improving the prompt to get a better response."
    )

    # Call the OpenAI API to get feedback from ChatGPT
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose another model if needed
            prompt=evaluation_prompt,
            max_tokens=150,
            temperature=0.7,
        )
        # Extract and return the feedback from the response
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred while evaluating the prompt: {e}"


# Display feedback if prompt is provided
if st.button("Get Feedback"):
    if user_prompt.strip():
        feedback = evaluate_prompt_with_chatgpt(user_prompt)
        st.write("### ChatGPT's Feedback:")
        st.write(feedback)
    else:
        st.warning("Please enter a prompt.")
