import json 
import DBConn

with open('TPark.json') as f:
    datalist = json.load(f)
    out_data = []
    for data in datalist[1:]:
    	tmp_dict = {'name':data['pm_name'],'longitude':data['pm_lon'],'latitude':data['pm_lat'],'address':data['pm_location']}
    	out_data.append(tmp_dict)
    DBConn.put_park(out_data)
