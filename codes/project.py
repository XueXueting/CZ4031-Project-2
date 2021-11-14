import psycopg2
import psycopg2.pool
import preprocessing as pre
import annotation as anno
import interface
from configparser import ConfigParser

pool = None


def connect():
    try:
        print('Connecting to database..')
        global pool
        params = config()
        pool = psycopg2.pool.SimpleConnectionPool(**params)

        conn = pool.getconn()
        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        return

    except (Exception, psycopg2.DatabaseError) as error:
        print('Login error:', error)
        print('Please enter valid authentication details in the database.ini file.')


def show_display():
    cur = pool.getconn().cursor()
    cur.execute('SELECT schema_name FROM information_schema.schemata')
    raw_schemas = cur.fetchall()
    processed_schemas = pre.process_schemas(raw_schemas)
    interface.loadInterface(processed_schemas)


def process_query(selected_schema, sql_query):
    schema_option_string = '-c search_path=dbo,' + selected_schema
    global pool
    params = config()
    pool = psycopg2.pool.SimpleConnectionPool(options=schema_option_string, **params)
    cur = pool.getconn().cursor()
    raw_qep = ''
    try:
        cur.execute(cur.mogrify('explain ' + sql_query))
        raw_qep = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Database Error:', error)
        interface.display_message('Invalid query. Please enter a valid query for this schema!')

    if raw_qep != '':
        processed_qep = pre.process_qep(raw_qep)
        annotations = anno.generate_annotations(sql_query, processed_qep)
        interface.create_annotation(annotations)
        pre.create_graphical_qep(raw_qep)
        interface.display_query_success(sql_query)


def close_connection():
    conn = pool.getconn()
    if conn is not None:
        conn.close()
        print('Database connection closed.')


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def set_schema_config(selected_schema):
    parser = ConfigParser()
    schema_option_string = '-c search_path=dbo,' + selected_schema
    parser.set('postgresql', 'options', schema_option_string)
    with open('database.ini', 'wb') as configfile:
        parser.write(configfile)


def run():
    connect()
    if pool is not None:
        show_display()
        close_connection()


if __name__ == '__main__':
    run()

