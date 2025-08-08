import requests
from Departamento import Departamento

class Museo:
    def __init__(self):
        self.departamentos = []
        self.autores = []
        self.obras = []
        self.nacionalidades = []

    def cargar_api(self):
        """
        Obtiene la lista de departamentos desde la API
        y los almacena en el atributo `self.departamentos`.
        """

        #Peticion GET a la API para obtener los departamentos
        response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")

        #Valido que la respuesta hay sido exitosa
        if response.status_code == 200:
            data = response.json()
            #recorre cada elemento en el campo "departments" del JSON
            for info_depto in data["departments"]:
                

                depto_id = info_depto["departmentId"]       
                nombre = info_depto["displayName"]

                # Creamos un departamento y lo añadimos a lista de departamentos
                self.departamentos.append(Departamento(depto_id, nombre))
        else:
            print(f"Error {response.status_code}")

    def cargar_csv(self):
        """
        Carga un listado de nacionalidades desde un archivo CSV y las almacena
        en el atributo self.nacionalidades.
        """

        #Abre el fichero 'CH_Nationality_List_20171130_v1.csv' usando codificación UTF-8.
        with open('CH_Nationality_List_20171130_v1.csv', encoding='utf-8') as archivo:
            for linea in archivo:
                #elimina espacios en los extremos
                linea = linea.strip()

                #Valido que la linea sea diferente a "", es decir, que no este vacia
                if linea:
                    #añade la cadena resultante a self.nacionalidades.
                    self.nacionalidades.append(linea)


    def buscar_obras_departamentos(self):
        indice = 1
        for departamento in self.departamentos:
            print(f"{indice}. {departamento}")
            indice+=1


    def buscar_obras_nacionalidad(self):
        indice = 1
        for nacionalidad in self.nacionalidades:
            print(f"{indice}. {nacionalidad}")
            indice+=1


    def menu(self):
        """
        Funcion para iniciar el programa. Llama a la funcion que carga 
        los departamentos a traves de la API y luego llama a la funcion que
        carga el CSV con las nacionalidades. Por ultimo, muestra el menu de opciones
        del sistema
        """

        self.cargar_api()
        self.cargar_csv()

        while True:
            opcion = input("""
Bienvenidos a MetroArt
1. Ver lista de obras por Departamento
2. Ver lista de obras por Nacionalidad del autor
3. Ver lista de obras por nombre del autor
4. Salir

Ingrese la opcion deseada
--> """)
            if opcion == "1":
                self.buscar_obras_departamentos()
            elif opcion == "2":
                self.buscar_obras_nacionalidad()
            elif opcion == "3":
                pass
            elif opcion == "4":
                print("\nAdios!")
                break
            else:
                print("\nOpcion Invalida!\n")