# Fase 4 — revisión y notebook personal

Entrega bajo protocolo 2.0.2 congelado. Todas las fases anteriores se consultan en
lectura. No se reentrenó el piloto en esta fase. Mejora verificada: 18.392545281085766%.

Abrir `notebooks/01_notebook_personal.ipynb` desde el repositorio o sus subcarpetas y
seleccionar el entorno exacto de `../fase2/requirements.lock.txt`: Python 3.12.14,
scikit-learn 1.9.1, semilla 20261010. El entorno local comprobado es
`/tmp/icfes-v2-fase2-venv/bin/python`; su disponibilidad futura no se presupone.
No se instalan paquetes automáticamente. Celdas en orden; `MODO='verificar'` por defecto.

Fuentes editables y orden de generación, con el Python del entorno comprobado:

1. `fuentes/revision.py`: manifiestos/lock y auditoría de predicciones, selección y ledger.
2. `fuentes/presentar.py`: recálculo y tablas/gráficos en `resultados/`.
3. `fuentes/generar_notebook.py`: notebook desde `01_notebook_personal.py`; cinco celdas
   ejecutadas en modo verificar mediante Python exec; nbformat; tres gráficos incrustados.
4. `fuentes/generar_informe.py`: informe desde los CSV y controles actuales.
5. Actualizar continuidad v2; `fuentes/cerrar.py`: conservación y manifiesto sin modificar
   fases previas. El commit se informa fuera del manifiesto.

Entradas: panel validado fase1, configuraciones y funciones compartidas fase2, registros
fase3. Salidas: informe, métricas de nueve procedimientos por año/territorio/conjunto,
2021–2024 separado y 2025, comparaciones con media/tres OLS/v1, 165 diferencias
emparejadas firmadas/absolutas/cuadráticas, deterioros, gráficos, evidencia y notebook.
`resultados/notebook_verificacion/` contiene la ejecución real de lectura del notebook.
Los resultados completos están en CSV; el chat muestra únicamente resúmenes.

Para reejecución VOLUNTARIA completa, cambiar MODO a `reejecutar` en el notebook o ejecutar
`fuentes/reejecutar.py`. No se hizo en esta entrega. Genera un destino único en
`fase4/reproducciones/`, presupuesto de 7200 segundos para TODO el piloto nuevo, sin
reutilizar modelos de fase3 ni modificar su ledger. Duración histórica ~25.7 minutos,
variable con el equipo. Conserva fallos/estado incompleto si no termina. No borrar ni
reiniciar ledgers; el adaptador no reutiliza destinos existentes. Usa Runner compartido,
100 configuraciones/semilla/criterios congelados; nunca entrenamiento final ni simulación.

Interpretación: igual peso por territorio-año; geografía del colegio; casos completos;
2020 excluido; 2025 exploratorio. Umbral práctico, sin significancia. Predicciones
contemporáneas ecológicas, sin causalidad ni pronóstico anterior a publicación del IPM.
Las enmiendas E3-01 y E3-02 se conservan. Ocho territorios deterioran MAE, aunque los
cinco años mejoran; conservar estos resultados al reutilizar el notebook.
