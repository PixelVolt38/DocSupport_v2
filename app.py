#streamlit run 
import streamlit as st
from conversacion import *

#crear_conversacion()
st.cache_data.clear()
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
# st.sidebar.markdown("---")

# input_language = st.sidebar.selectbox("idioma",
#                     ['Español', 'English'],
#                     on_change=updatemol,
#                     #help="""Choose the input info of your molecule. If the app is slow, use SMILES input.""" + smiles_help
#                     )

#if input_language:
#    cambiar_idioma(input_language)
#    #st.session_state.clear()
#    print(input_language)

#st.image("interfaz/imgs/inetum_logo.jpg")
# Streamed response emulator
def response_generator():
    if not prompt:
        response = "¡Hola! Soy DataQuality Support, un chatbot que busca ayudar a solucionar cualquier duda que tengas acerca de la plataforma DataQuality Platform. Hazme cualquier pregunta que tengas."
        image_paths = []
    else:
        response = ask(prompt)
        #response="Hola, a ver si te funciona la imagen"
        # Get context images based on user query
        matching_results_image_fromdescription_data, _ = context_image(prompt)
    
        # Extract only the image paths from the first three results
        image_paths = [
        matching_results_image_fromdescription_data[i]["img_path"]
        for i in range(min(3, len(matching_results_image_fromdescription_data)))
        ]
    return [response, image_paths]
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
    with st.chat_message(role):
        st.write(message["content"][0])
        with st.expander("Estas imágenes pueden resultarte útiles"):
            for im in message["content"][1]:
                st.image(im, width=400)
    

# Accept user input
if prompt := st.chat_input(""):
    # Display user message in chat message container
    with st.chat_message("user"):   
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": [prompt,()]})


# Display assistant response in chat message container
with st.chat_message("assistant",):
    #response = st.write_stream(response_generator())
    response, image_paths = response_generator()
    st.write(response)
    with st.expander("Estas imágenes pueden resultarte útiles"):
        for img in image_paths:
            st.image(img, width=800)
    
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": [response,image_paths] })