import yaml
import pathlib
import mysql.connector


def read_yaml(file_path):
    """Extracts data from a .yaml file (eg. config)

    Args:
        file_path (str): Path to the .yaml file of interest

    Returns:
        dict: Information defined in the .yaml file
    """
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def files_count(dir_path):
    """Counts the number of files in a directory

    Args:
        dir (str): Path to the directory

    Returns:
        int: Number of files in the defined directory
    """
    cnt = 0
    for path in pathlib.Path(dir_path).iterdir():
        if path.is_file():
            cnt += 1
    return cnt


def insert_data(db, sql,db_log,error_log):
    """Load data as a row in a table of a defined database

    Args:
        db (list): List with database connection informations
        sql (str): SQL statement that loads data to db

    Returns:
        str: Status of the recent data insert
    """
    #establishing the connection
    conn = mysql.connector.connect(user=db[2], password=db[3], host=db[0], database=db[1], consume_results=True)
    
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    try:
        # Executing the SQL command
        cursor.execute(sql)
        
        # Commit your changes in the database
        conn.commit()
        status = 'ok'
        #print("Data inserted")

    except:
        # Rolling back in case of error
        conn.rollback()
        status ='error'
        if(status =='error'):
                flog = open('insert-error.txt', "a")
                flog.write(f"{sql} --")
                flog.write("\n")
        
    # Closing the connection
    conn.close()
    return status

def select_data(db,sql):
  #establishing the connection
  conn = mysql.connector.connect(user=db[2], password=db[3], host=db[0], database=db[1], consume_results=True)
  
  #Creating a cursor object using the cursor() method
  cursor = conn.cursor(buffered=True)

  # Preparing SQL
 
  try:
    # Executing the SQL command
    cursor.execute(sql)
    #myresult = cursor.fetchall()
    #return myresult
    return cursor

  except:
    # Rolling back in case of error
    conn.rollback()
    status ='error'
    
    
def delete_data(db, sql,db_log,error_log):
    """delete data as a row in a table of a defined database

    Args:
        db (list): List with database connection informations
        sql (str): SQL statement that loads data to db

    Returns:
        str: Status of the recent data insert
    """
    #establishing the connection
    conn = mysql.connector.connect(user=db[2], password=db[3], host=db[0], database=db[1], consume_results=True)
    
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    try:
        # Executing the SQL command
        cursor.execute(sql)
        
        # Commit your changes in the database
        conn.commit()
        status = 'ok'
        #print("Data deleted")

    except:
        # Rolling back in case of error
        conn.rollback()
        status ='error'
        if(status =='error'):
                flog = open('delete-error.txt', "a")
                flog.write(f"{sql} --")
                flog.write("\n")
        
    # Closing the connection
    conn.close()
    return status