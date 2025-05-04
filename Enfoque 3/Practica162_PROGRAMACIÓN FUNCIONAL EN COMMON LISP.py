;;; =============================================
;;; PROGRAMACIÓN FUNCIONAL EN COMMON LISP
;;; =============================================

;;; ----------------------------
;;; 1. LISTAS (Estructura fundamental)
;;; ----------------------------
(setq numeros '(1 2 3 4 5))
(setq frutas '("manzana" "banana" "naranja"))

;;; ----------------------------
;;; 2. FUNCIONES
;;; ----------------------------
(defun suma (a b)
  "Suma dos números"
  (+ a b))

;; Función de orden superior
(defun aplicar-funcion (func x y)
  "Aplica una función a dos argumentos"
  (funcall func x y))

;;; ----------------------------
;;; 3. LAMBDA (Funciones anónimas)
;;; ----------------------------
(setq doble (lambda (x) (* x 2)))
(setq sumar (lambda (a b) (+ a b)))

;;; ----------------------------
;;; 4. RECURSIVIDAD
;;; ----------------------------
(defun factorial (n)
  "Calcula factorial recursivamente"
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(defun fibonacci (n)
  "Calcula el n-ésimo número de Fibonacci"
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (t (+ (fibonacci (- n 1))
              (fibonacci (- n 2))))))

;;; =============================================
;;; EJEMPLOS PRÁCTICOS
;;; =============================================

;;; Mapcar (equivalente a map)
(print (mapcar doble numeros)) ; (2 4 6 8 10)

;;; Filter (usando remove-if-not)
(print (remove-if-not (lambda (x) (= (mod x 2) 0)) numeros)) ; (2 4)

;;; Reduce
(print (reduce #'+ numeros)) ; 15

;;; Funciones y lambdas
(print (suma 5 3)) ; 8
(print (funcall sumar 5 3)) ; 8
(print (aplicar-funcion #'+ 10 20)) ; 30

;;; Recursividad
(print (factorial 5)) ; 120
(print (fibonacci 6)) ; 8