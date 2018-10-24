from database import Database

db_path = 'db.db'
DB = Database()
DB.open(db_path)
# DB.create()
#columns = 'nombre, imagen, nfc'
#data = "'Equipo1', 'imagen1', '1234'"

columns = 'nombre, usuario, password, cuenta'
data = " 'Jhon Doe','user', '1234', 'Usuario' "

#DB.write('Usuarios', columns, data)
is_login = DB.login("'user'","'1234'")
print('login:  ', is_login)


DB.close()

print("Ok insertada") 
