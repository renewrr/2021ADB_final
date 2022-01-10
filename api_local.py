from flask import Flask,render_template,jsonify,request
import psycopg
from decimal import Decimal

district_lookup = {'Beitou':'北投區','Neihu':'內湖區','Datong':'大同區','Zhongshan':'中山區','Shongshan':'松山區','Shihlin':'士林區','Daan':'大安區','Xinyi':'信義區','Nangang':'南港區','Wanhua':'萬華區','Zhongzeng':'中正區','Wenshan':'文山區'}
type_lookup = {'住宅大樓(11層含以上有電梯)':'Apartment(11 stories or more)','公寓(5樓含以下無電梯)':'Walk-Up Apartment','華廈(10層含以下有電梯)':'Apartment(10 stories or less)','透天厝':'House','其他':'Other'}

app = Flask('__name__')
app.config['JSON_AS_ASCII'] = False

@app.route('/getSaleData')
def gsd():
    specific_district = request.args.get('district')
    park_max_dist = request.args.get('park_dist')
    park_list = request.args.get('park_list')
    mrt_max_dist = request.args.get('mrt_dist')
    station_list = request.args.get('station_list')
    if park_max_dist is None:
        park_max_dist = 300
    if mrt_max_dist is None:
        mrt_max_dist = 300
    if specific_district is None:
        specific_district = "__區"
    else:
        if specific_district in district_lookup:
            specific_district = district_lookup[specific_district]
    print(specific_district)
    with psycopg.connect("user=postgres password=adbfinals host=adbtest.c9d470mwdvu3.ap-northeast-1.rds.amazonaws.com") as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            cur.execute("SELECT (serial_number,area,building_type,built_date,price,longitude,latitude) FROM property_data JOIN (SELECT ST_Union(geom) as stations FROM public.mrt_data) as s_data ON True JOIN (SELECT ST_Union(geom) as parks FROM public.park_data) as p_data ON True WHERE ST_DWithin(ST_Transform(geom,3826),ST_Transform(stations,3826),%s) AND ST_DWithin(ST_Transform(geom,3826),ST_Transform(parks,3826),%s) AND district like %s",(mrt_max_dist,park_max_dist,specific_district))
            #cur.execute("SELECT * FROM property_data;")
            cur.fetchone()
            out = []
            for record in cur:
                record = record[0]
                tmp = {'Building_id':record[0],'Area':record[1],'Building_type':type_lookup[record[2]],'Built_date':record[3],'price':record[4],'longitude':Decimal(record[5]),'latitude':Decimal(record[6])}
                out.append(tmp)
        conn.commit()
    return jsonify(out)
@app.route('/getLongLatSaleData')
def gllsd():
    longitude = request.args.get('long')
    latitude = request.args.get('lat')
    radius = request.args.get('radius')
    if radius is None:
        radius = 200
    radius = float(radius)
    if longitude is None or latitude is None:
        return jsonify([])
    with psycopg.connect("user=postgres password=adbfinals host=adbtest.c9d470mwdvu3.ap-northeast-1.rds.amazonaws.com") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT (serial_number,area,building_type,built_date,price,longitude,latitude,ST_Distance((ST_Transform(geom,3826)),ST_Transform(ST_SetSRID(ST_Point(%s,%s), 4326),3826))) FROM property_data WHERE ST_Distance((ST_Transform(geom,3826)),ST_Transform(ST_SetSRID(ST_Point(%s,%s), 4326),3826)) <= %s",(longitude,latitude,longitude,latitude,radius))
            print(cur._query.query)
            cur.fetchone()
            out = []
            for record in cur:
                record = record[0]
                tmp = {'Building_id':record[0],'Area':record[1],'Building_type':type_lookup[record[2]],'Built_date':record[3],'price':record[4],'longitude':Decimal(record[5]),'latitude':Decimal(record[6]),'distance':record[7]}
                out.append(tmp)
        conn.commit()
    return jsonify(out)
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
    #app.run(debug=True) #can alter host and port number here. Right now the default host is localhost and port is 5000
