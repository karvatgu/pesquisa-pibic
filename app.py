import streamlit as st
import gspread

# Configuração da página e título do projeto
st.set_page_config(page_title="Pesquisa PIBIC - VOIDING AI LITE", layout="centered")
st.title("Pesquisa: VOIDING AI LITE")

# --- SEÇÃO 1: TCLE (Termo de Consentimento) ---
st.markdown("### TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO")
st.info("""
Você está sendo convidado(a) como voluntário(a) a participar do estudo VOIDING AI LITE - PADRÕES MICCIONAIS E ESTRESSE EM ESTUDANTES DE MEDICINA... 
O objetivo é avaliar a prevalência de distúrbios miccionais em estudantes de medicina.
""")

opcoes_tcle = [
    "Selecione uma opção...", 
    "Aceito e sou maior de 18 anos", 
    "Não aceito e/ou sou menor de 18 anos"
]
aceite_tcle = st.radio("Você concorda em participar desta pesquisa?", opcoes_tcle)

if aceite_tcle == "Não aceito e/ou sou menor de 18 anos":
    st.warning("Agradecemos o seu interesse! A pesquisa é encerrada aqui.")
    st.stop()

elif aceite_tcle == "Aceito e sou maior de 18 anos":
    st.success("Obrigado por aceitar! Por favor, preencha o questionário abaixo.")
    
    with st.form("questionario_pibic"):
        
        # --- 1. DADOS BÁSICOS ---
        st.header("1. Dados Básicos")
        doenca_previa = st.radio("Possui diagnóstico prévio de doença no trato urinário?", ["Não", "Sim"])
        idade = st.number_input("Idade", min_value=18, max_value=100, step=1, value=None, placeholder="Sua idade")
        sexo = st.selectbox("Sexo", ["Selecione", "Feminino", "Masculino"])
        
        # Peso em kg e Altura em cm
        peso = st.number_input("Peso aproximado (kg)", min_value=30.0, step=0.1, value=None, placeholder="Ex: 70.5")
        altura = st.number_input("Altura em centímetros (Ex: 175)", min_value=100, max_value=250, step=1, value=None, placeholder="Ex: 175")
        
        periodo = st.selectbox("Período da faculdade", [f"{i}º" for i in range(1, 13)])
        faculdade = st.text_input("Em qual faculdade você estuda?")
        estado = st.selectbox("Estado", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])

        st.divider()

        # --- 2. HÁBITOS DE VIDA (Água e Cafeína em ml) ---
        st.header("2. Hábitos de Vida")
        hidratacao = st.number_input("Água ingerida por dia (ml)", min_value=0, step=100, value=None, placeholder="Ex: 2000")
        cafeina = st.number_input("Cafeína por dia em ml (café, energéticos):", min_value=0, step=50, value=None, placeholder="Ex: 250")

        st.divider()

        # --- 3. QUESTIONÁRIO ICIQ-SF (Sintomas Urinários) ---
        st.header("3. Incontinência Urinária (ICIQ-SF)")
        iciq_3 = st.radio("Frequência que perde urina:", ["0 - Nunca", "1 - Uma vez por semana ou menos", "2 - 2-3 vezes por semana", "3 - Uma vez ao dia", "4 - Diversas vezes ao dia", "5 - O tempo todo"])
        iciq_4 = st.radio("Quantidade que perde:", ["0 - Nenhuma", "2 - Pequena", "4 - Moderada", "6 - Grande"])
        iciq_5 = st.slider("Interferência na vida diária (0-10):", 0, 10, 0)
        
        st.divider()

        # --- 4. QUESTIONÁRIO ICIQ-OAB (Bexiga Hiperativa) ---
        st.header("4. Bexiga Hiperativa (ICIQ-OAB)")
        oab_3a = st.radio("Frequência diurna:", ["0 - 1-6x", "1 - 7-8x", "2 - 9-10x", "3 - 11-12x", "4 - 13x+"])
        oab_4a = st.radio("Levanta à noite para urinar:", ["0 - Nenhuma", "1 - Uma", "2 - Duas", "3 - Três", "4 - Quatro ou mais"])

        st.divider()

        # --- 5. QUESTIONÁRIO PSS-10 (Estresse) ---
        st.header("5. Percepção de Estresse (PSS-10)")
        opcoes_pss = ["0 - Nunca", "1 - Quase nunca", "2 - Às vezes", "3 - Frequentemente", "4 - Muito frequentemente"]
        pss_1 = st.selectbox("Sentiu-se chateado por algo inesperado?", opcoes_pss)
        pss_2 = st.selectbox("Sentiu-se incapaz de controlar coisas importantes?", opcoes_pss)

        st.divider()

        # --- 6. QUESTIONÁRIO PSQI-BR (Sono) ---
        st.header("6. Qualidade do Sono (PSQI-BR)")
        psqi_1 = st.time_input("Hora usual de deitar:")
        psqi_2 = st.number_input("Minutos para dormir:", min_value=0, value=None, placeholder="Ex: 30")
        psqi_4 = st.number_input("Horas de sono real por noite:", min_value=0.0, step=0.5, value=None, placeholder="Ex: 7.0")

        submit_button = st.form_submit_button(label="Finalizar e Enviar Respostas")

        if submit_button:
            with st.spinner("Conectando ao banco de dados e salvando..."):
                try:
                    # --- LÓGICA DE CONEXÃO SEGURA ---
                    # Pegamos os dados do painel Secrets do Streamlit
                    creds_dict = dict(st.secrets["gcp_service_account"])
                    
                    # CORRETOR AUTOMÁTICO DE CHAVE (Resolve o erro Invalid Private Key)
                    if "\n" not in creds_dict["private_key"]:
                        # Se a chave veio sem os \n (quebras de linha), nós os recolocamos
                        pk = creds_dict["private_key"]
                        pk = pk.replace("-----BEGIN PRIVATE KEY-----", "-----BEGIN PRIVATE KEY-----\n")
                        pk = pk.replace("-----END PRIVATE KEY-----", "\n-----END PRIVATE KEY-----")
                        # O segredo é que o miolo da chave não pode ter espaços, deve ter quebras de linha
                        creds_dict["private_key"] = pk

                    # Conexão com o Google Sheets
                    cliente = gspread.service_account_from_dict(creds_dict)
                    link_planilha = "https://docs.google.com/spreadsheets/d/1FoXC3MIutbs0Ri4MxVKLf0E7fo91ODgTVx6au_P6NYU/edit?usp=sharing"
                    planilha = cliente.open_by_url(link_planilha)
                    aba = planilha.sheet1
                    
                    # Preparação da linha de dados
                    nova_linha = [
                        str(doenca_previa), str(idade), sexo, str(peso), str(altura), 
                        periodo, faculdade, estado, str(hidratacao), str(cafeina), 
                        iciq_3, iciq_4, str(iciq_5), oab_3a, oab_4a, 
                        pss_1, pss_2, str(psqi_1), str(psqi_2), str(psqi_4)
                    ]
                    
                    aba.append_row(nova_linha)
                    st.success("Tudo certo! Suas respostas foram enviadas com sucesso.")
                
                except Exception as e:
                    st.error(f"Erro ao salvar na planilha: {e}")
