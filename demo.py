import requests
import bs4
import datetime
import smtplib
import pymysql

class Main:

	#main function
	def __init__(self ):
		
		self.emailID = None
		self.emailID1 = None
		self.seriesName = None
		self.seriesName1 = None


	def userInput(self):

		""" 
		Takes Input from User
		"""
		print('Enter Your Email ID', end=': ')
		self.emailID = input()
		self.emailID1=self.emailID.lower()
		
		print()

		print('Enter the name of the Series', end=': ')
		self.seriesName = input()
		self.seriesName1=self.seriesName.lower()
	

	def createConnectionToDB(self):     

		""" 
		Establishes a connection to the database
		"""
		db = pymysql.connect("localhost" , "root" , "lnmiit" , "testDB")
		
		return db


	def insertIntoDB(self , db , cnt):  
		
		"""
			Enters the user information into the database
		"""
		seriesName = self.seriesName1
		emailID = self.emailID1
		sql = "Insert into userInfo(ID, emailID, tvSeries) values (%s, %s, %s)"
		cursor = db.cursor()
		cursor.execute(sql , (cnt, emailID, seriesName))
		db.commit()   # commoits the changes made to the database


	def getSeriesList(self , count , M):	
		
		"""
		Returns a dictionary structure which contains the list of Tv Series, each series mapped to a set containing id's of users 
		"""
		cursor = db.cursor()
		sql = "select tvSeries from userInfo where ID = (%s)"
		cursor.execute(sql , count)
		data = cursor.fetchone()

		data = str(data)
		
		data = (data[2 : len(data) - 3])
		sList = data.split(',')

		for t in sList:

			li = set()
			li.add(count)

			t = t.strip()

			if(t in M):
				
				M[t].add(count)
			else:
				M[t] = li

		return M
				
	
	def getEmailList(self , count , eMap):		
		
		"""
		Returns a dictionary structure which conatins the id's of users mapped to their email id's
		"""

		cursor = db.cursor()
		sql = "select emailID from userInfo where ID = (%s)"
		cursor.execute(sql , count)
		data = cursor.fetchone()

		data = str(data)
		data = (data[2 : len(data) - 3])
			
		eMap[count] = data

		return eMap	

	def closeDB(self):

		db.close()


	def constructUrl1(self , seriesName):	

		"""
		Constructs a url to search the given Tv series on IMDB		
		"""
		seriesList = seriesName.split()
		url1 = 'https://www.imdb.com/find?ref_=nv_sr_fn&q='
		url1Post = '&s=all'

		c = 0;
		length = len(seriesList)

		for t in seriesList:

			url1 = url1 + t
			c += 1

			if(c < length):
				url1 = url1 + '+'

		url1 = url1 + url1Post
		return url1



	def getUrlCode(self , url1):
	
		"""
		Returns a code corresponding to that particular Tv Series
		"""

		res = requests.get(url1)
		soup = bs4.BeautifulSoup(res.text , 'lxml')

		r = soup.find('td' , {'class' : 'result_text'}).findAll('a')

		st = []
		for x in r:
			st.append(str(x))


		tmp = str(st[0])

		t1 = tmp.find('tt')
		t2 = tmp.find('/' , t1 + 1)

		urlCode = tmp[t1:t2]
		return urlCode


	def getLastSeason(self , urlCode):	
		
		"""
		Get the last or current season of the Tv Series
		"""
		url2 = 'https://www.imdb.com/title/'
		url2Post = '/episodes?ref_=tt_ov_epl'

		url2 = url2 + urlCode + url2Post

		res2 = requests.get(url2)
		soup2 = bs4.BeautifulSoup(res2.text , 'lxml')

		op = soup2.select('select > option')

		lastSeason = -1
		para = []

		for p in op:

			tempstr = (p.text).strip()

			if(len(tempstr) > 0):
				para.append(tempstr)


		for t in para:

			if(t.isdigit()):
				num = int(t)

				if(num > lastSeason and num < 1900):
					lastSeason = num


		return lastSeason

	
	def getDates(self , lastSeason):	

		"""
		Returns a list containing all the dates when various episodes of the last season are released
		"""
		url3 = 'https://www.imdb.com/title/'
		url3Post = '/episodes?season='

		url3 = url3 + urlCode + url3Post + str(lastSeason)

		res3 = requests.get(url3)
		soup3 = bs4.BeautifulSoup(res3.text , 'html.parser')
		dates = soup3.find_all('div' , attrs = {'class' : 'airdate'})
		return dates


	def getMessage(self , dates):

		"""
		Returns a message with the status of the Tv Series that has to be sent to the user
		"""
		airDates = []
		for d in dates:
			airDates.append(d.text.strip())


		map = {'Jan' : 1 , 'Feb' : 2 , 'Mar' : 3 , 'Apr' : 4 , 'May' : 5 , 'Jun' : 6 , 'Jul' : 7 , 'Aug' : 8 , 'Sep' : 9 , 'Oct' : 10 , 'Nov' : 11 , 'Dec' : 12}

		currentDate = datetime.datetime.now()

		dd = []
		flag = 2
		resultDate = datetime.time(0,0,0)


		for tt in airDates:

			if(len(tt) > 4):
				temp = []
				temp = tt.split()	
				tmpDate = datetime.datetime(int(temp[2]) , map[temp[1][0:3]] , int(temp[0]))

				if(tmpDate > currentDate):
					resultDate = tmpDate
					flag = 1;
					break
			
			else:
				resultY = tt
				flag = 3
				break



		if(flag == 2):
			msg = 'Status: The show has finished streaming all its episodes.'
		elif(flag == 1):
			msg ='Status: The Next Episode airs on ' + str(resultDate.date()) + '.'
		else:
			msg = 'Status: The next Season begins in ' + resultY + '.'

		return msg


def sendemail(from_addr, to_addr_list, subject, message, login, password, smtpserver='smtp.gmail.com:587'):  

	"""
	Sends an email regarding the status of the Tv Series mentioned by user	
	"""
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % to_addr_list
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


	
response = ''
cnt = 0

db = pymysql.connect("localhost" , "root" , "lnmiit")
cursor = db.cursor()
sql1 = "use information_schema"

cursor.execute(sql1)
dbName = "testDB"
sql2 = "select count(*) from schemata where schema_name = (%s)"
cursor.execute(sql2 , dbName)
data = cursor.fetchone()
#db.commit()


data = str(data)
data = data[1 : len(data) - 2]
data = int(data)

if(data == 0):
	sql = 'create database testDB'
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit();
	db2 = db = pymysql.connect("localhost" , "root" , "lnmiit" , "testDB")
	cursor2 = db2.cursor()
	sql = "create table userInfo(ID int not null , emailID varchar(256) not null , tvSeries text not null , primary key(ID))"
	cursor2.execute(sql)
	db2.commit();
	

while(True):											
	print('Press Y to enter details of User and N to exit' , end = ': ' )			# User from Input
	response = input()
	print()
	if(response == 'N'):
		break
	elif(response == 'Y'):
		cnt += 1
		ss = Main()

			
		ss.userInput()
		db = ss.createConnectionToDB()
		ss.insertIntoDB(db , cnt)

	else:
		print('Wrong Input')
		
		
M = {}
tmp = cnt
while(tmp > 0):
	
	M = ss.getSeriesList(tmp , M)
	tmp -= 1


tmp = cnt
eMap = {}

while(tmp > 0):
	
	eMap = ss.getEmailList(tmp , eMap)
	tmp -= 1

ss.closeDB()		# Closing the Database Connection


resM = {}

for t in M:			# Scraping for information of Tv Series mentioned in the dict

	url1 = ss.constructUrl1(t)
	urlCode = ss.getUrlCode(url1)
	lastSeason = ss.getLastSeason(urlCode)
	dates = ss.getDates(lastSeason)
	msg = ss.getMessage(dates)
	msg = 'Tv Series name: ' + str(t) + '\n' + msg + '\n'
	for t2 in M[t]:

		li = []
		li.append(msg)
		if(t2 in resM):
			
			resM[t2].append(msg)
		
		else:

			resM[t2] = li
				

for t in resM:
	msg = ''
	for t2 in resM[t]:
		msg = msg + t2
		
	sendemail(from_addr    = 'demo.spoileralert@gmail.com', 
		      to_addr_list =  eMap[t],
		      subject      = 'Spoiler Alert', 
		      message      =  msg , 
		      login        = 'demo.spoileralert@gmail.com', 
		      password     = 'legendsareborninnovember')


