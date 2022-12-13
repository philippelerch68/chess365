#!/usr/bin/python3
import mysql.connector

def insert_data(sql):
    
  #establishing the connection
  conn = mysql.connector.connect(
    user='philippe', password='philippe', host='192.168.0.35', database='Datascientest')

  #Creating a cursor object using the cursor() method
  cursor = conn.cursor()

  # Preparing SQL query to INSERT a record into the database.
  #sql='INSERT INTO chess(id,Event, Site, Date, Round, White, Black, Result, WhiteElo, BlackElo, ECO, Game) VALUES (3,"World school-ch U07 3rd","Chalkidiki","2007.05.01","5.1","Puranik, Abhimanyu","Ioannidis, Evgenios","1-0","0","0","C65","1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. O-O b6 5. Bxc6 dxc6 6. Nxe5 Qd4 7. Nxc6 Qxe4  8. Re1 Qxe1+ 9. Qxe1+ Be6 10. d3 Rd8 11. Nxd8 Kxd8 12. Bg5 h6 13. Bxf6+ gxf6  14. Qc3 Bg7 15. Nd2 Rg8 16. Qa3 Bf8 17. Qxa7 Bd5 18. Qb8+ Ke7 19. Qxc7+ Ke8 20.  Re1+ Be6 21. Ne4 Rg6 22. Qc6+ Kd8 23. Qxb6+ Ke8 24. Nc5 Bxc5 25. Qxc5 1-0")'

  try:
    # Executing the SQL command
    cursor.execute(sql)
    
    # Commit your changes in the database
    conn.commit()
    #print("Data inserted")

  except:
    # Rolling back in case of error
    conn.rollback()
    print("Data insert ERROR !")

  

  # Closing the connection
  conn.close()


'''

CREATE TABLE `Datascientest`.`chess` (
  `id` INT(5) NOT NULL,
  `Event` VARCHAR(40) NULL,
  `Site` VARCHAR(30) NULL,
  `Date` varchar(12) NULL,
  `Round` VARCHAR(6) NULL,
  `White` VARCHAR(35) NULL,
  `Black` VARCHAR(35) NULL,
  `Result` varchar(10) NULL,
  `WhiteElo` VARCHAR(5) NULL,
  `BlackElo` VARCHAR(5) NULL,
  `ECO` VARCHAR(5) NULL,
  `Game` mediumtext(2000) NULL,
  PRIMARY KEY (`id`));
'''
