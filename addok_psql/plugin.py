from addok.config import config
from addok.helpers import import_by_path, iter_pipe
from addok.batch import batch


def preprocess():
    return iter_pipe(None, config.PSQL_PROCESSORS)


def process(args):
    print('Import from Postgresql')
    keys = ['dbname', 'user', 'host', 'port']
    for key in keys:
        value = getattr(args, key, None)
        if value:
            config.PSQL[key.upper()] = value
    if args.limit:
        config.PSQL_LIMIT = args.limit
    batch(preprocess())


def preconfigure(config):
    from . import config as localconfig
    config.extend_from_object(localconfig)


def register_command(subparsers):
    parser = subparsers.add_parser('psql', help='Import from PostgreSQL')
    parser.set_defaults(func=process)
    parser.add_argument('--host', help='PostgreSQL host')
    parser.add_argument('--user', help='PostgreSQL user')
    parser.add_argument('--dbname', help='PostgreSQL name')
    parser.add_argument('--port', help='PostgreSQL port')
    parser.add_argument('--limit', help='Limit retrieved rows')
