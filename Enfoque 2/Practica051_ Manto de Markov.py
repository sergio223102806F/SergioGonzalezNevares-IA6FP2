from collections import defaultdict

class MarkovBlanket:
    def __init__(self):
        """Inicializa estructura para almacenar relaciones en una red bayesiana"""
        self.parents = defaultdict(list)  # {nodo: [padres]}
        self.children = defaultdict(list) # {nodo: [hijos]}
        self.spouses = defaultdict(list)  # {nodo: [cónyuges]}

    def add_relation(self, parent: str, child: str):
        """Añade una relación padre-hijo a la red"""
        self.parents[child].append(parent)  # Añade padre al hijo
        self.children[parent].append(child) # Añade hijo al padre
        
        # Actualiza cónyuges (otros padres de los hijos)
        for spouse in self.parents[child]:
            if spouse != parent and spouse not in self.spouses[parent]:
                self.spouses[parent].append(spouse)
                self.spouses[spouse].append(parent)

    def get_markov_blanket(self, node: str) -> list:
        """Obtiene el Manto de Markov de un nodo (padres + hijos + cónyuges)"""
        blanket = []
        blanket.extend(self.parents[node])    # Padres directos
        blanket.extend(self.children[node])   # Hijos directos
        blanket.extend(self.spouses[node])    # Cónyuges (otros padres de los hijos)
        return list(set(blanket))  # Elimina duplicados

# Ejemplo: Diagnóstico médico con Manto de Markov
if __name__ == "__main__":
    print("=== Manto de Markov en Red Bayesiana (Ejemplo Médico) ===")
    mb = MarkovBlanket()

    # Definir relaciones (padre -> hijo)
    mb.add_relation("Fiebre", "Gripe")       # Fiebre -> Gripe
    mb.add_relation("Tos", "Gripe")          # Tos -> Gripe
    mb.add_relation("Gripe", "Fatiga")       # Gripe -> Fatiga
    mb.add_relation("Gripe", "Dolor_Cabeza") # Gripe -> Dolor de cabeza
    mb.add_relation("Alergia", "Tos")        # Alergia -> Tos

    # Obtener Manto de Markov de "Gripe"
    nodo = "Gripe"
    blanket = mb.get_markov_blanket(nodo)

    print(f"\nManto de Markov de '{nodo}':")
    print(" - Padres:", mb.parents[nodo])         # ["Fiebre", "Tos"]
    print(" - Hijos:", mb.children[nodo])         # ["Fatiga", "Dolor_Cabeza"]
    print(" - Cónyuges:", mb.spouses[nodo])       # ["Alergia"] (porque Alergia también causa Tos)
    print("\nTotal:", blanket)                    # ["Fiebre", "Tos", "Fatiga", "Dolor_Cabeza", "Alergia"]
