;;; =============================================
;;; PROGRAMACIÓN FUNCIONAL EN SCHEME
;;; =============================================

;;; ----------------------------
;;; 1. LISTAS
;;; ----------------------------
(define numeros '(1 2 3 4 5)) ; Define una lista llamada 'numeros' con los elementos 1, 2, 3, 4 y 5
(define frutas '("manzana" "banana" "naranja")) ; Define una lista llamada 'frutas' con nombres de frutas

;;; ----------------------------
;;; 2. FUNCIONES
;;; ----------------------------
(define (suma a b) ; Define una función llamada 'suma' que toma dos argumentos, 'a' y 'b'
  "Suma dos números" ; Docstring: Descripción de la función
  (+ a b)) ; Suma 'a' y 'b' y devuelve el resultado

;; Función de orden superior
(define (aplicar-funcion func x y) ; Define una función llamada 'aplicar-funcion' que toma una función 'func' y dos argumentos 'x' e 'y'
  (func x y)) ; Llama a la función 'func' con los argumentos 'x' e 'y'

;;; ----------------------------
;;; 3. LAMBDA
;;; ----------------------------
(define doble (lambda (x) (* x 2))) ; Define una función anónima (lambda) que multiplica 'x' por 2 y la asigna a la variable 'doble'
(define sumar (lambda (a b) (+ a b))) ; Define una función anónima (lambda) que suma 'a' y 'b' y la asigna a la variable 'sumar'

;;; ----------------------------
;;; 4. RECURSIVIDAD
;;; ----------------------------
(define (factorial n) ; Define una función recursiva llamada 'factorial' que calcula el factorial de un número 'n'
  (if (= n 0) ; Si 'n' es igual a 0 (caso base)
      1 ; Devuelve 1
      (* n (factorial (- n 1))))) ; De lo contrario, multiplica 'n' por el resultado de llamar recursivamente a 'factorial' con 'n-1'

(define (fibonacci n) ; Define una función recursiva llamada 'fibonacci' que calcula el n-ésimo número de Fibonacci
  (cond ((= n 0) 0) ; Si 'n' es 0, devuelve 0
        ((= n 1) 1) ; Si 'n' es 1, devuelve 1
        (else (+ (fibonacci (- n 1)) ; De lo contrario, calcula el resultado sumando los dos números de Fibonacci anteriores
                 (fibonacci (- n 2))))))

;;; =============================================
;;; EJEMPLOS PRÁCTICOS
;;; =============================================

;;; Map
(display (map doble numeros)) (newline) ; (2 4 6 8 10) ; Aplica la función 'doble' a cada elemento de la lista 'numeros'

;;; Filter
(display (filter (lambda (x) (= (modulo x 2) 0)) numeros)) (newline) ; (2 4) ; Filtra los números pares de la lista 'numeros'

;;; Reduce (fold-left en Scheme)
(display (fold-left + 0 numeros)) (newline) ; 15 ; Suma todos los elementos de la lista 'numeros' usando 'fold-left'

;;; Funciones y lambdas
(display (suma 5 3)) (newline) ; 8 ; Llama a la función 'suma' con los argumentos 5 y 3
(display (sumar 5 3)) (newline) ; 8 ; Llama a la función anónima 'sumar' con los argumentos 5 y 3
(display (aplicar-funcion + 10 20)) (newline) ; 30 ; Llama a la función 'aplicar-funcion' con la función '+' y los argumentos 10 y 20

;;; Recursividad
(display (factorial 5)) (newline) ; 120 ; Llama a la función 'factorial' con el argumento 5
(display (fibonacci 6)) (newline) ; 8 ; Llama a la función 'fibonacci' con el argumento 6
