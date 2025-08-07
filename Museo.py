import requests

class Museo:
    def __init__(self):
        self.departamentos = []
        self.autores = []
        self.obras = []
        self.nacionalidades = []

    def cargar_api(self):
        pass

    def cargar_csv(self):
        pass

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
                pass
            elif opcion == "2":
                pass
            elif opcion == "3":
                pass
            elif opcion == "4":
                print("\nAdios!")
                break
            else:
                print("\nOpcion Invalida!\n")