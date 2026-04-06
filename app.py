import streamlit as st
import gspread

# Configurações do App
st.set_page_config(page_title="Pesquisa PIBIC - VOIDING AI LITE", layout="centered")
st.title("Pesquisa: VOIDING AI LITE")

# --- SEÇÃO 1: TCLE ---
st.markdown("### TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO")
st.info("Estudo sobre padrões miccionais e estresse em estudantes de medicina.")

opcoes_tcle = ["Selecione...", "Aceito e sou maior de 18 anos", "Não aceito"]
aceite_tcle = st.radio("Você concorda em participar?", opcoes_tcle)

if aceite_tcle == "Não aceito":
    st.warning("Pesquisa encerrada.")
    st.stop()

elif aceite_tcle == "Aceito e sou maior de 18 anos":
    with st.form("questionario_pibic"):
        # Dados simplificados para testar a conexão primeiro
        st.header("1. Dados de Identificação")
        idade = st.number_input("Idade", min_value=18, max_value=100, step=1, value=None)
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"])
        faculdade = st.text_input("Faculdade")
        
        # Sintomas Urinários (ICIQ-SF)
        st.header("2. Sintomas Urinários")
        iciq_3 = st.radio("Frequência da perda:", ["Nunca", "1x semana", "2-3x semana", "Diário", "Sempre"])
        
        submit = st.form_submit_button("Finalizar e Enviar")

        if submit:
            try:
                # --- SISTEMA DE CONEXÃO BLINDADO ---
                s = st.secrets["gcp_service_account"]
                
                # Criamos o dicionário de credenciais exatamente como o Google quer
                creds_dict = {
                    "type": s["type"],
                    "project_id": s["project_id"],
                    "private_key_id": s["private_key_id"],
                    "private_key": s["private_key"].replace("\\n", "\n"), # CORREÇÃO CRÍTICA
                    "client_email": s["client_email"],
                    "client_id": s["client_id"],
                    "auth_uri": s["auth_uri"],
                    "token_uri": s["token_uri"],
                    "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": s["client_x509_cert_url"]
                }
                
                cliente = gspread.service_account_from_dict(creds_dict)
                planilha = cliente.open_by_url("https://docs.google.com/spreadsheets/d/1FoXC3MIutbs0Ri4MxVKLf0E7fo91ODgTVx6au_P6NYU/edit?usp=sharing")
                aba = planilha.sheet1
                
                aba.append_row([str(idade), sexo, faculdade, iciq_3])
                st.success("Dados salvos com sucesso!")
            except Exception as e:
                st.error(f"Erro técnico: {e}")
