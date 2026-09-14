import streamlit as st

# --- НАСТРОЙ (PAGE CONFIG) ---
st.set_page_config(page_title="Интерактивный скрипт продаж: ЭВО", layout="wide")

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (SESSION STATE) ---
if 'step' not in st.session_state:
    st.session_state.step = 'step1'

if 'client_data' not in st.session_state:
    st.session_state.client_data = {
        'competitor': '',
        'price': '',
        'pain': '',
        'cross_sell': False
    }

def reset_app():
    st.session_state.step = 'step1'
    st.session_state.client_data = {'competitor': '', 'price': '', 'pain': '', 'cross_sell': False}

# --- СТИЛИЗАЦИЯ (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .manager-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-left: 10px solid #2,196f3;
        border-radius: 5px;
        margin-bottom: 20px;
        font-size: 18px;
        color: #0d47a1;
    }
    .client-box {
        background-color: #f1f8e9;
        padding: 20px;
        border-left: 10px solid #4caf50;
        border-radius: 5px;
        margin-bottom: 20px;
        font-size: 18px;
        color: #1b5e20;
    }
    .step-title {
        color: #1e88e5;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Управление скриптом")
    st.info("Используйте кнопки ниже, чтобы переходить по веткам диалога.")
    if st.button("🔄 Начать заново"):
        reset_app()
        st.rerun()
    st.divider()
    st.subheader("Данные звонка")
    st.write(f"**Этап:** {st.session_state.step}")

# --- ОСНОВНОЙ КОНТЕНТ ---

# ШАГ 1: УСТАНОВЛЕНИЕ КОНТАКТА
if st.session_state.step == 'step1':
    st.markdown("<div class='step-title'>1. Установление контакта и Крючок</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='manager-int'>
        <b style='color:#0d47a1'>Менеджер:</b> Здравствуйте! [Имя клиента]<br><br>
        <b style='color:#0d47a1'>Менеджер (Вариативный инфоповод):</b> Меня зовут [Имя менеджера], компания ЭВО — наш местный городской провайдер связи. [Имя клиента], звоню буквально на полторы минуты. Мы сейчас проводим плановую модернизацию сети и обновление оборудования по Ульяновской области.<br><br>
        <b style='color:#0d47a1'>Менеджер (Программирование):</b> Задам буквально два технических вопроса, чтобы проверить, стабильно ли у вас работают услуги связи, и предложу наш готовый тариф для вашего дома. Хорошо?
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Клиент согласен (Да/Ну давайте)"):
            st.session_state.step = 'step2'
            st.rerun()
    with col2:
        if st.button("❌ Клиент: 'Я уже пользуюсь другим провайдером'"):
            st.session_state.client_data['competitor'] = "Другой провайдер"
            st.session_state.step = 'step2_alt'
            st.rerun()

# ШАГ 2 (Вариант А): АУДИТ
elif st.session_state.step == 'step2':
    st.markdown("<div class='step-title'>2. Профессиональный аудит</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='manager-box'>
        <b>Менеджер:</b> Подскажите, пожалуйста, сейчас дома интернетом от какого провайдера пользуетесь? Ростелеком, Дом.ру, МТС или Билайн? Интернет с ТВ или по отдельности?
    </div>
    """, unsafe_allow_html=True)
    
    comp = st.text_input("Введите название конкурента:", value=st.session_state.client_data['competitor'])
    st.session_state.client_data['competitor'] = comp
    
    price = st.text_input("Сколько сейчас в месяц уходит (руб)?", value=st.session_state.client_data['price'])
    st.session_state.client_data['price'] = price

    st.write("**Реакция на качество связи:**")
    pain_col1, pain_col2 = st.columns(2)
    with pain_col1:
        if st.button("🔴 Есть боли (подтупливает вечером)"):
            st.session_state.client_data['pain'] = 'pain_yes'
            st.session_state.step = 'step2_finish'
            st.rerun()
    with pain_col2:
        if st.button("🟢 Нет болей (все нормально)"):
            st.session_state.client_data['pain'] = 'pain_no'
            st.session_state.step = 'step2_finish'
            st.rerun()

# ШАГ 2 (Вариант Б): АУДИТ (Если уже есть другой провайдер)
elif st.session_state.step == 'step2_alt':
    st.markdown("<div class='step-title'>2. Отработка сопротивления и Аудит</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='manager-box'>
        <b>Менеджер:</b> Это отлично, без интернета сейчас никуда. А пользуетесь Ростелекомом, МТС, Билайн или Дом.ру? Просто мы — местная городская компания, и сейчас переключаем жителей вашего дома на наше новое оборудование по сниженной цене, чтобы вы не переплачивали за архивные тарифы гигантов. Сколько сейчас в месяц отдаете?
    </div>
    """, unsafe_allow_html=True)
    
    comp = st.text_input("Название конкурента:", value=st.session_state.client_data['competitor'])
    price = st.text_input("Сколько платите сейчас (руб):", value=st.session_state.client_data['price'])
    
    if st.button("Далее к проверке качества"):
        st.session_state.client_data['competitor'] = comp
        st.session_state.client_data['price'] = price
        st.session_state.step = 'step2_finish'
        st.rerun()

# ЗАВЕРШЕНИЕ АУДИТА
elif st.session_state.step == 'step2_finish':
    st.markdown("<div class='step-title'>2. Фиксация и Спрос</div>", unsafe_allow_html=True)
    
    if st.session_state.client_data['pain'] == 'pain_no':
        st.markdown(f"""
        <div class='client-box'><b style='color:#1b5e20'>Клиент:</b> Да нет, все нормально работает.</div>
        <div class='manager-box'>
            <b style='color:#0d47a1'>Менеджер:</b> Это отлично. А оборудование (роутер) давно меняли? Больше двух лет назад? Просто старые роутеры со временем начинают резать скорость, из-за чего приходится переплачивать за лишний тариф.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='client-box'><b style='color:#1b5e20'>Клиент:</b> Да, бывает, подтупливает вечером.</div>
        <div class='manager-box'>
            <b style='color:#0d47a1'>Менеджер:</b> Понял вас.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='manager-box'>
        <b style='color:#0d47a1'>Менеджер (Финансовый маркер):</b> И для сверки подскажите: за интернет и телевидение сейчас суммарно сколько в месяц уходит? Больше 700–800 рублей?
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='manager-box'>
        <b style='color:#0d47a1'>Менеджер (Фиксация и спрос):</b> Я вас услышал. То есть сейчас у вас {st.session_state.client_data['competitor']}, платите около {st.session_state.client_data['price']} рублей, но при этом стабильности по вечерам не хватает (или: оборудование уже старовато)/ То есть вам важно, чтобы интернет не падал, когда дети играют. Правильно я вас понял?
    </div>
    """, unsafe_allow_html=True)

    if st.button("Перейти к Презентации"):
        st.session_state.step = 'step3'
        st.rerun()

elif st.session_state.step == 'step3':
    st.info("Конец демонстрации. Здесь будет блок презентации.")
    if st.button("Вернуться в начало"):
        reset_app()
        st.rerun()
