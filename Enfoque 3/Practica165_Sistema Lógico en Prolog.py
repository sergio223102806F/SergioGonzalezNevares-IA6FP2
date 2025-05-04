/* Sistema Lógico en Prolog */

% ----------------------------
% 1. HECHOS (Facts)
% ----------------------------
vuela(pajaro).
es_pajaro(pinguino).

% Excepción
no_vuela(pinguino).

% ----------------------------
% 2. REGLAS (Rules)
% ----------------------------
% Regla básica
puede_volar(X) :- es_pajaro(X), not(no_vuela(X)).

% Regla con negación
no_puede_volar(X) :- no_vuela(X).

% ----------------------------
% 3. INFERENCIA (Queries)
% ----------------------------
% ¿Puede volar un pájaro típico?
% Consulta: puede_volar(pajaro). → true

% ¿Puede volar un pingüino?
% Consulta: puede_volar(pinguino). → false

% ----------------------------
% 4. DEDUCCIÓN (Backward Chaining automático)
% ----------------------------
% Prolog usa deducción automática por backtracking

% ----------------------------
% 5. INDUCCIÓN (Ejemplo simplificado)
% ----------------------------
% Prolog puede implementar inducción con metaprogramación
aprender_regla(Ejemplo) :- asserta(Ejemplo).

% Ejemplo de uso:
% aprender_regla(vuela(aguila)).