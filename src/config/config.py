import yaml


class BotConfig:
    def __init__(self, token: str):
        self.token = token


class APIConfig:
    def __init__(self, base_url: str):
        self.base_url = base_url


class Config:
    def __init__(self, bot_config: BotConfig, api_config: APIConfig):
        self.bot_config = bot_config
        self.api_config = api_config


def parse_config(path: str) -> Config:
    with open(path) as f:
        conf_dict = yaml.safe_load(f)
    bot_conf = BotConfig(conf_dict['bot']['token'])
    api_conf = APIConfig(conf_dict['api']['base-url'])
    return Config(bot_conf, api_conf)
