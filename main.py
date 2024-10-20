import streamlit as st
import openai
from _secrets import api_key
# Set your OpenAI API key
openai.api_key = api_key

st.title("AI Prompt App")

# Input prompt from the user
user_prompt = st.text_area("Enter your prompt:")

# Button to generate a response
if st.button("Generate Response"):
    if user_prompt.strip():
        # Call the OpenAI API to get the response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Ensure the model is correct
                messages=[
                    {"role": "user", "content": user_prompt}
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
