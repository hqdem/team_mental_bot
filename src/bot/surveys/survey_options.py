import random

surveys_variations = [
    {
        'name': 'Хей приятель! Как ты? Все в порядке?',
        0: 'Не выдерживаю 🤖',
        1: 'Бывало и лучше 😐',
        2: 'Все отлично 🤩'
    },
    {
        'name': 'Хей приятель! Как ты?',
        0: 'Откровенно не очень 😤',
        1: 'Не бомба, но и не кайф 🤨',
        2: 'У меня все замечательно 🤩'
    },
    {
        'name': 'Здравствуй! Предлагаю поговорить на чистоту… Каков текущий градус напряжения?',
        0: 'У меня горит 🥵',
        1: 'Потихоньку справляюсь 😌',
        2: 'Никакого напряга 🥳'
    },
    {
        'name': 'Это снова я! Угадай что? Правильно, настало время опроса) Как ты себя чувствуешь?',
        0: 'Я совсем устал 😟',
        1: 'Не прям кайф 🧐',
        2: 'Сил море 😄'
    },
    {
        'name': 'Хей! Как прошел твой день? Справляешься с задачами?',
        0: 'Это просто невозможно 📛',
        1: 'Тяжело, но стараюсь 🤨',
        2: 'Заряжен на все 💯'
    },
    {
        'name': 'Привет-привет! Давно тебе не писал. Рассказывай, как ты. Чего с последнего опроса было больше: приятного или негативного?',
        0: 'Жизнь боль 🥴',
        1: '50/50 🤐',
        2: 'Сейчас на позитиве ✅'
    },
    {
        'name': 'Удивлен? Это снова я! Как, по-твоему: твое самочувствие было хорошим? На сколько баллов по 5-балльной шкале ты его оцениваешь?',
        0: 'Шкала ушла в ➖',
        1: 'Ну на троечку 🥱',
        2: '10 😸'
    },
    {
        'name': 'Тук-тук. Кто там? Да-да, время узнать про твое самочувствие. Как ты??',
        0: 'Не выдерживаю 🤖',
        1: 'Ну так 😵‍💫',
        2: 'Я полон сил ⚡️'
    },
    {
        'name': 'Привет! Сегодня день опроса. Давай обсудим, как твое состояние?',
        0: 'Я очень истощен(а) 😿',
        1: 'Честно, не очень 😾',
        2: 'Потрясающее 😸'
    },
    {
        'name': 'Хеей! Настал день чекапа! Расскажи, что-нибудь порадовало тебя с момента последнего опроса, что улучшило твое состояние?',
        0: 'Ничего, все 👎',
        1: 'Не совсем все гуд 😕',
        2: 'Да, все супер 🤪'
    },
    {
        'name': 'Рад тебе написать! Сейчас нам предстоит поговорить о твоем самочувствии. Поделись, как твоя энергия сегодня?',
        0: 'Из энергии только энергетики 🪫',
        1: 'Могло быть и лучше 🤨',
        2: 'Я полон(на) сил 🔋'
    },
    {
        'name': ' Салют! Пришло время узнать о твоем ментальном состоянии. Сегодняшний день не принес проблем?',
        0: 'Мне очень тяжело 🫥',
        1: 'Было много сложностей 🗿',
        2: 'Все великолепно 💎'
    },
    {
        'name': 'Приветствую! Поговорим о том, как ты себя чувствуешь? Ты удовлетворен своим самочувствием?',
        0: 'Не справляюсь 🧟',
        1: 'Вполне нормально 🥸',
        2: 'Все офигенно 🤩'
    },
    {
        'name': 'Это снова я! Предлагаю провести чекап: расскажи, все получается, как ты хочешь?',
        0: 'Я вымотался(лась) 🥴',
        1: 'Ну как сказать.. 🙂',
        2: 'Все идет как по маслу 🤗'
    },
    {
        'name': 'Привет, друг! Самое время провести опрос о твоем самочувствии. Ты испытываешь необходимость в поддержке?',
        0: 'Я не вывожу 🤯',
        1: 'Отдых не помешал бы 🤌',
        2: 'Все чудесно 😃'
    },
]


def get_readable_list_survey_options():
    option_to_readable_survey = random.choice(surveys_variations)
    return option_to_readable_survey['name'], [option_to_readable_survey[i] for i in range(3)]
