import streamlit as st
from openai import OpenAI
import os

# Configuração da chave da API
default_api_key =st.secrets["CHATGPT"]  # A chave da API deve estar na variável de ambiente OPENAI_API_KEY

# Títulos e descrição
st.title("💭 Descubra o significado do seu sonho")
st.write(
    "Traição, perseguição, morte, casamento, gravidez, caindo, bicho... Sonhos podem ter significados profundos. "
    "Descreva seu sonho para descobrir o que ele pode revelar!"
)


client = OpenAI(api_key=default_api_key)

# Inicializar mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada para o sonho
if sonho := st.chat_input("Descreva o seu sonho aqui..."):
    # Adicionar o sonho ao histórico
    st.session_state.messages.append({"role": "user", "content": sonho})
    with st.chat_message("user"):
        st.markdown(sonho)

    # Criar o prompt para a API
    prompt = """
    Você é um especialista em interpretação de sonhos. Receberá um texto descrevendo um sonho e deverá identificar os temas principais relacionados, como gravidez, traição, perseguição, morte, ou outros temas relevantes.
    Analise o sonho detalhadamente.
    Identifique os temas centrais do sonho.
    Explique brevemente por que esses temas são relevantes com base na descrição fornecida.

    """

    try:
        # Chamar a API da OpenAI
        # Usa a chave da API inserida ou a padrão
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ou "gpt-4" dependendo da sua chave de API
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": sonho},
            ],
            temperature=0.7,  # Ajuste a criatividade
        )

        # Processar a resposta
        resposta = response.choices[0].message.content  # Correção na extração da resposta

        # Adicionar a resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.markdown(resposta)

    except Exception as e:
        st.error(f"Erro ao se conectar à API: {e}")