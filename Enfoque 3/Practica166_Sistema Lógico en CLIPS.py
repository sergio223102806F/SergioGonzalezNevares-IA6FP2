; Sistema Lógico en CLIPS

; ----------------------------
; 1. HECHOS (Deftemplate)
; ----------------------------
(deftemplate hecho (slot nombre))

; ----------------------------
; 2. REGLAS (Defrule)
; ----------------------------
(defrule regla-vuelo
    (hecho (nombre "es_pajaro"))
    (not (hecho (nombre "no_vuela")))
    =>
    (assert (hecho (nombre "puede_volar"))))

(defrule regla-pinguino
    (hecho (nombre "es_pajaro"))
    (hecho (nombre "es_pinguino"))
    =>
    (assert (hecho (nombre "no_vuela"))))

; ----------------------------
; 3. INFERENCIA (Forward Chaining)
; ----------------------------
(assert (hecho (nombre "es_pajaro")))
(assert (heque (nombre "es_pinguino")))

(run) ; Ejecuta el motor de inferencia

; ----------------------------
; 4. DEDUCCIÓN (Queries)
; ----------------------------
(defquery puede-volar?
    (hecho (nombre "puede_volar")))

; ----------------------------
; 5. INDUCCIÓN (Simplificada)
; ----------------------------
(defrule aprender-por-ejemplo
    ?ejemplo <- (ejemplo-positivo ?x)
    (not (ejemplo-negativo ?x))
    =>
    (assert (hecho (nombre (str-cat "puede_" ?x))))))
