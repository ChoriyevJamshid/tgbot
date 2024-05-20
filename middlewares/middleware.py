from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject


class SessionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.session = dict()
        self.bot: Bot = bot

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['session'] = self.session
        data['bot'] = self.bot
        return await handler(event, data)
