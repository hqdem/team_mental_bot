import asyncio
import datetime
import os

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.filters import CommandStart
from mental_api_client.client import TeamMentalClient
from mental_api_client import api_types
from mental_api_client import exceptions

from src.config.config import parse_config
from src.bot.filters.commands import IsCustomCommand
from src.bot.surveys.survey_options import get_readable_list_survey_options


conf = parse_config("configs/config.yaml")

dp = Dispatcher()
bot = Bot(conf.bot_config.token)
api = TeamMentalClient(conf.api_config.base_url)


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    team_name = str(message.chat.id)
    team = api_types.Team(None, team_name)
    try:
        api.create_team(team)
    except exceptions.APIException as ex:
        if ex.code == 'UNIQUE_CONSTRAINT_VIOLATED':
            pass

    await message.reply('Всем привет!'
                        ' Я бот Василий и я помогу вам разобраться с вашим эмоциональным состоянием!'
                        ' Ментальное здоровье команды - одна из важнейших составляющих продуктивной и слаженной работы!'
                        ' Я буду опрашивать вас по поводу вашего самочувствия,'
                        ' после чего вы адекватно сможете распределить нагрузку и сделать выводы,'
                        ' кого на данный период времени лучше не трогать)')


@dp.message(IsCustomCommand('/join'))
async def handle_join(message: types.Message):
    team = api.get_team(str(message.chat.id))
    username = message.from_user.full_name

    user = api_types.User(None, username=username, team_id=team.id)
    try:
        api.create_user(user)
    except exceptions.APIException as ex:
        pass

    api.add_user_to_team(team.id, user.username)

    await message.reply('Вы в команде')


@dp.message(IsCustomCommand('/survey'))
async def handle_create_survey(message: types.Message):
    active_surveys = api.get_active_team_surveys(str(message.chat.id))
    if active_surveys:
        await message.reply('Завершите предыдущий опрос, прежде чем начать новый')
        return

    name, options = get_readable_list_survey_options()
    poll = await message.answer_poll(
        question=name,
        options=options,
        is_anonymous=False,
    )

    team = api.get_team(str(message.chat.id))
    survey = api_types.Survey(None, None, None, team.id, poll.message_id)
    api.create_survey(survey)


@dp.poll_answer()
async def handle_survey_answer(poll_answer: types.PollAnswer):
    user = api.get_user(poll_answer.user.full_name)
    user_answer = poll_answer.option_ids[0] + 1

    team = api.get_team(user.team_id)
    active_surveys = api.get_active_team_surveys(team.name)
    now_survey = active_surveys[0]

    vote_survey = api_types.VoteSurveyPayload(user.id, user_answer)
    api.vote_survey(now_survey.id, vote_survey)


@dp.message(IsCustomCommand('/end'))
async def handle_end_survey(message: types.Message):
    team = api.get_team(str(message.chat.id))
    active_surveys = api.get_active_team_surveys(team.name)
    if not active_surveys:
        await message.reply("У вас нет активных опросов")
        return
    now_survey = active_surveys[0]

    api.end_survey(now_survey.id)
    await bot.stop_poll(message.chat.id, now_survey.telegram_msg_id)
    await message.reply("Опрос успешно завершен")

    results = api.get_survey_results(now_survey.id)
    msg = ''
    for res in results:
        now_user = api.get_user(res.user_id)
        msg += f'{now_user.username} - {res.result}\n'
    await bot.send_message(message.chat.id, f'Результаты опроса:\n{msg}')


# @dp.message(IsCustomCommand('/test'))
# async def handle_test_command(message: types.Message):
#     today = datetime.date.today()
#     first = today.replace(day=1)
#     last_month = first - datetime.timedelta(days=1)
#     last_month.replace(day=1)
#
#     surveys = api.get_surveys_period(api_types.GetSurveyEdges(
#         team_id=1,
#         from_dt=last_month,
#         to_dt=datetime.datetime.now() + datetime.timedelta(days=1),
#     ))
#
#     users_results_and_count = {}
#
#     for survey in surveys:
#         results = api.get_survey_results(survey.id)
#         for res in results:
#             user = api.get_user(res.user_id)
#             if user.username not in users_results_and_count:
#                 users_results_and_count[user.username] = [res.result, 1]
#                 continue
#             users_results_and_count[user.username][0] += res.result
#             users_results_and_count[user.username][1] += 1
#
#     for user, (sum_res, count) in users_results_and_count.items():
#         print(user, round(sum_res / count, 2))


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
