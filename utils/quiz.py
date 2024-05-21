import dotenv
dotenv.load_dotenv()
import replicate

TEMPLATE = """
<|im_start|>system
You are a helpful assistant programmed to generate questions based on any prompt provided. For every chunk of text you receive, you're tasked with designing 5 distinct questions. Each of these questions will be accompanied by 3 possible answers: one correct answer and two incorrect ones. 

For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

Your output should be shaped as follows:

1. An outer list that contains 5 inner lists.
2. Each inner list represents a set of question and answers, and contains exactly 4 strings in this order:
- The generated question.
- The correct answer.
- The first incorrect answer.
- The second incorrect answer.

Your output should mirror this structure:
[
    ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
    ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
    ...
]

It is crucial that you adhere to this format as it's optimized for further Python processing.
<|im_end|>

<|im_start|>user
{prompt}<|im_end|>

<|im_start|>assistant
"""

def get_quiz_data(prompt):

    input = {
        "top_k": 50,
        "top_p": 0.9,
        "prompt": prompt,
        "temperature": 0.2,
        "max_new_tokens": 512,
        "min_new_tokens": 0,
        "stop_sequences": "<|im_end|>",
        "prompt_template": TEMPLATE,
        "presence_penalty": 1.15,
        "frequency_penalty": 0.2
        }

    response = []

    for event in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input=input
    ):
        response.append(str(event))

    return "".join(response)

if __name__ == "__main__":

    prompt = """
    The Mughal Empire, reigning from 1526 to 1857, was a dominant force in South Asian history. Founded by Babur, a Central Asian ruler of Turkic-Mongol descent, the empire thrived for over two centuries. 

    The Mughals were skilled administrators, establishing a centralized government with a vast network for tax collection, record keeping, and communication. This efficiency, coupled with their control of trade routes, led to immense wealth and prosperity.

    Several emperors played a key role in shaping the empire's legacy. Akbar, who ruled from 1556 to 1605, is considered the greatest Mughal emperor. He implemented tolerant religious policies, promoting harmony between the Muslim rulers and the Hindu majority. Akbar also streamlined administration, standardized weights and measures, and encouraged trade. 

    Shah Jahan, who ruled from 1628 to 1658, is known for his architectural marvels. The Taj Mahal, a stunning white marble mausoleum built in memory of his favorite wife Mumtaz Mahal, is a testament to his love and the Mughal artistic genius.

    The empire's decline began in the late 17th century under Aurangzeb, who focused on military expansion but alienated non-Muslims with stricter religious policies. This, combined with rising regional powers like the Marathas, weakened the Mughal hold. The empire eventually crumbled in the 19th century, succumbing to internal rebellions and British colonialism.

    Despite its eventual demise, the Mughal Empire left an enduring impact on India. They fostered a rich blend of cultures, evident in art, architecture, literature, and cuisine. The magnificent monuments they built continue to stand as a reminder of their power and artistry. 
    """

    response = get_quiz_data(prompt)

    print(type(response))

    print('-'*100)

    print(response)

