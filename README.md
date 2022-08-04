# kryton-discord-bot

### Usage

```
usage: 

kryton.py [-h] [--stdout] [--debug] [--config CONFIG] [--syslog-facility SYSLOG_FACILITY]
          [--syslog-identity SYSLOG_IDENTITY] [--syslog-server SYSLOG_SERVER]

optional arguments:
  -h, --help                            show this help message and exit
  --stdout, -s                          Log into STDOUT without using SYSLOG
  --debug, -d                           Enable debugging
  --config CONFIG, -c CONFIG            Config file
  --syslog-facility SYSLOG_FACILITY     Syslog facility
  --syslog-identity SYSLOG_IDENTITY     Syslog identity
  --syslog-server SYSLOG_SERVER         Syslog server/socket
```


```
kryton.py -c config/kryton.yml -s -d
```
