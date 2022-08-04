import logging
import logging.handlers
from os.path import exists


class KrytonLogger:
    syslogDefaultPort = 514

    def __init__(self, args):

        if args.stdout:
            hdlr = logging.StreamHandler()
            hdlr.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(name)-15s[%(process)6d](%(module)17s:%(lineno)-4d) %(levelname)-7s %(message)s",
                    "%Y.%m.%d %H:%M:%S",
                )
            )
        else:
            if exists(args.syslog_server):
                addr = args.syslog_server
            else:
                if ":" in args.syslog_server:
                    server, port = args.syslog_server.split(":")
                else:
                    server = args.syslog_server
                    port = self.syslogDefaultPort
                    addr = (server, int(port))

            # because prior to python 3.3 SysLogHandler lacks attribute "ident",
            # we have to add the ident by this stupid way ;-(
            hdlr = logging.handlers.SysLogHandler(addr, args.syslog_facility)

            hdlr.setFormatter(
                logging.Formatter(
                    args.syslog_identity
                    + "[%(process)6d]: %(name)8s %(levelname)-7s %(message)s"
                )
            )

        if args.debug:
            logging.root.setLevel(logging.DEBUG)
        else:
            logging.root.setLevel(logging.INFO)

        logging.root.addHandler(hdlr)
