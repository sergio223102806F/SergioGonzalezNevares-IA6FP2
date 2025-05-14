; Sistema Difuso en Fuzzy CLIPS

; ----------------------------
; 1. HECHOS DIFUSOS
; ----------------------------
(deffacts hechos-iniciales
    (habilidad_volar pajaro 0.9)  ; Define el hecho difuso: el pájaro tiene una habilidad de volar de 0.9
    (habilidad_volar pinguino 0.1)) ; Define el hecho difuso: el pingüino tiene una habilidad de volar de 0.1

; ----------------------------
; 2. REGLAS DIFUSAS
; ----------------------------
(defrule regla-vuelo-difuso
    (habilidad_volar ?animal ?grado) ; Si existe un animal con un grado de habilidad de volar
    (test (> ?grado 0.5))       ; Y si el grado es mayor que 0.5
    =>
    (assert (puede_volar ?animal (round ?grado)))) ; Entonces, afirma que el animal puede volar con el grado de confianza redondeado

; ----------------------------
; 3. FUNCIONES DIFUSAS
; ----------------------------
(deffunction fuzzy-and (?a ?b)
    (min ?a ?b))                ; Define la función difusa AND: el mínimo de dos valores

(deffunction fuzzy-or (?a ?b)
    (max ?a ?b))                ; Define la función difusa OR: el máximo de dos valores

; ----------------------------
; 4. INFERENCIA DIFUSA
; ----------------------------
(defrule clasificar-vuelo
    ?h <- (habilidad_volar ?animal ?grado) ; Captura el hecho de la habilidad de volar de un animal
    =>
    (if (>= ?grado 0.7) then             ; Si el grado es mayor o igual a 0.7
        (assert (excelente_volador ?animal))) ; Afirma que el animal es un excelente volador
    else if (>= ?grado 0.4) then        ; De lo contrario, si el grado es mayor o igual a 0.4
        (assert (volador_regular ?animal))))  ; Afirma que el animal es un volador regular

; ----------------------------
; 5. DESFUSIFICACIÓN
; ----------------------------
(defrule mostrar-resultado
    ?f <- (puede_volar ?animal ?confianza) ; Captura el hecho de que un animal puede volar con cierta confianza
    =>
    (printout t ?animal " puede volar con confianza " ?confianza crlf)) ; Imprime el resultado: animal y su confianza de vuelo
