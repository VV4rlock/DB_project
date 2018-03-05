
import MySQLdb as mysql
import hashlib

class Category_exist_exception(Exception):
    pass

class User_exist_exception(Exception):
    pass

class DbManager:
    def __init__(self):
        hostname = "127.0.0.1"
        user = "vlad"
        passwd = "123"
        dbname = "db_project"
        charset = "utf8"
        self.db = mysql.connect(host=hostname,port=8806, user=user, passwd=passwd, db=dbname, charset=charset)
        self.md5 = hashlib.md5()

    def signup(self,login,password,email,purse):
        cursor = self.db.cursor()
        cursor.execute("select * from `users` where login='{}'".format(login))
        users=cursor.fetchall()
        if len(users)!=0:
            raise User_exist_exception()

        sql = """INSERT INTO `users` (`id`, `login`, `purse`, `pass`, `e-mail`, `modification_date`)
         VALUES (NULL, '{}', '{}', '{}', '{}', NULL)""".format(login,purse,password,email)
        cursor.execute(sql)
        self.db.commit()
        return True

    def get_account_by_id(self,id):
        cursor = self.db.cursor()
        sql = """SELECT login,`e-mail`,purse FROM `users` WHERE id={} """.format(id)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)==1:
            return data[0]
        return None

    def change_pass(self,login,old_pass,new_pass):
        self.md5.update(old_pass.encode())
        cursor = self.db.cursor()
        sql = """SELECT id,login FROM `users` 
                        WHERE login='{}' AND pass='{}' """.format(login, self.md5.hexdigest())
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        if len(data) == 1:
            update="UPDATE `users` SET `pass` = '{}' WHERE `users`.`login` = '{}'".format(new_pass,login)
            cursor.execute(update)
            self.db.commit()
            return True
        else:
            return False

    def auth(self,login,password):
        self.md5.update(password.encode())
        cursor = self.db.cursor()
        sql = """SELECT id,login FROM `users` 
                WHERE login='{}' AND pass='{}' """.format(login, self.md5.hexdigest())
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)==1:
            return data[0]
        return None


    def get_lots(self):
        cursor = self.db.cursor()
        sql = """SELECT lots.id,description,price,login,category.name FROM lots 
                    INNER JOIN users ON seller=users.id 
                    INNER JOIN category ON lots.category=category.id"""
        cursor.execute(sql)
        return ("description", "price", "seller", "category"), cursor.fetchall()

    def search_lots_by_description(self,search_line):
        cursor = self.db.cursor()
        sql = """SELECT lots.id,description,price,login,category.name FROM lots 
                            INNER JOIN users ON seller=users.id 
                            INNER JOIN category ON lots.category=category.id
                            WHERE description='{}'""".format(search_line)
        cursor.execute(sql)
        return ("description", "price", "seller", "category"), cursor.fetchall()

    def get_bills(self,user_id):
        cursor = self.db.cursor()
        sql="""SELECT bill.id,u1.login AS seller,u2.login AS buyer,date,commodity AS description,category.name,price FROM `bill` INNER JOIN users AS u1 ON seller=u1.id 
        INNER JOIN users AS u2 ON buyer=u2.id 
        INNER JOIN category ON bill.category=category.id 
        WHERE u1.id="{id}" OR u2.id="{id}" """.format(id=user_id)
        cursor.execute(sql)
        return ("seller","buyer","date","description", "category","price"), cursor.fetchall()

    def get_categories(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM `category`")
        return cursor.fetchall()

    def create_category(self,name,meas):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM `category` WHERE name='{}'".format(name))
        data=cursor.fetchall()
        if len(data)!=0:
            raise Category_exist_exception()
        else:
            sql = "INSERT INTO `category` (`id`, `name`, `measuring`) " \
                  "VALUES (NULL, '{}', '{}')".format(name, meas)
            cursor.execute(sql)
            self.db.commit()

    def buy_lot(self,buyer_id,lot_id):
        cursor = self.db.cursor()
        sql="SELECT * FROM `lots` WHERE `lots`.`id` = '{}'".format(lot_id)
        cursor.execute(sql)
        data=cursor.fetchall()
        if len(data)!=1:
            return None
        del_sql="DELETE FROM `lots` WHERE `lots`.`id` = '{}'".format(lot_id)
        cursor.execute(del_sql)
        self.db.commit()
        lot=data[0]
        insert_sql="""INSERT INTO `bill` (`id`, `seller`, `buyer`, `date`, `commodity`,
                    `category`, `point`, `price`) VALUES (NULL, '{}', '{}', NULL, '{}', '{}', '{}', '{}')
                    """.format(lot[1],buyer_id,lot[4],lot[5],1,lot[2])
        cursor.execute(insert_sql)
        self.db.commit()
        return True



    def create_lot(self,description,price,amount,seller_id,category):
        cursor = self.db.cursor()
        sql = """INSERT INTO `lots` (`id`, `seller`, `price`, `amount`,
                `description`, `category`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}')
                """.format(seller_id, price,amount,description,category)
        cursor.execute(sql)
        self.db.commit()


if __name__=="__main__":
    db=DbManager()
    db.auth("Surge","qwert")