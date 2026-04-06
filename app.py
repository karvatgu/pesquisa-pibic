import streamlit as st
import gspread
import json

# Configuração inicial
st.set_page_config(page_title="Pesquisa PIBIC - VOIDING AI LITE", layout="centered")
st.title("Pesquisa: VOIDING AI LITE")

# --- SEÇÃO 1: TCLE ---
st.markdown("### TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO")
st.info("""
Você está sendo convidado(a) como voluntário(a) a participar do estudo VOIDING AI LITE - PADRÕES MICCIONAIS E ESTRESSE EM ESTUDANTES DE MEDICINA - UM ESTUDO TRANSVERSAL E REVISÃO DE LITERATURA, que tem como objetivo avaliar a prevalência e distúrbios miccionais em estudantes de medicina através do desenvolvimento de um aplicativo. Acreditamos que esta pesquisa seja importante porque é um assunto pouco explorado nessa população, além de ter evidências de alta prevalência na literatura, podendo ajudar na triagem e ampliamento do conhecimento urológico dos estudantes.

PARTICIPAÇÃO NO ESTUDO
A sua participação no referido estudo será de responder aos questionários propostos pelo estudo, dentre eles: ICIQ-SF (sobre sintomas de incontinência urinária), ICIQ-OAB (sobre sintomas de bexiga hiperativa), PSQI-BR (sobre qualidade do sono), PSS-10 (para quantificação de estresse) e perguntas direcionadas à ingestão de cafeína e água. O tempo total para resposta das perguntas girará em torno de 15-20 minutos, com direito à recusa ou abandono do questionário quando for conveniente ao participante. Os questionários serão disponibilizados de forma online por meio de um aplicativo desenvolvido pelos pesquisadores.

RISCOS E BENEFÍCIOS
O participante receberá um relatório individual de risco de disfunção miccional gerado pelo modelo de inteligência artificial no final do estudo. Este feedback imediato pode alertá-lo sobre a possível necessidade de acompanhamento médico antes do surgimento de sintomas. O feedback é apenas um modelo experimental e não um diagnóstico médico validado. Riscos potenciais incluem desconfortos psicossociais e violação de confidencialidade. Para minimizar tais riscos, os dados serão pseudoanonimizados, sem a identificação do nome do paciente. Caso alguma adversidade venha a acontecer, será realizado o encaminhamento a um profissional de saúde mental do serviço de psicologia da PUCPR.

SIGILO E PRIVACIDADE
Garantiremos a você que sua privacidade será respeitada. Nós pesquisadores nos responsabilizaremos pela guarda e confidencialidade dos dados.

AUTONOMIA E RESSARCIMENTO
Você pode se recusar a participar do estudo, ou retirar seu consentimento a qualquer momento. Na ocorrência de algum dano decorrente de sua participação no estudo, você será devidamente indenizado.

CONTATO
Pesquisador: Rogério de Fraga da PUCPR | Tel: +55(41)99127-2194
Comitê de Ética em Pesquisa da PUCPR (CEP) | Tel: (41) 3271-2103 | E-mail: nep@pucpr.br

DECLARAÇÃO
Declaro que li e entendi todas as informações presentes neste Termo de Consentimento Livre e Esclarecido.
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
    st.success("Obrigado por aceitar participar! Por favor, preencha o questionário.")
    
    with st.form("questionario_pibic"):
        
        st.header("1. Dados Básicos")
        opcoes_sn = ["Não", "Sim"]
        doenca_previa = st.radio("Você possui diagnóstico prévio de doença no trato urinário?", opcoes_sn)
        
        idade = st.number_input("Idade", min_value=18, max_value=100, step=1, value=None, placeholder="Sua idade")
        
        opcoes_sexo = ["Selecione", "Feminino", "Masculino"]
        sexo = st.selectbox("Sexo", opcoes_sexo)
        
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, step=0.1, value=None, placeholder="Ex: 70.5")
        altura = st.number_input("Altura em centímetros (Ex: 175)", min_value=100, max_value=250, step=1, value=None, placeholder="Ex: 175")
        
        opcoes_periodo = [
            "1º", "2º", "3º", "4º", "5º", "6º", 
            "7º", "8º", "9º", "10º", "11º", "12º"
        ]
        periodo = st.selectbox("Período da faculdade", opcoes_periodo)
        
        faculdade = st.text_input("Em qual faculdade você estuda?")
        
        opcoes_estados = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        estado = st.selectbox("Em qual estado fica essa faculdade?", opcoes_estados)

        st.divider()

        st.header("2. Hábitos de Vida")
        hidratacao = st.number_input("Água em ml por dia (1 litro = 1000 ml)", min_value=0, step=100, value=None, placeholder="Ex: 2000")
        cafeina = st.number_input("Cafeína em ml por dia (café, energéticos):", min_value=0, step=50, value=None, placeholder="Ex: 250")

        st.divider()

        st.header("3. Avaliação de Incontinência Urinária (ICIQ-SF)")
        
        opcoes_iciq_3 = [
            "0 - Nunca", 
            "1 - Uma vez por semana ou menos", 
            "2 - Duas ou três vezes por semana", 
            "3 - Uma vez ao dia", 
            "4 - Diversas vezes ao dia", 
            "5 - O tempo todo"
        ]
        iciq_3 = st.radio("Com que frequência você perde urina?", opcoes_iciq_3)
        
        opcoes_iciq_4 = [
            "0 - Nenhuma", 
            "2 - Uma pequena quantidade", 
            "4 - Uma moderada quantidade", 
            "6 - Uma grande quantidade"
        ]
        iciq_4 = st.radio("Quantidade de urina que você pensa que perde:", opcoes_iciq_4)
        
        iciq_5 = st.slider("Quanto que perder urina interfere em sua vida diária? (0-10)", 0, 10, 0)
        
        st.write("Quando você perde a urina? (Selecione todas que se aplicam)")
        iciq_6_1 = st.checkbox("Nunca")
        iciq_6_2 = st.checkbox("Perco antes de chegar ao banheiro")
        iciq_6_3 = st.checkbox("Perco quando tusso ou espirro")
        iciq_6_4 = st.checkbox("Perco quando estou dormindo")
        iciq_6_5 = st.checkbox("Perco quando estou fazendo atividades físicas")
        iciq_6_6 = st.checkbox("Perco quando terminei de urinar e estou me vestindo")
        iciq_6_7 = st.checkbox("Perco sem razão óbvia")
        iciq_6_8 = st.checkbox("Perco o tempo todo")
        
        st.divider()

        st.header("4. Bexiga Hiperativa (ICIQ-OAB)")
        
        opcoes_oab_3a = [
            "0 - 1 a 6 vezes", 
            "1 - 7 a 8 vezes", 
            "2 - 9 a 10 vezes", 
            "3 - 11 a 12 vezes", 
            "4 - 13 ou mais vezes"
        ]
        oab_3a = st.radio("3a. Frequência que urina durante o dia?", opcoes_oab_3a)
        oab_3b = st.slider("3b. O quanto isso te incomoda? (0-10)", 0, 10, 0, key='oab3b')
        
        opcoes_oab_4a = [
            "0 - Nenhuma", 
            "1 - Uma", 
            "2 - Duas", 
            "3 - Três", 
            "4 - Quatro ou mais"
        ]
        oab_4a = st.radio("4a. Durante a noite, quantas vezes levanta para urinar?", opcoes_oab_4a)
        oab_4b = st.slider("4b. O quanto isso te incomoda? (0-10)", 0, 10, 0, key='oab4b')
        
        opcoes_oab_5a = [
            "0 - Nunca", 
            "1 - Ocasionalmente", 
            "2 - Às vezes", 
            "3 - Na maioria das vezes", 
            "4 - O tempo todo"
        ]
        oab_5a = st.radio("5a. Tem que correr para o banheiro para urinar?", opcoes_oab_5a)
        oab_5b = st.slider("5b. O quanto isso te incomoda? (0-10)", 0, 10, 0, key='oab5b')
        oab_6a = st.radio("6a. Vaza urina antes de conseguir chegar ao banheiro?", opcoes_oab_5a)
        oab_6b = st.slider("6b. O quanto isso te incomoda? (0-10)", 0, 10, 0, key='oab6b')

        st.divider()

        st.header("5. Percepção de Estresse (PSS-10)")
        
        opcoes_pss = [
            "0 - Nunca", 
            "1 - Quase nunca", 
            "2 - Às vezes", 
            "3 - Frequentemente", 
            "4 - Muito frequentemente"
        ]
        
        pss_1 = st.selectbox("1. Sentiu-se chateado por algo inesperado?", opcoes_pss)
        pss_2 = st.selectbox("2. Sentiu-se incapaz de controlar coisas importantes?", opcoes_pss)
        pss_3 = st.selectbox("3. Sentiu-se nervoso e estressado?", opcoes_pss)
        pss_4 = st.selectbox("4. Sentiu-se confiante para lidar com problemas?", opcoes_pss)
        pss_5 = st.selectbox("5. Sentiu que as coisas iam do seu jeito?", opcoes_pss)
        pss_6 = st.selectbox("6. Achou que não conseguia lidar com tudo?", opcoes_pss)
        pss_7 = st.selectbox("7. Controlou irritações na vida?", opcoes_pss)
        pss_8 = st.selectbox("8. Sentiu que estava no controle?", opcoes_pss)
        pss_9 = st.selectbox("9. Ficou irritado com coisas fora do controle?", opcoes_pss)
        pss_10 = st.selectbox("10. Sentiu dificuldades se acumulando?", opcoes_pss)

        st.divider()

        st.header("6. Qualidade do Sono (PSQI-BR)")
        psqi_1 = st.time_input("1. Quando geralmente foi para a cama à noite?")
        psqi_2 = st.number_input("2. Minutos para dormir:", min_value=0, value=None, placeholder="Ex: 30")
        psqi_3 = st.time_input("3. Quando geralmente levantou de manhã?")
        psqi_4 = st.number_input("4. Horas de sono por noite:", min_value=0.0, step=0.5, value=None, placeholder="Ex: 7.0")
        
        opcoes_psqi_freq = [
            "Nenhuma no último mês", 
            "Menos de uma vez por semana", 
            "Uma ou duas vezes por semana", 
            "Três ou mais vezes na semana"
        ]
        
        psqi_5a = st.selectbox("5A) Não adormeceu em 30 min", opcoes_psqi_freq)
        psqi_5b = st.selectbox("5B) Acordou no meio da noite", opcoes_psqi_freq)
        psqi_5c = st.selectbox("5C) Levantou para ir ao banheiro", opcoes_psqi_freq)
        psqi_5d = st.selectbox("5D) Não respirou bem", opcoes_psqi_freq)
        psqi_5e = st.selectbox("5E) Tossiu ou roncou forte", opcoes_psqi_freq)
        psqi_5f = st.selectbox("5F) Sentiu frio", opcoes_psqi_freq)
        psqi_5g = st.selectbox("5G) Sentiu calor", opcoes_psqi_freq)
        psqi_5h = st.selectbox("5H) Teve sonhos ruins", opcoes_psqi_freq)
        psqi_5i = st.selectbox("5I) Teve dor", opcoes_psqi_freq)
        
        opcoes_psqi_6 = ["Muito boa", "Boa", "Ruim", "Muito ruim"]
        psqi_6 = st.radio("6. Qualidade geral do sono:", opcoes_psqi_6)
        
        psqi_7 = st.selectbox("7. Tomou remédio para dormir?", opcoes_psqi_freq)
        psqi_8 = st.selectbox("8. Dificuldade para ficar acordado de dia?", opcoes_psqi_freq)
        
        opcoes_psqi_9 = [
            "Nenhuma dificuldade", 
            "Um problema leve", 
            "Um problema razoável", 
            "Um grande problema"
        ]
        psqi_9 = st.radio("9. Problema para manter o entusiasmo?", opcoes_psqi_9)
        
        opcoes_psqi_10 = [
            "Não", 
            "Sim, em outro quarto", 
            "Sim, em outra cama", 
            "Sim, na mesma cama"
        ]
        psqi_10 = st.radio("10. Parceiro ou colega de quarto?", opcoes_psqi_10)
        
        st.divider()

        submit_button = st.form_submit_button(label="Finalizar e Enviar Respostas")

        if submit_button:
            with st.spinner("Salvando respostas no banco de dados..."):
                try:
                    # --- A MUDANÇA MÁGICA FINAL: LENDO A CHAVE NOVA SEM ERROS ---
                    credenciais_json = json.loads(st.secrets["gcp_json"])
                    cliente = gspread.service_account_from_dict(credenciais_json)
                    
                    # LINK DA PLANILHA
                    link_da_sua_planilha = "https://docs.google.com/spreadsheets/d/1FoXC3MIutbs0Ri4MxVKLf0E7fo91ODgTVx6au_P6NYU/edit?usp=sharing"
                    
                    planilha_completa = cliente.open_by_url(link_da_sua_planilha)
                    aba = planilha_completa.sheet1
                    
                    # Formatação de motivos
                    motivos = []
                    if iciq_6_1: motivos.append("Nunca")
                    if iciq_6_2: motivos.append("Antes banheiro")
                    if iciq_6_3: motivos.append("Tosse/Espirro")
                    if iciq_6_4: motivos.append("Dormindo")
                    if iciq_6_5: motivos.append("Ativ Física")
                    if
