# Precisión de ubicación de E2-01

El documento congelado ENMIENDA_AUDITORIA_E2_01.md decía «primera auditoría
detenida en2021». La comprobación de todos los tipos leídos en el orden original
identifica el primer y único punto de diferencia en **externo2022, procedimiento
persistencia, columna cambio_predicho**: float64 en externas_2022.csv, int64 en
persistencia/e2022_externo_persistencia/predicciones.csv. En2021 ambos son enteros.
Evidencia: resultados/diagnostico_tipos_csv.json, procedimiento documentado allí.

Esta precisión corrige una ubicación transcrita por inferencia; el archivo congelado
se conserva íntegro para no alterar su SHA después de la ejecución. El punto de
código(verificar.py:126), causa, extensión, igualdad exacta, pruebas, controles y
resultados son correctos. No cambia datos/particiones/métricas/selección/criterios,
ni añade ajustes. Impacto: evitar una referencia temporal equivocada en la incidencia.
Alternativa y resolución: cotejar los tipos por ventana/procedimiento y conservar
esta fe de erratas explícita con la evidencia; no reapertura del piloto.
