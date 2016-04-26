from addok import config
from addok.helpers import import_by_path, iter_pipe
from addok.batch import batch


def preprocess():
    # Do not import at load time, because we don't want to have a hard
    # dependency to psycopg2.
    PSQL_PROCESSORS = [import_by_path(path) for path in config.PSQL_PROCESSORS]
    return iter_pipe(None, PSQL_PROCESSORS)


def process(args):
    print('Import from Postgresql')
    keys = ['dbname', 'dbuser', 'dbhost', 'dbport']
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
    parser.add_argument('--dbhost', help='PostgreSQL host')
    parser.add_argument('--dbuser', help='PostgreSQL user')
    parser.add_argument('--dbname', help='PostgreSQL name')
    parser.add_argument('--dbport', help='PostgreSQL port')
    parser.add_argument('--limit', help='Limit retrieved rows')
