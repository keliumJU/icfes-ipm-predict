"""Casos conocidos de recálculo independiente, sin panel ni ajustes."""
from enmienda_reporte import *

def test():
 known=independent([1,2,3],[2,2,1]);assert known['mae']==1;assert math.isclose(known['rmse'],math.sqrt(5/3));assert known['sesgo']==-1/3;assert known['r2']==-1.5
 assert independent([2,2],[2,3])['r2'] is None
 assert re.fullmatch(r'e(202[1-5])_i(2019|202[1-4])_(.+)','e2023_i2022_ols_ipm_00')
 assert not re.fullmatch(r'e(202[1-5])_i(2019|202[1-4])_(.+)','e2023_externo_ols_ipm_00')
 # Dos errores anuales: RMSE conjunto, nunca promedio de RMSE por año.
 joint=independent([0,0],[0,4]);assert joint['rmse']==math.sqrt(8) and joint['rmse']!=2
 guardar(F3/'resultados/pruebas_recalculo.json',dict(aprobado=True,origen='sintetico',pruebas=['metricas conocidas y sesgo','R2 nulo denominador cero','regex separa interno de externo IPM','RMSE errores concatenados'],ajustes=0));print('Recálculo sintético independiente aprobado.')
if __name__=='__main__':test()
