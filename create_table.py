import sqlite3

def create_connection(db_file):
	""" 
	create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

	return None


def create_table(conn, create_table_sql):
	""" create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)


def main():
	database = 'pythonsqlite.db'

	sql_create_user_table = """
	CREATE TABLE IF NOT EXISTS User (
	username 	text PRIMARY KEY,
	email 		text
	);
	"""

	# create a database connection
	conn = create_connection(database)
	if conn is not None:
		# create user table
		create_table(conn, sql_create_user_table)
	else:
		print("Error! Cannot create table");


if __name__ == '__main__':
	main()