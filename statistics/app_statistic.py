from mysql.connector import Error
import numpy as np, pandas as pd
from helpers import select_data, insert_data
import fnmatch
import os

    
   
def start_stat(db,db_log,error_log):
    """_summary_ : list
    Start from here
    Args:
        db (_type_): Database
        db_log (_type_): log
        error_log (_type_): error
    """
    summary ={}
    summary = {
                    'total_files_games':0,
                    'total_files_players':0
        } 
    
    summary = files_info(summary)
    summary = tables_raw_total(db,db_log,error_log,summary)
    summary = moves_stat(db,db_log,error_log,summary)
    summary = import_error(summary)
    summary = calculation(summary)
    export_stat_db(db,db_log,error_log,summary)

    #display(summary)
    

def display(summary):
    """_summary_: list
    Display part
    Args:
        summary (_type_): list summary
    """
    df_s = pd.DataFrame([summary]) 
    print(df_s.transpose())
    


def files_info(summary):
    """_summary_: list
    information about files 
    Args:
        summary (_type_): list summary

    Returns:
        _type_: list summary
    """
    dir_list =  {
                "1" : { "path":"./data/Games", "name": "total_files_games","suffix":"*.pgn"},
                "2" : {"path":"./data/Players", "name": "total_files_players","suffix":"*.json"}
                }

    for i in dir_list:
        dirpath = dir_list[i]['path']
        nbr = len(fnmatch.filter(os.listdir(dirpath), dir_list[i]['suffix']))
        summary[dir_list[i]['name']]= nbr
        
    return summary


# files_info()

def tables_raw_total(db,db_log,error_log,summary):
    """_summary_: list
    info of all tables
    Args:
        db (_type_): Database
        db_log (_type_): log
        error_log (_type_): error

    Returns:
        _type_: list summary
    """

    tables_list =['dim_eco','dim_event','dim_federation','dim_result','dim_site','dim_title','game','games_raw','player','playerdetails','players_raw']
    for i in tables_list:
        sql =f"SELECT count(*) FROM {i};"
        cursor=select_data(db,sql,db_log,error_log)
        result = cursor.fetchall()
        summary[i]=str(result[0][0])
    return summary

def moves_stat(db,db_log,error_log,summary):
    """_summary_: list
    moves describe
    Args:
        db (_type_): Database
        db_log (_type_): log
        error_log (_type_): error

    Returns:
        _type_: list summary
    """
  
    sql =f"SELECT nbr_move FROM app_move_nbr where nbr_move > 3"
    cursor=select_data(db,sql,db_log,error_log)
    df_m = pd.DataFrame(cursor.fetchall())
    summary['moves_min'] = df_m.min()[0]
    summary['moves_mean'] = int(df_m.mean()[0])
    summary['moves_max'] = df_m.max()[0]
    return summary


def import_error(summary):
    """_summary_: list
    import error info
    Args:
        summary (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    with open("./insert-error.txt") as f:
        contents = f.read()
        summary['total_error_import'] = contents.count("Event")
    return summary


def calculation(summary):
    """_summary_: list
    import stat 
    Args:
        summary (_type_): _description_

    Returns:
        _type_: list summary
    """
    
    summary['total_begin'] = int(summary['games_raw'])+int(summary['total_error_import'])
    summary['lost_import_percent'] = round(((float(summary['total_error_import'])/float(summary['total_begin']))*100),2)
    return summary


def export_stat_db(db,db_log,error_log,summary):
    """_summary_: list
    export summary list to db app_stat

    Args:
        db (_type_): Database
        db_log (_type_): log
        error_log (_type_): error
    """
    
    sql='TRUNCATE TABLE app_stat;'
    cursor=insert_data(db,sql,db_log,error_log)
    tab = summary.keys()
    for k in tab:
        sql = f"INSERT INTO app_stat (title,data1) VALUES('{k}','{summary[k]}');"
        print(sql)
        cursor=insert_data(db, sql,db_log,error_log)
        print (cursor)
            

