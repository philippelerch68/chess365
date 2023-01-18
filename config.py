# config.py
# Configuration

url = "https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/AE_ChessAnalytics.7z"
save_as = "AE_ChessAnalytics.7z"
data_dir ="../data/"
games_dir = data_dir+"Games/"
players_dir = data_dir +"Players/"
games_to_csv = data_dir +"games.csv"

#  Database info
#  user='philippe', password='philippe', host='192.168.0.35', database='Datascientest')
db_host='localhost'
db_database='Datascientest'
db_user='host'
db_password='cuchri_dev'

'''
def connection_test():
    sql='SELECT Event FROM Datascientest.chess limit 10;'
    data=select_data(sql)
   
    for x in data:
        print(x[0])
    
connection_test()
'''