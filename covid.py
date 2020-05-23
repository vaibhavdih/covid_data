import json
import requests
import datetime
import xlsxwriter


a=requests.get("https://api.covid19india.org/districts_daily.json")
json_data = json.loads(a.text)

start_date='2020-04-20'

count=0
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet=workbook.add_worksheet()


today_date = datetime.date.today()





def get_place(start_date,ob_date,count):
	a_=start_date.split("-")
	day_=int(a_[2])
	month_ = int(a_[1])
	year_ = int(a_[0])
	a=ob_date.split("-")
	day=int(a[2])
	month = int(a[1])
	year = int(a[0])
	
	date_ = datetime.date(year_,month_,day_)
	new_date = datetime.date(year,month,day)
	difference = ((new_date-date_).days)*4
	column = difference+3
	row = count+2
	#print(row,column)

	return row,column


	
def set_header(start_date,today_date):
	worksheet.write(0,0, "SI No")
	worksheet.write(0,1, "District")
	worksheet.write(0,2, "State")

	a_=start_date.split("-")
	day_=int(a_[2])
	month_ = int(a_[1])
	year_ = int(a_[0])
	
	date_ = datetime.date(year_,month_,day_)
	
	difference = ((today_date-date_).days)
	count_=0
	for single_date in (date_ + datetime.timedelta(n) for n in range(difference+1)):
		worksheet.write(0,count_+3,str(single_date))
		worksheet.write(0,count_+4,str(single_date))
		worksheet.write(0,count_+5,str(single_date))
		worksheet.write(0,count_+6,str(single_date))
		worksheet.write(1,count_+3,'Confirmed')
		worksheet.write(1,count_+4,'Active')
		worksheet.write(1,count_+5,'Recovered')
		worksheet.write(1,count_+6,'Deceased')
		print(single_date)
		count_=count_+4



set_header(start_date,today_date)




for state,state_data in json_data['districtsDaily'].items():
	for district, district_data in state_data.items():
		
		worksheet.write(count+2,0,count+1)
		worksheet.write(count+2,1,district)
		worksheet.write(count+2,2,state)

		for data in district_data:
			active=data['active']
			confirmed = data['confirmed']
			deceased = data['deceased']
			recovered = data['recovered']
			date = data['date']
			row,column = get_place(start_date,date,count)
			worksheet.write(row,column,confirmed)
			worksheet.write(row,column+1,active)
			worksheet.write(row,column+2,recovered)
			worksheet.write(row,column+3,deceased)

			#print(state,district, active, confirmed, deceased, recovered, date)

		count=count+1


workbook.close()







