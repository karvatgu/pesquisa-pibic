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
        
        opcoes
