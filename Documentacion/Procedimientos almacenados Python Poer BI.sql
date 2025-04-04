CREATE PROCEDURE sp_CalcularPromedios
AS
BEGIN
    SELECT
        AVG(salud) AS promedio_salud,
        AVG(crecimiento_personal) AS promedio_crecimiento,
        AVG(familia_amigos) AS promedio_familia_amigos,
        AVG(amor) AS promedio_amor,
        AVG(ocio) AS promedio_ocio,
        AVG(trabajo) AS promedio_trabajo,
        AVG(dinero) AS promedio_dinero
    FROM usuario;
END;

EXEC sp_CalcularPromedios;



CREATE PROCEDURE sp_CalcularDesviaciones
AS
BEGIN
    SELECT
        STDEV(salud) AS desviacion_salud,
        STDEV(crecimiento_personal) AS desviacion_crecimiento,
        STDEV(familia_amigos) AS desviacion_familia_amigos,
        STDEV(amor) AS desviacion_amor,
        STDEV(ocio) AS desviacion_ocio,
        STDEV(trabajo) AS desviacion_trabajo,
        STDEV(dinero) AS desviacion_dinero
    FROM usuario;
END;


EXEC sp_CalcularDesviaciones;



CREATE PROCEDURE sp_CalcularMedianas
AS
BEGIN
    SELECT
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salud) OVER () AS mediana_salud,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY crecimiento_personal) OVER () AS mediana_crecimiento,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY familia_amigos) OVER () AS mediana_familia_amigos,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amor) OVER () AS mediana_amor,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ocio) OVER () AS mediana_ocio,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY trabajo) OVER () AS mediana_trabajo,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY dinero) OVER () AS mediana_dinero
    FROM usuario;
END;




EXEC sp_CalcularMedianas;
