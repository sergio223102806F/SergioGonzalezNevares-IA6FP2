"""
ENCAPSULADO EN PYTHON - 
--------------------TACI----------------------------
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
    banco = "Banco Nacional"  # Público
    
    def __init__(self, titular: str, saldo_inicial: float = 0):
        """
        Constructor - Inicializa los atributos de la cuenta
        
        Args:
            titular: Nombre del titular (público)
            saldo_inicial: Saldo inicial (protegido)
        """
        # Atributo público - Accesible directamente
        self.titular = titular
        
        # Atributo protegido (convención: _nombre) - "Sugerencia" de no acceso externo
        self._saldo = saldo_inicial  # Debería ser accedido solo por la clase/subclases
        
        # Atributo privado (convención: __nombre) - Name mangling aplicado
        self.__pin = "1234"  # Python renombra este atributo para "ocultarlo"
        
        # Atributo público que usa métodos protegidos/privados internamente
        self.numero_transacciones = 0
    
    # ============ MÉTODOS PÚBLICOS ============
    def depositar(self, monto: float) -> None:
        """
        Método público para depositar dinero.
        Valida el monto y actualiza el saldo.
        """
        if monto > 0:
            self._actualizar_saldo(monto)
            self.__registrar_transaccion("deposito", monto)
            print(f"Depósito exitoso. Nuevo saldo: ${self._saldo:.2f}")
        else:
            print("Error: El monto debe ser positivo")
    
    def retirar(self, monto: float, pin: str) -> None:
        """
        Método público para retirar dinero.
        Requiere validación de PIN.
        """
        if not self.__validar_pin(pin):
            print("Error: PIN incorrecto")
            return
        
        if monto > 0 and monto <= self._saldo:
            self._actualizar_saldo(-monto)
            self.__registrar_transaccion("retiro", monto)
            print(f"Retiro exitoso. Nuevo saldo: ${self._saldo:.2f}")
        else:
            print("Error: Monto inválido o fondos insuficientes")
    
    def consultar_saldo(self) -> float:
        """Método público para consultar el saldo"""
        return self._saldo
    
    # ============ MÉTODOS PROTEGIDOS ============
    def _actualizar_saldo(self, cambio: float) -> None:
        """
        Método protegido para modificar el saldo.
        Para uso interno o por subclases.
        """
        self._saldo += cambio
    
    # ============ MÉTODOS PRIVADOS ============
    def __validar_pin(self, pin_ingresado: str) -> bool:
        """
        Método privado para validar el PIN.
        Python aplica name mangling: _CuentaBancaria__validar_pin
        """
        return self.__pin == pin_ingresado
    
    def __registrar_transaccion(self, tipo: str, monto: float) -> None:
        """
        Método privado para registrar transacciones.
        """
        self.numero_transacciones += 1
        print(f"Transacción #{self.numero_transacciones}: {tipo} ${monto:.2f}")

# ============ SUBCLASE QUE HEREDA ============
class CuentaDeAhorros(CuentaBancaria):
    """
    Subclase que demuestra el acceso a miembros protegidos
    y la imposibilidad de acceder a miembros privados directamente.
    """
    
    def __init__(self, titular: str, saldo_inicial: float = 0, interes: float = 0.01):
        super().__init__(titular, saldo_inicial)
        self._interes = interes  # Atributo protegido
    
    def aplicar_interes(self) -> None:
        """Método público que usa miembros protegidos de la clase base"""
        interes = self._saldo * self._interes  # Acceso a _saldo (protegido)
        self._actualizar_saldo(interes)        # Llamada a método protegido
        self.__registrar_transaccion("interés", interes)  # Error (método privado)
        # Python intentará llamar a _CuentaDeAhorros__registrar_transaccion
    
    # Podríamos acceder al método privado de la clase base así (no recomendado):
    def _acceder_metodo_privado(self):
        return self._CuentaBancaria__validar_pin("1234")  # Name mangling explícito

# ============ DEMOSTRACIÓN DE USO ============
def demostrar_encapsulamiento():
    """Función que demuestra los diferentes niveles de acceso"""
    print("\n=== DEMOSTRACIÓN DE ENCAPSULAMIENTO ===")
    
    # 1. Crear una cuenta bancaria
    cuenta = CuentaBancaria("Juan Pérez", 1000)
    print(f"\n1. Cuenta creada para {cuenta.titular} en {cuenta.banco}")
    
    # 2. Acceso a atributos públicos
    print("\n2. Acceso a miembros públicos:")
    print(f" - Titular: {cuenta.titular}")
    print(f" - Banco: {cuenta.banco}")
    print(f" - Saldo inicial: ${cuenta.consultar_saldo():.2f}")
    
    # 3. Acceso a atributos protegidos (no recomendado, pero posible)
    print("\n3. Acceso a miembros protegidos (no recomendado):")
    print(f" - Saldo (acceso directo): ${cuenta._saldo:.2f}")
    cuenta._actualizar_saldo(100)  # Llamada directa a método protegido
    print(f" - Saldo después de actualización: ${cuenta._saldo:.2f}")
    
    # 4. Intentar acceso a atributos privados (fallará)
    print("\n4. Intentar acceso a miembros privados:")
    try:
        print(f" - PIN (acceso directo): {cuenta.__pin}")  # AttributeError
    except AttributeError as e:
        print(f" - Error al acceder: {e}")
    
    # 5. Uso correcto a través de métodos públicos
    print("\n5. Operaciones a través de métodos públicos:")
    cuenta.depositar(500)
    cuenta.retirar(200, "1234")  # PIN correcto
    cuenta.retirar(200, "0000")  # PIN incorrecto
    
    # 6. Demostración en subclase
    print("\n6. Demostración en subclase CuentaDeAhorros:")
    ahorros = CuentaDeAhorros("María García", 2000, 0.02)
    print(f" - Saldo inicial: ${ahorros.consultar_saldo():.2f}")
    ahorros.aplicar_interes()  # Generará error por el método privado
    
    # 7. Acceso name mangling (no recomendado en código normal)
    print("\n7. Acceso forzado con name mangling (no recomendado):")
    print(f" - PIN (acceso forzado): {ahorros._CuentaBancaria__pin}")
    print(f" - Validar PIN: {ahorros._acceder_metodo_privado()}")

# ============ BUENAS PRÁCTICAS ============
class EjemploBuenasPracticas:
    """
    Clase que muestra el uso recomendado de encapsulamiento.
    """
    
    def __init__(self):
        self.atributo_publico = "Accesible desde cualquier lugar"
        self._atributo_protegido = "Solo para clase/subclases (convención)"
        self.__atributo_privado = "Realmente privado (name mangling)"
    
    def metodo_publico(self):
        """Interfaz pública para interactuar con el objeto"""
        return self.__metodo_privado()
    
    def _metodo_protegido(self):
        """Para uso interno o por subclases"""
        pass
    
    def __metodo_privado(self):
        """Implementación interna que no debería ser accedida externamente"""
        return "Datos sensibles"

if __name__ == "__main__":
    demostrar_encapsulamiento()
    
    print("\n=== BUENAS PRÁCTICAS ===")
    ejemplo = EjemploBuenasPracticas()
    print(" - Uso correcto:", ejemplo.metodo_publico())
    print(" - Acceso directo a protegido:", ejemplo._atributo_protegido)
    print(" - Intento acceso privado:", end=" ")
    try:
        print(ejemplo.__atributo_privado)
    except AttributeError as e:
        print(e)