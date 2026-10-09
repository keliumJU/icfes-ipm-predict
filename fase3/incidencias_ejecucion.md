# Incidencias de infraestructura y ejecución

2026-10-09. Complemento posterior a decisiones.md; no modifica criterios congelados.

## I01 — instalación

El primer intento de pip dentro del sandbox informó DNS no disponible y terminó sin instalar scikit-learn. Se repitió la misma solicitud con autorización de red. Se instaló exactamente sklearn 1.9.1 y se fijaron todas las dependencias resueltas en requirements.lock.txt antes del primer entrenamiento. pip check no encontró dependencias incompatibles. Advertencia del cache pip: carpeta de usuario no escribible; no afecta instalación ni modelos. No se cambió versión para mejorar métricas.

## I02 — kernel local

El primer generador no produjo notebooks ni resultados después de varios minutos; se interrumpió (código130). Evidencia: solo preparacion.json y notebook01 existían al comprobar. No se realizó ajuste. Impacto: no podía verificarse ejecución real en Jupyter. Alternativa: mismo generador y mismo entorno fuera del sandbox con permiso para conexiones locales del kernel. Se solicitó autorización explícita; el segundo intento ejecutó notebook02. La causa exacta del bloqueo no se demostró: restricciones de conexiones locales son explicación plausible, no causa certificada. El cierre verificará notebook03/04 ejecutados, sus salidas y ausencia de errores. No se elude permiso ni se cambia método.

## I03 — precisión al releer CSV

El primer verificador exigía igualdad bit a bit entre observados exportados y base al usar el parser ordinario pandas. Nueve de 99 observados de una configuración diferían como máximo 5.68434189e-14, aproximadamente dos unidades de último lugar: no era cambio de fuente. Impacto: falso rechazo de conservación de valores serializados. Alternativa verificable: float_precision='round_trip' en lectura de CSV de predicciones. Decisión: usar ese parser y conservar igualdad estricta, sin redondear ni modificar métricas ni archivos de entrenamiento. La comprobación independiente de métricas mantiene tolerancia numérica 1e-12 (control de representación, no criterio de selección). No se amplían grillas ni se reajusta por este control.

## I04 — nombres Unicode en el control de integridad

La primera comprobación de archivos Git falló al interpretar nombres con acentos escapados en salida de ls-tree. No afectó ajuste ni predicciones. Se corrigió el inventario de verificación a salida delimitada por NUL (`-z`), con UTF-8, y el control posterior confirmó 152 archivos anteriores intactos. Es un fallo del verificador, no del dataset ni del modelo. No se reabrió evidencia histórica ni se modificaron nombres.

El conteo real adicional de la sesión es seis ajustes de verificación del ganador: tres antes de que el control fallara en nombres Unicode y tres en el control aprobado. No son candidatos nuevos ni una segunda selección. Cada ejecución individual del verificador realiza tres; el cierre separa conteo por invocación y total de sesión. La finalización documental no repite ajustes.
