import streamlit as st

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Скрипт продаж: ЭВО", layout="centered")

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (State Machine) ---
## if 'step' not in st.session_state:
    st.session_state.step = 'contact'
## if 'client_info' not in st.session_state:
    st.session_state.client_info = {
        'has_competitor': False,
        'pain': None,
        'price': 0
    }

# Функция для сброса скрипта
## def reset_script():
    st.session_state.step = 'contact'
    st.session_state.client_info = {'has_competitor': False, 'pain': None, 'price': 0}

# --- СТИЛИЗАЦИЯ (CSS) ---
st.markdown("""
    <style>
    .step-indicator {
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 5px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }
    .manager-box {
        padding: 20px;
        background-color: #e1f5fe;
        border-left: 5px solid #0288d1;
        border-radius: 5px;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    .client-box {
        padding: 20px;
        background-color: #f1f8e9;
        border-left: 5px solid #689f38;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ЛОГИКА СКРИПТА ---

# Боковая панель с управлением
## with st.sidebar:
    st.title("Управление")
    ## if st.button("🔄 Начать заново"):
        reset_script()
        st.rerun()
    st.divider()
    st.write("**Текущие данные:**")
    st.write(st.session_state.client_info)

# --- ЭТАП 1: УСТАНОВЛЕННЫЙ КОНТАКТ ---
## if st.session_state.step == 'contact':
    st.markdown("<div class='step-indicator'>Этап 1: Установление контакта</div>", unsafe_allow_html=True)
    
    m_text = """
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Здравствуйте! [Имя клиента]. Меня зовут [Имя менеджера], компания ЭВО — наш местный городской провайдер связи. 
        Задам буквально два технических вопроса, чтобы проверить, стабильно ли у вас работают услуги связи, 
        и предложу наш готовый тариф для вашего дома. Хорошо?
    </div>
    """
    st.markdown(m_text, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    ## with col1:
        ## if st.button("✅ Согласен (Да)"):
            st.session_state.step = 'audit'
            st.rerun()
    ## with colint2 := col2:
        ## if st.button("❌ Уже есть провайдер"):
            st.session_state.client_info['has_competitor'] = True
            st.session_state.step = 'audit'
            st.rerun()

# --- ЭТАП 2: АУДИТ ---
## elif st.session_state.step == 'audit':
    st.markdown("<div class='step-indicator'>Этап 2: Профессиональный аудит</div>", unsafe_allow_html=True)
    
    # Если клиент сказал, что у него уже есть провайдер, добавляем уточняющую фразу
    intro_text = ""
    ## if st.session_state.client_info.get('has_competitor'):
        intro_text = "Это отлично, без интернета сейчас никуда. А пользуетесь Ростелекомом, МТС, Билайн или Дом.ру? "
    
    m_text = f"""
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        {intro_text}Подскажите, пожалуйста, сейчас дома интернетом от какого провайдера пользуетесь? 
        Интернет с ТВ или по отдельности? И подскажите, за интернет и ТВ сейчас суммарно сколько в месяц уходит?
    </div>
    """
    st.markdown(m_text, unsafe_allow_html=True)

    # Ввод данных (имитация ответа клиента)
    ## with st.container():
        price_input = st.number_input("Сколько платите сейчас (руб)?", min_value=0, value=850)
        st.session_state.client_info['price'] = price_input
        
        st.write("Были ли проблемы с качеством?")
        pain_choice = st.radio("Вариант ответа клиента:", ["Все отлично", "Да, вечером скорость падает", "Роутер старый"])
        
        ## if st.button("Продолжить к презентации"):
            ## if pain_choice == "Все отлично":
                st.session_state.client_info['pain'] = 'none'
            ## elif pain_choice == "Да, вечером скорость падает":
                st.session_state.client_info['pain'] = 'speed_drop'
            ## else:
                st.session_state.client_info['pain'] = 'router'
            
            st.session_state.step = 'presentation'
            st.rerun()

# --- ЭТАП 3: ПРЕЗЕНТАЦИЯ ---
## elif st.session_state.step == 'presentation':
    st.markdown("<div class='step-indicator'>Этап 3: Презентация-решение</div>", unsafe_allow_html=True)
    
    # Логика формирования текста на основе боли
    pain_msg = ""
    ## if st.session_state.client_info.get('pain') == "speed_drop":
        pain_msg = "стабильности по вечерам не хватает"
    ## elif st.session_state.client_info.get('pain') == "router":
        pain_msg = "оборудование уже старовато"
    ## else:
        pain_msg = "важно, чтобы связь была надежной"

    price_old = st.session_state.client_info.get('price', 850)
    
    m_text = f"""
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><int>Смотрите, почему я и звоню. Мы — местная компания, наши узлы связи прямо в вашем районе, поэтому сеть вечером не перегружается. 
        Мы можем подключить наш хит-тариф: стабильный интернет на честной скорости, плюс пакет цифрового ТВ. 
        При этом мы ставим современное оборудование. И по деньгам: вместо ваших {price_old} рублей, наш пакет будет стоить всего 650 рублей. 
        Вы экономите более рыночной цены в год, при этом вам важно, чтобы {pain_msg}. 
        Плюс, при оформлении сегодня, мы закрепим цену и сделаем скидку 50% на первый месяц!</int>
    </div>
    """
    st.markdown(m_text, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    ## with col1:
        ## if st.button("✅ Согласен (Переходим к возражениям)"):
            st.session_state.step = 'objections'
            st.rerun()
    ## with col2:
        if st.
            st.session_state.step = 'closing'
            st.rerun()

# --- ЭТАП 4: ВОЗРАЖЕНИЯ ---
## elif st.session_state.step == 'objections':
    st.markdown("<div class='step-indicator'>Этап 4: Отработка возражений</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='client-box'>
        <strong>👤 Клиент:</strong><br>
        "Мне неохота менять, это опять провода тянуть, ремонт портить..."
    </div>
    """, unsafe_allow_html=True)

    m_text = """
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Подскажите, вас смущает именно сам процесс переподключения или всё-таки цена?
    </div>
    """
    st.markdown(m_text, unsafe_allow_html=True)

    ## if st.button("Ответ: 'Только процесс!'"):
        st.session_state.step = 'closing
