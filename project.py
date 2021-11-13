import psycopg2
import psycopg2.pool
import preprocessing as pre
import annotation as anno
import interface

pool = None


def connect():
    try:
        # testing connection on local databases, will need to try on remote database using ip address
        # for now, use your own postgresql password
        print('Connecting to database..')
        global pool
        pool = psycopg2.pool.SimpleConnectionPool(1, 10, host="192.168.1.150",
                                                  database="TPC-H",
                                                  user="postgres",
                                                  password="password")
        conn = pool.getconn()
        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        return

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print('Login error:', error)


def show_display():
    cur = pool.getconn().cursor()
    cur.execute('SELECT schema_name FROM information_schema.schemata')
    raw_schemas = cur.fetchall()
    processed_schemas = pre.process_schemas(raw_schemas)
    # interface.loadInterface(processed_schemas)
    interface.loadInterface()



def process_query():
    cur = pool.getconn().cursor()
    sql_query = "SELECT sum(s_acctbal) " \
                "FROM REGION as R, region as re, nation as n, supplier as s " \
                "WHERE " \
                "n.n_nationkey > 10 " \
                "AND n.n_regionkey = r.r_regionkey " \
                "AND s.s_nationkey = n.n_nationkey " \
                "GROUP BY r.r_name " \

    raw_qep = ''
    try:
        cur.execute(cur.mogrify('explain ' + sql_query))
        raw_qep = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Database Error:', error)

    if raw_qep != '':
        processed_qep = pre.process_qep(raw_qep)
        annotations = anno.generate_annotations(sql_query, processed_qep)
        print('Number of annotations:', len(annotations))
        # interface.render_annotations(annotations)

        pre.create_graphical_qep(raw_qep)
        # interface.render_graphical_qep()


def close_connection():
    conn = pool.getconn()
    if conn is not None:
        conn.close()
        print('Database connection closed.')


def main():
    #temp put it here so it can show without connect
    interface.loadInterface()
    connect()
    if pool is not None:
        show_display()
        process_query()
        close_connection()
        # interface.loadInterface()


main()
