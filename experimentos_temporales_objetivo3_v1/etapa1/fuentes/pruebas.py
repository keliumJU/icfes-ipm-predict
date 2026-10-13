"""Controles completos con inventados/dobles; nunca recibe/reconstruye panel real."""
import copy
import inspect
import io
import json
import math
import multiprocessing as mp
import sys
import unittest
import uuid
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
from sklearn import config_context,get_config
from sklearn.exceptions import ConvergenceWarning
from comun import *
from seguridad import destino,guardar,texto_nuevo,leer,checkpoint
from motor import PresupuestoInventado,proceso
from worker import prueba_hijo
from orquestacion import plan_contratado,dividir,ventana_inventada,comprobar_global_inventado


def inventado(ncodes=3):
    rows = []
    cov = [c.removeprefix('cambio_') for c in GROUPS['cambio_ambas'][1:]]
    for i in range(ncodes):
        for year in YEARS:
            r = dict(codigo_departamento=f'{i+1:02d}',anio=year,prom_punt_global=100.+i+(year-2018)*3)
            r.update({v:float(j+i+(year-2018)*.2) for j,v in enumerate(cov)})
            rows.append(r)
    p = historial(pd.DataFrame(rows),cov)
    p.attrs['origen'] = 'inventado'
    return p


def train_inventado():
    p = inventado()
    q = p[p.anio.isin([2019,2021,2022])].sort_values(KEYS).reset_index(drop=True).copy()
    q.attrs['origen'] = 'inventado'
    return q


class DobleModelo:
    def predict(self,X):
        return np.full(len(X),3.)


def executor_doble(c,train,context,saldo):
    X,y = matrices(train,c)
    w,meta = pesos(train[KEYS])
    return (DobleModelo(),dict(origen='inventado',tipo='doble sin fit',pesos=meta,
                               contexto=context,ruta_fit=list(fit_kwargs(c,w)))),.001


class Controles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = destino(TEST/('sesion_'+uuid.uuid4().hex),TEST)
        cls.base.mkdir(parents=True)
        cls.context = dict(origen='inventado',semilla=SEED)
        cls.fit_count = 0

    def rejects(self,fn,*args,**kwargs):
        with self.assertRaises((ValueError,RuntimeError,TimeoutError,OSError,EOFError,AssertionError,KeyError,FileExistsError)):
            fn(*args,**kwargs)

    def budget(self,name,limit=20):
        return PresupuestoInventado(self.base/(name+'.json'),self.context,limit)

    def test_01_pesos_formula_independiente(self):
        keys = pd.DataFrame({'codigo_departamento':['01']*3,'anio':[2019,2021,2023]})
        w,m = pesos(keys)
        expected = [float(Fraction(3)*v/Fraction(7,4)) for v in [Fraction(1,4),Fraction(1,2),Fraction(1)]]
        self.assertEqual(w.tolist(),expected)
        self.assertEqual(m['ancla_train'],2023)
        self.assertEqual(math.fsum(w),3.)
        self.assertTrue((w>0).all())

    def test_02_pesos_anios_territorios_uniforme(self):
        q = train_inventado()
        w,m = pesos(q[KEYS])
        for a in q.anio.unique():
            self.assertEqual(len(set(w[q.anio.eq(a)])),1)
        self.assertAlmostEqual(math.fsum(w),len(q),places=12)
        uniform,um = pesos(q[q.anio.eq(2019)][KEYS])
        self.assertTrue(np.array_equal(uniform,np.ones(3)))
        explicit,_ = pesos(q[KEYS],'uniforme')
        self.assertTrue(np.array_equal(explicit,np.ones(len(q))))

    def test_03_train_only_y_rechazos(self):
        self.assertEqual(list(inspect.signature(pesos).parameters),['train_keys','esquema'])
        q = train_inventado()
        old = pesos(q[KEYS])
        future = inventado()
        future.prom_punt_global = 999999.
        np.testing.assert_array_equal(old[0],pesos(q[KEYS])[0])
        self.rejects(pesos,q[KEYS+['prom_punt_global']])
        self.rejects(pesos,q[KEYS].iloc[::-1])
        self.rejects(pesos,q[KEYS].iloc[:0])
        self.rejects(pesos,q[KEYS],'h1')
        self.rejects(pesos,pd.concat([q[KEYS],q[KEYS].iloc[:1]]))
        self.rejects(pesos,pd.DataFrame({'codigo_departamento':['01'],'anio':[np.inf]}))
        self.rejects(pesos,pd.DataFrame({'codigo_departamento':['01'],'anio':[2021.5]}))
        self.rejects(pesos,pd.DataFrame({'codigo_departamento':['01','01'],'anio':[-100000,2021]}))

    def test_04_intervalos_negativos_sin_anualizar(self):
        p = inventado(1)
        self.assertEqual(p[p.anio.eq(2021)].anio_previo.iloc[0],2019)
        self.assertEqual(p[p.anio.eq(2021)].intervalo.iloc[0],2)
        self.assertEqual(p[p.anio.eq(2021)].cambio_observado.iloc[0],6.)
        self.assertEqual(p[p.anio.eq(2019)].cambio_observado.iloc[0],3.)
        source = pd.DataFrame(dict(codigo_departamento=['01','01'],anio=[2019,2021],prom_punt_global=[10.,2.]))
        q = historial(source,[])
        self.assertEqual(q.cambio_observado.iloc[-1],-8.)

    def test_05_defaults_36_entradas(self):
        self.assertTrue(comprobar_defaults())
        self.assertEqual(sum(c['familia']=='mediana' for c in CS),15)
        self.assertEqual(sum(c['familia']=='boosting_absoluto' for c in CS),20)
        self.assertFalse(set(INPUTS)&{'anio','codigo_departamento','intervalo','n_estudiantes','n'})
        q = train_inventado()
        for c in CS[1:]:
            X,y = matrices(q,c)
            self.assertEqual(X.shape,(len(q),c['n_ajustadas']))
        c = copy.deepcopy(CS[1]); c['entradas'].append('anio')
        self.rejects(construir,c)
        self.rejects(matrices,q,CS[0])
        self.rejects(construir,CS[0])

    def test_06_routing_dobles_modelos_reciben_peso(self):
        q = train_inventado()
        calls = []
        class Spy:
            def fit(self,X,y,**kwargs):
                calls.append((X.copy(),y.copy(),kwargs,get_config()['enable_metadata_routing']))
                return self
        for c in CS[1:]:
            _,meta = ajustar_inventado(c,q,self.context,constructor=lambda _:Spy())
            X,y,kw,routing = calls[-1]
            expected = ['escalado__sample_weight','modelo__sample_weight'] if c['familia']=='mediana' else ['sample_weight']
            self.assertEqual(list(kw),expected)
            for weight in kw.values():
                np.testing.assert_array_equal(weight,pesos(q[KEYS])[0])
            self.assertFalse(routing)
            np.testing.assert_array_equal(y,q.cambio_observado)
            self.assertEqual(meta['origen'],'inventado')
        one = q[q.anio.eq(2019)].copy()
        for c in (CS[1],CS[16]):
            ajustar_inventado(c,one,self.context,constructor=lambda _:Spy())
            self.assertEqual(calls[-1][2],{})

    def test_07_fits_inventados_35_scaler_uniformidad(self):
        q = train_inventado()
        one = q[q.anio.eq(2019)].copy()
        records = []
        with config_context(enable_metadata_routing=True):
            for c in CS[1:]:
                model,meta = ajustar_inventado(c,q,self.context)
                records.append(meta)
                type(self).fit_count += 1
                self.assertTrue(get_config()['enable_metadata_routing'])
                self.assertEqual(meta['ruta_fit'],list(fit_kwargs(c,pesos(q[KEYS])[0])))
                weighted_predictions = model.predict(q[c['entradas']].to_numpy(float))
                self.assertTrue(np.isfinite(weighted_predictions).all())
                actual,uniform_meta = ajustar_inventado(c,one,self.context)
                records.append(uniform_meta)
                type(self).fit_count += 1
                X,y = matrices(one,c)
                original = construir(c)
                with config_context(enable_metadata_routing=False):
                    original.fit(X,y)
                type(self).fit_count += 1
                np.testing.assert_array_equal(actual.predict(X),original.predict(X))
                self.assertEqual(uniform_meta['ruta_fit'],[])
                if c['familia']=='mediana':
                    self.assertEqual(meta['transformaciones']['suma_pesos'],math.fsum(pesos(q[KEYS])[0]))
                    np.testing.assert_array_equal(actual.named_steps['escalado'].mean_,original.named_steps['escalado'].mean_)
        guardar(self.base/'metadatos_modelos_inventados.json',dict(origen='inventado',
                ajustes_ponderados_y_uniformes=records,ruta_original_sin_pesos=35,
                originales_defaults=[c['parametros_completos'] for c in CS[1:]],
                originales_train_llaves=one[KEYS].values.tolist(),semilla=SEED,sklearn=sklearn.__version__,
                notas='Todas pruebas inventadas; no resultados ni modelos del panel real'))

    def test_08_prohibicion_real_y_convergencia(self):
        q = train_inventado(); q.attrs.clear()
        self.rejects(ajustar_inventado,CS[1],q,self.context)
        q = train_inventado()
        self.rejects(ajustar_inventado,CS[1],q,dict(origen='real'))
        class Warn:
            def fit(self,*args,**kwargs):
                __import__('warnings').warn('doble',ConvergenceWarning)
        self.rejects(ajustar_inventado,CS[1],q,self.context,constructor=lambda _:Warn())

    def rows(self,expected):
        return [dict(id=c['id'],estado='completo',ventanas=expected,mae=10.,rmse=10.,razon=None) for c in CS]

    def test_09_bandas_global_grupos_y_orden(self):
        r = self.rows([2021])
        r[0].update(mae=1.1,rmse=1.1)
        r[1].update(mae=1.,rmse=1.)
        self.assertEqual(seleccionar(r,[2021],2022)['global_id'],'persistencia')
        r[0]['mae'] = np.nextafter(1.1,math.inf)
        self.assertEqual(seleccionar(r,[2021],2022)['global_id'],CS[1]['id'])
        r = self.rows([2021])
        r[1].update(mae=1.,rmse=1.2)
        r[2].update(mae=1.05,rmse=1.)
        self.assertEqual(seleccionar(r,[2021],2022)['global_id'],CS[2]['id'])
        r[1]['rmse'] = 1.1
        self.assertEqual(seleccionar(r,[2021],2022)['global_id'],CS[1]['id'])
        r = self.rows([2021])
        r[1].update(mae=2.,rmse=2.)
        r[4].update(mae=1.,rmse=1.)
        d = seleccionar(r,[2021],2022)
        self.assertEqual(d['global_id'],CS[4]['id'])
        self.assertEqual(d['especificaciones']['historico'],CS[1]['id'])
        r[16].update(mae=1.,rmse=1.)
        r[1].update(mae=1.,rmse=1.)
        self.assertEqual(seleccionar(r,[2021],2022)['global_id'],CS[1]['id'])
        self.assertEqual(len(ids_externos(d)),len(set(ids_externos(d))))

    def test_10_seleccion_cobertura_fallos_2021(self):
        fixed = seleccionar([],[],2021)
        self.assertEqual(set(ids_externos(fixed)),{'persistencia'})
        self.rejects(seleccionar,self.rows([2021]),[2021],2021)
        self.rejects(seleccionar,self.rows([2021])[:-1],[2021],2022)
        r = self.rows([2021]); r[1]['mae_externo']=0
        self.rejects(seleccionar,r,[2021],2022)
        r = self.rows([2021]); r[1]['id']=r[0]['id']
        self.rejects(seleccionar,r,[2021],2022)
        r = self.rows([2021]); r[1].update(estado='fallo',razon='inventado',mae=None,rmse=None)
        self.assertEqual(seleccionar(r,[2021],2022)['global_id'],'persistencia')
        r[1]['razon']=None
        self.rejects(seleccionar,r,[2021],2022)
        r = self.rows([2021]); r[0].update(estado='fallo',razon='inventado')
        self.rejects(seleccionar,r,[2021],2022)
        self.rejects(seleccionar,self.rows([2021]),[2022],2022)

    def test_11_csv_exacto_errores_y_finitos(self):
        a = pd.DataFrame({'codigo_departamento':['01','02'],'anio':[2021,2021],'valor':[0.,1.]})
        b = a.copy(); b.valor = [0,1]
        exact(a,b)
        p = self.base/'exacto.csv'
        a.to_csv(p,index=False,float_format='%.17g')
        exact(a,csv(p))
        b = a.copy(); b.loc[0,'valor']=1e-11
        self.rejects(exact,a,b)
        self.rejects(exact,a,a.iloc[::-1].reset_index(drop=True))
        self.rejects(exact,a,a[['anio','codigo_departamento','valor']])
        self.rejects(exact,a,a.drop(columns='valor'))
        self.rejects(exact,a,a.iloc[:1])
        self.rejects(validate,pd.concat([a,a.iloc[:1]],ignore_index=True))
        b = a.copy(); b.loc[0,'codigo_departamento']=None
        self.rejects(validate,b)
        for v in [math.nan,math.inf,-math.inf]:
            b = a.copy(); b.loc[0,'valor']=v
            self.rejects(validate,b,finite=['valor'])
        b = a.copy(); b.loc[0,'codigo_departamento']='03'
        self.rejects(validate,b,expected=a[KEYS])

    def test_12_aritmetica_independiente(self):
        y = [0.,1.,-2.]; pred = [1.,3.,-4.]
        errors = [Fraction.from_float(p)-Fraction.from_float(t) for p,t in zip(pred,y)]
        m = metricas(y,pred)
        self.assertEqual(m['mae'],float(sum(abs(e) for e in errors)/3))
        self.assertEqual(m['rmse'],math.sqrt(float(sum(e*e for e in errors)/3)))
        self.assertEqual(m['sesgo'],float(sum(errors)/3))
        for args in [([],[]),([1],[math.nan]),([1],[1,2])]:
            self.rejects(metricas,*args)

    def test_13_orquestacion_36_cobertura_linaje(self):
        p = inventado(33)
        b = self.budget('orquestacion',100)
        parts,outs,signatures = [],[],{}
        for year in range(2021,2026):
            result = ventana_inventada(p,year,b,executor_doble)
            comprobar_global_inventado(p,result,year,b,executor_doble)
            outs.append(result['externas']); parts.extend(result['internas']); signatures.update(result['firmas'])
            if year == 2021:
                self.assertFalse(b.data['ajustes'])
                self.assertTrue(result['externas'].id.eq('persistencia').all())
        all_internal = pd.concat(parts,ignore_index=True)
        self.assertEqual(len(all_internal),11880)
        unique,lineage = colapsar(all_internal,signatures)
        self.assertEqual(len(unique),4752)
        self.assertEqual(len(lineage),11880)
        out = pd.concat(outs,ignore_index=True)
        self.assertTrue(cobertura(out,p.codigo_departamento))
        self.rejects(cobertura,out.iloc[:-1],p.codigo_departamento)
        bad = out.copy(); bad.loc[0,'observado'] += 1e-11
        self.rejects(cobertura,bad,p.codigo_departamento)
        bad = out.copy(); bad.loc[0,'prediccion']=math.inf
        self.rejects(cobertura,bad,p.codigo_departamento)
        bad = all_internal.copy(); bad.loc[0,'prediccion'] += 1e-11
        self.rejects(colapsar,bad,signatures)
        badsign = copy.deepcopy(signatures)
        key = next(k for k in badsign if k[0]==2025 and k[2]==2021)
        badsign[key]['semilla'] = 3
        self.rejects(colapsar,all_internal,badsign)
        self.rejects(colapsar,pd.concat([all_internal,all_internal.iloc[:1]]),signatures)
        plan = plan_contratado()
        self.assertEqual(plan['cota_internos'],350)
        self.assertEqual(plan['cota_total'],350+24+4)
        self.assertFalse(plan['disponible_en_etapa1'])
        self.rejects(dividir,p,[2019],2022)
        self.rejects(dividir,p[p.codigo_departamento.ne('01')|p.anio.ne(2022)],[2019,2021],2022)
        p.attrs.clear()
        self.rejects(ventana_inventada,p,2022,b,executor_doble)
        guardar(self.base/'orquestacion_resumen.json',dict(origen='inventado',dobles_sin_fit=len(b.data['ajustes']),
            internas=len(all_internal),unicas=len(unique),linaje=len(lineage),externas=len(out),meta_real=False))

    def test_14_destinos_y_symlinks(self):
        self.rejects(destino,ROOT/'diseno_temporal_objetivo3_v1/x')
        self.rejects(destino,E1/'../x')
        self.rejects(PresupuestoInventado,OUT/'ledger.json',self.context,10)
        self.rejects(PresupuestoInventado,self.base/'real.json',dict(origen='real'),10)
        link = self.base/'link'
        link.symlink_to(ROOT/'diseno_temporal_objetivo3_v1',target_is_directory=True)
        self.rejects(destino,link/'x',TEST)
        filelink = self.base/'link_archivo'
        filelink.symlink_to(ROOT/'AGENTS.md')
        self.rejects(texto_nuevo,filelink,'prohibido')
        new = self.base/'nuevo.txt'
        texto_nuevo(new,'inventado')
        self.rejects(texto_nuevo,new,'distinto')

    def test_15_fallos_retry_reanudacion_contexto(self):
        q = train_inventado()
        b = self.budget('retry')
        n = [0]
        def retry(c,train,context,saldo):
            n[0] += 1
            if n[0] == 1:
                raise OSError('doble infraestructura')
            return executor_doble(c,train,context,saldo)
        b.ajustar('job',CS[1],q,self.context,retry)
        self.assertEqual(len(b.data['ajustes']),2)
        self.assertEqual(b.data['ajustes'][0]['clase_fallo'],'infraestructura')
        artifact = self.base/'artefacto.json'
        guardar(artifact,dict(origen='inventado'))
        self.assertTrue(b.reanudar_completo('job',self.context,{str(artifact):sha(artifact)}))
        self.rejects(b.reanudar_completo,'job',dict(origen='inventado',semilla=1),{str(artifact):sha(artifact)})
        self.rejects(b.reanudar_completo,'job',self.context,{str(artifact):'0'*64})
        self.rejects(b.reanudar_completo,'job',self.context,{})
        self.rejects(b.ajustar,'job',CS[1],q,self.context,retry)
        self.rejects(PresupuestoInventado,b.path,self.context,21)
        self.rejects(PresupuestoInventado,b.path,dict(origen='inventado',semilla=2),20)
        recovered = PresupuestoInventado(b.path,self.context,20)
        self.assertEqual(recovered.data,b.data)
        for name,exc,expected in [('numerico',ValueError,'numerico_convergencia'),('infra2',OSError,'infraestructura')]:
            b = self.budget(name)
            def fail(*args):
                raise exc('doble')
            self.rejects(b.ajustar,'fallo',CS[1],q,self.context,fail)
            count = len(b.data['ajustes'])
            self.assertEqual(count,1 if exc is ValueError else 2)
            self.assertEqual(b.data['ajustes'][-1]['clase_fallo'],expected)
            self.rejects(b.ajustar,'fallo',CS[1],q,self.context,fail)
            self.assertEqual(len(b.data['ajustes']),count)

    def test_16_tiempo_inclusivo_caida_no_medida(self):
        q = train_inventado()
        b = self.budget('limite',.1)
        self.rejects(b.ajustar,'limite',CS[1],q,self.context,lambda *args:((DobleModelo(),{}),.1))
        self.assertEqual(b.data['consumido'],.1)
        self.rejects(b.ajustar,'sin_saldo',CS[1],q,self.context,executor_doble)
        self.assertEqual(len(b.data['ajustes']),1)
        b = self.budget('caida',2)
        b.data['pendiente'] = dict(etiqueta='caida#1',saldo=2)
        checkpoint(b.path,b.data)
        recovered = PresupuestoInventado(b.path,self.context,2)
        self.assertEqual(recovered.data['consumido'],2)
        self.assertEqual(recovered.data['ajustes'][-1]['estado'],'interrupcion_no_medida')
        self.rejects(recovered.ajustar,'nuevo',CS[1],q,self.context,executor_doble)
        corrupt = self.budget('corrupto',2)
        corrupt.data['consumido'] = -1
        checkpoint(corrupt.path,corrupt.data)
        self.rejects(PresupuestoInventado,corrupt.path,self.context,2)

    def test_17_hijos_imports_terminacion_fit_real_inventado(self):
        before = {p.pid for p in mp.active_children()}
        status = proceso(prueba_hijo,('imports',),10)
        self.assertEqual(status['imports_ajenos'],[])
        self.assertTrue(status['bytecode'])
        self.rejects(proceso,prueba_hijo,('bloqueo',),.15)
        self.rejects(proceso,prueba_hijo,('caida',),5)
        self.assertEqual({p.pid for p in mp.active_children()},before)
        b = self.budget('spawn',15)
        model,meta = b.ajustar('spawn',CS[1],train_inventado(),self.context)
        type(self).fit_count += 1
        self.assertEqual(meta['origen'],'inventado')
        self.assertEqual(meta['ruta_fit'],['escalado__sample_weight','modelo__sample_weight'])
        self.assertGreater(b.data['consumido'],0.)
        guardar(self.base/'metadata_spawn.json',meta)


class Registro(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.registros=[]
    def addSuccess(self,test):
        super().addSuccess(test)
        self.registros.append(dict(prueba=test.id(),estado='aprobada'))
    def addFailure(self,test,err):
        super().addFailure(test,err)
        self.registros.append(dict(prueba=test.id(),estado='fallo',detalle=self._exc_info_to_string(err,test)))
    def addError(self,test,err):
        super().addError(test,err)
        self.registros.append(dict(prueba=test.id(),estado='error',detalle=self._exc_info_to_string(err,test)))


def ejecutar_pruebas(output=OUT/'pruebas.json'):
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream,verbosity=2,resultclass=Registro).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controles))
    value = dict(aprobado=result.wasSuccessful(),grupos_ejecutados=result.testsRun,controles=result.registros,
                 registro=stream.getvalue(),ajustes_estimadores_inventados=Controles.fit_count,
                 fits_panel_real=0,modelos_historicos_cargados=0,directorio_inventados=str(Controles.base))
    guardar(output,value)
    print(stream.getvalue())
    return value


if __name__ == '__main__':
    results = ejecutar_pruebas()
    sys.exit(0 if results['aprobado'] else 1)
