from requests import get
from json import loads
from datetime import datetime
from pandas import DataFrame
from schedule import every, run_pending
from time import sleep
class TasaMonedas(object):
    '''
        Clase encargada de realizar las conexiones con 
        una API encargada de proporcionar los datos
        si la url y id_conn no son entregados se usa 
        por defecto OPEN EXCHANGE RATES
    '''
    def __init__(self, url, id_conn, variables, key_data):
        if not (url and id_conn):
            self.url = 'https://openexchangerates.org/api/latest.json?app_id='
            self.id_ = '871483fc39874aa5a2554bc05552020e'
            self.conn_API = False
            self.k = 15.315500100061781
            self.key_data = 'rates'
            self.variables = {
                'USDtoCOP': 'COP',
                'USDtoARSc': 'ARS',
                'USDtoARSv': 'ARS',
                'UVRtoCOP': 'COP',
            }
        else:
            self.url = url
            self.id_ = id_conn
            self.conn_API = True
            self.k = 1
            self.variables = variables
            self.key_data = key_data
    def get_data_from_API(self):
        '''
            Está función crea una conexión con la API y obtiene los datos
            input:
                url: url donde se encuenta la API
                id_conn: id para la conexión con la API
            return:
                data: datos consutlados en la API, en formato Json -> dict Python
        '''
        # create connetion with API
        response = get(f'{self.url}{self.id_}')
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            if self.key_data:
                self.data = loads(response.content).get(self.key_data)
            else:
                self.data = loads(response.content)
        else:
            # failed get data from API
            self.data = None
            print('Failed to retrieve data. Status code:', 
                    response.status_code)
        return None
    def get_calculate_values(self):
        '''
            Está función permite obtener los datos y calcular los datos calculados
            permite guardar los datos obtenidos y calculados en la variable self.data_values
            input:
                self:   para obtener la variable previamente calculada self.data, 
                        self.variables y self.k
            return:
                None
        '''
        self.data_values = [
            [self.data.get(self.variables.get('USDtoCOP')), 'USD', 'COP'],
            [self.data.get(self.variables.get('USDtoCOP')), 'USD', 'COP'],
            [self.data.get(self.variables.get('USDtoARSc')), 'USD', 'ARS'],
            [self.data.get(self.variables.get('USDtoARSv')), 'USD', 'ARS'],
            [self.data.get(self.variables.get('USDtoCOP'))\
                /self.data.get(self.variables.get('USDtoARSv')), 'ARS', 'COP'],
            [self.data.get(self.variables.get('USDtoCOP'))\
                /self.data.get(self.variables.get('USDtoARSv')), 'ARS', 'COP'],
            [self.data.get(self.variables.get('UVRtoCOP'))\
                /self.k, 'UVR', 'COP'],
            [self.data.get(self.variables.get('UVRtoCOP'))\
                /self.k, 'UVR', 'COP'],
            [self.data.get(self.variables.get('USDtoCOP'))\
                /(self.data.get(self.variables.get('UVRtoCOP'))/self.k), 'USD', 'UVR'],
            [self.data.get(self.variables.get('USDtoCOP'))\
                /(self.data.get(self.variables.get('UVRtoCOP'))/self.k), 'USD', 'UVR'],
        ]
    def export_data(self, path, name):
        '''
            Está función permite exportar los datos en .csv y Excel
            input:
                self:   para obtener la variable previamente calculada self.data
                path: ruta donde se guardan los archivos
            return:
                None
        '''
        self.time = datetime.now()
        fecha = f'{self.time.year}-{self.time.month}-{self.time.day} {self.time.hour}:{self.time.minute}'
        data_export = []
        for i, data in enumerate(self.data_values):
            data_export.append({
                'Compra_venta':'M' if i%2 else 'G', 
                'fecha':fecha,
                'monedaDe':data[1],
                'valor': data[0],
                'monedaA':data[2],
            })
        print(f'Se realiza la tarea {fecha}')
        df = DataFrame(data_export)
        fecha_name = fecha.replace('-','').replace(':','.')
        df.to_csv(f'{path}\\{name} {fecha_name}.csv', 
                    encoding='latin-1',
                    sep='|', index=False)
        df.to_excel(f'{path}\\{name} {fecha_name}.xlsx', 
                    index=False) 
        print('Se exportan los datos a .CSV y .Excel\n')
    def do_task(self, horarios, task, test=False):
        '''
            Está función permite crear la realización de las tareas horarias
            si se pasa test=True, se ejecutaran cada 20segundos
            input:
                horarios: lista de los horarios a ejecutar las tareas
                task: función de la tarea a realizar
                test: realización de la prueba cada 20 segundos
            return:
                None
        '''
        if test:
            every(20).seconds.do(task)
        else:
            for hour in horarios:
                every().day.at(hour).do(task)
        print('\nSe inicia el script de consulta a la API\n')
        while True:
            run_pending()
            sleep(1)        