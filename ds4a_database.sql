create table  barrios(
	Cod_Barrio text, 
	Barrio text
)



     
Cod_Barrio	Barrio	Vigencia	Fecha_Corte	Tipo_AlojM	Tipo_AlquM	HabitacionesP	Tasa_O2	Ingreso_USDS	Ingreso_Hab_Dia	...	Calif-LimpiezaP	Calif_LocalizaciónP	Calif_ValoresP	MascotasM	ComodidadesM	Localidad	Cant_PropiedadesS	EstratoM	Percapita	Media_Arriendo
select * from airbnb;



select count(*)
from 
(
select distinct "Cod_Barrio", "Barrio"
from airbnb
) a; 


insert into barrios 
select distinct "Cod_Barrio", "Barrio"
from airbnb;

select *
from barrios; 


select "Cod_Barrio", "Barrio", "Fecha_Corte", "Cant_PropiedadesS"
from airbnb
where "Cod_Barrio" = '008214'
order by 3; 