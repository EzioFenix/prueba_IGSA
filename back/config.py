# config.py

class Config:
    # 🔧 Reemplaza estos valores con los tuyos
    SERVER = '82.197.92.81'           # Ej: 'localhost', '192.168.1.10', 'tu-servidor.database.windows.net'
    DATABASE = 'TEST101'    # Nombre de tu base de datos
    USERNAME = 'user_test101'          # Usuario de SQL Server (ej: sa)
    PASSWORD = 'N7#pWk!2rXeD9@uL'       # Contraseña del usuario
    DRIVER = 'ODBC Driver 17 for SQL Server'  # Asegúrate de tenerlo instalado

    # 🔗 Cadena de conexión completa
    CONNECTION_STRING = (
        f'DRIVER={DRIVER};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={USERNAME};'
        f'PWD={PASSWORD};'
        f'Encrypt=no;'               # Cambia a 'yes' si usas Azure
        f'TrustServerCertificate=no' # Cambia a 'yes' si tienes problemas de certificado
    )