class Autor:
    def __init__(self, nombre, nacionalidad, nacimiento, muerte):
        self.nombre = nombre
        self.nacionalidad = nacionalidad
        self.nacimiento = nacimiento
        self.muerte = muerte

    def show(self):
        """
        Mostrar atributos del Autor
        """
        print(f"-Nombre Completo: {self.nombre}")
        print(f"-Nacionalidad: {self.nacionalidad}")
        print(f"-Fecha de Nacimiento: {self.nacimiento}")
        print(f"-Fecha de Muerte: {self.muerte}")
        