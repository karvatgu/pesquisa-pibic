import streamlit as st
import gspread

# Configuração da página
st.set_page_config(page_title="Pesquisa PIBIC - VOIDING AI LITE", layout="centered")
st.title("Pesquisa: VOIDING AI LITE")

# --- SEÇÃO 1: TCLE ---
st.markdown("### TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO")
st.info("Você está sendo convidado(a) como voluntário(a) a participar do estudo VOIDING AI LITE...")

opcoes_tcle = ["Selecione...", "Aceito e sou maior de 18 anos", "Não aceito"]
aceite_tcle = st.radio("Você concorda em participar?", opcoes_tcle)

if aceite_tcle == "Não aceito":
    st.warning("Pesquisa encerrada.")
    st.stop()

elif aceite_tcle == "Aceito e sou maior de 18 anos":
    with st.form("questionario_pibic"):
        # 1. DADOS BÁSICOS
        st.header("1. Dados Básicos")
        doenca = st.radio("Diagnóstico prévio de doença urinária?", ["Não", "Sim"])
        idade = st.number_input("Idade", min_value=18, max_value=100, step=1, value=None)
        sexo = st.selectbox("Sexo", ["Selecione", "Feminino", "Masculino"])
        peso = st.number_input("Peso (kg)", min_value=30.0, step=0.1, value=None)
        altura = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1, value=None)
        periodo = st.selectbox("Período", [f"{i}º" for i in range(1, 13)])
        faculdade = st.text_input("Faculdade")
        estado = st.selectbox("Estado", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])

        # 2. HÁBITOS
        st.header("2. Hábitos de Vida")
        agua = st.number_input("Água por dia (ml)", min_value=0, step=100, value=None)
        cafeina = st.number_input("Cafeína por dia (ml)", min_value=0, step=50, value=None)

        # 3. ICIQ-SF
        st.header("3. Incontinência Urinária (ICIQ-SF)")
        iciq_3 = st.radio("Frequência da perda:", ["0 - Nunca", "1 - < 1x semana", "2 - 2-3x semana", "3 - 1x dia", "4 - Várias x dia", "5 - O tempo todo"])
        iciq_4 = st.radio("Quantidade da perda:", ["0 - Nenhuma", "2 - Pequena", "4 - Moderada", "6 - Grande"])
        iciq_5 = st.slider("Interferência (0-10):", 0, 10, 0)

        # 4. ICIQ-OAB
        st.header("4. Bexiga Hiperativa (ICIQ-OAB)")
        oab_3a = st.radio("Frequência diurna:", ["0 - 1-6x", "1 - 7-8x", "2 - 9-10x", "3 - 11-12x", "4 - 13x+"])
        oab_4a = st.radio("Levanta à noite:", ["0 - Nenhuma", "1 - Uma", "2 - Duas", "3 - Três", "4 - Quatro ou mais"])

        # 5. PSS-10
        st.header("5. Estresse (PSS-10)")
        opcoes_pss = ["0 - Nunca", "1 - Quase nunca", "2 - Às vezes", "3 - Frequentemente", "4 - Muito"]
        pss_1 = st.selectbox("Sentiu-se chateado inesperadamente?", opcoes_pss)
        pss_2 = st.selectbox("Incapaz de controlar coisas importantes?", opcoes_pss)

        # 6. PSQI-BR
        st.header("6. Qualidade do Sono (PSQI-BR)")
        psqi_1 = st.time_input("Hora de deitar:")
        psqi_2 = st.number_input("Minutos para dormir:", min_value=0, value=None)
        psqi_4 = st.number_input("Horas de sono real:", min_value=0.0, step=0.5, value=None)

        submit = st.form_submit_button("Finalizar e Enviar")

        if submit:
            try:
                # TRATAMENTO DA CHAVE PRIVADA
                creds = dict(st.secrets["gcp_service_account"])
                # Remove aspas extras e garante que as quebras de linha (\n) existam
                creds["private_key"] = creds["private_key"].replace("\\n", "\n")
                
                cliente = gspread.service_account_from_dict(creds)
                planilha = cliente.open_by_url("https://docs.google.com/spreadsheets/d/1FoXC3MIutbs0Ri4MxVKLf0E7fo91ODgTVx6au_P6NYU/edit?usp=sharing")
                aba = planilha.sheet1
                
                linha = [str(doenca), str(idade), sexo, str(peso), str(altura), periodo, faculdade, estado, str(agua), str(cafeina), iciq_3, iciq_4, str(iciq_5), oab_3a, oab_4a, pss_1, pss_2, str(psqi_1), str(psqi_2), str(psqi_4)]
                aba.append_row(linha)
                st.success("Dados salvos com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
