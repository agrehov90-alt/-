import streamlit as st

# --- КОНФИГУРАЦИЯ СТРАНИЦЫ ---
st.set_page_config(page_title="Скрипт продаж: ЭВО", layout="wide")

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (SESSION STATE) ---
if 'step' not in st.session_state:
    st.session_state.step = 'start'
if 'history' not in st.session_state:
    st.session_state.history = []
if 'client_info' not in st.session_state:
    st.session_state.client_info = {"competitor": "", "price": "", "pain": ""}

def log_action(manager_text, client_text):
    st.session_state.history.append({"manager": manager_text, "client": client_text})

# --- СТИЛИЗАЦИЯ ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ffffff; border: 1px solid #d1d5db; }
    .stButton>button:hover { border-color: #ff4b4b; color: #ff4b4#ff4b4b; }
    .manager-box { background-color: #e1f5fe; padding: 20px; border-radius: 10px; border-left: 5px solid #0288d1; margin-bottom: 20px; }
    .client-box { background-color: #f1f8e9; padding: 20px; border-radius: 10px; border-left: 5px solid #689f38; margin-bottom: 20px; }
    .step-indicator { font-size: 1.2em; font-weight: bold; color: #555; }
    </rate>
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГИКА ПРИЛОЖЕНИЯ ---

# Sidebar: Прогресс и История
with st.sidebar:
    st.title("📊 Статус звонка")
    steps_order = ["start", "contact", "audit", "presentation", "objections", "closing", "end"]
    current_idx = steps_order.index(st.session_state.step)
    st.progress((current_idx) / (len(steps_order) - 1))
    
    st.subheader("📜 История диалога")
    for entry in st.session_state.history:
        st.caption(f"👤: {entry['client']}")
        st.caption(f"🎙: {entry['manager']}")
    
    if st.button("🔄 Сбросить звонок"):
        st.session_state.clear()
        st.rerun()

# --- ГЛАВНЫЙ ЭКРАН ---

# ЭТАП 0: ЗАПУСК
if st.session_state.step == 'start':
    st.title("🚀 Интерактивный скрипт продаж")
    st.write("Нажмите кнопку ниже, чтобы начать звонок.")
    if st.button("Начать звонок"):
        st.session_state.step = 'contact'
        st.rerun()

# ЭТАМУ 1: УСТАНОВЛЕНИЕ КОНТАКТА
elif st.session_state.step == 'contact':
    st.markdown("<div class='step-indicator'>Этап 1: Установление контакта</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Здравствуйте! [Имя клиента]. Меня зовут [Имя], компания ЭВО — наш местный городской провайдер связи. 
        Звоню буквально на полторы минуты. Мы сейчас проводим модернизацию сети по Ульяновской области. 
        Задам буквально два технических вопроса, чтобы проверить стабильность связи и предложу наш тариф. Хорошо?
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Согласие (Да, давайте)"):
            log_action("Здравствуйте... Задам два вопроса. Хорошо?", "Да, давайте.")
            st.session_state.step = 'audit'
            st.rerun()
    with col2:
        if st.button("❌ Уже есть провайдер"):
            log_action("Здравствуйте... Задам два вопроса. Хорошо?", "Я уже пользуюсь другим провайдером.")
            st.session_state.client_info['has_competitor'] = True
            st.session_state.step = 'audit'
            st.rerun()

# ЭТАП 2: АУДИТ
elif st.session_state.step == 'audit':
    st.markdown("<div class='step-indicator'>Этап 2: Профессиональный аудит</div>", unsafe_allow_html=True)
    
    # Динамическая реплика в зависимости от того, есть ли конкурент
    if st.session_state.client_info.get('has_competitor'):
        m_text = "Это отлично, без интернета сейчас никуда. А пользуетесь Ростелекомом, МТС, Билайн или Дом.ру? Просто мы — местная компания, и сейчас переключаем жителей на новое оборудование по сниженной цене. Сколько сейчас в месяц отдаете?"
    else:
        m_text = "Подскажите, пожалуйста, сейчас дома интернетом от какого провайдера пользуетесь? Ростелеком, Дом.ру, МТС или Билайн? Интернет с ТВ или по отдельности?"
    
    st.markdown(f"<div class='manager-box'><strong>🎙 Менеджер:</strong><br>{m_text}</div>", unsafe_allow_html=True)

    st.subheader("🔍 Выявление болей")
    st.write("Качество связи:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 Есть проблемы (тормозит вечером)"):
            log_action(m_text, "Да, бывает, подтупливает вечером.")
            st.session_state.client_info['pain'] = "speed_drop"
            st.session_state.step = 'presentation'
            st.rerun()
    with col2:
        if st.button("🟢 Все работает хорошо"):
            log_action(m_text, "Да нет, все нормально работает.")
            st.session_state.client_info['pain'] = "no_pain"
            st.session_state.step = 'presentation'
            st.rerun()

    st.divider()
    st.subheader("💰 Финансовый маркер")
    st.write("Сколько платите в месяц?")
    price_input = st.number_input("Сумма в рублях", min_value=0, value=850)
    if st.button("Зафиксировать цену"):
        st.session_rate.client_info['price'] = price_input
        log_action("Сколько сейчас в месяц отдаете?", f"Около {price_input} руб.")
        st.session_state.step = 'presentation'
        st.rerun()

# ЭТАП 3: ПРЕЗЕНТАЦИЯ
elif st.session_state.step == 'presentation':
    st.markdown("<div class='step-indicator'>Этап 3: Презентация-решение</div>", unsafe_allow_html=True)
    
    pain_msg = "стабильности по вечерам не хватает" if st.session_state.client_info.get('pain') == "speed_drop" else "оборудование уже старовато"
    price = st.session_state.client_info.get('price', 850)
    
    m_text = f"""
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Смотрите, почему я и звоню. Мы — местная компания, наши узлы связи прямо в вашем районе, поэтому сеть вечером не перегружается. 
        Мы можем подключить наш хит-тариф: стабильный интернет на честной скорости, плюс пакет цифрового ТВ. 
        При этом мы ставим современное оборудование. И по деньгам: вместо ваших {price} рублей, наш пакет будет стот всего 650 рублей. 
        Вы экономите более 2400 рублей в год, при этом вам важно, чтобы {pain_msg}. 
        Плюс, при оформлении сегодня, мы закрепим цену и сделаем скидку 50% на первый месяц!
    </div>
    """, unsafe_allow_html=True)
    st.markdown(m_text, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Согласен / Интересно"):
            log_action("Презентация тарифа...", "Интересно, давайте.")
            st.session_state.step = 'closing'
            st.rerun()
    with col2:
        if st.button("❌ Возражение (Дорого/Не хочу)"):
            log_action("Презентация тарифа...", "Мне неохота менять, это опять провода тянуть...")
            st.session_state.step = 'objections'
            st.rerun()

# ЭТАП 4: ОТРАБОТКА ВОЗРАЖЕНИЙ
elif st.session_state.step == 'objections':
    st.markdown("<div class='step-indicator'>Этап 4: Отработка возражений</div>", unsafe_allow_html=True)
    
    m_text = """
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Подскажите, вас смущает именно сам процесс переподключения или всё-таки цена?<br><br>
        (Если процесс): Понимаю вас, ремонт — дело святое. Именно поэтому наши ребята работают аккуратно: мы используем уже существующий кабель. 
        Ничего сверлить не придется. Мастер просто переключит провод и настроит роутер за 15 минут.
    </div>
    """, unsafe_allow_html=True)
    st.markdown(m_text, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Понятно, тогда давайте"):
            log_action("Отработка процесса", "Ладно, давайте попробуем.")
            st.session_state.step = 'closing'
            st.rerun()
    with col2:
        if st.button("❌ Все равно нет"):
            log_action("Отработка процесса", "Нет, не хочу.")
            st.session_state.step = 'end'
            st.rerun()

# ЭТАП 5: ЗАКРЫТИЕ
elif st.session_state.step == 'closing':
    st.markdown("<div class='step-indicator'>Этап 5: Закрытие и Кросс-продажа</div>", unsafe_allow_html=True)
    
    m_text = f"""
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Подведем итоги: тариф, подключение произойдет в течение 3 рабочих дней. <br><br>
        Кстати, пока мастер будет у вас, мы можем абсолютно бесплатно выдать вам нашу сим-карту на пробу, привезти её вместе с договором?
    </div>
    """, unsafe_allow_html=True)
    st.markdown(m_text, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Да, привозите"):
            log_action("Предложение сим-карты", "Да, давайте.")
            st.session_state.step = 'end'
            st.rerun()
    with col2:
        if st.button("❌ Нет, не нужно"):
            log_action("Предложение сим-карты", "Нет, не надо.")
            st.session_state.step = 'end'
            st.rerun()

# ЭТАП 6: ЗАВЕРШЕНИЕ
elif st.session_state.step == 'end':
    st.success("🎉 Звонок завершен!")
    st.markdown("""
    <div class='manager-box'>
        <strong>🎙 Менеджер:</strong><br>
        Договорились. В ближайшие сутки с Вами свяжется специалист для согласования времени. 
        Нужен будет паспорт. Оплату можно внести через ЛК, приложение EVO L!fe или Сбербанк Онлайн. 
        Вопросы остались? Спасибо за уделенное время! Хорошего дня!
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏁 Завершить сессию"):
        st.session_state.clear()
        st.rerun()
