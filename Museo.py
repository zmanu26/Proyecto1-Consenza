import requests
import time
from PIL import Image
from Departamento import Departamento
from Obra import Obra
from Autor import Autor

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
        """
        Permite al usuario seleccionar un departamento y listar obras en bloques.
        """

        # Mostrar lista numerada de departamentos
        indice = 1
        for departamento in self.departamentos:
            print(f"{indice}.")
            departamento.show()
            print()
            indice+=1

        # Solicitar selección válida
        opcion = input("\nIngrese el numero del departamento que deseas ver: ")
        while (not opcion.isnumeric()) or (not int(opcion) in range(1, indice+1)):
            print("Error!")
            opcion = input("\nIngrese el numero del departamento que deseas ver: ")

        # Obtener objeto Departamento seleccionado
        depto_select = self.departamentos[int(opcion)-1]

         # Llamada a la API para obtener los IDs de las obras
        response = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={depto_select.id}")

        if response.status_code == 200:
            ids_obras = response.json()["objectIDs"]
            
            total = len(ids_obras)
            inicio = 0
            lote = 10
            
            # Mostrar obras en bloques de tamaño 'lote'
            while inicio < total:
                
                #Recorrer el lote
                for obra_id in ids_obras[inicio: inicio + lote]:
                    #Obtener el detalle de una obra
                    detalle = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra_id}")
                    
                    #Verificar el status
                    if detalle.status_code == 200:

                        #Convertir el detalle a json
                        detalle = detalle.json()

                        # Verificar si la obra ya existe
                        obra = self.verificar_obra(detalle, depto_select)

                        #Si no existe Crear la obra
                        if obra == None:

                            #Obtener los atributos necesarios para la creacion de la obra
                            id = detalle["objectID"]
                            titulo=detalle["title"]
                            departamento=depto_select
                            autor=None

                            #Verificar si al autor existe
                            if self.verificar_autor(detalle) == None:

                                #Si no existe, crear el autor y añadirlo a la lista de autores
                                nombre=detalle["artistDisplayName"]
                                nacionalidad=detalle["artistNationality"]
                                nacimiento=detalle["artistBeginDate"]
                                muerte=detalle["artistEndDate"]

                                autor_nuevo = Autor(nombre, nacionalidad, nacimiento, muerte)

                                self.autores.append(autor_nuevo)

                                autor = autor_nuevo

                            else:
                                #Si existe asignar el objeto Autor a la obra actual
                                autor=self.verificar_autor(detalle)

                            tipo=detalle["classification"]
                            anio=detalle["objectDate"]
                            imagen=detalle["primaryImage"]


                            #Crear la obra nueva y añadirla a la lista de obras
                            obra_nueva = Obra(id, titulo, departamento, autor, tipo, anio, imagen)
                            self.obras.append(obra_nueva)

                            #Mostrar la obra
                            print("\n-----------------------------------------------")
                            obra_nueva.show()
                            print("-----------------------------------------------")

                        else:
                            #Si existe, solo mostrar la obra
                            print("\n-----------------------------------------------")
                            obra.show()
                            print("-----------------------------------------------")

                    else:
                        print(f"Error {detalle.status_code}")
                
                inicio += lote
                if inicio >= total:
                    print("No hay más obras.")
                    break
                respuesta = input("¿Mostrar las siguientes 15 obras? (s/n): ").lower()
                if respuesta != "s":
                    print("Finalizando.")
                    break
                time.sleep(2)

    def verificar_obra(self, data, depto):
        """
        Verifica si una obra existe o no existe.
        """
        for obra in self.obras:
            if obra.id == data["objectID"]:
                return obra
        
        return None
    
    def verificar_autor(self, data):
        """
        Verifica si un autor existe o no existe.
        """
        for autor in self.autores:
            if autor.nombre == data["artistDisplayName"]:
                return autor

        return None
    
    def mostrar_imagen(self, id):
        obra_select = None

        for obra in self.obras:
            if obra.id == id:
                obra_select = obra
                break

        url = obra_select.imagen

        self.guardar_imagen()

    def guardar_imagen(self):
        pass

    def buscar_obras_nacionalidad(self):
        """
        Muestra las obras cuyo autor coincide con la nacionalidad elegida.
        """

        # Mostrar opciones de nacionalidades
        indice = 1
        for nacionalidad in self.nacionalidades:
            print(f"{indice}. {nacionalidad}")
            indice+=1

        # Leer y validar selección
        opcion = input("\nIngrese el numero de la nacionalidad: ")
        while (not opcion.isnumeric()) or (not int(opcion) in range(1, indice+1)):
            print("Error!")
            opcion = input("\nIngrese el numero de la nacionalidad: ")

        nacionalidad_select = self.nacionalidades[int(opcion)-1]

        # Filtrar obras por nacionalidad del autor
        obras_nacionalidad = []

        for obra in self.obras:
            if nacionalidad_select.lower() in obra.autor.nacionalidad.lower():
                obras_nacionalidad.append(obra)

        if len(obras_nacionalidad) != 0:
            for obra in obras_nacionalidad:
                print("")
                obra.show()
        else:
            print(f"\nNo se encontraron obras cuya nacionalidad del autor sea: {nacionalidad_select}")


    def buscar_obras_autor(self):
        """
        Busca y muestra todas las obras de un autor por nombre exacto.
        """
        nombre = input("\nIngrese el nombre del autor: ")

        obras_autor = []

        # Recolectar obras cuyo autor coincida exactamente
        for obra in self.obras:
            if obra.autor.nombre.lower() == nombre.lower():
                obras_autor.append(obra)

        # Mostrar resultados o mensaje si no hay coincidencias
        if len(obras_autor) != 0:
            for obra in obras_autor:
                print("")
                obra.show()
        else:
            print(f"\nNo se encontraron obras cuyo autor sea: {nombre}")

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
                if len(self.obras) != 0:
                    self.buscar_obras_nacionalidad()
                else:
                    print("""
\nPor favor realice una busqueda por departamentos para cargar alguna obras y luego poder probar esta funcionalidad
                          """)
            elif opcion == "3":
                if len(self.obras) != 0:
                    self.buscar_obras_autor()
                else:
                    print("""
\nPor favor realice una busqueda por departamentos para cargar alguna obras y luego poder probar esta funcionalidad
                          """)
            elif opcion == "4":
                print("\nAdios!")
                break
            else:
                print("\nOpcion Invalida!\n")