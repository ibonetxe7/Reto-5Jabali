CREATE DATABASE if not exists JABALI;
use  JABALI;

CREATE TABLE if not exists USUARIO(
id_usu INT AUTO_INCREMENT PRIMARY KEY ,
nombre_usu VARCHAR(50), 
apellido1_usu varchar(50),
apellido2_usu varchar(50),
mail_usu varchar(255),
telefono INT,
localidad varchar(50)
);
CREATE TABLE if not exists CLIENTE(
id_cli INT AUTO_INCREMENT PRIMARY KEY,
id_usu INT NOT NULL,
num_logs INT, 
num_recetas INT,
contrasenia VARCHAR (200),
FOREIGN KEY (id_usu) references USUARIO(id_usu) on delete cascade
);
CREATE TABLE  if not exists INGREDIENTE(
id_ingrediente INT PRIMARY KEY AUTO_INCREMENT,
nombre_ingrediente VARCHAR(50),
sostenibilidad_producto ENUM("Km0", "Colindante", "Nacional", "Global"),
cecliaco boolean,
caducidad date	
);

CREATE TABLE if not exists RECETA(
id_receta INT PRIMARY KEY AUTO_INCREMENT, 
id_cli INT not null, 
nombre_receta VARCHAR(50),
valor_nutricional INT,
nutriscore char,
fecha_creacion datetime,
foreign key (id_cli) references CLIENTE(id_cli) ON DELETE CASCADE
    
);

CREATE TABLE IF NOT EXISTS RECETA_INGREDIENTE(
id_receta INT PRIMARY KEY,
id_ingrediente INT,
FOREIGN KEY (id_receta) references RECETA (id_receta) on delete cascade,
foreign key (id_ingrediente) references INGREDIENTE(id_ingrediente) 
    on delete cascade
    );

CREATE TABLE if not exists ALERGENO(
id_alergeno INT PRIMARY KEY AUTO_INCREMENT,
descripción VARCHAR(50)
);

CREATE TABLE INGREDIENTE_ALERGENO(
id_ingrediente INT not null ,
id_alergeno INT not null,
foreign key(id_ingrediente) references INGREDIENTE(id_ingrediente)on delete cascade,
foreign key(id_alergeno) references ALERGENO(id_alergeno) on delete cascade
);
CREATE VIEW recetas_celiacos AS
SELECT r.*
FROM receta r
WHERE r.id_receta NOT IN (
    SELECT ri.id_receta
    FROM receta_ingrediente ri
    JOIN ingrediente i ON ri.id_ingrediente = i.id_ingrediente
    WHERE i.cecliaco = TRUE
);
CREATE VIEW ingredientes_hipoalergenicos AS
SELECT i.*
FROM ingrediente i
WHERE i.id_ingrediente NOT IN (
    SELECT ia.id_ingrediente
    FROM ingrediente_alergeno ia
);
CREATE TABLE if not exists ADMINISTRADOR(
id_admin INT AUTO_INCREMENT PRIMARY KEY,
id_usu INT NOT NULL,
fecha_inicio date, 
fecha_fin date,
nombre_usu varchar (200),
contrasenia VARCHAR (200),
FOREIGN KEY (id_usu) references USUARIO(id_usu) on delete cascade
);
CREATE TABLE if not exists IMC(
	id_IMC INT PRIMARY KEY AUTO_INCREMENT,
    id_cli INT ,
    IMC DECIMAL(5,2),
    altura INT ,
    edad INT,
    foreign key (id_cli) references CLIENTE(id_cli) ON DELETE CASCADE
    );