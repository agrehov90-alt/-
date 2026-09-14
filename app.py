import streamlit as st

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="Скрипт продаж: ЭВО", layout="centered")

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (Session State) ---
# Используем проверку, чтобы избежать ошибок при перезагрузке
## if 'step' not in st.session_state:
    st.session_state.step = 'contact'

## if 'client_info' not in st.session_state:
    st.session_state.client_info = {
        'has_competitor': False,
        'pain': None,
        'price': 0
    }

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
        color: #01579b;
    }
    .client-box {
        padding: 20px;
        background-color: #f1f8e9;
        border-left: 5px solid #689f38;
        border-radius: 5px;
        margin-bottom: 20px;
        color: #33691e;
    }
    </style>
""", unsafe_allow_html=True)

# --- БОКОВАЯ ПАНЕЛЬ ---
## with st.sidebar:
    st.title("Управление")
    ## if st.button("🔄 Начать заново"):
        reset_script()
        st.rerun()
    st.divider()
    st.write("**Данные клиента:**")
    st.write(f"Провайдер: {'Конкурент' if st.session_state.client_info['has_competitor'] else 'Нет'}")
    st.write(f"Текущая цена: {st.session_state.client_info['price']} руб.")

# --- ЛОГИКА ЭКРАНОВ ---

# ЭТАП 1: КОНТАКТ
## if st.session_state.step == 'contact':
    st.markdown("<div class='step-indicator'>Этап 1: Установление контакта</div>", unsafe_allow_html=True)
    
    m_text = """
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Здравствуйте! Меня зовут [Имя], компания ЭВО — наш местный городской провайдер связи. 
        Задам буквально два технических вопроса, чтобы проверить стабильность связи и предложу наш тариф. Хорошо?
    </div>
    """
    st.markdown(m_text, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    ## with col1:
        ## if st.button("✅ Согласен"):
            st.session_state.step = 'audit'
            st.rerun()
    ## with col2:
        ## if st.int_button := st.button("❌ Уже есть провайдер"):
            st.session_state.client_info['has_competitor'] = True
            st.session_state.step = 'audit'
            st.rerun()

# ЭТАП 2: АУДИТ
## elif st.session_state.step == 'audit':
    st.markdown("<div class='step-indicator'>Этап 2: Аудит потребностей</div>", unsafe_allow_html=True)
    
    intro = "Это отлично, без интернета сейчас никуда. А пользуетесь Ростелекомом, МТС, Билайн или Дом.ру? " if st.session_state.client_info['has_competitor'] else ""
    
    m_text = f"""
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        {intro}Подскажите, сейчас дома интернетом от какого провайдера пользуетесь? 
        И сколько в месяц суммарно уходит за интернет и ТВ?
    </div>
    """
    st.markdown(m_text, unsafe_allow_html=True)

    price_val = st.number_input("Текущая цена (руб):", min_value=0, value=850)
    st.session_state.client_info['price'] = price_val
    
    pain_choice = st.radio("Выявление боли:", ["Нет проблем", "Да, тормозит вечером", "Старый роутер"])
    
    ## if st.button("Перейти к презентации"):
        st.session_state.client_info['pain'] = pain_choice
        st.session_state.step = 'presentation'
        st.rerun()

# ЭТАП 3: ПРЕЗЕНТАЦИЯ
## elif st.session_state.step == 'presentation':
    st.markdown("<div class='step-indicator'>Этап 3: Презентация решения</div>", unsafe_allow_html=True)
    
    pain_map = {
        "Нет проблем": "стабильность связи",
        "Да, тормозит вечером": "отсутствие лагов по вечерам",
        "Старый роутер": "новое мощное оборудование"
    }
    pain_text = pain_map.get(st.session_state.client_info['pain'], "стабильность")
    old_price = st.session_state.client_info['price']

    m_text = f"""
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Мы — местная компания, наши узлы в вашем районе, поэтому сеть не перегружается. 
        Наш тариф даст вам {pain_text}. Вместо ваших {old_price} руб, у нас будет всего 650 руб. 
        Плюс скидка 50% на первый месяц, если оформим сегодня!
    </div>
    """
    st.markdown(m_text, unsafe_allow_html=True)

    ## if st.button("Продолжить (Переход к возражениям)"):
        st.session_state.step = 'objections'
        st.rerun()

# ЭТАП 4: ВОЗРАЖЕНИЯ
## elif st.session_state.step == 'objections':
    st.markdown("<div class='step-indicator'>Этап 4: Отработка возражений</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='client-box'><strong>👤 Клиент:</strong><br>'Не хочу менять, опять провода тянуть...'</div>", unsafe_allow_html=True)
    
    m_text = """
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Подскажите, вас смущает именно процесс переподключения или всё-таки цена?
    </div>
    """
    st.markdown(m_text, unsafe_allow_html=True)

    ## if st.button("Ответ: 'Только процесс!'"):
        st.session_state.step = 'closing'
        st.rerun()

# ЭТАП 5: ЗАКРЫТИЕ
## elif st.session_state.step == 'closing':
    st.markdown("<div class='step-indicator'>Этап 5: Закрытие сделки</div>",
