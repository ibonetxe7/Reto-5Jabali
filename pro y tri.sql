USE JABALI;
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

INSERT INTO RECETA (valor_nutricional, fecha_creacion) values (350, now());

