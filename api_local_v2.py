from flask import Flask,render_template,jsonify,request
import psycopg
from decimal import Decimal

district_lookup = {'Beitou':'北投區','Neihu':'內湖區','Datong':'大同區','Zhongshan':'中山區','Shongshan':'松山區','Shihlin':'士林區','Daan':'大安區','Xinyi':'信義區','Nangang':'南港區','Wanhua':'萬華區','Zhongzeng':'中正區','Wenshan':'文山區'}
type_lookup = {'住宅大樓(11層含以上有電梯)':'Apartment(11 stories or more)','公寓(5樓含以下無電梯)':'Walk-Up Apartment','華廈(10層含以下有電梯)':'Apartment(10 stories or less)','透天厝':'House','其他':'Other'}

app = Flask('__name__')
app.config['JSON_AS_ASCII'] = False

@app.route('/get/SaleData/longlat')
def gsll():
    longitude = request.args.get('long')
    latitude = request.args.get('lat')
    if(longitude is None or latitude is None):
        return jsonify("No longitude or latitude given")
    radius = request.args.get('radius')
    if radius is None:
        radius = 500
    park_max_dist = request.args.get('park_dist')
    mrt_max_dist = request.args.get('mrt_dist')
    park_dist_given = not(park_max_dist is None)
    mrt_dist_given = not(mrt_max_dist is None)
    with psycopg.connect("user=postgres password=adbfinals host=adbtest.c9d470mwdvu3.ap-northeast-1.rds.amazonaws.com") as conn:
        with conn.cursor() as cur:
            query = "SELECT (serial_number,area,building_type,built_date,price,longitude,latitude) FROM property_with_criterias WHERE ST_DWithin(ST_Transform(geom,3826),ST_Transform(ST_SetSRID(ST_Point(%s,%s), 4326),3826),%s)"
            params = [longitude,latitude,radius]
            if(park_dist_given):
                query = query + "AND ST_DWithin(ST_Transform(geom,3826),ST_Transform(parks,3826),%s)" 
                params.append(park_max_dist)
            if(mrt_dist_given):
                query = query + "AND ST_DWithin(ST_Transform(geom,3826),ST_Transform(stations,3826),%s)"
                params.append(mrt_max_dist)
            params = tuple(params)
            cur.execute(query,params)
            cur.fetchone()
            out = []
            for record in cur:
                record = record[0]
                tmp = {'Building_id':record[0],'Area':record[1],'Building_type':type_lookup[record[2]],'Built_date':record[3],'price':record[4],'longitude':Decimal(record[5]),'latitude':Decimal(record[6])}
                out.append(tmp)
        conn.commit()
    return jsonify(out)
@app.route('/get/SaleData/district')
def gsd2():
    specific_district = request.args.get('district')
    if(specific_district is None):
        return jsonify("No district given")
    if specific_district in district_lookup:
        specific_district = district_lookup[specific_district]
    park_max_dist = request.args.get('park_dist')
    mrt_max_dist = request.args.get('mrt_dist')
    park_dist_given = not(park_max_dist is None)
    mrt_dist_given = not(mrt_max_dist is None)
    with psycopg.connect("user=postgres password=adbfinals host=adbtest.c9d470mwdvu3.ap-northeast-1.rds.amazonaws.com") as conn:
        with conn.cursor() as cur:
            query = "SELECT (serial_number,area,building_type,built_date,price,longitude,latitude) FROM property_with_criterias WHERE district like %s"
            params = [specific_district]
            if(park_dist_given):
                query = query + "AND ST_DWithin(ST_Transform(geom,3826),ST_Transform(parks,3826),%s)" 
                params.append(park_max_dist)
            if(mrt_dist_given):
                query = query + "AND ST_DWithin(ST_Transform(geom,3826),ST_Transform(stations,3826),%s)"
                params.append(mrt_max_dist)
            params = tuple(params)
            cur.execute(query,params)
            cur.fetchone()
            out = []
            for record in cur:
                record = record[0]
                tmp = {'Building_id':record[0],'Area':record[1],'Building_type':type_lookup[record[2]],'Built_date':record[3],'price':record[4],'longitude':Decimal(record[5]),'latitude':Decimal(record[6])}
                out.append(tmp)
        conn.commit()
    return jsonify(out)
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
    #app.run(debug=True) #can alter host and port number here. Right now the default host is localhost and port is 5000
