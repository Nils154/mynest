# This assumes you have mysql installed, like a LAMP install
# (Linux, Apache, MySQL and PhP)
# and install the python part:
# sudo apt-get install python-mysql*
# Here is an example:
# https://randomnerdtutorials.com/raspberry-pi-apache-mysql-php-lamp-server/
# go into mysql like this: sudo mysql -u root -p
# and create a database with: create database mynestdb;
# or use existing database (I used existing wordpress database)
# you can check what you have with: show databases;
# create a table in the database with:
#   CREATE TABLE mynesttable (
#     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,
#     Tinside decimal(4,2),
#     TDownstairs decimal(4,2),
#     TBedroom decimal(4,2),
#     Toutside decimal(5,2),
#     DewpointInside decimal(4,2),
#     DewpointOutside decimal(4,2),
#     HInside decimal(5,2),
#     HOutside decimal(5,2),
#     HTarget decimal(5,2),
#     Status varchar(16),
#     Away varchar(16),
#     NestMode varchar(16),
#     NestState varchar(16),
#     FanRequest varchar(16));
# note that you can add columns later if you want to start simple, for example:
# ALTER TABLE mynesttable ADD NestMode varchar(16);
# the date could be a bit tricky, is has to be a string formatted the right way
# for the database to understand
# you need to change database parameters on line 43-45

import mysql.connector
from mysql.connector import Error

        
def insert_record(date, tinside, tdownstairs, tbedroom, toutside, dewpointinside,
                  dewpointoutside, hinside, houtside, htarget,
                  status, away, nestmode, neststate, fanrequest):
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='wordpress',
                                       user='root',
                                       password='yourpassword')
        if conn.is_connected():
            print('Connected to MySQL database')
    except Error as e:
        print(e)
    query = "INSERT INTO mynesttable (date,TInside,TDownstairs," \
            "TBedroom,TOutside,DewpointInside,DewpointOutside," \
            "HInside,HOutside,HTarget,"\
            "Status,Away,NestMode,NestState,FanRequest) " \
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    args = (date, tinside, tdownstairs, tbedroom, toutside, dewpointinside,
            dewpointoutside, hinside, houtside, htarget,
            status, away, nestmode, neststate, fanrequest)
    try:
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


def main():
    insert_record('2019-07-21_14:50:34', '73', '74', '75', '79', '60',
                  '63', '45', '70', '45',
                  'AC', 'home', 'cool', 'cooling', 'off')


if __name__ == '__main__':
    main()
