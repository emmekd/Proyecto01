class Usuario:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email
        
    def mostrarInfo(self):
        return f"{self.nombre} ({self.email})"
        
class Estudiantes(Usuario):
    def __init__(self, id, nombre, email):
        super().__init__(nombre, email)
        self.id = id
        self.cursos = [] # Cursos inscritos
        self.calificaciones = {} # Calificaciones por curso
        
    def inscribirCurso(self, curso):
        if curso not in self.cursos:
            self.cursos.append(curso)
            curso.estudiantes.append(self)
        else:
            raise ValueError("Ya esta inscrito en este curso")
        
    def verNotas(self, curso):
        return {eval_id: self.calificaciones.get((curso.id, eval_id)) for eval_id in curso.evaluaciones.keys()}
       
class Catedratico(Usuario):
    def __init__(self, nombre, email):
        super().__init__(nombre, email)
        self.cursos = [] # Lista de cursos que da
        
    def crearCurso(self, codigo, nombre):
        curso = Curso(codigo, nombre, self)
        self.cursos.append(curso)
        return curso
    
    def asignarNota(self, estudiante, evaluacion, nota):
        if nota < 0 or nota > evaluacion.puntaje_max:
            raise ValueError("Nota fuera de rango")
        estudiante.calificaciones[(evaluacion.curso.id, evaluacion.id)] = nota

class Curso:
    def __init__(self, codigo, nombre, catedratico):
        self.id = codigo
        self.nombre = nombre
        self.catedratico = catedratico
        self.estudiantes = []
        self.evaluaciones = {}
        
    def agregarEvaluacion(self, evaluacion):
        self.evaluaciones[evaluacion.id] = evaluacion

class Evaluacion:
    def __init__(self, id, tipo, puntaje_max, curso):
        self.id = id
        self.tipo = tipo
        self.puntaje_max = puntaje_max
        self.curso = curso
        self.calificaciones = {}

class Examen(Evaluacion):
    def __init__(self, id, puntaje_max, curso, tiempoMin):
        super().__init__(id, "Examen", puntaje_max, curso)
        self.tiempoMin = tiempoMin

class Tarea(Evaluacion):
    def __init__(self, id, puntaje_max, curso, fechaEntrega):
        super().__init__(id, "Tarea", puntaje_max, curso)
        self.fechaEntrega = fechaEntrega
            
# Uso
if __name__ == "__main__":
    # Crear profesor
    profesor = Catedratico("Dr. Martinez", "gabmartinez@edu.com")
    print("INFORMACIÓN DEL CATEDRÁTICO")
    print(f"Profesor: {profesor.mostrarInfo()}")
    
    # Crear curso
    curso = profesor.crearCurso("C204", "Introduccion a la Programacion")
    print(f"Curso creado: {curso.nombre} (Código: {curso.id})")
    print(f"Profesor del curso: {curso.catedratico.mostrarInfo()}")
    
    # Crear y inscribir estudiante
    alumno = Estudiantes("A1001", "Ana Gomez", "anagomez@emai.com")
    print(f"\nINFORMACIÓN DEL ESTUDIANTE")
    print(f"Estudiante: {alumno.mostrarInfo()}")
    print(f"ID del estudiante: {alumno.id}")
    
    # Inscribir al curso
    alumno.inscribirCurso(curso)
    print(f"Estudiante inscrito en: {curso.nombre}")
    
    # Mostrar estudiantes del curso
    print(f"\nESTUDIANTES INSCRITOS EN {curso.nombre}")
    for estudiante in curso.estudiantes:
        print(f"- {estudiante.mostrarInfo()} (ID: {estudiante.id})")
    
    # Crear evaluación
    examen1 = Examen("E1", 100, curso, 90)
    curso.agregarEvaluacion(examen1)
    print(f"\nEVALUACIONES DEL CURSO")
    for eval_id, evaluacion in curso.evaluaciones.items():
        print(f"- {evaluacion.tipo} {eval_id}: {evaluacion.puntaje_max} puntos")
        if hasattr(evaluacion, 'tiempoMin'):
            print(f"  Tiempo: {evaluacion.tiempoMin} minutos")
    
    # Asignar nota
    profesor.asignarNota(alumno, examen1, 85)
    print(f"\nNOTAS ASIGNADAS")
    print(f"Nota asignada a {alumno.nombre} en {examen1.tipo} {examen1.id}: 85/{examen1.puntaje_max}")
    
    # Mostrar todas las notas del estudiante
    print(f"\nREPORTE DE NOTAS DE {alumno.nombre}")
    notas = alumno.verNotas(curso)
    for evaluacion_id, nota in notas.items():
        if nota is not None:
            evaluacion = curso.evaluaciones[evaluacion_id]
            print(f"{evaluacion.tipo} {evaluacion_id}: {nota}/{evaluacion.puntaje_max} puntos")
        else:
            print(f"Evaluación {evaluacion_id}: Sin calificar")