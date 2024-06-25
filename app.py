import streamlit as st
from openai import OpenAI

key = st.secrets["OPENAI_API_KEY"]


client = OpenAI(api_key=key)

# Load product data from products.txt
def load_product_data():
    with open("products.txt", "r") as file:
        return file.read()

# Load product data
product_data = load_product_data()

# st.title("Tea Product Explorer")
hide_streamlit_style = """
            <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize chat history and check if it's the first run
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_prompt = (
        "You are performing an interview to find the best tea from the following list of products: \n"
        + product_data +
        "\nAlways ask more than one question, but never more than three. Always be very concise."
        "\nWhen you indentify which tea the user wants, please output the product descripton complete with the hyperlink and image. Never output a list of products, only one at a time."
        "\nIf you ask them if they want to buy and say yes, paste the link to the product as a hyperlink that says 'Buy Now' along with the requisite image. If they say no, suggest another similar product."
    )
    st.session_state.messages.append({"role": "system", "content": initial_prompt})
    initial_response = "**Hello, I'm Bloom!** I'm here to help you find the best tea from our selection.\n\nTo get started, could you tell me a bit about your taste preferences? Do you prefer green tea, black tea, herbal tea, or something else?"
    st.session_state.initialized = False
else:
    st.session_state.initialized = True

# Display chat messages from history on app rerun, skipping the system message
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = ":material/spa:" if message["role"] == "assistant" else ":material/mood:"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# If it's the first time around, display the initial assistant message only once
if not st.session_state.initialized:
    with st.chat_message("assistant", avatar=":material/spa:"):
        st.markdown(initial_response)
    st.session_state.messages.append({"role": "assistant", "content": initial_response})
    st.session_state.initialized = True

# Accept user input
if prompt := st.chat_input("Ask about our tea products!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=":material/mood:"):
        st.markdown(prompt)

    # Display thinking loader with spinner
    with st.chat_message("assistant", avatar=":material/spa:"):
        message_placeholder = st.empty()
        with st.spinner(''):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )

    assistant_message = response.choices[0].message.content

    # Update assistant response in chat message container
    message_placeholder.markdown(assistant_message)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
