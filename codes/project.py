import psycopg2
import psycopg2.pool
import preprocessing as pre

pool = None


def connect():
    conn = None
    try:
        # testing connection on local databases, will need to try on remote database using ip address
        # for now, use your own postgresql password
        print('Connecting to database..')
        global pool
        pool = psycopg2.pool.SimpleConnectionPool(1, 10, host="localhost",
                                                  database="TPC-H",
                                                  user="postgres",
                                                  password="password")
        conn = pool.getconn()
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        # cur.execute('SELECT datname FROM pg_database')
        # databases = cur.fetchall()
        # print("Databases:", databases)

        return cur

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def show_display():
    cur = pool.getconn().cursor()
    cur.execute('SELECT schema_name FROM information_schema.schemata')
    raw_schemas = cur.fetchall()
    processed_schemas = pre.process_schemas(raw_schemas)


def process_query():
    cur = pool.getconn().cursor()
    sql_query = "SELECT * FROM region, nation"
    cur.execute(cur.mogrify('explain ' + sql_query))
    analyze_fetched = cur.fetchall()
    print(analyze_fetched)


def main():
    connect()
    show_display()
    process_query()


main()
