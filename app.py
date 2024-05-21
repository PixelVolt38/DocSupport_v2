#streamlit run 
import streamlit as st
from conversacion import *

#crear_conversacion()
st.cache_data.clear()
user_avatar = "😀"
assistant_avatar = "interfaz/imgs/Galleta.jpg"
#imgs/Galleta.jpg  🤖

st.set_page_config(
    page_title="DocSupport ",
    page_icon="interfaz/imgs/inetum_logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://www.inetum.com/es",
        "Report a bug": "https://www.inetum.com/es",
        "About": """
            ## DocSupport
            
            Es un chatbot de apoyo al cliente donde el usuario 
            puede hacer preguntas y resolver dudas de distintos dominios 
            y niveles de complejidad sobre la plataforma de DataQuality, 
            además de preguntas acerca sobre diversas áreas de Data, 
            como Gobierno del Dato o Calidad del Dato. 
        """
    }
)
# st.sidebar.markdown(
#         f'<img src="interfaz\imgs\inetum_logo.jpg" />',
#         unsafe_allow_html=True,
# )

def updatemol():
    """Allow to upload molecule"""
    st.session_state['update_mol'] = True
    return

st.sidebar.image("interfaz/imgs/inetum_logo.jpg", width=200)
st.sidebar.image("interfaz/imgs/LogoCeep.png", width=200)
st.sidebar.markdown("---")

input_language = st.sidebar.selectbox("idioma",
                    ['Español', 'English'],
                    on_change=updatemol,
                    #help="""Choose the input info of your molecule. If the app is slow, use SMILES input.""" + smiles_help
                    )

#if input_language:
#    cambiar_idioma(input_language)
#    #st.session_state.clear()
#    print(input_language)

#st.image("interfaz/imgs/inetum_logo.jpg")
# Streamed response emulator
def response_generator():
    if not prompt:
        response = "¡Hola! Soy DocSupport, un chatbot que busca ayudar a solucionar cualquier duda que tengas acerca de la plataforma DataQuality Platform y el propio DocSupport. Hazme cualquier pregunta que tengas."
    else:
        response = ask(prompt)
    return response
    # for word in response.split(): 
    #     yield word + " "
    #     time.sleep(0.05)



st.title("DocSupport")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    role = message["role"]
    # Set avatar based on role
    if role == "assistant":
        avatar_image = assistant_avatar
    elif role == "user":
        avatar_image = user_avatar
    else:
        avatar_image = None
    with st.chat_message(role, avatar=avatar_image):
        st.write(message["content"])
    

# Accept user input
if prompt := st.chat_input(""):
    # Display user message in chat message container
    with st.chat_message("user", avatar = user_avatar):   
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


# Display assistant response in chat message container
with st.chat_message("assistant", avatar = assistant_avatar):
    #response = st.write_stream(response_generator())
    response = response_generator()
    st.write(response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})


