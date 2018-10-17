

Project Scrapping: Web Scraping from IMDB

To Subscribe to the Project:

1. Input Y to input to subscribe a new user.

2. Input N to exit program

3. Enter the user&#39;s Email ID to receive email.

4. Enter the list of Tv Series separated by comma.

5. The subscribed email ID&#39;s will receive an email.

**A Screenshot of Input:**
![Input Demo](/1.jpg)

**A Screenshot of the database:**

**Database Structure:**

**Table Name: userInfo**

**Table Structure: As shown below.**

**Relation : Many to Many.**
![DB Structure](/2.jpg)

**A Screenshot of Output**
![Output Demo](/3.jpg)


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Program Overview:**

Class Name : Main

**Methods**

**userInput** (self): takes input from user

**CreateConnectionToDB** (self): Establishes a connection to the 


**insertIntoDB** (self , db , cnt): Enters the user information into the database

**getSeriesList** (self , count , M): Returns a dictionary structure which contains the list of Tv Series, each series mapped to a set containing id&#39;s of users

**getEmailList** (self , count , eMap): Returns a dictionary structure which conatins the id&#39;s of users mapped to their email id&#39;s

**constructUrl1** (self , seriesName): Constructs a url to search the given Tv series on IMDB

**getUrlCode** (self , url1): Returns a code corresponding to that particular Tv Series

**getLastSeason** (self , urlCode): Get the last or current season of the Tv Series

**getDates** (self , lastSeason): Returns a list containing all the dates when various episodes of the last season are released

**getMessage** (self , dates): Returns a message with the status of the Tv Series that has to be sent to the user

**sendemail** (from\_addr, to\_addr\_list, subject, message, login, password, smtpserver=&#39;smtp.gmail.com:587&#39;): Sends an email regarding the status of the Tv Series mentioned by user


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


**Guidelines to change System Email:**

**       ** _sendemail(from\_addr        = &#39;demo.spoileralert@gmail.com&#39;,_

_                     to\_addr\_list =  eMap[t],_

_                     subject          = &#39;Spoiler Alert&#39;,_

_                     message          =  msg ,_

_                     login            = &#39;demo.spoileralert@gmail.com&#39;,_

_                     password         = &#39;legendsareborninnovember&#39;)_



To change System Email change the corresponding entering(at line no. 379).

**To run Program on your System change root username and Password for mysql database on the following lines:**

Line no. 39

Line no. 285

Line no. 306

