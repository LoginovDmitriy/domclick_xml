# -*- coding: utf-8 -*-
import xml.etree.ElementTree as xml
from xml.dom import minidom
import datetime
import pymysql.cursors  
import os

def createXML(filename):
	"""
	Создаем соединение с базой данных и объявляем переменные
	"""
	connection = pymysql.connect(host='mysql.9967724406.myjino.ru',
							user='047077889_eci',
							password='*******',
							db='9967724406_eci',
							charset='utf8mb4',
							cursorclass=pymysql.cursors.DictCursor)
	print ("connect successful!!")
	
	connection2 = pymysql.connect(host='mysql.9967724406.myjino.ru',
							user='047077889_lds',
							password='******',
							db='9967724406_lds',
							charset='utf8mb4',
							cursorclass=pymysql.cursors.DictCursor)
	print ("connect successful!!")

	with connection.cursor() as cursor:
		sql = "SELECT * FROM flats WHERE deadline LIKE 'Дом сдан' OR deadline LIKE 'Заселен' OR deadline LIKE 'Собств-ть'" #jk='GreenЛандия-2'
		cursor.execute(sql)
		c = cursor.fetchall()

	with connection2.cursor() as cursor1:
		sql1 = "SELECT * FROM newbuildings"	
		# sql1 = "SELECT * FROM newbuildings WHERE JK LIKE " + "'%" + jk + "%'" + " AND OCH LIKE '" + och + "'" 
		cursor1.execute(sql1)
		c1 = cursor1.fetchall()

	creation_date = datetime.datetime.now().isoformat()
	root = xml.Element('realty-feed', attrib={'xmlns':"http://webmaster.yandex.ru/schemas/feed/realty/2010-06"})
	date = xml.SubElement(root, "generation-date")
	date.text = creation_date

	for i in range(len(c)):

		jk = c[i]['jk'].strip()
		print(c[i]['ids'], jk.strip())
		try:
			och = int(c[i]['och'])
			# print(och)
		except:
			och = 1
		address = []
		# print(jk)
		city = 'Санкт-Петербург'
		for a in range(len(c1)):
			jk1 = c1[a]['JK']
			# print(jk1)
			adr = c1[a]['ADDRESS']
			if jk in jk1:
				# print(jk, 'ЖК найден в каталоге')
				address.append(adr)
				# print(address)
		# try:
		obl = 0
		# print(address)
		try:
			# print(address)
			address = address[(och-1)]
		except:
			address = address[0]
		if 'Санкт-Петербург' in address:
			city = 'Санкт-Петербург'
			address = address.split(', ')
			# print(address)
			address = address[-2] +', '+ address[-1]

			# print(address)			
		else:
			obl = 1
			address = address.split(', ')
			region = address[1]
			address = address[-2] + address[-1]
			# print(address)

		# except:
		# 	# pass
		# 	# address = 'Нет адреса'
		# 	print(jk, '- не найден')


		ids = c[i]['ids']
		# adress = c[i]['street'] + ' ' + c[i]['house']
		flat_type = c[i]['room']
		area = str(c[i]['area'])
		floor = str(c[i]['floor'])
		t_floor = str(c[i]['t_floor'])
		price = str(c[i]['price'])
		creation_date = datetime.datetime.now().isoformat()
		
		living_space = str(round(float(c[i]['area']) * 0.5))
		if flat_type == '1 к' or flat_type == '2Е':
			rooms = '1'
		elif flat_type == '2 к' or flat_type == '3Е':
			rooms = '2'
		elif flat_type == '3 к' or flat_type == '4Е':
			rooms = '3'		
		elif flat_type == '4 к':
			rooms = '4'
		else:
			rooms = None
		if flat_type != 'Ст.':
			room_d = flat_type + '-комнатная квартира.'
		else:
			room_d = 'квартира-студия'
		description = 'Id - ' + ids +  '. Вашему вниманию представлена ' + room_d + ' Объект расопложен в ЖК ' + jk + '. Дом полностью потроен и сдан. Собсвтенность еще не получена. Квартира расположена на ' + floor + ' этаже ' + t_floor + ' этажного дома. Отделка - ' + c[i]['decor'] + '. Подробную информацию можно получить по телефону.'
		
		new_object = xml.Element("offer", attrib={'internal-id': (str(11) + str(ids))})

		new_object_type = xml.SubElement(new_object, 'type')
		new_object_type.text = 'продажа'

		new_object_property_type = xml.SubElement(new_object, 'property-type')
		new_object_property_type.text = 'жилая'

		new_object_category = xml.SubElement(new_object, 'category')
		new_object_category.text = 'квартира'

		new_object_creation_date = xml.SubElement(new_object, 'creation-date')
		new_object_creation_date.text = creation_date

		new_object_location = xml.SubElement(new_object, 'location')
		new_object_location_country = xml.SubElement(new_object_location, 'country')
		new_object_location_country.text = 'Россия'

		if obl == 1:
			new_object_location_region = xml.SubElement(new_object_location, 'region')
			new_object_location_region.text = 'Ленинградская область'

			new_object_location_district = xml.SubElement(new_object_location, 'district')
			new_object_location_district.text = region		


		new_object_location_locality_name = xml.SubElement(new_object_location, 'locality-name')
		new_object_location_locality_name.text = city
		new_object_location_adress = xml.SubElement(new_object_location, 'address')
		new_object_location_adress.text = address
		# print(address)


		new_object_sales_agent = xml.SubElement(new_object, 'sales-agent')
		new_object_sales_agent_name = xml.SubElement(new_object_sales_agent, 'name')
		new_object_sales_agent_name.text = 'Менеджер отдела продаж'
		new_object_sales_agent_phone = xml.SubElement(new_object_sales_agent, 'phone')
		new_object_sales_agent_phone.text = '+79959111639'	
		new_object_sales_agent_category = xml.SubElement(new_object_sales_agent, 'category')
		new_object_sales_agent_category.text = 'агентство'


		new_object_price = xml.SubElement(new_object, 'price')
		new_object_price_value = xml.SubElement(new_object_price, 'value')
		new_object_price_value.text = price
		new_object_price_currency = xml.SubElement(new_object_price, 'currency')
		new_object_price_currency.text = 'RUR'


		new_object_mortgage = xml.SubElement(new_object, 'mortgage')
		new_object_mortgage.text = 'да'

		new_object_deal_status = xml.SubElement(new_object, 'deal-status')
		new_object_deal_status.text = 'прямая продажа'	


		new_object_area = xml.SubElement(new_object, 'area')
		new_object_area_value = xml.SubElement(new_object_area, 'value')
		new_object_area_value.text = area
		new_object_area_unit = xml.SubElement(new_object_area, 'unit')
		new_object_area_unit.text = 'кв.м.'	
		
		new_object_living_space = xml.SubElement(new_object, 'living-space')
		new_object_living_space_value = xml.SubElement(new_object_living_space, 'value')
		new_object_living_space_value.text = living_space
		new_object_livind_space_unit = xml.SubElement(new_object_living_space, 'unit')
		new_object_livind_space_unit.text = 'кв.м.'	


		l = os.listdir('C:\\Python37\\ECN\\'+str(ids)+'\\')
		number = len(l)
		for i in range(number-1):
			new_object_image = xml.SubElement(new_object, 'image')
			r = 'http://9967724406.myjino.ru/ECI/'+str(ids)+'/'+str(i+1)+'.jpg'
			new_object_image.text = r


		new_object_renovation = xml.SubElement(new_object, 'renovation')
		new_object_renovation.text = 'евроремонт'

		new_object_description = xml.SubElement(new_object, 'description')
		new_object_description.text = description

		if flat_type != 'Ст.' or flat_type == '1Е':
			new_object_rooms = xml.SubElement(new_object, 'rooms')
			new_object_rooms.text = rooms
			new_object_rooms_offered = xml.SubElement(new_object, 'rooms-offered')
			new_object_rooms_offered.text = rooms


		new_object_floor = xml.SubElement(new_object, 'floor')
		new_object_floor.text = floor

		if flat_type == 'Ст.' or flat_type == '1Е':
			new_object_studio = xml.SubElement(new_object, 'studio')
			new_object_studio.text = 'да'


		new_object_floors_total = xml.SubElement(new_object, 'floors-total')
		new_object_floors_total.text = t_floor

		root.append(new_object)

    
	tree = xml.ElementTree(root)



	with open(filename, "wb") as fh:
		tree.write(fh, encoding="UTF-8", xml_declaration=True)
	# print(prettify(root))

def prettify(elem):
	rough_string = xml.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml()


if __name__ == "__main__":
	createXML("appt.xml")
