import csv
import pymysql

fin = open("/Users/anhyebin/Documents/SKN21/SKN21-2nd-4Team/data/interim/Customer_Churn_Dataset_0_impute.csv", 'r')
data = csv.reader(fin)

print(data)

# fin.close()

header = next(data)

print(header)


# # DB 연결 설정
# dbhost = 'localhost'
# dbuser = 'your_username'
# dbpassword = 'your_password'
# dbname = 'your_database_name'

# try:
#     # 데이터베이스 연결
#     connection = pymysql.connect(
#         host=dbhost,
#         user=dbuser,
#         password=dbpassword,
#         db=dbname,
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor # 딕셔너리 형태로 결과 반환
#     )
#     print("DB 연결 성공!")

#     # 커서 생성
#     with connection.cursor() as cursor:
#         # SQL 쿼리 실행 예시 (SELECT)
#         sql = "SELECT * FROM users WHERE age > %s"
#         cursor.execute(sql, (25,))
#         result = cursor.fetchall()

#         for row in result:
#             print(row)

#         # INSERT, UPDATE, DELETE 작업 시에는 commit 필수
#         # sql_insert = "INSERT INTO users (name, age) VALUES (%s, %s)"
#         # cursor.execute(sql_insert, ('John Doe', 30))
#         # connection.commit()
#         # print("데이터 삽입 성공!")

# except pymysql.Error as e:
#     print(f"DB 연결 중 오류 발생: {e}")

# finally:
#     # 연결 종료
#     if connection:
#         connection.close()
#         print("DB 연결 종료.")
