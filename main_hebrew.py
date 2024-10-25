import streamlit as st
import openai
import re

# Set your OpenAI API key
openai.api_key = "Your_key"


st.title("אפליקציה ללימוד שימוש בבינה מלאכותית")


def create_image(prompt: str):
    fixed_prompt = prompt[::-1]
    print(f"{fixed_prompt = }")
    # Generate the image
    response = openai.Image.create(
        prompt=fixed_prompt,
        n=1,  # Number of images to generate
        size="1024x1024"  # Image size, can be 256x256, 512x512, or 1024x1024
    )

    # Get the URL of the generated image
    image_url = response['data'][0]['url']
    st.write("Generated Image URL:", image_url)


def test_if_prompt_good_enough(user_prompt, ai_response):
    if ai_response.endswith("Pass"):
        st.session_state.user_prompt = user_prompt
        return True
    else:
        return False


def evaluate_prompt_with_heuristics(prompt):
    """Evaluates the quality of the prompt."""
    if len(prompt.split(" ")) < 3:
        return "הפרומפט קצר מידי ודומה לחיפוש בגוגל"
    elif ("חתול" not in prompt) and ("גזעי" not in prompt):
        return "הפרומפט לא כולל פרטים רלוונטיים"
    elif len(prompt.split(" ")) > 300:
        return "הפרומפט ארוך מידי"
    else:
        return None


def get_cat_breeds_list(text: str):
    regex = r'(\[.*?\])'

    extraction_prompt = f"""
        היי :)
        בבקשה תוציא את רשימת גזעי החתולים מתוך הטקסט הבא:
        {text}\n\n


דוגמאות:
1.
אם המשפט הוא:        
        בעבר שרר בלבול באשר למוצאו של גזע זה, ובתחילה הוא נקרא בשם "כחול ארכנגלסק". רק בשנות ה-40 של המאה ה-20 קיבל הגזע את שמו הנוכחי. החתול הרוסי הכחול הפך להיות פופולרי בבריטניה, והחל מ-1912 התקבל גם כגזע מוכר לתערוכות. הרוסי הכחול היה ידוע גם בארצות הברית, והחל משנת 1900 הוא מופיע שם בתערוכות תחת השם "חתול מלטזי".

        
        
תוצאה טובה תהיה:
 ['חתול מלטזי', 'רוסי הכחול', 'כחול ארכנגלסק'']
  
  
2.
אם המשפט הוא:
בזמן מלחמת העולם השנייה נכחד הגזע בבריטניה כמעט לחלוטין, וכתוצאה מחוסר בחתולים טהורים מגזע זה השתמשו המגדלים לרבייה גם בחתולים בריטיים קצרי שיער כחולים, ובחתולים סיאמיים, בעלי מאפיינים דומים. 
תגובה טובה תהיה:
 ['בריטיים קצרי שיער כחולים', 'חתולים סיאמיים']

  
3.
אם המשפט הוא:
גזעי חתולים עם שיער קצר מגוונים ומרהיבים. כמה מהם כוללים:

    סיאמי - חתולים אלגנטיים וחסוניים עם צבע גוף בהיר ועיניים כחולות.
    בומביי - חתולים גדול


תגובה טובה תהיה:
 ['סיאמי', 'בומביי']

  
     
        """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure the model is correct
            messages=[
                {"role": "user", "content": extraction_prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        # Extract and display the AI's response
        ai_response = response['choices'][0]['message']['content'].strip()
        print(f"{ai_response = }")
        match = re.search(regex, ai_response)
        if match:
            cat_breeds_list = match.group(1)
            print(cat_breeds_list)
            return cat_breeds_list
    except Exception as e:
        st.error(f"Invalid request error: {e}")


def screen_1():
    user_prompt = st.text_area("המטרה שלך היא ללמוד על גזעי החתולים השונים, כתבו את הפרומפט שיוציא את המידע הזה")
    evaluation_prompt = f"""
    בבקשה תן הערכה של איכות הפרומפט של המשתמש, המטרה של הפרומפט של המשתמש היא להוציא מידע על גזעי חתולים שונים.
        
        
אם הפרומפט של המשתמש מספיק טוב, כתוב Pass בסוף התגובה שלך.
אבל תכתוב את זה רק אם הפרומפט טוב מספיק לדעתך, אחרת, אל תכתוב Pass
אם הבעיות בפרומפט של המשתמש הן קטנות, ובסופו של דבר הפרומפט מתמקד בחיפוש מידע על גזעי חתולים ומתאים לחיפוש באמצעות AI, אז כן תכתוב Pass בסוף התגובה שלך.

דוגמאות:
1.
אם הפרומפט של המשתמש הוא רק:
גזעי חתולים

תגובה טובה שלך תהיה:
הפרומפט דומה מידי לחיפוש בגוגל


2.
אם הפרומפט של המשתמש הוא:
ספר לי של מלחמצ העולם השנייה

תגובה טובה שלך תהיה:
הפרומפט לא ממוקד בחיפוש מידע על גזעי חתולים

3.
אם הפרומפט של המשתמש הוא:
שלום, בבקשה ספר לי על גזעי חתולים שונים, ספציפית אלו עם פרווה קצרה.

תגובה טובה שלך תהיה:
הפרומפו תקין,
Pass

        
        
הפרומפט של המשתמש:
        {user_prompt}\n\n

    """

    # Button to generate a response
    if st.button("בדיקת פרומפט"):
        response = evaluate_prompt_with_heuristics(user_prompt)

        # if heuristics cancelled it
        if response is not None:
            st.write("### תשובה היוריסטית:")
            st.write(response)

        # if the prompt passes heuristics
        else:
            # Call the OpenAI API to get the response
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Ensure the model is correct
                    messages=[
                        {"role": "user", "content": evaluation_prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.7,
                )
                # Extract and display the AI's response
                ai_response = response['choices'][0]['message']['content'].strip()
                st.write("### תשובת AI:")
                st.write(ai_response)
                prompt_is_good_enough = test_if_prompt_good_enough(user_prompt, ai_response)
                if prompt_is_good_enough:
                    st.session_state.screen_num = 2
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",  # Ensure the model is correct
                            messages=[
                                {"role": "user", "content": st.session_state.user_prompt}
                            ],
                            max_tokens=150,
                            temperature=0.7,
                        )
                        # Extract and display the AI's response
                        ai_response = response['choices'][0]['message']['content'].strip()
                        st.session_state.ai_response = ai_response
                    except Exception as e:
                        st.error(f"Invalid request error: {e}")

                    st.rerun()

            except Exception as e:
                st.error(f"Invalid request error: {e}")

            else:
                st.warning("Please enter a prompt.")


def screen_2():
    st.write("### תשובת AI:")
    print(f"{st.session_state.ai_response = }")
    st.write(st.session_state.ai_response)

    cat_breed_choices = get_cat_breeds_list(st.session_state.ai_response[::-1])
    print(f"{cat_breed_choices = }")
    cat_breed_choices_fixed = [breed[::-1] for breed in eval(cat_breed_choices)]
    option = st.selectbox(
        "נא לבחור גזע של חתולים",
        cat_breed_choices_fixed)

    if st.button("המשך"):
        print(f"{option = }")
        st.session_state.chosen_cat_breed = option
        st.session_state.screen_num = 3
        st.rerun()


def screen3():
    cat_breed = st.session_state.chosen_cat_breed
    suggested_prompt = f"  {cat_breed}בסגנון של וינסנט ואן גוך  "
    st.write(suggested_prompt)
    user_prompt = st.text_area("הכניסו את הפרומפט:")

    if st.button("יצירת תמונה"):
        create_image(user_prompt)


if __name__ == "__main__":

    if 'screen_num' not in st.session_state:
        st.session_state.screen_num = 1

    if st.session_state.screen_num == 1:
        screen_1()

    elif st.session_state.screen_num == 2:
        screen_2()

    elif st.session_state.screen_num == 3:
        screen3()

    else:
        raise ValueError("unknown screen number")


