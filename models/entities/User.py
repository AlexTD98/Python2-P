from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, username, password, email="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def check_password(self,hashed_password,password):
       return check_password_hash(hashed_password, password)


# Datos para ingresar Alberto
# User: Alberto
# Password: prueba123
# Email: albertocruz290@gmail.com

# Datos para ingresar Alejandro
# User: AlexTD98
# Password: alejandro
# Email: alextd_98@hotmail.com

# Datos para ingresar Mayra
# User: MayraLMZ
# Password: mayra
# Email: mayramata_2000@gmail.com