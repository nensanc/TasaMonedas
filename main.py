
# local library
from _source.tasamonedas import TasaMonedas

# creamos las variables de conexión con la API
# la API debe entregar los datos en formato JSON 
url = None # url de la API
id_conn = None # id para tener acceso a la API
key_data = None # key de los datos

# Key de las variables de los datos JSON de la API
variables = {
    'USDtoCOP': None,
    'USDtoARSc': None,
    'USDtoARSv': None,
    'UVRtoCOP': None,
}

# path y nombre
path = r'C:\Users\50457\Downloads'
name = 'compra_venta'


# Instanciamos la clase  
tasamonedas = TasaMonedas(url, id_conn, variables, key_data)

def task():
    # Obtenemos los datos de la API
    tasamonedas.get_data_from_API()

    # obtenemos y calculamos los datos a exportar 
    tasamonedas.get_calculate_values()

    # exportamos los datos
    tasamonedas.export_data(path, name)

# ejecución de tareas 
horarios = [
    '12:00', '12:55', '18:00', '18:55', 
    '00:00', '00:55', '06:00', '06:55'
    ]
tasamonedas.do_task(horarios, task, test=False)