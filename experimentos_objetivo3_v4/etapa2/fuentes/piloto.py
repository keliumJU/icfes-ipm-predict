"""Piloto v4 serial: reutiliza comun_v4 y constructor/motor v2 en lectura."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'experimentos_objetivo3_v4/etapa1/fuentes'))
from comun_v4 import *
import platform, importlib.metadata as md, subprocess, traceback, joblib, time, hashlib
ANIOS=anterior.ANIOS
np.random.seed(SEMILLA) # también al importar en el proceso spawn; sin cambiar defaults
sys.path.insert(0,str(Path(__file__).resolve().parent))
from datetime import datetime,timezone
E2=V4/'etapa2'
OUT=E2/'resultados'
CONFIG=E1/'resultados/configuraciones_congeladas.json'
PANEL=E1/'reconstrucciones/panel_cambios.csv'
def now():return datetime.now(timezone.utc).isoformat()
def csv(path,frame):frame.to_csv(destino(path),index=False,float_format='%.17g')
def loadcsv(path):return pd.read_csv(path,dtype={'codigo_departamento':str},float_precision='round_trip')
def check_hashes(mapping):
    for p,h in mapping.items():assert sha(ROOT/p)==h,p

def verificar_etapa1():
    # Continuidad puede actualizarse al cerrar etapa2; su huella inicial se conserva en Git.
    manifest=read(E1/'resultados/manifiesto_cierre.json')
    for p,h in manifest['entregables_sha256'].items():
        if p=='experimentos_objetivo3_v4/CONTINUIDAD_V4.md':
            import hashlib
            saved=subprocess.check_output(['git','show','7f25ad066386965a75058e96b4716cdd8a9adb52:'+p],cwd=ROOT)
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
    assert len(env['paquetes'])==54 and md.version('scikit-learn')=='1.9.1'
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip()=='codex/objetivo3-v4-correcciones'
    subprocess.run(['git','merge-base','--is-ancestor','7f25ad066386965a75058e96b4716cdd8a9adb52','HEAD'],cwd=ROOT,check=True)
    snapshot={p:sha(ROOT/p) for p in subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().rstrip('\0').split('\0')}
    assert sha(anterior.BASE)==anterior.BASE_SHA
    panel=compartido.normalizar_codigos(loadcsv(anterior.BASE));compartido.validar_panel(panel)
    p=loadcsv(PANEL);expected=historial(panel).reset_index(drop=True)
    expected['fuente_sha256']=anterior.BASE_SHA
    pd.testing.assert_frame_equal(p,expected,check_dtype=False)
    assert len(p)==231 and len(p[p.anio>2018])==198
    assert np.isfinite(p.loc[p.anio>2018,['cambio_'+s for s in COV]].to_numpy()).all()
    conf=read(CONFIG);assert conf['configuraciones']==candidatos() and conf['grupos']==GRUPOS and conf['ventanas']==ventanas()
    assert sha(PANEL)==conf['panel_derivado_sha256']
    refs=read(E1/'resultados/referencias_guardadas.json')
    check_hashes(refs['archivos_sha256']);check_hashes(refs['selecciones_sha256'])
    guardar(OUT/'entorno.json',env)
    guardar(OUT/'partida.json',dict(commit_partida=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),rama='codex/objetivo3-v4-correcciones',git_inicial=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT).decode(),snapshot_versionados=snapshot,panel_sha256=sha(PANEL),fuente_sha256=sha(anterior.BASE),cierre_etapa1='7f25ad066386965a75058e96b4716cdd8a9adb52',pdf_leidos=[]))
    print('Partida/entorno/congelación, 231 filas/198 cambios y referencias aprobados.',flush=True)

class Runner:
    def __init__(self,out,panel,cs=None,executor=None,limit=7200):
        self.out=destino(out);self.out.mkdir(exist_ok=True);self.panel=panel
        self.cs=cs or candidatos();self.byid={c['id']:c for c in self.cs};self.executor=executor
        self.budget=Presupuesto(self.out/'ledger.json',limit)
        self.origin='sintetico_doble' if executor else 'real'
        self.context=dict(panel_memoria_sha256=hashlib.sha256(panel.to_csv(index=False,float_format='%.17g').encode()).hexdigest(),configuraciones=self.cs,origen=self.origin,limite=limit,congelacion_sha256=sha(OUT/'congelacion_operativa.json') if (OUT/'congelacion_operativa.json').exists() else None)
        ctx=self.out/'contexto.json'
        if ctx.exists():
            assert read(ctx)==self.context,'contexto de reanudación alterado'
            self.verify_checkpoint()
        else:
            assert not self.budget.data['ajustes'], 'ledger existente sin contexto'
            guardar(ctx,self.context);self.checkpoint()
    def checkpoint(self):
        files={str(p.relative_to(self.out)):sha(p) for p in sorted(self.out.rglob('*')) if p.is_file() and p.name!='indice_integridad.json'}
        guardar(self.out/'indice_integridad.json',dict(archivos_sha256=files))
    def verify_checkpoint(self):
        saved=read(self.out/'indice_integridad.json')['archivos_sha256']
        actual={str(p.relative_to(self.out)):sha(p) for p in sorted(self.out.rglob('*')) if p.is_file() and p.name!='indice_integridad.json'}
        assert saved==actual,'artefactos/ledger añadidos, ausentes o alterados'
        for r in self.budget.data['ajustes']:
            assert r.get('etiqueta') and r['estado'] in ('ok','error','limite')
        assert len({r['etiqueta'] for r in self.budget.data['ajustes']})==len(self.budget.data['ajustes'])
    def validate_predictions(self,p,test,c,label):
        assert len(p)==len(test) and not p.duplicated(LLAVES).any()
        assert p[LLAVES].values.tolist()==test[LLAVES].values.tolist()
        assert p.id.eq(c['id']).all() and p.ajuste.eq(label).all()
        for field,column in [('observado',anterior.RESULTADO),('puntaje_previo','puntaje_previo'),('anio_previo','anio_previo')]:
            np.testing.assert_array_equal(p[field],test[column])
        np.testing.assert_array_equal(p.prediccion,p.puntaje_previo+p.cambio_predicho)
        np.testing.assert_array_equal(p.error,p.prediccion-p.observado)
        assert np.isfinite(p[['observado','prediccion','cambio_predicho']].to_numpy()).all()
    def fit(self,label,c,train):
        target=destino(self.out/'ajustes'/label);target.mkdir(exist_ok=True)
        meta=target/'ajuste.json';artifact=target/'modelo.joblib'
        X,y=matrices_entrenamiento(train,c)
        base=dict(id=c['id'],etiqueta=label,entrenamiento=sorted(train.anio.unique().tolist()),llaves_entrenamiento=train[LLAVES].values.tolist(),n=len(train),parametros_completos=c['parametros_completos'],entradas=c['entradas'],objetivo='cambio_observado',semilla=SEMILLA,origen=self.origin,datos_X_sha256=__import__('hashlib').sha256(X.tobytes()).hexdigest(),datos_y_sha256=__import__('hashlib').sha256(y.tobytes()).hexdigest(),panel_sha256=sha(PANEL),entorno_sha256=sha(OUT/'entorno.json') if (OUT/'entorno.json').exists() else None,congelacion_sha256=sha(OUT/'congelacion_operativa.json') if (OUT/'congelacion_operativa.json').exists() else None)
        if meta.exists():
            old=read(meta)
            for key,value in base.items():assert old[key]==value,('contexto ajuste',label,key)
            if old['estado']=='ok':
                assert sha(artifact)==old['modelo_sha256']
                assert old['tiempo'] in self.budget.data['ajustes'] and old['tiempo']['estado']=='ok'
                return joblib.load(artifact),old
            if old['estado'] in ('numerico','numerico_prediccion'):return None,old
            if old['estado']=='limite':raise TimeoutError('ajuste anterior agotó presupuesto')
        if self.budget.data['consumido']>=self.budget.limit:raise TimeoutError('presupuesto agotado; sin nuevo intento')
        used=[r for r in self.budget.data['ajustes'] if r.get('etiqueta','').startswith(label+'_intento')]
        if any(r['estado']=='ok' for r in used):raise RuntimeError('éxito sin artefacto íntegro: '+label)
        if len(used)>=2:raise RuntimeError('dos intentos ya consumidos: '+label)
        for attempt in range(len(used)+1,3):
            fit_start=now()
            try:
                model,captured=self.budget.ajustar(label+f'_intento{attempt}',construir(c),X,y,executor=self.executor)
            except (KeyboardInterrupt,SystemExit):raise
            except Exception as e:
                numerical=isinstance(e,(ValueError,FloatingPointError)) or any(s in str(e) for s in ('convergencia','ValueError:','FloatingPointError:','OverflowError:','LinAlgError:'))
                state='limite' if isinstance(e,TimeoutError) else 'numerico' if numerical else 'infraestructura'
                info={**base,'instante_inicio':fit_start,'estado':state,'traceback':traceback.format_exc(),'intento':attempt,'tiempo':self.budget.data['ajustes'][-1] if self.budget.data['ajustes'] else None}
                self.budget.data['ajustes'][-1]['clase_fallo']=state;guardar(self.budget.path,self.budget.data)
                info['tiempo']=self.budget.data['ajustes'][-1]
                guardar(target/f'fallo_{attempt}.json',info);guardar(meta,info);self.checkpoint()
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
            if c['familia']=='correccion_comun' and self.origin=='real':
                assert model.mediana_==float(np.median(y)) and model.n_train_==len(y)
            joblib.dump(model,destino(artifact),compress=3)
            csv(target/'entradas_entrenamiento.csv',train[[*LLAVES,*c['entradas'],'cambio_observado']])
            info={**base,'instante_inicio':fit_start,'estado':'ok','advertencias':captured,'transformacion_ajustada':transform,'modelo_sha256':sha(artifact),'tiempo':self.budget.data['ajustes'][-1],'intento':attempt}
            info['entradas_entrenamiento_sha256']=sha(target/'entradas_entrenamiento.csv')
            info['mediana_train']=float(model.mediana_) if hasattr(model,'mediana_') else None
            guardar(meta,info);self.checkpoint();return model,info
    def predict(self,label,c,train,test,recalculate=False):
        target=destino(self.out/('persistencia' if c['familia']=='persistencia' else 'ajustes')/label)
        file=target/'predicciones.csv';meta=target/('calculo.json' if c['familia']=='persistencia' else 'ajuste.json')
        if file.exists() and not recalculate:
            info=read(meta);assert sha(file)==info['predicciones_sha256'];p=loadcsv(file)
            self.validate_predictions(p,test,c,label);return p
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
                info['estado']='numerico_prediccion';guardar(meta,info)
                guardar(target/'prediccion_no_finita.json',dict(etiqueta=label,traceback=traceback.format_exc()));self.checkpoint();return None
        frame=test[[*LLAVES,'anio_previo','puntaje_previo']].copy()
        frame['id']=c['id'];frame['ajuste']=label;frame['observado']=test[anterior.RESULTADO].to_numpy();frame['cambio_predicho']=delta
        frame['prediccion']=pred;frame['error']=pred-frame.observado;frame['origen']=self.origin
        self.validate_predictions(frame,test,c,label)
        csv(target/'entradas_prediccion.csv',test[[*LLAVES,*c['entradas']]])
        csv(file,frame);info.update(predicciones_sha256=sha(file),segundos_prediccion=time.monotonic()-started,fuera_0_500=int(((pred<0)|(pred>500)).sum()))
        info['entradas_prediccion_sha256']=sha(target/'entradas_prediccion.csv')
        guardar(meta,info);self.checkpoint();return frame
    def window(self,w):
        year=w['externo'];expected=[i['validacion'] for i in w['internas']];scores=[]
        if year!=2021:
            for c in self.cs:
                parts=[];valid=[]
                for i in w['internas']:
                    tr,te=dividir(self.panel,i['entrenamiento'],i['validacion'])
                    p=self.predict(f"e{year}_i{i['validacion']}_{c['id']}",c,tr,te)
                    if p is not None:parts.append(p);valid.append(i['validacion'])
                score=dict(id=c['id'],estado='completo' if valid==expected else 'inelegible',ventanas=valid,mae=None,rmse=None)
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
        self.checkpoint()
        roles={'procedimiento_v4':decision['global_id'],**{f'procedimiento_{s}':v for s,v in decision['especificaciones'].items()},'persistencia':'persistencia'}
        tr,te=dividir(self.panel,w['entrenamiento'],year);preds={}
        for ident in sorted(set(roles.values()),key=lambda ident:self.byid[ident]['orden']):
            p=self.predict(f'e{year}_externo_{ident}',self.byid[ident],tr,te)
            if p is None:raise RuntimeError('ganador externo fallido: '+ident)
            preds[ident]=p
        rows=[]
        for role,ident in roles.items():
            p=preds[ident].copy();p['procedimiento']=role;p['externo']=year;p['seleccion_sha256']=sha(selection);rows.append(p)
        csv(self.out/f'externas_{year}.csv',pd.concat(rows));self.checkpoint()
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
        guardar(self.out/'estado.json',dict(completo=True,consumido=self.budget.data['consumido'],ajustes=len(self.budget.data['ajustes']),segundos_ejecucion_invocacion=time.monotonic()-started,terminado=now(),origen=self.origin));self.checkpoint()

def auditar_orden(out,cs):
    """Orden exacto del ledger, incluyendo intentos fallidos; no realiza ajustes."""
    ledger=read(out/'ledger.json');expected=[]
    for w in ventanas():
        year=w['externo'];decision=read(out/f'seleccion_{year}.json')
        for c in cs:
            if c['familia']!='persistencia':
                expected.extend(f"e{year}_i{i['validacion']}_{c['id']}" for i in w['internas'])
        expected.extend(f'e{year}_externo_{ident}' for ident in ids_externos(decision) if ident!='persistencia')
    expected.extend(f"e{w['externo']}_repeticion_{read(out/f"seleccion_{w['externo']}.json")['global_id']}" for w in ventanas() if read(out/f"seleccion_{w['externo']}.json")['global_id']!='persistencia')
    actual=[]
    for label in expected:
        meta=read(out/'ajustes'/label/'ajuste.json')
        assert meta['intento'] in (1,2)
        actual.extend(label+f'_intento{i}' for i in range(1,meta['intento']+1))
        assert meta['tiempo']==next(r for r in ledger['ajustes'] if r['etiqueta']==actual[-1])
        if '_externo_' in label:
            year=int(label[1:5]);d=read(out/f'seleccion_{year}.json')
            assert datetime.fromisoformat(d['instante_antes_externo'])<datetime.fromisoformat(meta['instante_inicio'])
    assert actual==[r['etiqueta'] for r in ledger['ajustes']],'orden de ajustes/intentos incorrecto'
    return dict(aprobado=True,ajustes_distintos=len(expected),intentos=len(actual))

def freeze():
    assert not (OUT/'piloto/ledger.json').exists(),'no recongelar tras primer fit'
    assert read(OUT/'pruebas_sinteticas.json')['aprobado']
    check_hashes(read(OUT/'pruebas_sinteticas.json')['fuentes_sha256'])
    artifacts=[*sorted((E2/'fuentes').glob('*.py')),OUT/'entorno.json',OUT/'pruebas_sinteticas.json',CONFIG,PANEL,E1/'resultados/congelacion_previa.json']
    artifacts += [E2/'PROTOCOLO_OPERATIVO.md',E2/'.gitattributes']
    artifacts += [ROOT/p for p in read(E1/'resultados/congelacion_previa.json')['artefactos_sha256']]
    guardar(OUT/'congelacion_operativa.json',dict(instante=now(),artefactos_sha256={str(p.relative_to(ROOT)):sha(p) for p in artifacts},semilla=SEMILLA,limite=7200,cota_sin_fallos=308,ajustes_antes=0,orden='externos crecientes; candidatos JSON; internas crecientes; selección antes de externos; IDs externos por JSON; cinco repeticiones globales',motor='comun_v4.Presupuesto/comun.Presupuesto: Pipeline completo, spawn serial terminable'))

def verify_freeze():
    verificar_etapa1();check_hashes(read(OUT/'congelacion_operativa.json')['artefactos_sha256']);environment()

def main():
    if '--preflight' in sys.argv:preflight();return
    if '--freeze' in sys.argv:freeze();return
    verify_freeze();runner=None
    try:
        runner=Runner(OUT/'piloto',loadcsv(PANEL));runner.run()
    except BaseException:
        ledger=read(OUT/'piloto/ledger.json') if (OUT/'piloto/ledger.json').exists() else dict(consumido=0,ajustes=[])
        guardar(OUT/'piloto/estado.json',dict(completo=False,consumido=ledger['consumido'],ajustes=len(ledger['ajustes']),traceback=traceback.format_exc(),terminado=now()))
        if runner is not None:runner.checkpoint()
        raise
if __name__=='__main__':main()
