# -*- coding: future_fstrings -*-

import datetime

import aiogram.exceptions

from src.config.config import parse_config
from src.bot.surveys.survey_options import get_readable_list_survey_options

from celery import Celery
from celery.schedules import crontab
from asgiref.sync import async_to_sync
from aiogram import Bot
from mental_api_client.client import TeamMentalClient
from mental_api_client import api_types

app = Celery("tasks", broker="redis://redis:6379")


@app.task
def process_team_surveys():
    async_to_sync(process_team_task)()


@app.task
def process_team_monthly_results():
    async_to_sync(send_monthly_results)()


async def process_team_task():
    conf = parse_config("/app/configs/config.yaml")
    bot = Bot(conf.bot_config.token)
    api = TeamMentalClient(conf.api_config.base_url)
    teams = api.list_teams()

    for team in teams:
        surveys = api.get_active_team_surveys(team.name)
        if surveys:
            now_survey = surveys[0]
            if (datetime.datetime.now() - now_survey.start_date).days >= 3:
                await end_survey(api, bot, now_survey, team)
                await start_survey(api, bot, team)
            continue
        await start_survey(api, bot, team)


async def end_survey(api, bot, survey, team):
    api.end_survey(survey.id)
    await bot.stop_poll(
        chat_id=team.name,
        message_id=survey.telegram_msg_id,
    )
    await bot.send_message(
        chat_id=team.name,
        text='Опрос успешно завершен',
        reply_to_message_id=survey.telegram_msg_id
    )
    results = api.get_survey_results(survey.id)
    msg = ''
    for res in results:
        now_user = api.get_user(res.user_id)
        msg += f'{now_user.username} - {res.result}\n'
    await bot.send_message(
        chat_id=team.name,
        text=f'Результаты опроса:\n{msg}'
    )


async def start_survey(api, bot, team):
    name, options = get_readable_list_survey_options()
    msg = await bot.send_poll(
        chat_id=team.name,
        question=name,
        options=options,
        is_anonymous=False,
    )
    survey = api_types.Survey(None, None, None, team.id, msg.message_id)
    api.create_survey(survey)


async def send_monthly_results():
    conf = parse_config("/app/configs/config.yaml")
    bot = Bot(conf.bot_config.token)
    api = TeamMentalClient(conf.api_config.base_url)

    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    last_month.replace(day=1)

    teams = api.list_teams()
    for team in teams:

        surveys = api.get_surveys_period(api_types.GetSurveyEdges(
            team_id=team.id,
            from_dt=last_month,
            to_dt=datetime.datetime.now() + + datetime.timedelta(days=1),
        ))

        users_results_and_count = {}

        for survey in surveys:
            results = api.get_survey_results(survey.id)
            for res in results:
                user = api.get_user(res.user_id)
                if user.username not in users_results_and_count:
                    users_results_and_count[user.username] = [res.result, 1]
                    continue
                users_results_and_count[user.username][0] += res.result
                users_results_and_count[user.username][1] += 1

        msg = 'Результаты команды за месяц:\n'
        for user, (sum_res, count) in users_results_and_count.items():
            msg += f'{user} - {round(sum_res / count, 2)}\n'
        await bot.send_message(
            chat_id=team.name,
            text=msg
        )


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        5.0,
        process_team_surveys.s(),
        name="test_task"
    )
    sender.add_periodic_task(
        2629746,  # 1 month
        process_team_monthly_results.s(),
        name="monthly_results"
    )
