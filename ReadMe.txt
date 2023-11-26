If you run the Python file name "AWS_Acccess.py" the file should run as normal,
the .env has been cleared, but if you add
host = "AWS RDS host name"
user = "RDS username"
password = "RDS password"
charset = utf8mb4
cursorclass = pymysql.cursors.DictCursor
this file will be a straight forwards login system
