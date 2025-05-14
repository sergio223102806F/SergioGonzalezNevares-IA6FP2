# -*- coding: utf-8 -*-

# Importación de las bibliotecas necesarias de rdflib
from rdflib import Graph, Namespace, Literal  # Graph para crear el grafo RDF, Namespace para espacios de nombres, Literal para valores literales
from rdflib.namespace import RDF, RDFS  # RDF y RDFS son vocabularios estándar para ontologías

def crear_ontologia():
    """
    Función que crea y retorna una ontología básica sobre educación
    """

    # 1. Creación del grafo RDF que contendrá la ontología
    grafo = Graph()  # Inicializa un grafo RDF vacío

    # 2. Definición del namespace (espacio de nombres) para nuestra ontología
    # Esto evita colisiones con otros vocabularios y permite modularidad
    ex = Namespace("http://ejemplo.org/ontologia#")  # Usamos una URL ficticia como base

    # 3. Añadimos las clases (conceptos principales) de la ontología

    # Clase Persona (clase raíz)
    grafo.add((ex.Persona, RDF.type, RDFS.Class))  # Indica que Persona es una clase
    grafo.add((ex.Persona, RDFS.label, Literal("Persona")))  # Añade un nombre legible

    # Clase Profesor (subclase de Persona)
    grafo.add((ex.Profesor, RDF.type, RDFS.Class))  # Define Profesor como clase
    grafo.add((ex.Profesor, RDFS.subClassOf, ex.Persona))  # Establece herencia de Persona
    grafo.add((ex.Profesor, RDFS.label, Literal("Profesor")))  # Etiqueta legible

    # Clase Estudiante (subclase de Persona)
    grafo.add((ex.Estudiante, RDF.type, RDFS.Class))  # Define Estudiante como clase
    grafo.add((ex.Estudiante, RDFS.subClassOf, ex.Persona))  # Hereda de Persona
    grafo.add((ex.Estudiante, RDFS.label, Literal("Estudiante")))  # Etiqueta legible

    # Clase Curso (clase independiente)
    grafo.add((ex.Curso, RDF.type, RDFS.Class))  # Define Curso como clase
    grafo.add((ex.Curso, RDFS.label, Literal("Curso")))  # Etiqueta legible

    # 4. Añadimos propiedades (relaciones entre clases)

    # Propiedad 'enseña' (relaciona Profesor con Curso)
    grafo.add((ex.enseña, RDF.type, RDF.Property))  # Define 'enseña' como propiedad
    grafo.add((ex.enseña, RDFS.domain, ex.Profesor))  # El dominio (origen) es Profesor
    grafo.add((ex.enseña, RDFS.range, ex.Curso))  # El rango (destino) es Curso

    # Propiedad 'tomaCurso' (relaciona Estudiante con Curso)
    grafo.add((ex.tomaCurso, RDF.type, RDF.Property))  # Define 'tomaCurso' como propiedad
    grafo.add((ex.tomaCurso, RDFS.domain, ex.Estudiante))  # Dominio: Estudiante
    grafo.add((ex.tomaCurso, RDFS.range, ex.Curso))  # Rango: Curso

    # 5. Creamos individuos (instancias concretas de las clases)

    # Instancia de Profesor
    grafo.add((ex.profesorJuan, RDF.type, ex.Profesor))  # Crea individuo profesorJuan
    grafo.add((ex.profesorJuan, RDFS.label, Literal("Juan Pérez")))  # Nombre legible

    # Instancia de Estudiante
    grafo.add((ex.estudianteMaria, RDF.type, ex.Estudiante))  # Crea individuo estudianteMaria
    grafo.add((ex.estudianteMaria, RDFS.label, Literal("María García")))  # Nombre legible

    # Instancia de Curso
    grafo.add((ex.cursoIA, RDF.type, ex.Curso))  # Crea individuo cursoIA
    grafo.add((ex.cursoIA, RDFS.label, Literal("Inteligencia Artificial")))  # Nombre legible

    # 6. Establecemos relaciones entre los individuos

    # Relación: profesorJuan enseña cursoIA
    grafo.add((ex.profesorJuan, ex.enseña, ex.cursoIA))

    # Relación: estudianteMaria toma cursoIA
    grafo.add((ex.estudianteMaria, ex.tomaCurso, ex.cursoIA))

    return grafo  # Retorna el grafo con la ontología completa

def consultar_ontologia(grafo):
    """
    Función que realiza consultas sobre la ontología y muestra resultados
    """
    ex = Namespace("http://ejemplo.org/ontologia#")  # Recuperamos el namespace

    print("\n=== Consultas sobre la Ontología ===")

    # Consulta 1: Listar todas las clases definidas
    print("\nClases definidas:")
    for s, p, o in grafo.triples((None, RDF.type, RDFS.Class)):  # Busca todas las clases
        label = grafo.value(s, RDFS.label)  # Obtiene la etiqueta legible
        print(f"- {label if label else s.split('#')[-1]}")  # Muestra la etiqueta o el nombre

    # Consulta 2: Mostrar profesores y los cursos que enseñan
    print("\nProfesores y sus cursos:")
    for profesor in grafo.subjects(RDF.type, ex.Profesor):  # Busca todos los profesores
        nombre_prof = grafo.value(profesor, RDFS.label)  # Obtiene nombre del profesor
        for curso in grafo.objects(profesor, ex.enseña):  # Busca cursos que enseña
            nombre_curso = grafo.value(curso, RDFS.label)  # Obtiene nombre del curso
            print(f"- {nombre_prof} enseña {nombre_curso}")

    # Consulta 3: Mostrar estudiantes y los cursos que toman
    print("\nEstudiantes y sus cursos:")
    for estudiante in grafo.subjects(RDF.type, ex.Estudiante):  # Busca todos los estudiantes
        nombre_est = grafo.value(estudiante, RDFS.label)  # Obtiene nombre del estudiante
        for curso in grafo.objects(estudiante, ex.tomaCurso):  # Busca cursos que toma
            nombre_curso = grafo.value(curso, RDFS.label)  # Obtiene nombre del curso
            print(f"- {nombre_est} toma {nombre_curso}")

def guardar_ontologia(grafo, archivo="ontologia.ttl"):
    """
    Función que guarda la ontología en un archivo en formato Turtle
    """
    with open(archivo, "w", encoding="utf-8") as f:  # Abre el archivo en modo escritura
        f.write(grafo.serialize(format="turtle").decode("utf-8"))  # Serializa en Turtle
    print(f"\nOntología guardada en {archivo}")

def main():
    """
    Función principal que orquesta la creación, consulta y almacenamiento
    """
    # Paso 1: Crear la ontología
    print("Creando ontología educativa...")
    ontologia = crear_ontologia()

    # Paso 2: Consultar la ontología
    print("\nRealizando consultas...")
    consultar_ontologia(ontologia)

    # Paso 3: Guardar la ontología
    print("\nGuardando ontología...")
    guardar_ontologia(ontologia)

    # Paso 4: Mostrar un fragmento de la ontología serializada
    print("\nFragmento de la ontología en formato Turtle:")
    print(ontologia.serialize(format="turtle").decode("utf-8")[:500] + "...")

if __name__ == "__main__":
    main()  # Ejecuta la función principal si el script es ejecutado directamente
