import streamlit as st

from utils.ocr import get_text_from_image

from utils.quiz import get_quiz_data
from utils.toast import get_random_toast

from utils.helpers import string_to_list
from utils.helpers import get_randomized_options

from utils.youtube import get_transcript_text
from utils.youtube import extract_video_id_from_url

st.set_page_config(
    page_title="StudyBuddy",
    page_icon="🧠",
    layout="centered",
)

# Check if user is new or returning using session state.
# If user is new, show the toast message.

if 'first_time' not in st.session_state:
    st.snow()
    message, icon = get_random_toast()
    st.toast(message, icon=icon)
    st.session_state.first_time = False

with st.sidebar:
    st.header("👨‍💻 About Me")
    st.write("""
    Hey, my name's **Soham** and I'm a tech enthusiast. Driven by passion and a love for sharing knowledge, I've created this platform to make learning more interactive and fun.

    Connect, contribute, or just say hi!
    """)

    st.divider()
    st.subheader("🔗 Connect with Me", anchor=False)
    st.markdown(
        """
        - [📧 E-Mail](mailto:dattasoham805@gmail.com)
        - [🐙 GitHub](https://github.com/tech-savvy-guy/StudyBuddy)
        - [🎥 YouTube](https://youtube.com/@tech_savvy_guy)
        - [👔 LinkedIn](https://www.linkedin.com/in/soham-datta-631809245/)
        """
    )

    st.divider()
    st.subheader("🏆 THE FUTURE OF AI IS OPEN", anchor=False)
    st.write("StudyBuddy proudly stands as my innovative entry for the SnowFlake + Streamlit Hackathon held in May 2024. A testament to the power of imagination and code!")

    st.divider()
    st.write("Made with 🩷 by Soham Datta.")

st.title(":red[StudyBuddy] — Watch. Learn. Quiz.", anchor=False)
st.write("""
Ever watched a YouTube video and wondered how well you understood its content? Here's a fun twist: Instead of just watching on YouTube, come to **StudyBuddy** and test your comprehension!

**How does it work?** 🤔\n\
    \n- Simply, paste in the YouTube video URL of your recently watched video.

⚠️ Important: The video **must** have English captions for the tool to work.

Once you've input the details, voilà! Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the video. Let's put your knowledge to the test! 
""")

with st.expander("💡 Video Tutorial"):
    with st.spinner("Loading video.."):
        st.video("https://youtu.be/yzBr3L2BIto", format="video/mp4", start_time=0)

with st.form("user_input"):
    YOUTUBE_URL = st.text_input("Enter the YouTube video link:", value="https://www.youtube.com/watch?v=fMsmCxIEQr4")
    submitted = st.form_submit_button("Craft my quiz!")

if submitted or ('quiz_data_list' in st.session_state):
    if not YOUTUBE_URL:
        st.info("Please provide a valid YouTube video link. Head over to [YouTube](https://www.youtube.com/) to fetch one.")
        st.stop()
        
    with st.spinner("Crafting your quiz...🤓"):
        if submitted:
            st.snow()
            video_id = extract_video_id_from_url(YOUTUBE_URL)
            video_transcription = get_transcript_text(video_id)
            quiz_data_str = get_quiz_data(video_transcription)
            st.session_state.quiz_data_list = string_to_list(quiz_data_str)

            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            for q in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        with st.form(key='quiz_form'):
            st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index  # Update the stored answer right after fetching it


            results_submitted = st.form_submit_button(label='Unveil My Score!')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

                if score == len(st.session_state.quiz_data_list):  # Check if all answers are correct
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    if incorrect_count == 1:
                        st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                    else:
                        st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Question: {q[0]}")
                            st.error(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")

st.title(":blue[Breaking the limits?]", anchor=False)
st.write("""
What if you could go beyond the quiz and explore the video content in more detail?👀 \n\
\nWant to chat with StudyBuddy using images?! 🔍 No problem! Just say the word! 🗣️\n\
\n**How does it work?** 🤔\n\
\n- Simply, upload an image of your choice.\n\
\n- StudyBuddy will analyze the image and provide you with a detailed description of its contents.\n\
\n- It's that simple! Let's dive in! 🚀        
         
⚠️ Important: The image **must** have a decent resolution for the tool to work best.         
""")

# Create a new form for image analysis
with st.form("image_input"):
    image = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    instructions = st.text_input("What would you like to do with the image?")
    image_submit = st.form_submit_button("Analyze my image!")

if image_submit:
    if image is None:
        st.info("Please provide a valid image file.")
        st.stop()

    with st.spinner("Analyzing your image...🔍"):
        st.snow()

        image_data = image.getvalue()
        

        st.image(image, caption="image.png", use_column_width=True)
        st.write(get_text_from_image(image_data))

