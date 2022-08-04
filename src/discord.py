import discord
import logging
from functools import wraps


class KrytonDiscord(discord.Client):
    __kryton_callbacks = {}

    def kryton_init_callbacks(self):
        if not self.__kryton_callbacks:
            self.__kryton_callbacks = {}

    def kryton_register_callback(self, **kwargs):
        self.kryton_init_callbacks()

        for key, value in kwargs.items():
            if callable(value):
                self.__kryton_callbacks[key] = value

    async def __kryton_callback_execute(self, method, *args, **kwargs):
        if method in self.__kryton_callbacks:
            logging.debug(f"Execute discord callback: {method}")
            await self.__kryton_callbacks[method](discord.Client, *args, **kwargs)

    async def on_ready(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_ready", *args, **kwargs)

    async def on_connect(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_connect", *args, **kwargs)

    async def on_disconnect(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_disconnect", *args, **kwargs)

    async def on_resumed(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_resumed", *args, **kwargs)

    async def on_error(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_error", *args, **kwargs)

    async def on_typing(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_typing", *args, **kwargs)

    async def on_message(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_message", *args, **kwargs)

    async def on_message_delete(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_message_delete", *args, **kwargs)

    async def on_bulk_message_delete(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_bulk_message_delete", *args, **kwargs)

    async def on_message_edit(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_message_edit", *args, **kwargs)

    async def on_reaction_add(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_reaction_add", *args, **kwargs)

    async def on_reaction_remove(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_reaction_remove", *args, **kwargs)

    async def on_reaction_clear(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_reaction_clear", *args, **kwargs)

    async def on_raw_reaction_clear(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_raw_reaction_clear", *args, **kwargs)

    async def on_reaction_clear_emoji(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_reaction_clear_emoji", *args, **kwargs)

    async def on_member_join(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_member_join", *args, **kwargs)

    async def on_member_remove(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_member_remove", *args, **kwargs)

    async def on_member_update(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_member_update", *args, **kwargs)

    async def on_user_update(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_user_update", *args, **kwargs)

    async def on_member_ban(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_member_ban", *args, **kwargs)

    async def on_member_unban(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_member_unban", *args, **kwargs)

    async def on_invite_create(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_invite_create", *args, **kwargs)

    async def on_invite_delete(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_invite_delete", *args, **kwargs)

    async def on_group_join(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_group_join", *args, **kwargs)

    async def on_group_remove(self, *args, **kwargs):
        await self.__kryton_callback_execute("on_group_remove", *args, **kwargs)
