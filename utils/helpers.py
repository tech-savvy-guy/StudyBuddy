import random
import ast

import streamlit as st

def string_to_list(s):
    try:
        return ast.literal_eval(s.strip())
    except (SyntaxError, ValueError) as e:
        st.error(f"Error: The provided input is not correctly formatted. {e}")
        st.stop()

def get_randomized_options(options):
    correct_answer = options[0]
    random.shuffle(options)
    return options, correct_answer

if __name__ == "__main__":

    text = """
        [
            ["Who was the founder of the Mughal Empire?", "Babur", "Akbar", "Shah Jahan"],
            ["When did the Mughal Empire reign?", "1526 to 1857", "1400 to 1600", "1600 to 1900"],
            ["What were some key factors in the Mughal Empire's prosperity?", "Efficient administration, control of trade routes, and skilled rulers", "Large military forces, abundant natural resources, and favorable climate", "Religious tolerance, architectural achievements, and cultural blending"],
            ["Which Mughal emperor is known for his religious tolerance?", "Akbar", "Shah Jahan", "Aurangzeb"],
            ["Which Mughal emperor built the Taj Mahal?", "Shah Jahan", "Akbar", "Babur"]
        ]
    """

    questions = string_to_list(text)
    print(questions)