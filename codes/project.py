import psycopg2


def connect():
    conn = None
    try:
        # testing connection on local databases, will need to try on remote database using ip address
        # for now, use your own postgresql password
        print('Connecting to database..')
        conn = psycopg2.connect(host="localhost",
                                database="TPC-H",
                                user="postgres",
                                password="password")
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        sql_query = "SELECT * FROM region"
        cur.execute(cur.mogrify('explain analyze ' + sql_query))
        analyze_fetched = cur.fetchall()
        print(analyze_fetched)

        cur.execute('SELECT datname FROM pg_database')
        databases = cur.fetchall()
        print("Databases:", databases)

        cur.execute('SELECT schema_name FROM information_schema.schemata')
        schemas = cur.fetchall()
        print("Schemas:", schemas)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


connect()
