'''
Código creado por Jonathan Vásquez para EvoAcademy.

¿Dudas del proceso de fine-tuning? 
Revisa este tutorial: 

¿Quieres saber más sobre Inteligencia Artificial y Tecnología
Síguenos en nuestras redes:
- TikTok: https://www.tiktok.com/@evoacdm
- Instagram: https://www.instagram.com/evoacdm/
- LinkedIn: https://www.linkedin.com/company/evoacmd/

Y visita https://www.evoacademy.cl/

'''
import openai
import streamlit as st
from streamlit import runtime
runtime.exists()

avatar = {
    'user': 'lorelei',
    'assistant': 'pixel-art'
}


st.title("Chat con Burro de Shrek 💬🫏")

with st.sidebar:
    st.title('Configuraciones')
    st.sidebar.info('por EvoAcademy: https://www.evoacademy.cl/', icon='ℹ️')
    # if ('APIKEY' in st.secrets) and ('IDMODEL' in st.secrets):
    #     st.success('Credenciales secretas cargadas!', icon='✅')
    #     api_key = st.secrets['APIKEY']
    #     id_model = st.secrets['IDMODEL']
    
    # else:
    placeholder = st.empty()
    api_key = st.text_input('API Key:', placeholder='Aquí tu API Key de OpenAI', type='password')
    id_model = st.text_input('Id Modelo:', placeholder='Id de tu modelo de fine-tuning', type='password')
    with placeholder.container():
        if not (api_key and id_model):
            st.warning('Por favor, ingresa tus credenciales!', icon='⚠️')
        else:
            st.success('Procede a ingresar los mensajes!', icon='👉')
            
    system_message = st.text_area(label='Mensaje de sistema:',
                                height=180,
                                placeholder='Instrucciones que complementan el comportamiento de tu modelo de fine-tuning. Ej: Responde siempre alegre.')
    memory = st.slider(label='Memoria conversación (num. mensajes):',value=4,min_value=1)
    openai.api_key = api_key


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_message},
        ]

for message in st.session_state.messages:
    if message['role']=='system': continue
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = st.session_state.messages = [
        {"role": "system", "content": system_message},
        ]
st.sidebar.button('Limpiar chat', on_click=clear_chat_history)

def generate_response(model):
    history = [st.session_state.messages[0]]+st.session_state.messages[-memory:] if len(st.session_state.messages)>5 else st.session_state.messages
    response = openai.chat.completions.create(
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