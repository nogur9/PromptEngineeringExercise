import streamlit as st
import openai
# Set your OpenAI API key
openai.api_key = "your_key"


def evaluate_prompt_with_heuristics(prompt):
    """Evaluates the quality of the prompt."""
    if len(prompt.split(" ")) < 3:
        return "The prompt is too short and written like a Google search. Try to rewrite it with more details or a specific question."
    elif "cat breeds" not in prompt.lower():
        return "The prompt could be more specific. Try asking for differences between specific breeds or details about their characteristics."
    elif len(prompt.split(" ")) > 300:
        return "prompt too long"
    else:
        return None





st.title("AI Prompt App")

# Input prompt from the user
user_prompt = st.text_area("Enter your prompt:")
evaluation_prompt = f"""
    Please evaluate the quality of the following prompt for learning about cat breeds, 
    and provide feedback on how to improve it:\n\n"
    Prompt: {user_prompt}\n\n
    Your feedback should include: 
    1. Whether the prompt is too broad, too short, or too specific. 
    2. Suggestions for improving the prompt to get a better response.
    """
# Button to generate a response
if st.button("Generate Response"):
    if user_prompt.strip():
        response = evaluate_prompt_with_heuristics(user_prompt)
        if response is not None:
            st.write("### heuristic Response:")
            st.write(response)
        else:
            # Call the OpenAI API to get the response
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Ensure the model is correct
                    messages=[
                        {"role": "user", "content": evaluation_prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7,
                )
                # Extract and display the AI's response
                ai_response = response['choices'][0]['message']['content'].strip()
                st.write("### AI Response:")
                st.write(ai_response)
            except openai.error.InvalidRequestError as e:
                st.error(f"Invalid request error: {e}")
            except openai.error.AuthenticationError as e:
                st.error(f"Authentication error: {e}")
            except openai.error.APIError as e:
                st.error(f"API error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
            else:
                st.warning("Please enter a prompt.")
