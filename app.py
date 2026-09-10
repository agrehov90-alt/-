import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Скрипт продаж ЭВО", layout="centered")

# Инициализация состояния приложения (состояние шага)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'client_provider' not in st.session_state:
    st.session_state.client_provider = ""
if 'current_price' not in st.session_state:
    st.session_state.current_price = 0

def next_step(step_number):
    st.session_state.step = step_terminator(step_number)

def step_terminator(n):
    return n

# Стилизация
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .script-text { font-size: 1.2em; color: #2c3e50; background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin-bottom: 20px; }
    .instruction { font-style: italic; color: #7f8c8d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Скрипт продаж: Интернет + ТВ (ЭВО)")

# --- ШАГ 1: УСТАНОВЛЕНИЕ КОНТАКТА ---
if st.session_state.step == 1:
    st.subheader("Этап 1: Установление контакта")
    st.markdown('<div class="script-text"><b>Менеджер:</b> Здравствуйте! [Имя клиента]. Меня зовут [Имя менеджера], компания ЭВО — наш местный городской провайдер связи. [Имя клиента], звоню буквально на полторы минуты. Мы сейчас проводим плановую модернизацию сети и обновление оборудования по Ульяновской области. Задам буквально два технических вопроса, чтобы проверить, стабильно ли у вас работают услуги связи, и предложу наш готовый тариф для вашего дома. Хорошо?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Клиент: «Да, давайте»"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Клиент: «Уже есть провайдер»"):
            st.session_state.client_provider = "Другой провайдер"
            st.session_state.step = 2
            st.rerun()

# --- ШАГ 2: АУДИТ ---
elif st.session_state.step == 2:
    st.subheader("Этап 2: Профессиональный аудит")
    
    if st.session_state.client_provider == "Другой провайдер":
        st.markdown('<div class="script-text"><b>Менеджер:</b> Это отлично, без интернета сейчас никуда. А пользуетесь Ростелекомом, МТС, Билайн или Дом.ру? Просто мы — местная городская компания, и сейчас переключаем жителей вашего дома на наше новое оборудование по сниженной цене. Сколько сейчас в месяц отдаете?</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="script-text"><b>Менеджер:</b> Подскажите, пожалуйста, сейчас дома интернетом от какого провайдера пользуетесь? Интернет с ТВ или по отдельности?</div>', unsafe_allow_html=
True)

    st.info("Введите текущую стоимость услуг (для расчета экономии):")
    st.session_state.current_price = st.number_input("Цена в рублях", value=st.session_state.current_price)

    st.markdown("---")
    st.markdown('<div class="instruction">Выберите реакцию клиента на вопрос о качестве связи:</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Клиент: «Бывают проблемы (тормозит)»"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Клиент: «Все работает хорошо»"):
            st.session_state.step = 3
            st.rerun()

# --- ШАГ 3: ПРЕЗЕНТАЦИЯ ---
elif st.session_state.step == 3:
    st.subheader("Этап 3: Презентация-решение")
    
    savings = st.session_state.current_price - 650 # Предположим, наш тариф 650
    
    st.markdown(f'''
    <div class="script-int">
        <div class="script-text">
        <b>Менеджер:</b> Смотрите, [Имя клиента], почему я и звоню. Мы — местная компания, наши узлы связи находятся прямо в вашем районе, поэтому городская сеть вечером не перегружается. Мы можем подключить вам наш хит-тариф: стабильный интернет на честной скорости, плюс пакет цифрового ТВ.
        <br><br>
        <b>Финансовая выгода:</b> Вместо ваших <b>{st.session_state.current_price} руб.</b>, наш пакет будет стоить всего <b>650 рублей</b> в месяц. Вы экономите около <b>{savings * 12} рублей в год!</b>
        <br><br>
        <b>Оффер:</b> При оформлении заявки сегодня, мы закрепим за вами эту цену и сделаем скидку 50% на первый месяц!
        </div>
    </div>
    ''', unsafe_allow_html=True)

    if st.button("Перейти к возражениям"):
        st.session_state.step = 4
        st.rerun()

# --- ШАГ 4: ВОЗРАЖЕНИЯ ---
elif st.session_state.step == 4:
    st.subheader("Этап 4: Отработка возражений")
    st.markdown('<div class="instruction">Если клиент говорит, что не хочет менять провайдера из-за проводов:</div>', unsafe_allow_html=True)
    st.markdown('<div class="script-text"><b>Менеджер:</b> Подскажите, вас смущает именно сам процесс переподключения или всё-таки цена? <br><br> <b>Если процесс:</b> Понимаю вас, ремонт — дело святое. Именно поэтому наши ребята работают аккуратно: мы используем уже существующий кабель. Мастер просто переключит провод за 15 минут, и всё заработает.</div>', unsafe_allow_html=True)
    
    if st.button("Перейти к закрытию"):
        st.session_state.step = 5
        st.rerun()

# --- ШАГ 5: ЗАКРЫТИЕ ---
elif st.session_state.step == 5:
    st.subheader("Этап 5: Закрытие сделки")
    st.markdown('<div class="script-text"><b>Менеджер:</b> [Имя клиента], у нас как раз завтра или в субботу мастер будет работать в вашем доме. Вам в какое время было бы удобнее, чтобы он заглянул — в первой половине дня или после обеда?</div>', unsafe_allow_html=True)
    
    st.info("Зафиксируйте данные клиента:")
    name = st.text_input("ФИО клиента")
    phone = st.text_input("Номер телефона")
    time = st.selectbox("Время визита", ["Утро", "День", "Вечер"])

    st.markdown('<div class="script-text"><b>Менеджер:</b> Отлично. Записываю: [Время]. Кстати, пока мастер будет у вас, мы можем бесплатно выдать вам нашу сим-карту на пробу?</div>', unsafe_allow_html=True)
    
    if st.button("Завершить звонок"):
        st.success("Сделка зафиксирована! Не забудьте отправить СМС-подтверждение клиенту.")
        if st.button("Начать новый звонок"):
            st.session_state.step = 1
            st.session_state.client_provider = ""
            st.rerun()

# Кнопка сброса (всегда внизу)
if st.session_state.step != 1:
    if st.button("🔄 Начать заново"):
        st.session_state.step = 1
        st.session_state.client_provider = ""
        st.rerun()
