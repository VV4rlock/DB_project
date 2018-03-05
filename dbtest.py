import MySQLdb as mysql
import string

hostname="192.168.56.101"
user="vlad"
passwd="123"
dbname="test"
charset="utf8"

db=mysql.connect(host=hostname, user=user, passwd=passwd, db=dbname, charset=charset)
print(db)

# формируем курсор, с помощью которого можно исполнять SQL-запросы
cursor = db.cursor()

# открываем исходный csv-файл
f = open("log", "r")
# представляем его в виде массива строк
lines = f.readlines()

for line in lines:
    # если в строе присутствует емейл (определяем по наличию "@")
    if string.find(line, "@") > -1:
        # извлекаем данные из строки
        #fname, fmail, fadres, ftel =unpack_line(line)
        # подставляем эти данные в SQL-запрос
        sql = """INSERT INTO contacts(name, mail, adres, tel)
        VALUES ('%(name)s', '%(mail)s', '%(adres)s', '%(tel)s')
        """%{"name":fname, "mail":fmail, "adres":fadres, "tel":ftel}
        # исполняем SQL-запрос
        cursor.execute(sql)
        # применяем изменения к базе данных
        db.commit()

    cursor = db.cursor()

    # запрос к БД
    sql = """SELECT mail, name FROM eadres WHERE mail LIKE '%yandex.ru' LIMIT 10"""
    # выполняем запрос
    cursor.execute(sql)

    # получаем результат выполнения запроса
    data = cursor.fetchall()
    # перебираем записи
    for rec in data:
        # извлекаем данные из записей - в том же порядке, как и в SQL-запросе
        mail, name = rec
        # выводим информацию
        print(name, mail)


# закрываем соединение с базой данных
db.close()
# закрываем файл
f.close()