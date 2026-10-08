# Reproducción y organización por etapas

Solo fase 2 está ejecutada. Entradas existentes: panel agregado, diccionario y evidencia
de fase 1, con huellas en `evidencia/verificacion_fase2.json`. No se leen TXT individuales,
no se repiten inventarios, no se incluyen datos personales. Salidas nuevas bajo protocolo/
y notebooks/; originales y evidencia histórica quedan intactos.

## Orden ejecutado

Desde raíz del repositorio, con Python 3.12.14 disponible:

```bash
python3 protocolo/fuentes/controles.py
python3 protocolo/fuentes/generar_notebooks.py
python3 protocolo/fuentes/verificar_cierre.py
```

En esta sesión `python3` corresponde al ejecutable explícito
`/home/kelium/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
El comando del sistema apunta a Python 3.14.7; los controles requieren Python >=3.10
y biblioteca estándar, y no se supone que ambos entornos tengan los mismos paquetes.
No ejecutar con `-O`: los controles usan assert. Versiones presentes/ausentes se registran
sin instalar dependencias. Semilla 20261008 declarada para futuros estimadores aleatorios;
estos controles/generador son deterministas y no requieren semilla.

1. `controles.py`: comprueba las 198 filas completas, columnas/llaves/territorios,
   rangos/denominadores, evidencia validada de fase 1 y separación temporal; guarda
   verificación y lista ordenada de candidatos **sin construir estimadores**.
2. `generar_notebooks.py`: convierte marcadores `# %%` de la fuente editable en celdas
   Markdown/code, valida su subconjunto nbformat4.5, relee el archivo y ejecuta las tres
   celdas de código secuencialmente con compile/exec. Guarda comprobación/huellas separada;
   notebook distribuido sin execution_count ni salidas. No afirma ejecución Jupyter.
3. `verificar_cierre.py`: coteja reproducción, conserva huellas de insumos, verifica
   coherencia de configuración y entregables, genera manifiesto final con huellas.

Nunca editar JSON de .ipynb ni su lista de candidatos a mano. Editar fuentes Python y
regenerar; parámetros, columnas y particiones viven en `configuracion.py`. El generador
solo tiene una etapa autorizada: no crea plantillas con entrenamientos/simulaciones.
Su validador comprueba todos los campos del subconjunto que produce; para notebooks
arbitrarios se requerirá nbformat.validate, todavía no instalado. Preparar un kernel
ipykernel en la fase de modelos antes de afirmar reproducción en Jupyter.

## Notebooks por etapas útiles

| Orden / estado | Fuente/notebook previstos | Entradas y salidas | Lógica común |
|---|---|---|---|
| 01 / creado ahora | protocolo/fuentes/01_protocolo_controles.py → notebooks/01_protocolo_controles.ipynb | Panel agregado y evidencia → controles/ventanas; sin métricas de modelos | configuracion.py y controles.py |
| 02 / solo diseño, crear con autorización posterior | 02_preparacion_desarrollo.py → 02_preparacion_desarrollo.ipynb | Panel y protocolo congelados → X/y de desarrollo, reserva separada, máscaras y manifiesto de entorno | Reusar carga/controles/configuración; no reabrir población |
| 03 / solo diseño, crear con autorización de modelos | 03_modelos_validacion.py → 03_modelos_validacion.ipynb | Desarrollo132 + grillas → 67 configuraciones, errores de ventanas, selección y ajustes finales congelados | Módulo compartido de pipelines, métricas, selección/persistencia; bucle por especificación/familia, no notebook por algoritmo |
| 04 / solo diseño, crear con autorización de evaluación/contrastes | 04_reevaluacion_contrastes.py → 04_reevaluacion_contrastes.ipynb | Artefactos congelados + reserva66; desarrollo para contraste territorial → tablas anuales/conjuntas y diagnóstico separado | Misma implementación de métricas y manifiestos; no reselección |
| 05 / solo diseño, crear con autorización de escenarios | 05_escenarios_predictivos.py → 05_escenarios_predictivos.ipynb | Modelo congelado y escenarios previamente acordados → predicciones y advertencias de soporte | Mismos transformadores/esquema; escenarios no son efectos causales |

Son cinco etapas lógicas, no cinco archivos generados ahora. Las fuentes y módulos
posteriores se crean solo al autorizar su trabajo; no contienen hoy resultados ficticios.
Los artefactos de modelos futuros deben separarse por ejecución, sin sobrescribir la
base/evidencia. Documentar entradas, salidas, orden, hashes, paquetes, semilla, parámetros
completos y fallos antes del primer ajuste. Nada de 2023–2024 entra en selección.
