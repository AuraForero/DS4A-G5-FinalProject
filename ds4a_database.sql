create table      
     
Cod_Barrio	Barrio	Vigencia	Fecha_Corte	Tipo_AlojM	Tipo_AlquM	HabitacionesP	Tasa_O2	Ingreso_USDS	Ingreso_Hab_Dia	...	Calif-LimpiezaP	Calif_LocalizaciónP	Calif_ValoresP	MascotasM	ComodidadesM	Localidad	Cant_PropiedadesS	EstratoM	Percapita	Media_Arriendo
select * from airbnb;



select count(*)
from 
(
select distinct "Cod_Barrio", "Barrio"
from airbnb
) a; 