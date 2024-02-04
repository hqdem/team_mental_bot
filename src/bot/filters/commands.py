from aiogram.filters import Filter
from aiogram.types import Message


class IsCustomCommand(Filter):
    def __init__(self, cmd_text: str) -> None:
        self.cmd = cmd_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.cmd
