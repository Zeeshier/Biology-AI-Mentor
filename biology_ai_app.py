from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage

# Set up Streamlit page configuration with a blue theme
st.set_page_config(page_title="Biology AI App", page_icon="🔬", layout="wide")

# Sidebar configuration for a modern look
st.sidebar.header("Biology AI App 🌱")
st.sidebar.write("### Your Biology Guide")
st.sidebar.info("Ask any questions related to biology topics, such as cells, genetics, ecology, and human biology.")

# Initialize session state variables
if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI-generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ""  # Store the Google API key

# Define function to submit user input
def submit():
    st.session_state.entered_prompt = st.session_state.prompt_input
    st.session_state.prompt_input = ""

# Function to initialize the chat model
def init_chat_model():
    if st.session_state['api_key']:
        return ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.5,
            api_key=st.session_state['api_key']
        )
    return None

def build_message_list():
    # Include introductory message for the AI only for the first interaction
    zipped_messages = []
    if len(st.session_state['past']) == 0:
        initial_message = (
            "Your name is Biology Mentor, an AI Technical Expert. "
            "You are here to guide and assist students with biology-related questions. "
            "Please provide accurate and helpful information in a polite and professional tone. "
            "Your responses should be brief, around 100 words or fewer. "
            "If a query falls outside biology, kindly inform the user that the topic is out of scope."
        )
        zipped_messages.append(HumanMessage(content=initial_message))

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(content=human_msg))
        if ai_msg is not None:
            zipped_messages.append(AIMessage(content=ai_msg))

    return zipped_messages

def generate_response(user_query):
    # Ensure the query is relevant to biology before sending it to the AI model
    biology_keywords = [
        "biology", "cell", "organism", "ecosystem", "biosphere", "species", "population", 
        "community", "habitat", "niche", "cell membrane", "nucleus", "cytoplasm", 
        "mitochondria", "ribosome", "endoplasmic reticulum", "golgi apparatus", 
        "chloroplast", "cell wall", "plasma membrane", "dna", "rna", "gene", 
        "chromosome", "allele", "genotype", "phenotype", "homozygous", "heterozygous", 
        "mutation", "natural selection", "adaptation", "speciation", "phylogenetics", 
        "extinction", "evolution", "common ancestor", "fossil record", "artificial selection", 
        "biomass", "trophic levels", "food chain", "food web", "biogeochemical cycle", 
        "symbiosis", "mutualism", "commensalism", "parasitism", "carrying capacity", 
        "homeostasis", "metabolism", "photosynthesis", "cellular respiration", "hormones", 
        "neurons", "immune system", "endocrine system", "cardiovascular system", 
        "digestive system", "bacteria", "virus", "fungi", "protozoa", "microbiome", 
        "antibiotics", "pathogen", "infection", "immunology", "vaccination", 
        "protein", "enzyme", "amino acid, mitosis, meiosis, genetics, heredity, inheritance"
    ]

    if any(keyword in user_query.lower() for keyword in biology_keywords):
        # Build the list of messages
        zipped_messages = build_message_list()
        # Generate response using the chat model
        chat = init_chat_model()
        if chat is not None:
            try:
                ai_response = chat(zipped_messages)
                response = ai_response.content
                return response
            except Exception as e:
                return f"An error occurred while generating the response: {str(e)}"
        else:
            return "Please enter a valid API key."
    else:
        return "I'm sorry, but that topic is outside of my expertise in biology. Please ask a biology-related question!"

# Main container for chat messages
st.markdown("<h2 style='color: #007acc; text-align: center;'>Biology AI App 💬</h2>", unsafe_allow_html=True)

# Input container for API key and chat messages
with st.container():
    # Input field for the API key
    api_key_input = st.text_input("Enter your Google Gemini API Key:", key='api_key', type='password', placeholder="Your API Key...")
    st.write("")  # Add some space
    user_input = st.text_input("YOU: ", key='prompt_input', on_change=submit, placeholder="Type your biology question here... 🧬", label_visibility="collapsed")
    st.write("")  # Add some space

if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt
    st.session_state.past.append(user_query)  # Append to past queries

    # Generate response
    output = generate_response(user_query)
    st.session_state.generated.append(output)  # Append AI response

# Display chat history
if st.session_state['generated']:
    with st.container():
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            # Display AI response
            message(st.session_state["generated"][i], key=str(i))
            # Display user message
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
