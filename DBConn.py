import psycopg

def put_addr(datalist):
	# Connect to an existing database
	with psycopg.connect("user=postgres password=adbfinals host=adbtest.c9d470mwdvu3.ap-northeast-1.rds.amazonaws.com") as conn:

	    # Open a cursor to perform database operations
	    with conn.cursor() as cur:

	        # Pass data to fill a query placeholders and let Psycopg perform
	        # the correct conversion (no SQL injections!)
	        for data in datalist:
	        	cur.execute('INSERT INTO "property_data" (serial_number, longitude, latitude, district, area, transaction_date, building_type, built_date, price, property_type, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(data['serial'],data['longitude'],data['latitude'],data['district'],data['area'],data['trade_date'],data['btype'],data['built_date'],data['price'],data['ptype'],data['address']))

	        # Make the changes to the database persistent
	        conn.commit()
def put_park(datalist):
	with psycopg.connect("user=postgres password=adbfinals host=adbtest.c9d470mwdvu3.ap-northeast-1.rds.amazonaws.com") as conn:
	    with conn.cursor() as cur:
	    	for data in datalist:
	    		cur.execute('INSERT INTO "park_data" (name,longitude,latitude,address) VALUES (%s,%s,%s,%s)',(data['name'],data['longitude'],data['latitude'],data['address']))
	    	conn.commit()