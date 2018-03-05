import MySQLdb as mysql
import string
import random
import hashlib

hostname = "127.0.0.1"
user = "vlad"
passwd = "123"
dbname = "db_project"
charset = "utf8"
server_port = 8806

db=mysql.connect(host=hostname, port=server_port, user=user, passwd=passwd, db=dbname, charset=charset)
print(db)

asd={"leg":15000,"heart":500000, "kidney":150000, "liver":200000, "eye":50000, "arm":20000}
r=[i for i in range(50)]
random.shuffle(r)
nicks=""
nicks=nicks.split()
print(nicks)
# формируем курсор, с помощью которого можно исполнять SQL-запросы
cursor = db.cursor()

types=['plane', 'car', 'ship', 'courier']
countries=['usa','russia','UK','Albania','Bolivia']
names=["Golden Ocean", "Bocimar International", "CTM"," Golden Union Shipping" , "Star Bulk Carriers"]
#sql = """INSERT INTO `bill` (`№`, `seller`, `buyer`, `date`, `commodity`,
#       `category`, `transport`, `legal`, `point`) VALUES
#       (NULL, `{seller}`, `{buyer}`, `{date}`, `{commodity}`,`{category}`, `{transport}`, `{legal}`, `{point}`))
#       """.format(seller=s,buyer=b,date=d, commodity=c,category=cat, transport=t,legal=l,point=p)
md=hashlib.md5()
sh=hashlib.sha256()
for i in range(50):
    # name=random.choice([chr(i) for i in range(85,90)])
    nick = random.choice(list(asd.keys()))
    # md.update(nick.encode())
    # pas=md.hexdigest()[random.randint(0,5):random.randint(11,15)]
    # print(pas)
    # sh.update(nick.encode())
    # purse=sh.hexdigest()
    # print(purse)
    # pas=random.randint(1,20)
    # email=nick+"@mail.ru"
    sql = """INSERT INTO `farry` (`id`, `name`, `country`, `price_for_km`, `type`) VALUES (NULL, '{}', '{}', '{}', '{}')
    """.format(random.choice(names)+str(r[i]),random.choice(countries), 0.57*random.randint(10,25),random.choice(types))
    try:
        cursor.execute(sql)
    except Exception:
        print("ne och")
    db.commit()
    print("exec")
#исполняем SQL-запрос
#cursor.execute(sql)
# применяем изменения к базе данных
#db.commit()