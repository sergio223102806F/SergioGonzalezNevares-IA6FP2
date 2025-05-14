;;; =============================================
;;; PROGRAMACIÓN FUNCIONAL EN COMMON LISP
;;; =============================================

;;; ----------------------------
;;; 1. LISTAS (Estructura fundamental)
;;; ----------------------------
(setq numeros '(1 2 3 4 5)) ; Crea una lista llamada 'numeros' con los elementos 1, 2, 3, 4 y 5
(setq frutas '("manzana" "banana" "naranja")) ; Crea una lista llamada 'frutas' con nombres de frutas

;;; ----------------------------
;;; 2. FUNCIONES
;;; ----------------------------
(defun suma (a b) ; Define una función llamada 'suma' que toma dos argumentos, 'a' y 'b'
  "Suma dos números" ; Docstring: Descripción de la función
  (+ a b)) ; Suma 'a' y 'b' y devuelve el resultado

;; Función de orden superior
(defun aplicar-funcion (func x y) ; Define una función llamada 'aplicar-funcion'
  "Aplica una función a dos argumentos" ; Docstring
  (funcall func x y)) ; Llama a la función 'func' con los argumentos 'x' e 'y'

;;; ----------------------------
;;; 3. LAMBDA (Funciones anónimas)
;;; ----------------------------
(setq doble (lambda (x) (* x 2))) ; Crea una función anónima que multiplica un número por 2 y la asigna a 'doble'
(setq sumar (lambda (a b) (+ a b))) ; Crea una función anónima que suma dos números y la asigna a 'sumar'

;;; ----------------------------
;;; 4. RECURSIVIDAD
;;; ----------------------------
(defun factorial (n) ; Define una función recursiva llamada 'factorial'
  "Calcula factorial recursivamente" ; Docstring
  (if (= n 0) ; Si 'n' es 0
      1 ; Devuelve 1 (caso base)
      (* n (factorial (- n 1))))) ; De lo contrario, multiplica 'n' por el factorial de 'n-1'

(defun fibonacci (n) ; Define una función recursiva llamada 'fibonacci'
  "Calcula el n-ésimo número de Fibonacci" ; Docstring
  (cond ((= n 0) 0) ; Si 'n' es 0, devuelve 0
        ((= n 1) 1) ; Si 'n' es 1, devuelve 1
        (t (+ (fibonacci (- n 1)) ; De lo contrario, calcula la suma de los dos números de Fibonacci anteriores
              (fibonacci (- n 2))))))

;;; =============================================
;;; EJEMPLOS PRÁCTICOS
;;; =============================================

;;; Mapcar (equivalente a map)
(print (mapcar doble numeros)) ; (2 4 6 8 10) ; Aplica la función 'doble' a cada elemento de 'numeros'

;;; Filter (usando remove-if-not)
(print (remove-if-not (lambda (x) (= (mod x 2) 0)) numeros)) ; (2 4) ; Filtra los números pares de 'numeros'

;;; Reduce
(print (reduce #'+ numeros)) ; 15 ; Suma todos los elementos de 'numeros'

;;; Funciones y lambdas
(print (suma 5 3)) ; 8 ; Llama a la función 'suma'
(print (funcall sumar 5 3)) ; 8 ; Llama a la función anónima 'sumar' usando 'funcall'
(print (aplicar-funcion #'+ 10 20)) ; 30 ; Llama a 'aplicar-funcion' con la función '+'

;;; Recursividad
(print (factorial 5)) ; 120 ; Llama a la función 'factorial'
(print (fibonacci 6)) ; 8 ; Llama a la función 'fibonacci'
