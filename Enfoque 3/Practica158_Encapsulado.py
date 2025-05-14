"""
ENCAPSULADO EN PYTHON -
-----------------------------------------------------------
Este código demuestra los niveles de acceso en Python:
1. Público - Accesible desde cualquier lugar
2. Protegido (_prefijo) - Convención para acceso interno/clases hijas
3. Privado (__prefijo) - Name mangling para restringir acceso
"""

# ============ CLASE BASE DEMOSTRATIVA ============
class CuentaBancaria:
    """
    Clase que demuestra los diferentes niveles de encapsulamiento.
    Python no tiene verdaderos atributos privados, pero usa convenciones.
    """
    
    # Atributo de clase público (compartido por todas las instancias)
    banco = "Banco Nacional"  # Público # Atributo de clase público: nombre del banco
    
    def __init__(self, titular: str, saldo_inicial: float = 0):
        """
        Constructor - Inicializa los atributos de la cuenta
        
        Args:
            titular: Nombre del titular (público)
            saldo_inicial: Saldo inicial (protegido)
        """
        # Atributo público - Accesible directamente
        self.titular = titular # Atributo de instancia público: nombre del titular de la cuenta
        
        # Atributo protegido (convención: _nombre) - "Sugerencia" de no acceso externo
        self._saldo = saldo_inicial  # Debería ser accedido solo por la clase/subclases # Atributo de instancia protegido: saldo de la cuenta
        
        # Atributo privado (convención: __nombre) - Name mangling aplicado
        self.__pin = "1234"  # Python renombra este atributo para "ocultarlo" # Atributo de instancia privado: PIN de la cuenta
        
        # Atributo público que usa métodos protegidos/privados internamente
        self.numero_transacciones = 0 # Atributo de instancia público: número de transacciones realizadas en la cuenta
    
    # ============ MÉTODOS PÚBLICOS ============
    def depositar(self, monto: float) -> None:
        """
        Método público para depositar dinero.
        Valida el monto y actualiza el saldo.
        """
        if monto > 0: # Si el monto es mayor que cero
            self._actualizar_saldo(monto) # Llama al método protegido para actualizar el saldo
            self.__registrar_transaccion("deposito", monto) # Llama al método privado para registrar la transacción
            print(f"Depósito exitoso. Nuevo saldo: ${self._saldo:.2f}") # Imprime un mensaje de éxito
        else: # Si el monto no es válido
            print("Error: El monto debe ser positivo") # Imprime un mensaje de error
    
    def retirar(self, monto: float, pin: str) -> None:
        """
        Método público para retirar dinero.
        Requiere validación de PIN.
        """
        if not self.__validar_pin(pin): # Si el PIN es incorrecto
            print("Error: PIN incorrecto") # Imprime un mensaje de error
            return # Sale de la función
        
        if monto > 0 and monto <= self._saldo: # Si el monto es válido y hay suficiente saldo
            self._actualizar_saldo(-monto) # Llama al método protegido para actualizar el saldo
            self.__registrar_transaccion("retiro", monto) # Llama al método privado para registrar la transacción
            print(f"Retiro exitoso. Nuevo saldo: ${self._saldo:.2f}") # Imprime un mensaje de éxito
        else: # Si el monto no es válido o no hay suficiente saldo
            print("Error: Monto inválido o fondos insuficientes") # Imprime un mensaje de error
    
    def consultar_saldo(self) -> float:
        """Método público para consultar el saldo"""
        return self._saldo # Devuelve el saldo actual (accediendo al atributo protegido)
    
    # ============ MÉTODOS PROTEGIDOS ============
    def _actualizar_saldo(self, cambio: float) -> None:
        """
        Método protegido para modificar el saldo.
        Para uso interno o por subclases.
        """
        self._saldo += cambio # Modifica el saldo sumando o restando el cambio
    
    # ============ MÉTODOS PRIVADOS ============
    def __validar_pin(self, pin_ingresado: str) -> bool:
        """
        Método privado para validar el PIN.
        Python aplica name mangling: _CuentaBancaria__validar_pin
        """
        return self.__pin == pin_ingresado # Compara el PIN ingresado con el PIN de la cuenta
    
    def __registrar_transaccion(self, tipo: str, monto: float) -> None:
        """
        Método privado para registrar transacciones.
        """
        self.numero_transacciones += 1 # Incrementa el número de transacciones
        print(f"Transacción #{self.numero_transacciones}: {tipo} ${monto:.2f}") # Imprime los detalles de la transacción

# ============ SUBCLASE QUE HEREDA ============
class CuentaDeAhorros(CuentaBancaria):
    """
    Subclase que demuestra el acceso a miembros protegidos
    y la imposibilidad de acceder a miembros privados directamente.
    """
    
    def __init__(self, titular: str, saldo_inicial: float = 0, interes: float = 0.01):
        super().__init__(titular, saldo_inicial) # Llama al constructor de la clase base
        self._interes = interes  # Atributo protegido # Atributo de instancia protegido: tasa de interés de la cuenta de ahorros
    
    def aplicar_interes(self) -> None:
        """Método público que usa miembros protegidos de la clase base"""
        interes = self._saldo * self._interes  # Acceso a _saldo (protegido) # Calcula el interés
        self._actualizar_saldo(interes)         # Llamada a método protegido # Actualiza el saldo con el interés
        self.__registrar_transaccion("interés", interes)  # Error (método privado) # Intenta llamar al método privado de la clase base (generará un error)
        # Python intentará llamar a _CuentaDeAhorros__registrar_transaccion
    
    # Podríamos acceder al método privado de la clase base así (no recomendado):
    def _acceder_metodo_privado(self):
        return self._CuentaBancaria__validar_pin("1234")  # Name mangling explícito # Accede al método privado de la clase base usando name mangling (no recomendado)

# ============ DEMOSTRACIÓN DE USO ============
def demostrar_encapsulamiento():
    """Función que demuestra los diferentes niveles de acceso"""
    print("\n=== DEMOSTRACIÓN DE ENCAPSULAMIENTO ===")
    
    # 1. Crear una cuenta bancaria
    cuenta = CuentaBancaria("Juan Pérez", 1000) # Crea una instancia de la clase CuentaBancaria
    print(f"\n1. Cuenta creada para {cuenta.titular} en {cuenta.banco}") # Imprime los detalles de la cuenta
    
    # 2. Acceso a atributos públicos
    print("\n2. Acceso a miembros públicos:")
    print(f" - Titular: {cuenta.titular}") # Accede al atributo público titular
    print(f" - Banco: {cuenta.banco}") # Accede al atributo de clase público banco
    print(f" - Saldo inicial: ${cuenta.consultar_saldo():.2f}") # Llama al método público consultar_saldo()
    
    # 3. Acceso a atributos protegidos (no recomendado, pero posible)
    print("\n3. Acceso a miembros protegidos (no recomendado):")
    print(f" - Saldo (acceso directo): ${cuenta._saldo:.2f}") # Accede directamente al atributo protegido _saldo
    cuenta._actualizar_saldo(100)  # Llamada directa a método protegido # Llama directamente al método protegido _actualizar_saldo()
    print(f" - Saldo después de actualización: ${cuenta._saldo:.2f}") # Imprime el saldo actualizado
    
    # 4. Intentar acceso a atributos privados (fallará)
    print("\n4. Intentar acceso a miembros privados:")
    try:
        print(f" - PIN (acceso directo): {cuenta.__pin}")  # AttributeError # Intenta acceder directamente al atributo privado __pin (generará un error)
    except AttributeError as e: # Captura el error AttributeError
        print(f" - Error al acceder: {e}") # Imprime el mensaje de error
    
    # 5. Uso correcto a través de métodos públicos
    print("\n5. Operaciones a través de métodos públicos:")
    cuenta.depositar(500) # Llama al método público depositar()
    cuenta.retirar(200, "1234")  # PIN correcto # Llama al método público retirar() con el PIN correcto
    cuenta.retirar(200, "0000")  # PIN incorrecto # Llama al método público retirar() con el PIN incorrecto
    
    # 6. Demostración en subclase
    print("\n6. Demostración en subclase CuentaDeAhorros:")
    ahorros = CuentaDeAhorros("María García", 2000, 0.02) # Crea una instancia de la subclase CuentaDeAhorros
    print(f" - Saldo inicial: ${ahorros.consultar_saldo():.2f}") # Imprime el saldo inicial
    ahorros.aplicar_interes()  # Generará error por el método privado # Llama al método aplicar_interes() que intenta acceder a un método privado
    
    # 7. Acceso name mangling (no recomendado en código normal)
    print("\n7. Acceso forzado con name mangling (no recomendado):")
    print(f" - PIN (acceso forzado): {ahorros._CuentaBancaria__pin}") # Accede al atributo privado __pin de la clase base usando name mangling
    print(f" - Validar PIN: {ahorros._acceder_metodo_privado()}") # Llama al método _acceder_metodo_privado() que accede al método privado de la clase base
    
# ============ BUENAS PRÁCTICAS ============
class EjemploBuenasPracticas:
    """
    Clase que muestra el uso recomendado de encapsulamiento.
    """
    
    def __init__(self):
        self.atributo_publico = "Accesible desde cualquier lugar" # Atributo público
        self._atributo_protegido = "Solo para clase/subclases (convención)" # Atributo protegido
        self.__atributo_privado = "Realmente privado (name mangling)" # Atributo privado
    
    def metodo_publico(self):
        """Interfaz pública para interactuar con el objeto"""
        return self.__metodo_privado() # Llama al método privado __metodo_privado()
    
    def _metodo_protegido(self):
        """Para uso interno o por subclases"""
        pass # Método protegido
    
    def __metodo_privado(self):
        """Implementación interna que no debería ser accedida externamente"""
        return "Datos sensibles" # Método privado
    
if __name__ == "__main__":
    demostrar_encapsulamiento() # Llama a la función para demostrar el encapsulamiento
    
    print("\n=== BUENAS PRÁCTICAS ===")
    ejemplo = EjemploBuenasPracticas() # Crea una instancia de la clase EjemploBuenasPracticas
    print(" - Uso correcto:", ejemplo.metodo_publico()) # Llama al método público metodo_publico()
    print(" - Acceso directo a protegido:", ejemplo._atributo_protegido) # Accede directamente al atributo protegido _atributo_protegido
    print(" - Intento acceso privado:", end=" ")
    try:
        print(ejemplo.__atributo_privado) # Intenta acceder directamente al atributo privado __atributo_privado (generará un error)
    except AttributeError as e:
        print(e) # Imprime el mensaje de error
