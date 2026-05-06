USE JABALI;
DELIMITER //
CREATE PROCEDURE calcular_imc_cliente(
    IN p_id_cli INT
)
BEGIN
    DECLARE v_peso DECIMAL(5,2);
    DECLARE v_altura_cm INT;
    DECLARE v_altura_m DECIMAL(4,2);
    DECLARE v_imc DECIMAL(5,2);

    -- Recuperar peso y altura tal como están en la BD
    SELECT peso, altura INTO v_peso, v_altura_cm
    FROM IMC
    INNER JOIN CLIENTE USING(id_cli)
    WHERE IMC.id_cli = p_id_cli
    LIMIT 1;

    -- Convertir a metros para calcular IMC (solo para el cálculo)
    SET v_altura_m = v_altura_cm / 100.0;

    IF v_altura_cm > 0 AND v_peso IS NOT NULL THEN
        SET v_imc = v_peso / (v_altura_m * v_altura_m);

        SELECT 
            p_id_cli AS id_cliente,
            v_peso AS peso_kg,
            v_altura_cm AS altura_cm,
            ROUND(v_imc, 2) AS imc;
    ELSE
        SELECT 'Altura inválida o cliente sin peso registrado' AS error;
    END IF;
END //

DELIMITER ;
DELIMITER //
CREATE PROCEDURE caclculo_nutriscore (
IN p_id_receta INT, 
out nutriscore char
)
BEGIN 
	declare exit handler for sqlexception
    begin 
    rollback;
	signal sqlstate "45000" set message_text = "El id introducido no existe";
    end;
    start transaction;
	IF (select  i.sostenibilidad_producto from ingrediente i
		join receta_ingrediente ri on ri.id_ingrediente = i.id_ingrediente
		where ri.id_receta = p_id_receta) = "km0" then 
		set nutriscore = "A";
	ELSEIF (select  i.sostenibilidad_producto from ingrediente i
		join receta_ingrediente ri on ri.id_ingrediente = i.id_ingrediente
		where ri.id_receta = p_id_receta) = "Colindante" then 
		set nutriscore = "B";
	ELSEIF  (select  i.sostenibilidad_producto from ingrediente i
		join receta_ingrediente ri on ri.id_ingrediente = i.id_ingrediente
		where ri.id_receta = p_id_receta) = "Nacional" then 
		set nutriscore = "C";
	ELSE set nutriscore = "D";
    end if;
    commit;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER tr_nutriscore AFTER insert on receta for each row
BEGIN
	if nutriscore is null then 
		call calculo_nutriscore(id_receta, @nutriscore);
        set new.nutriscore =  @nutriscore;
	end if;
END //
DELIMITER ;




