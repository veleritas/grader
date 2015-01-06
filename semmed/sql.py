import mysql.connector

def make_query(cursor, query):
	print "Making this query:", query
	cursor.execute(query)
	return cursor

def work(cnx):
	cursor = cnx.cursor()

	query = ("SELECT COUNT(*) FROM PREDICATION;")
	result = make_query(cursor, query)

	for row in result:
		for column in row:
			print column





def work2(cnx):
	query = ("SHOW TABLES;")
	cursor = cnx.cursor()
	cursor.execute(query)

	tables = []
	for res in cursor:
		print res[0]
		tables.append(res[0])



	for table in tables:
		print "----------------------"
		print table
		print "----------------------"
		query = ("SELECT COUNT(*) FROM %s;") % (table)
		cursor.execute(query)
#		query = ("SELECT * FROM %s LIMIT 5;") % (table)
		#query = ("SELECT COUNT(*) FROM " + table + ";")
#		cursor.execute(query, table)

		for res in cursor:
			print res


	cursor.close()

def prepare():
	cnx = mysql.connector.connect(user="toby", password="veritas",
		host="137.131.88.33", database="semmeddb")

	if cnx.is_connected():
		print "working fine!"
		work(cnx)

	cnx.close()

def main():
	prepare()

if __name__ == "__main__":
	main()
