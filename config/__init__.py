from .basic import *
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--env', help= f'environment of the server', default=ENV_DEBUG, choices=ENV_ALL)
parser.add_argument('--host', type=str, default=None, help='host of the server')
parser.add_argument('--port', type=int, default=None, help='port of the server')

parser.add_argument('--loglevel', '-ll', type=str, default=LOG_LEVEL_INFO, help='log level of the server', choices=[LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR])
parser.add_argument('--logpath', '-lp', type=str, default=LOG_FILE_PATH, help='log path of the server')
parser.add_argument('--logexpiration', '-le', type=int, default=LOG_EXPIRATION, help='log expiration (days) of the server')

parser.add_argument('--dbtype', '-dbt', type=str, default=DB_TYPE_SQLITE, help='database type of the server', choices=[DB_TYPE_SQLITE, DB_TYPE_POSTGRESQL])
parser.add_argument('--dbhost', '-dbh', type=str, default=DB_HOST, help='database host of the server')
parser.add_argument('--dbport', '-dbp', type=int, default=DB_PORT, help='database port of the server')
parser.add_argument('--dbuser', '-dbu', type=str, default=DB_USER, help='database user of the server')
parser.add_argument('--dbpassword', '-dbpw', type=str, default=DB_PASSWORD, help='database password of the server')
parser.add_argument('--dbdatabase', '-dbd', type=str, default=DB_DATABASE, help='database name of the server')
parser.add_argument('--dbpath', '-dbpa', type=str, default=DB_PATH, help='database path of the server (sqlite)')

args = parser.parse_known_args()[0]
if args.env == ENV_DEBUG:
    from .debug import *
elif args.env == ENV_PROD:
    from .prod import *
else:
    raise Exception(f"unknown environment {args.env}")

if args.host:
    HOST = args.host

if args.port:
    PORT = args.port

if args.loglevel:
    LOG_LEVEL = args.loglevel

if args.logpath:
    LOG_FILE_PATH = args.logpath

if args.logexpiration:
    LOG_EXPIRATION = args.logexpiration

if args.dbtype:
    DB_TYPE = args.dbtype

if args.dbhost:
    DB_HOST = args.dbhost

if args.dbport:
    DB_PORT = args.dbport

if args.dbuser:
    DB_USER = args.dbuser

if args.dbpassword:
    DB_PASSWORD = args.dbpassword

if args.dbdatabase:
    DB_DATABASE = args.dbdatabase

if args.dbpath:
    DB_PATH = args.dbpath
