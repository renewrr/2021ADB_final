import csv

district_lookup = {'Beitou':'北投區','Neihu':'內湖區','Datong':'大同區','Zhongshan':'中山區','Shongshan':'松山區','Shihlin':'士林區','Daan':'大安區','Xinyi':'信義區','Nangang':'南港區','Wanhua':'萬華區','Zhongzeng':'中正區','Wenshan':'文山區'}
type_lookup = {'住宅大樓(11層含以上有電梯)':'Apartment(11 stories or more)','公寓(5樓含以下無電梯)':'Walk-Up Apartment','華廈(10層含以下有電梯)':'Apartment(10 stories or less)','透天厝':'House','其他':'Other'}
prop_lookup = {'房地(土地+建物)':'property','車位':'parking space','房地(土地+建物)+車位':'property and parking space'}

reverse_dist = {}
for key in district_lookup:
	reverse_dist[district_lookup[key]] = key

with open('DBExport.csv', newline='',encoding="Big5") as csvfile:
	with open('DBExport_t.csv','w', newline='') as csvfile_out:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		spamwriter = csv.writer(csvfile_out, delimiter=',', quotechar='|')
		spamwriter.writerow(next(spamreader))
		for row in spamreader:
			row[3] = reverse_dist[row[3]]
			row[6] = type_lookup[row[6]]
			row[10] = prop_lookup[row[10]]
			spamwriter.writerow(row)