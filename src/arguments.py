import argparse


class KrytonArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.error = self.argsError
        self.parser.add_argument(
            "--stdout",
            "-s",
            action="store_true",
            help="Log into STDOUT without using SYSLOG",
        )
        self.parser.add_argument(
            "--debug", "-d", action="store_true", help="Enable debugging"
        )
        self.parser.add_argument("--config", "-c", help="Config file")
        self.parser.add_argument(
            "--syslog-facility", default="local4", help="Syslog facility"
        )
        self.parser.add_argument(
            "--syslog-identity", default="mirror", help="Syslog identity"
        )
        self.parser.add_argument(
            "--syslog-server", default="/dev/log", help="Syslog server/socket"
        )

    def parse_args(self):
        return self.parser.parse_args()

    def argsError(error):
        pass
