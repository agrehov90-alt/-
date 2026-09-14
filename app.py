import streamlit as st

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="Скрипт продаж: ЭВО", layout="centered")

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ ---
if 'step' not in st.session_state:
    st.session_state.step = 'contact'

if 'client_info' not in st.session_state:
    st.session_state.client_info = {
        'has_competitor': False,
        'pain_type': None,
        'current_price': 0,
        'cross_sell': False
    }

def reset_script():
    st.session_state.step = 'contact'
    st.session_state.client_info = {
        'has_competitor': False,
        'pain_type': None,
        'current_price': 0,
        'cross_sell': False
    }

# --- СТИЛИЗАЦИЯ ---
st.markdown("""
    <style>
    .step-header {
        font-size: 24px; font-weight: bold; color: #1E88E5;
        margin-bottom: 20px; border-bottom: 2px solid #1E88E5;
    }
    .manager-msg {
        padding: 15px; background-color: #E3F2FD;
        border-left: 5px solid #2196F3; border-radius: 5px;
        margin-bottom: 15px; font-size: 16px; color: #0D47A1;
    }
    .client-msg {
        padding: 15px; background-color: #F1F8E9;
        border-left: 5px solid #4CAF50; border-radius: 5px;
        margin-bottom: 15px; font-size: 16px; color: #1B5E20;
    }
    .info-box {
        padding: 10px; background-color: #FFF3E0;
        border: 1px solid #FFB74D; border-radius: 5/px; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📊 Прогресс звонка")
    st.write(f"**Текущий этап:** {st.session_state.step.upper()}")
    st.divider()
    if st.button("🔄 Сбросить звонок"):
        reset_script()
        st.rerun()
    
    st.subheader("Данные клиента")
    st.write(f"Провайдер: {'Конкурент' if st.session_state.client_info['has_competitor'] else 'Новый'}")
    st.write(f"Текущая цена: {st.session_state.client_info['current_price']} руб.")

# --- ЛОГИКА ЭКРАНОВ ---

# 1. УСТАНОВЛЕНИЕ КОНТАКТА
if st.session_state.step == 'contact':
    st.markdown("<div class='step-header'>1. Контакт и Крючок</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='manager-msg'>
        <b>🎙 Менеджер:</b><br>
        Здравствуйте! Мы проводим модернизацию сети в Ульяновской области. 
        Задам два технических вопроса, чтобы проверить стабильность связи и предложить тариф. Хорошо?
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Да, давайте"):
            st.session_state.step = 'audit'
            st.rerun()
    with col2:
        if st.button("❌ Уже есть провайдер"):
            st.session_state.client_info['has_competitor'] = True
            st.session_state.step = 'audit'
            st.rerun()

# 2. АУДИТ
elif st.session_state.step == 'audit':
    st.markdown("<div class='step-header'>2. Профессиональный аудит</div>", unsafe_allow_html=True)
    
    if st.session_state.client_info['has_competitor']:
        st.markdown("""
        <div class='client-msg'>
            <b>👤 Клиент:</b><br>
            Да, пользуюсь Ростелекомом.
        </div>
        <div class='manager-msg'>
            <b>🎙 Менеджер:</b><br>
            Это отлично, без интернета сейчас никуда. А сколько сейчас в месяц суммарно уходит?
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='manager-msg'>
            <b>🎙 Менеджер:</b><br>
            Подскажите, сейчас каким провайдером пользуетесь? И сколько в месяц уходит?
        </div>
        """, unsafe_allow_html=True)

    price_input = st.number_input("Текущая цена (руб):", min_value=0, value=850)
    st.session_state.client_info['current_price'] = price_input

    st.write("**Выявление боли (выберите реакцию клиента):**")
    pain_choice = st.radio("Реакция клиента:", ["Все работает отлично", "Да, вечером тормозит", "Часто пропадает связь"])
    
    if st.button("Перейти к презентации"):
        st.session_state.client_info['pain_type'] = pain_choice
        st.session_state.step = 'presentation'
        st.rerun()

# 3. ПРЕЗЕНТАЦИЯ
elif st.session_state.step == 'presentation':
    st.markdown("<div class='step-header'>3. Презентация решения</div>", unsafe_allow_html=True)
    
    pain = st.session_state.client_info['pain_type']
    old_p = st.session_state.client_info['current_price']
    
    # Логика подмены текста в зависимости от боли
    extra_info = ""
    if pain == "Все работает отлично":
        extra_info = "А оборудование (роутер) давно меняли? Старые роутеры могут резать скорость."
    else:
        extra_info = "Понимаю, это неприятно. У нас узлы прямо в вашем районе, поэтому перегрузок нет."

    st.markdown(f"""
    <div class='manager-multiline'>
        <div class='manager-msg'>
            <b>🎙 Менеджер:</b><br>
            {extra_info}<br><br>
            Мы можем подключить наш хит-тариф: 100/250 Мбит/с + ТВ. 
            Вместо ваших <b>{old_p} руб.</b>, у нас будет всего <b>650 руб.</b><br>
            Вы экономите более 2400 рублей в год! При оформлении сегодня — скидка 50% на первый месяц.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Перейти к возражениям"):
        st.session_state.step = 'objections'
        st.rerun()

# 4. ВОЗРАЖЕНИЯ
elif st.session_state.step == 'objections':
    st.markdown("<div class='step-header'>4. Отработка возражений</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='client-msg'>
        <b>👤 Клиент:</b><br>
        'Мне неохота менять, это опять провода тянуть, ремонт портить...'
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='manager-msg'>
        <b>🎙 Менеджер:</b><br>
        Подскажите, вас смущает именно сам процесс переподключения или всё-таки цена?
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Только процесс"):
            st.session_state.step = 'closing'
            st.rerun()
    with col2:
        if st.button("❌ Всё равно дорого"):
            st.session_state.step = 'closing' # Для упрощения ведем к закрытию
            st.rerun()

# 5. ЗАКРЫТИЕ
elif st.session_state.step == 'closing':
    st.markdown("<div class='step-header'>5. Закрытие сделки</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='manager-msg'>
        <b>🎙 Менеджер:</b><br>
        Подведем итоги: тариф зафиксирован, подключение в течение 3 рабочих дней. 
        Специалист свяжется с вами завтра для согласования времени.
    </div>
    """, unsafe_allow_html=True)

    st.write("**Кросс-продажа (Сим-карта):**")
    if st.button("➕ Предложить сим-карту"):
        st.session_state.client_info['cross_sell'] = True
        st.rerun()
    
    if st.session_state.client_info['cross_sell']:
        st.markdown("""
        <div class='client-msg'>
            <b>👤 Клиент:</b><br>
            'Ладно, давайте попробуем.'
        </div>
        <div class='manager-msg'>
            <b>🎙 Менеджер:</b><br>
            Отлично! Мастер привезет её вместе с договором.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.success("✅ Сделка зафиксирована! Не забудьте напомнить про оплату через приложение EVO Life.")
    
    if st.button("🏁 Завершить звонок"):
        reset_script()
        st.rerun()
