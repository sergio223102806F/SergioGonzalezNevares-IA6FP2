;;; =============================================
;;; PROGRAMACIÓN FUNCIONAL EN SCHEME
;;; =============================================

;;; ----------------------------
;;; 1. LISTAS
;;; ----------------------------
(define numeros '(1 2 3 4 5))
(define frutas '("manzana" "banana" "naranja"))

;;; ----------------------------
;;; 2. FUNCIONES
;;; ----------------------------
(define (suma a b)
  "Suma dos números"
  (+ a b))

;; Función de orden superior
(define (aplicar-funcion func x y)
  (func x y))

;;; ----------------------------
;;; 3. LAMBDA
;;; ----------------------------
(define doble (lambda (x) (* x 2)))
(define sumar (lambda (a b) (+ a b)))

;;; ----------------------------
;;; 4. RECURSIVIDAD
;;; ----------------------------
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(define (fibonacci n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (else (+ (fibonacci (- n 1))
                (fibonacci (- n 2))))))

;;; =============================================
;;; EJEMPLOS PRÁCTICOS
;;; =============================================

;;; Map
(display (map doble numeros)) (newline) ; (2 4 6 8 10)

;;; Filter
(display (filter (lambda (x) (= (modulo x 2) 0)) numeros)) (newline) ; (2 4)

;;; Reduce (fold-left en Scheme)
(display (fold-left + 0 numeros)) (newline) ; 15

;;; Funciones y lambdas
(display (suma 5 3)) (newline) ; 8
(display (sumar 5 3)) (newline) ; 8
(display (aplicar-funcion + 10 20)) (newline) ; 30

;;; Recursividad
(display (factorial 5)) (newline) ; 120
(display (fibonacci 6)) (newline) ; 8