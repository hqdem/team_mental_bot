FROM python:3.11

WORKDIR app/
COPY ./requirements.txt /Users/iademidov1/projects/python/team_mental_client/requirements.txt
COPY . .

RUN pip install -r requirements.txt
