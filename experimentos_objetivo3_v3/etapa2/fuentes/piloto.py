"""Piloto v3 serial: reutiliza comun_v3 y constructor/motor v2 en lectura."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'experimentos_objetivo3_v3/etapa1/fuentes'))
from comun_v3 import *
import platform, importlib.metadata as md, subprocess, traceback, joblib
from datetime import datetime,timezone
E2=V3/'etapa2'
OUT=E2/'resultados'
CONFIG=E1/'resultados/configuraciones_congeladas.json'
PANEL=E1/'reconstrucciones/panel_historial.csv'
def now():return datetime.now(timezone.utc).isoformat()
def csv(path,frame):frame.to_csv(destino(path),index=False,float_format='%.17g')
def loadcsv(path):return pd.read_csv(path,dtype={'codigo_departamento':str},float_precision='round_trip')
def check_hashes(mapping):
    for p,h in mapping.items():assert sha(ROOT/p)==h,p

def verificar_etapa1():
    # Continuidad puede actualizarse al cerrar etapa2; su huella inicial se conserva en Git.
    manifest=read(E1/'resultados/manifiesto_cierre.json')
    for p,h in manifest['entregables_sha256'].items():
        if p=='experimentos_objetivo3_v3/CONTINUIDAD_V3.md':
            import hashlib
            saved=subprocess.check_output(['git','show','45fa051ffadc0fc25a326605069dd2f93920898f:'+p],cwd=ROOT)
            assert hashlib.sha256(saved).hexdigest()==h
        else:assert sha(ROOT/p)==h,p
    check_hashes(read(E1/'resultados/congelacion_previa.json')['artefactos_sha256'])
    check_hashes(read(E1/'resultados/conservacion_final.json')['protegidos_sha256'])

def environment():
    versions={}
    assert platform.python_version()=='3.12.14'
    for line in (E1/'requirements.lock.txt').read_text().splitlines():
        name,version=line.split('==');versions[name]=md.version(name);assert versions[name]==version,(name,versions[name],version)
    result=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True,check=True)
    return dict(python=platform.python_version(),ejecutable=sys.executable,paquetes=versions,pip_check=result.stdout.strip(),advertencia_pip=result.stderr.strip(),semilla=SEMILLA,lock_sha256=sha(E1/'requirements.lock.txt'))

def preflight():
    assert not (OUT/'piloto/ledger.json').exists(), 'no sobrescribir partida/entorno durante piloto'
    verificar_etapa1();env=environment()
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip()=='codex/objetivo3-v3-historial'
    subprocess.run(['git','merge-base','--is-ancestor','45fa051ffadc0fc25a326605069dd2f93920898f','HEAD'],cwd=ROOT,check=True)
    snapshot={p:sha(ROOT/p) for p in subprocess.check_output(['git','ls-files'],cwd=ROOT).decode().splitlines() if (ROOT/p).is_file()}
    assert sha(anterior.BASE)==anterior.BASE_SHA
    p=loadcsv(PANEL);expected=historial(compartido.cargar_panel())
    expected['anio_previo']=expected.anio_previo.astype(float)
    expected['fuente_sha256']=anterior.BASE_SHA
    expected=expected.reset_index(drop=True)
    pd.testing.assert_frame_equal(p,expected,check_dtype=False)
    conf=read(CONFIG);assert conf['configuraciones']==candidatos()
    refs=read(E1/'resultados/referencias_guardadas.json');assert sha(ROOT/refs['archivo'])==refs['sha256']
    for year,h in refs['selecciones_sha256'].items():assert sha(ROOT/f'experimentos_objetivo3_v2/fase3/resultados/piloto/seleccion_{year}.json')==h
    guardar(OUT/'entorno.json',env)
    guardar(OUT/'partida.json',dict(commit_partida=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),rama='codex/objetivo3-v3-historial',git_inicial=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT).decode(),snapshot_versionados=snapshot,panel_sha256=sha(PANEL),fuente_sha256=sha(anterior.BASE),cierre_etapa1='45fa051ffadc0fc25a326605069dd2f93920898f',pdf_leidos=[]))
    print('Partida/entorno/congelación y referencias aprobados.',flush=True)

class Runner:
    def __init__(self,out,panel,cs=None,executor=None,limit=7200):
        self.out=destino(out);self.out.mkdir(exist_ok=True);self.panel=panel
        self.cs=cs or candidatos();self.byid={c['id']:c for c in self.cs};self.executor=executor
        self.budget=Presupuesto(self.out/'ledger.json',limit)
        self.origin='sintetico_doble' if executor else 'real'
    def fit(self,label,c,train):
        target=destino(self.out/'ajustes'/label);target.mkdir(exist_ok=True)
        meta=target/'ajuste.json';artifact=target/'modelo.joblib'
        if meta.exists():
            old=read(meta)
            if old['estado']=='ok':assert sha(artifact)==old['modelo_sha256'];return joblib.load(artifact),old
            if old['estado']=='numerico':return None,old
            if old['estado']=='limite':raise TimeoutError('ajuste anterior agotó presupuesto')
        X,y=matrices_entrenamiento(train,c)
        base=dict(id=c['id'],etiqueta=label,entrenamiento=sorted(train.anio.unique().tolist()),llaves_entrenamiento=train[LLAVES].values.tolist(),n=len(train),parametros_completos=c['parametros_completos'],entradas=c['entradas'],objetivo='cambio_observado',semilla=SEMILLA,origen=self.origin,datos_X_sha256=__import__('hashlib').sha256(X.tobytes()).hexdigest(),datos_y_sha256=__import__('hashlib').sha256(y.tobytes()).hexdigest(),panel_sha256=sha(PANEL),entorno_sha256=sha(OUT/'entorno.json') if (OUT/'entorno.json').exists() else None,congelacion_sha256=sha(OUT/'congelacion_operativa.json') if (OUT/'congelacion_operativa.json').exists() else None)
        used=[r for r in self.budget.data['ajustes'] if r.get('etiqueta','').startswith(label+'_intento')]
        if len(used)>=2:raise RuntimeError('dos intentos ya consumidos: '+label)
        for attempt in range(len(used)+1,3):
            try:
                model,captured=self.budget.ajustar(label+f'_intento{attempt}',construir(c),X,y,executor=self.executor)
            except (KeyboardInterrupt,SystemExit):raise
            except Exception as e:
                numerical=isinstance(e,(ValueError,FloatingPointError)) or any(s in str(e) for s in ('convergencia','ValueError:','FloatingPointError:','OverflowError:','LinAlgError:'))
                state='limite' if isinstance(e,TimeoutError) else 'numerico' if numerical else 'infraestructura'
                info={**base,'estado':state,'traceback':traceback.format_exc(),'intento':attempt,'tiempo':self.budget.data['ajustes'][-1] if self.budget.data['ajustes'] else None}
                guardar(target/f'fallo_{attempt}.json',info);guardar(meta,info)
                if state=='limite':raise
                if numerical:return None,info
                if attempt==2:raise
                continue
            # Errores de integridad/escritura no se clasifican como nuevos ajustes.
            transform={}
            if hasattr(model,'named_steps'):
                s=model.named_steps['escalado']
                transform=dict(mean=s.mean_.tolist(),scale=s.scale_.tolist(),var=s.var_.tolist(),n_samples_seen=int(s.n_samples_seen_))
                np.testing.assert_allclose(s.mean_,X.mean(axis=0),rtol=1e-12,atol=1e-12)
                assert int(s.n_samples_seen_)==len(train)
            joblib.dump(model,destino(artifact),compress=3)
            info={**base,'estado':'ok','advertencias':captured,'transformacion_ajustada':transform,'modelo_sha256':sha(artifact),'tiempo':self.budget.data['ajustes'][-1],'intento':attempt}
            guardar(meta,info);return model,info
    def predict(self,label,c,train,test,recalculate=False):
        target=destino(self.out/('persistencia' if c['familia']=='persistencia' else 'ajustes')/label)
        file=target/'predicciones.csv';meta=target/('calculo.json' if c['familia']=='persistencia' else 'ajuste.json')
        if file.exists() and not recalculate:
            info=read(meta);assert sha(file)==info['predicciones_sha256'];return loadcsv(file)
        started=time.monotonic()
        if c['familia']=='persistencia':
            pred,info=persistencia(test);info.update(id=c['id'],etiqueta=label,origen=self.origin,llaves=test[LLAVES].values.tolist(),anio_previo=test.anio_previo.tolist())
            delta=np.zeros(len(test))
        else:
            model,info=self.fit(label,c,train)
            if model is None:return None
            X=test[c['entradas']].to_numpy(float);assert np.isfinite(X).all()
            try:
                delta=model.predict(X);pred=reconstruir(test.puntaje_previo,delta)
            except (ValueError,FloatingPointError):
                guardar(target/'prediccion_no_finita.json',dict(etiqueta=label,traceback=traceback.format_exc()));return None
        frame=test[[*LLAVES,'anio_previo','puntaje_previo']].copy()
        frame['id']=c['id'];frame['ajuste']=label;frame['observado']=test[anterior.RESULTADO].to_numpy();frame['cambio_predicho']=delta
        frame['prediccion']=pred;frame['error']=pred-frame.observado;frame['origen']=self.origin
        csv(file,frame);info.update(predicciones_sha256=sha(file),segundos_prediccion=time.monotonic()-started,fuera_0_500=int(((pred<0)|(pred>500)).sum()))
        guardar(meta,info);return frame
    def window(self,w):
        year=w['externo'];expected=[i['validacion'] for i in w['internas']];scores=[]
        if year!=2021:
            for c in self.cs:
                parts=[];valid=[]
                for i in w['internas']:
                    tr,te=dividir(self.panel,i['entrenamiento'],i['validacion'])
                    p=self.predict(f"e{year}_i{i['validacion']}_{c['id']}",c,tr,te)
                    if p is not None:parts.append(p);valid.append(i['validacion'])
                score=dict(id=c['id'],estado='completo' if valid==expected else 'inelegible',ventanas=valid)
                if valid==expected:
                    joined=pd.concat(parts);m=metricas(joined.observado,joined.prediccion);score.update(mae=m['mae'],rmse=m['rmse'])
                scores.append(score)
        decision={**seleccionar(scores,expected,year),'externo':year,'metricas_internas':scores,'instante_antes_externo':now(),'origen':self.origin}
        selection=self.out/f'seleccion_{year}.json'
        if selection.exists():
            old=read(selection)
            for k in ('global_id','especificaciones','metricas_internas'):assert old[k]==decision[k],k
            decision=old
        else:guardar(selection,decision)
        roles={'procedimiento_v3':decision['global_id'],**{f'procedimiento_{s}':v for s,v in decision['especificaciones'].items()},'persistencia':'persistencia'}
        tr,te=dividir(self.panel,w['entrenamiento'],year);preds={}
        for ident in sorted(set(roles.values()),key=lambda ident:self.byid[ident]['orden']):
            p=self.predict(f'e{year}_externo_{ident}',self.byid[ident],tr,te)
            if p is None:raise RuntimeError('ganador externo fallido: '+ident)
            preds[ident]=p
        rows=[]
        for role,ident in roles.items():
            p=preds[ident].copy();p['procedimiento']=role;p['externo']=year;p['seleccion_sha256']=sha(selection);rows.append(p)
        csv(self.out/f'externas_{year}.csv',pd.concat(rows))
        print(f'Externo {year} completo; {len(self.budget.data["ajustes"])} ajustes; {self.budget.data["consumido"]:.1f}s acumulados.',flush=True)
    def run(self):
        started=time.monotonic()
        for w in ventanas():self.window(w)
        repeats=[]
        for w in ventanas():
            year=w['externo'];ident=read(self.out/f'seleccion_{year}.json')['global_id'];tr,te=dividir(self.panel,w['entrenamiento'],year)
            new=self.predict(f'e{year}_repeticion_{ident}',self.byid[ident],tr,te,recalculate=ident=='persistencia')
            old=loadcsv(self.out/('persistencia' if ident=='persistencia' else 'ajustes')/f'e{year}_externo_{ident}'/'predicciones.csv')
            assert new is not None
            np.testing.assert_allclose(new.prediccion,old.prediccion,atol=1e-10,rtol=0)
            repeats.append(dict(externo=year,id=ident,max_diferencia=float(np.max(np.abs(new.prediccion.to_numpy()-old.prediccion.to_numpy()))),ajustado=ident!='persistencia'))
        guardar(self.out/'reproducibilidad.json',dict(aprobado=True,atol=1e-10,rtol=0,repeticiones=repeats))
        guardar(self.out/'estado.json',dict(completo=True,consumido=self.budget.data['consumido'],ajustes=len(self.budget.data['ajustes']),segundos_ejecucion_invocacion=time.monotonic()-started,terminado=now(),origen=self.origin))

def freeze():
    assert not (OUT/'piloto/ledger.json').exists(),'no recongelar tras primer fit'
    assert read(OUT/'pruebas_sinteticas.json')['aprobado']
    artifacts=[*sorted((E2/'fuentes').glob('*.py')),OUT/'entorno.json',OUT/'pruebas_sinteticas.json',CONFIG,PANEL,E1/'resultados/congelacion_previa.json']
    guardar(OUT/'congelacion_operativa.json',dict(instante=now(),artefactos_sha256={str(p.relative_to(ROOT)):sha(p) for p in artifacts},semilla=SEMILLA,limite=7200,cota_sin_fallos=1010,ajustes_antes=0,orden='externos crecientes; candidatos JSON; internas crecientes; selección antes de externos; IDs externos por JSON; cinco repeticiones globales',motor='comun_v3.Presupuesto/comun.Presupuesto: Pipeline completo, spawn serial terminable'))

def verify_freeze():
    verificar_etapa1();check_hashes(read(OUT/'congelacion_operativa.json')['artefactos_sha256']);environment()

def main():
    if '--preflight' in sys.argv:preflight();return
    if '--freeze' in sys.argv:freeze();return
    verify_freeze();runner=Runner(OUT/'piloto',loadcsv(PANEL))
    try:runner.run()
    except BaseException:
        guardar(runner.out/'estado.json',dict(completo=False,consumido=runner.budget.data['consumido'],ajustes=len(runner.budget.data['ajustes']),traceback=traceback.format_exc(),terminado=now()));raise
if __name__=='__main__':main()
