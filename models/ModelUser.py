from .entities.User import User

class ModelUser():

    @classmethod
    def login(self,db, user):
        try:
            cursor = db.connection.cursor()
            sql="""SELECT id, username, email, password FROM users 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()

            if row != None:
                user = User(row[0],row[1],row[2],User.check_password(row[3],user.password))
                return user
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self,db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, email FROM users WHERE id = {}".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()

            if row != None:
                logged_user = User(row[0],row[1],row[2],None)
                return logged_user
            else:
                return None

        except Exception as ex:
            raise Exception(ex)