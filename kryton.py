"""
 *
 * KRYTON - discord bot
 * 
 * Petr Vavrin (peterbay)   pvavrin@gmail.com
 *                          https://github.com/peterbay
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
"""

import sys
import yaml
import logging
import discord
from os.path import abspath


from src.modules import KrytonModules
from src.discord import KrytonDiscord
from src.file_handler import KrytonFileObserver
from src.arguments import KrytonArguments
from src.logger import KrytonLogger


class Kryton:
    arguments = None
    logger = None
    modules = None
    observer = None
    intents = None
    client = None
    config = None

    def __init__(self):
        arguments = KrytonArguments()
        self.arguments = arguments.parse_args()
        self.logger = KrytonLogger(self.arguments)

        if not self.arguments.config:
            self.exit(1, "Missing config file argument")

        self.load_config()

        self.modules = KrytonModules(abspath("./modules"))
        self.observer = KrytonFileObserver(".", self.file_change)
        self.intents = discord.Intents.default()
        self.client = KrytonDiscord(intents=self.intents)

        self.client.kryton_register_callback(on_message=self.on_message)
        self.client.kryton_register_callback(on_typing=self.on_typing)
        self.client.kryton_register_callback(on_ready=self.on_ready)
        self.client.kryton_register_callback(on_error=self.on_error)

    def load_config(self):
        try:
            with open(self.arguments.config) as configFile:
                self.config = yaml.full_load(configFile)

        except Exception as e:
            self.exit(1, f"Error in config file: {e}")

    def file_change(self, event):
        # module reloading
        self.modules.reload(event.src_path)

        # config reloading
        if abspath(self.arguments.config) == abspath(event.src_path):
            self.load_config()

    def exit(self, status, message):
        if self.observer:
            self.observer.stop()

        if not status:
            if message:
                logging.info(message)

            sys.exit(0)

        else:
            if message:
                logging.error(message)

            sys.exit(1)

    def run(self):
        discord = self.config.get("discord", None)
        if not discord:
            self.exit(1, "Missing key 'discord' in config file")
            return

        token = discord.get("token", None)
        if not token:
            self.exit(1, "Missing key 'discord.token' in config file")
            return

        self.client.run(token)

    async def on_message(self, client, msg):
        if msg.author == client.user:
            return

        try:
            executed_module = await self.modules.match_module(client, msg)

        except Exception as e:
            logging.error(e)

        if not executed_module:
            pass

    async def on_typing(self, client, channel, user, when):
        pass
        # print(client.user, channel, user, when)

    async def on_ready(self, client):
        logging.info("Discord client READY")

    async def on_error(self, client, event_method, *args, **kwargs):
        pass
        # print("error", event_method)


def main(argv):
    krtn = Kryton()
    krtn.run()


if __name__ == "__main__":
    main(sys.argv)
