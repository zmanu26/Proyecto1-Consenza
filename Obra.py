class Obra:
    def __init__(self, id, titulo, departamento, autor, clasificacion, anio, imagen):
        self.id = id
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
        print(f"-ID: {self.id}")
        print(f"-Título: {self.titulo}")
        print(f"-Departamento: {self.departamento.nombre}\n")
        print("-Autor:")
        self.autor.show()
        print(f"\n-Clasificación: {self.clasificacion}")
        print(f"-Año de Creación: {self.anio}")
        print(f"-Imagen: {self.imagen}")