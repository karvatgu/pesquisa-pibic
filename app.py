import streamlit as st
import gspread

# Configuração inicial
st.set_page_config(page_title="Pesquisa PIBIC - VOIDING AI LITE", layout="centered")
st.title("Pesquisa: VOIDING AI LITE")

# --- SEÇÃO 1: TCLE ---
st.markdown("### TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO")
st.info("""
Você está sendo convidado(a) como voluntário(a) a participar do estudo VOIDING AI LITE. 
O objetivo é avaliar padrões miccionais e estresse em estudantes de medicina.
A sua participação consiste em responder questionários sobre saúde urinária, sono e estresse.
Os dados são confidenciais e sua participação é voluntária.
""")

opcoes_tcle = ["Selecione...", "Aceito", "Não aceito"]
aceite_tcle = st.radio("Você concorda em participar?", opcoes_tcle)

if aceite_tcle == "Não aceito":
    st.warning("Pesquisa encerrada.")
    st.stop()

elif aceite_tcle == "Aceito":
    with st.form("questionario_pibic"):
        # Dados Básicos
        st.header("1. Dados Básicos")
        idade = st.number_input("Idade", min_value=18, max_value=100, step=1)
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"])
        peso = st.number_input("Peso (kg)", min_value=30.0, step=0.1)
        altura = st.number_input("Altura (cm)", min_value=100, step=1)
        periodo = st.selectbox("Período", [f"{i}º" for i in range(1, 13)])
        faculdade = st.text_input("Faculdade")
        
        # Hidratação
        st.header("2. Hábitos")
        agua = st.number_input("Água por dia (ml)", min_value=0, step=100)
        
        # ICIQ-SF (Exemplo simplificado para teste)
        st.header("3. Sintomas")
        iciq_frequencia = st.selectbox("Frequência de perda urinária", ["Nunca", "Uma vez por semana", "Diário"])

        submit_button = st.form_submit_button(label="Enviar Respostas")

        if submit_button:
            with st.spinner("Enviando..."):
                try:
                    # AQUI ESTÁ A MUDANÇA MÁGICA:
                    # Ele vai ler a chave que você colou no painel "Secrets" do Streamlit
                    cliente = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
                    
                    link_planilha = "https://docs.google.com/spreadsheets/d/1FoXC3MIutbs0Ri4MxVKLf0E7fo91ODgTVx6au_P6NYU/edit?usp=sharing"
                    planilha = cliente.open_by_url(link_planilha)
                    aba = planilha.sheet1
                    
                    dados = [str(idade), sexo, str(peso), str(altura), periodo, faculdade, str(agua), iciq_frequencia]
                    aba.append_row(dados)
                    
                    st.success("Enviado com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {e}")
