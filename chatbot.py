import openai
import streamlit as st
from streamlit_chat import message

# openai_api_key = open('key.txt').read()
# openai.api_key = openai_api_key

avatar = {
    'user': 'lorelei',
    'assistant': 'pixel-art'
}

st.title("Chatea con Burro de Shrek :tada:")

with st.sidebar:
    st.title('🤗💬🫏 BurroChat')
    # if ('APIKEY' in st.secrets) and ('IDMODEL' in st.secrets):
    #     st.success('HuggingFace Login credentials already provided!', icon='✅')
    #     api_key = st.secrets['APIKEY']
    #     id_model = st.secrets['IDMODEL']
    #     openai.api_key = api_key
    # else:
    api_key = st.text_input('Ingresar API Key:', type='password')
    id_model = st.text_input('Ingresar Id Modelo:', type='password')
    if not (api_key and id_model):
        st.warning('Por favor, ingresa tus credenciales!', icon='⚠️')
    else:
        st.success('Procede a ingresar los mensajes!', icon='👉')


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres un Burro muy parlanchín y muy ingenioso en tus respuestas. \
Si deseas mostrar alguna acción. Debes usar corchetes []. Por ejemplo:\
Hola, como estás? [extiendo la mano]."},
        ]

for message in st.session_state.messages:
    if message['role']=='system': continue
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = st.session_state.messages = [
        {"role": "system", "content": "Eres un Burro muy parlanchín y muy ingenioso en tus respuestas. \
Si deseas mostrar alguna acción. Debes usar corchetes []. Por ejemplo:\
Hola, como estás? [extiendo la mano]."},
        ]
st.sidebar.button('Limpiar Historial del Chat', on_click=clear_chat_history)

def generate_response(model):
    history = [st.session_state.messages[0]]+st.session_state.messages[-4:] if len(st.session_state.messages)>5 else st.session_state.messages
    response = openai.ChatCompletion.create(
                        model=model,
                        messages=history,
                        temperature = .5,
                        max_tokens=400
                        )
    msg = response.choices[0].message.content
    return msg

if prompt := st.chat_input(disabled=not (api_key and id_model), placeholder='Tú mensaje...'):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generate_response(id_model) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)