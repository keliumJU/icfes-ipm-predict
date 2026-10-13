"""Genera, valida y ejecuta celdas reales con exec;solo lector de guardados, sin kernel."""
from comun_diagnostico import *
import ast
import base64
import contextlib
import io
import nbformat


def main():
    env = environment()
    source = F1 / 'fuentes/01_diagnostico.py'
    cells = source.read_text().split('# %%\n')[1:]
    assert len(cells) == 6
    notebook = nbformat.v4.new_notebook()
    notebook.metadata = dict(kernelspec=dict(display_name='Python 3.12.14 — solo guardados', language='python', name='python3'),
                             language_info=dict(name='python', version=env['python']),
                             diagnostico=dict(metodo='Python exec secuencial;sin kernelJupyter', fits=0, semilla=SEED,
                                               fuentes_sha256=sha(source), exploratorio=True))
    notebook.cells = [nbformat.v4.new_markdown_cell('''# Diagnóstico objetivo3 v1 — solo datos y predicciones guardados

Notebook descriptivo, no personal. Cero nuevos fits/carga de modelos. 2021–2025 ya
vistos: exploratorio, sin confirmación independiente, causalidad o pronóstico
anticipado demostrado. Ejecutar desde raíz o subcarpeta del repositorio con entorno
exacto Python3.12.14/sklearn1.9.1/54paqueteslock. Fuente editable `01_diagnostico.py`;
generador valida nbformat y ejecuta de verdad seis celdas mediante Python exec.
Tablas completas en fase1/tablas; unidades/n/límites acompañan resultados.
''')]
    namespace = {'__name__': '__notebook__'}
    emitted = []
    def mostrar_png(path):
        emitted.append(nbformat.v4.new_output(output_type='display_data', data={
            'image/png': base64.b64encode(path.read_bytes()).decode(), 'text/plain': str(path.name)}, metadata={}))
    namespace['mostrar_png'] = mostrar_png
    executed = []
    for number, text in enumerate(cells, 1):
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in {'fit', 'fit_transform', 'partial_fit', 'fit_predict', 'load', 'loads'}
        out = io.StringIO(); emitted.clear()
        with contextlib.redirect_stdout(out):
            exec(compile(text, str(source), 'exec'), namespace)
        cell = nbformat.v4.new_code_cell(text)
        cell.execution_count = number
        cell.outputs = [nbformat.v4.new_output(output_type='stream', name='stdout', text=out.getvalue()), *emitted]
        notebook.cells.append(cell)
        executed.append(dict(celda=number, ejecutada=True, error=False, imagenes=len(emitted),
                             salida_sha256=hashlib.sha256(out.getvalue().encode()).hexdigest()))
    nbformat.validate(notebook)
    target = destination(F1 / 'notebooks/01_diagnostico.ipynb')
    assert not target.exists()
    nbformat.write(notebook, target)
    reloaded = nbformat.read(target, as_version=4); nbformat.validate(reloaded)
    assert all(c.execution_count is not None and c.outputs for c in reloaded.cells if c.cell_type == 'code')
    write_json(OUT / 'verificacion_notebook_diagnostico.json', dict(aprobado=True, nbformat_validado=True,
        metodo='exec Python secuencial real;sin kernelJupyter', celdas=executed,
        fuente_sha256=sha(source), generador_sha256=sha(Path(__file__)), notebook_sha256=sha(target),
        python=env['python'], versiones=env['paquetes'], semilla=SEED, fits=0,
        datos_personales=False, imagenes_reales=5, fuente_editable=str(source.relative_to(ROOT))))
    print('Notebook validado:6celdas realmenteejecutadas,5PNGguardados,cero fits.')


if __name__ == '__main__':
    main()
