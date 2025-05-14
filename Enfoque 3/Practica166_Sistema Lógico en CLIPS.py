; Sistema Lógico en CLIPS

; ----------------------------
; 1. HECHOS (Deftemplate)
; ----------------------------
(deftemplate hecho (slot nombre)) ; Define una plantilla para los hechos, con un slot llamado 'nombre'

; ----------------------------
; 2. REGLAS (Defrule)
; ----------------------------
(defrule regla-vuelo
    (hecho (nombre "es_pajaro"))       ; Si existe un hecho que indica que algo "es_pajaro"
    (not (hecho (nombre "no_vuela"))) ; Y no existe un hecho que indique que "no_vuela"
    =>
    (assert (hecho (nombre "puede_volar"))))  ; Entonces, afirma el hecho de que "puede_volar"

(defrule regla-pinguino
    (hecho (nombre "es_pajaro"))    ; Si existe un hecho que indica que algo "es_pajaro"
    (hecho (nombre "es_pinguino"))  ; Y existe un hecho que indica que también "es_pinguino"
    =>
    (assert (hecho (nombre "no_vuela")))) ; Entonces, afirma el hecho de que "no_vuela"

; ----------------------------
; 3. INFERENCIA (Forward Chaining)
; ----------------------------
(assert (hecho (nombre "es_pajaro")))    ; Afirma el hecho de que algo "es_pajaro"
(assert (hecho (nombre "es_pinguino")))  ; Afirma el hecho de que algo "es_pinguino"

(run) ; Ejecuta el motor de inferencia hacia adelante (forward chaining)

; ----------------------------
; 4. DEDUCCIÓN (Queries)
; ----------------------------
(defquery puede-volar?
    (hecho (nombre "puede_volar"))) ; Define una consulta para encontrar hechos que indiquen "puede_volar"

; ----------------------------
; 5. INDUCCIÓN (Simplificada)
; ----------------------------
(defrule aprender-por-ejemplo
    ?ejemplo <- (ejemplo-positivo ?x)       ; Captura un hecho que indica un "ejemplo-positivo" de algo (?x)
    (not (ejemplo-negativo ?x))         ; Y no existe un hecho que indique un "ejemplo-negativo" de lo mismo (?x)
    =>
    (assert (hecho (nombre (str-cat "puede_" ?x))))) ; Entonces, afirma un hecho que indica "puede_" seguido del valor de ?x (inducción simplificada)
