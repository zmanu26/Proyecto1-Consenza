class Obra:
    def __init__(self, titulo, departamento, autor, clasificacion, anio, imagen):
        self.titulo = titulo
        self.departamento = departamento
        self.autor = autor
        self.clasificacion = clasificacion
        self.anio = anio
        self.imagen = imagen
    
    def show(self):
        """
        Mostrar atributos de la Obra
        """
        print(f"-Título: {self.titulo}")
        print(f"-Departamento: {self.departamento.nombre}")
        print(f"-Autor: {self.autor.nombre}")
        print(f"-Clasificación: {self.clasificacion}")
        print(f"-Año de Creación: {self.anio}")
        print(f"-Imagen: {self.imagen}")