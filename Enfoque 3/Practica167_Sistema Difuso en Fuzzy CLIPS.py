; Sistema Difuso en Fuzzy CLIPS

; ----------------------------
; 1. HECHOS DIFUSOS
; ----------------------------
(deffacts hechos-iniciales
    (habilidad_volar pajaro 0.9)
    (habilidad_volar pinguino 0.1))

; ----------------------------
; 2. REGLAS DIFUSAS
; ----------------------------
(defrule regla-vuelo-difuso
    (habilidad_volar ?animal ?grado)
    (test (> ?grado 0.5))
    =>
    (assert (puede_volar ?animal (round ?grado))))

; ----------------------------
; 3. FUNCIONES DIFUSAS
; ----------------------------
(deffunction fuzzy-and (?a ?b)
    (min ?a ?b))

(deffunction fuzzy-or (?a ?b)
    (max ?a ?b))

; ----------------------------
; 4. INFERENCIA DIFUSA
; ----------------------------
(defrule clasificar-vuelo
    ?h <- (habilidad_volar ?animal ?grado)
    =>
    (if (>= ?grado 0.7) then
        (assert (excelente_volador ?animal)))
    else if (>= ?grado 0.4) then
        (assert (volador_regular ?animal))))

; ----------------------------
; 5. DESFUSIFICACIÓN
; ----------------------------
(defrule mostrar-resultado
    ?f <- (puede_volar ?animal ?confianza)
    =>
    (printout t ?animal " puede volar con confianza " ?confianza crlf))