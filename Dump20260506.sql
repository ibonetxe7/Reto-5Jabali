-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: jabali
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administrador`
--

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrador` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `id_usu` int NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `nombre_usu` varchar(200) DEFAULT NULL,
  `contrasenia` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_admin`),
  KEY `id_usu` (`id_usu`),
  CONSTRAINT `administrador_ibfk_1` FOREIGN KEY (`id_usu`) REFERENCES `usuario` (`id_usu`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alergeno`
--

DROP TABLE IF EXISTS `alergeno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alergeno` (
  `id_alergeno` int NOT NULL AUTO_INCREMENT,
  `descripción` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_alergeno`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alergeno`
--

LOCK TABLES `alergeno` WRITE;
/*!40000 ALTER TABLE `alergeno` DISABLE KEYS */;
INSERT INTO `alergeno` VALUES (1,'Cereales con gluten'),(2,'Crustáceos'),(3,'Huevos'),(4,'Pescado'),(5,'Cacahuetes'),(6,'Soja'),(7,'Leche'),(8,'Frutos de cáscara'),(9,'Apio'),(10,'Mostaza'),(11,'Sésamo'),(12,'Dióxido de azufre y sulfitos'),(13,'Altramuces'),(14,'Moluscos');
/*!40000 ALTER TABLE `alergeno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cli` int NOT NULL AUTO_INCREMENT,
  `id_usu` int NOT NULL,
  `num_logs` int DEFAULT NULL,
  `num_recetas` int DEFAULT NULL,
  `contrasenia` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_cli`),
  KEY `id_usu` (`id_usu`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`id_usu`) REFERENCES `usuario` (`id_usu`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (200,200,NULL,NULL,NULL);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imc`
--

DROP TABLE IF EXISTS `imc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imc` (
  `id_IMC` int NOT NULL AUTO_INCREMENT,
  `id_cli` int DEFAULT NULL,
  `IMC` decimal(5,2) DEFAULT NULL,
  `altura` int DEFAULT NULL,
  `edad` int DEFAULT NULL,
  PRIMARY KEY (`id_IMC`),
  KEY `id_cli` (`id_cli`),
  CONSTRAINT `imc_ibfk_1` FOREIGN KEY (`id_cli`) REFERENCES `cliente` (`id_cli`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imc`
--

LOCK TABLES `imc` WRITE;
/*!40000 ALTER TABLE `imc` DISABLE KEYS */;
/*!40000 ALTER TABLE `imc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingrediente`
--

DROP TABLE IF EXISTS `ingrediente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingrediente` (
  `id_ingrediente` int NOT NULL AUTO_INCREMENT,
  `nombre_ingrediente` varchar(50) DEFAULT NULL,
  `sostenibilidad_producto` enum('Km0','Colindante','Nacional','Global') DEFAULT NULL,
  `cecliaco` tinyint(1) DEFAULT NULL,
  `caducidad` date DEFAULT NULL,
  PRIMARY KEY (`id_ingrediente`)
) ENGINE=InnoDB AUTO_INCREMENT=141 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingrediente`
--

LOCK TABLES `ingrediente` WRITE;
/*!40000 ALTER TABLE `ingrediente` DISABLE KEYS */;
INSERT INTO `ingrediente` VALUES (1,'Bacalao','Nacional',0,'2027-12-31'),(2,'Anchoa','Km0',0,'2026-12-31'),(3,'Merluza','Km0',0,'2026-06-15'),(4,'Txipiron (calamar)','Km0',0,'2026-06-15'),(5,'Pulpo','Nacional',0,'2026-06-15'),(6,'Gambas','Nacional',0,'2026-06-15'),(7,'Langostinos','Nacional',0,'2026-06-15'),(8,'Mejillones','Colindante',0,'2026-05-15'),(9,'Almejas','Km0',0,'2026-05-15'),(10,'Berberechos','Km0',0,'2026-05-15'),(11,'Nécoras','Km0',0,'2026-05-15'),(12,'Txangurro (centollo)','Km0',0,'2026-05-15'),(13,'Bonito del norte','Km0',0,'2026-06-15'),(14,'Atún rojo','Nacional',0,'2026-06-15'),(15,'Sardinas','Km0',0,'2026-05-15'),(16,'Besugo','Km0',0,'2026-06-15'),(17,'Lubina','Nacional',0,'2026-06-15'),(18,'Dorada','Nacional',0,'2026-06-15'),(19,'Rape','Nacional',0,'2026-06-15'),(20,'Kokotxas de bacalao','Nacional',0,'2026-06-15'),(21,'Angulas','Km0',0,'2026-05-15'),(22,'Percebes','Km0',0,'2026-05-15'),(23,'Langosta','Nacional',0,'2026-06-15'),(24,'Bogavante','Km0',0,'2026-05-15'),(25,'Vieiras','Colindante',0,'2026-05-15'),(26,'Ternera','Km0',0,'2026-06-20'),(27,'Txuleta (buey)','Km0',0,'2026-06-20'),(28,'Cordero','Nacional',0,'2026-06-20'),(29,'Cerdo ibérico','Nacional',0,'2027-12-31'),(30,'Pollo','Km0',0,'2026-06-20'),(31,'Pato','Nacional',0,'2026-06-20'),(32,'Conejo','Km0',0,'2026-06-18'),(33,'Cochinillo','Nacional',0,'2026-06-20'),(34,'Cabrito','Nacional',0,'2026-06-20'),(35,'Morcilla','Nacional',1,'2026-09-30'),(36,'Chorizo','Nacional',1,'2026-12-31'),(37,'Txistorra','Km0',1,'2026-07-31'),(38,'Jamón serrano','Nacional',0,'2028-01-01'),(39,'Jamón ibérico','Nacional',0,'2028-06-01'),(40,'Lomo embuchado','Nacional',0,'2027-12-31'),(41,'Pimiento rojo','Km0',0,'2026-06-28'),(42,'Pimiento verde','Km0',0,'2026-06-28'),(43,'Pimiento choricero','Km0',0,'2027-12-31'),(44,'Tomate','Km0',0,'2026-06-28'),(45,'Cebolla','Km0',0,'2026-07-31'),(46,'Ajo','Nacional',0,'2026-09-30'),(47,'Puerro','Km0',0,'2026-06-28'),(48,'Zanahoria','Km0',0,'2026-07-15'),(49,'Patata','Km0',0,'2026-08-28'),(50,'Berenjena','Km0',0,'2026-06-28'),(51,'Calabacín','Km0',0,'2026-06-28'),(52,'Espinacas','Km0',0,'2026-06-20'),(53,'Acelgas','Km0',0,'2026-06-20'),(54,'Coliflor','Km0',0,'2026-06-25'),(55,'Brócoli','Nacional',0,'2026-06-25'),(56,'Col','Km0',0,'2026-06-28'),(57,'Alcachofas','Nacional',0,'2026-06-28'),(58,'Espárragos blancos','Nacional',0,'2026-10-30'),(59,'Espárragos verdes','Nacional',0,'2026-10-30'),(60,'Judías verdes','Km0',0,'2026-06-25'),(61,'Guisantes','Km0',0,'2026-06-20'),(62,'Habas','Km0',0,'2026-06-20'),(63,'Pimientos de Gernika','Km0',0,'2026-06-28'),(64,'Tomate pera','Nacional',0,'2026-06-28'),(65,'Remolacha','Km0',0,'2026-07-15'),(66,'Apio','Nacional',0,'2026-06-25'),(67,'Nabo','Km0',0,'2026-07-15'),(68,'Hongos/setas','Km0',0,'2026-05-18'),(69,'Perretxikos','Km0',0,'2026-05-18'),(70,'Boletus','Colindante',0,'2026-05-18'),(71,'Trufas','Nacional',0,'2026-09-30'),(72,'Alubias rojas','Km0',0,'2027-12-31'),(73,'Alubia blanca','Nacional',0,'2027-12-31'),(74,'Alubias negras','Nacional',0,'2027-12-31'),(75,'Garbanzos','Nacional',0,'2027-12-31'),(76,'Lentejas','Nacional',0,'2027-12-31'),(77,'Pochas','Km0',0,'2027-12-31'),(78,'Huevos','Km0',0,'2026-07-15'),(79,'Leche entera','Km0',0,'2026-06-25'),(80,'Nata','Km0',0,'2026-06-22'),(81,'Mantequilla','Colindante',0,'2026-09-30'),(82,'Queso idiazábal','Km0',0,'2026-12-31'),(83,'Queso manchego','Nacional',0,'2026-12-31'),(84,'Queso de cabra','Nacional',0,'2026-08-28'),(85,'Requesón','Km0',0,'2026-06-22'),(86,'Harina de trigo','Nacional',1,'2027-12-31'),(87,'Pan blanco','Km0',1,'2026-05-10'),(88,'Pan de maíz (talo)','Km0',0,'2026-05-10'),(89,'Arroz','Nacional',0,'2027-12-31'),(90,'Maíz','Nacional',0,'2027-12-31'),(91,'Fideos','Nacional',1,'2027-12-31'),(92,'Pan rallado','Nacional',1,'2027-06-30'),(93,'Pasta','Nacional',1,'2027-12-31'),(94,'Aceite de oliva virgen extra','Nacional',0,'2028-06-01'),(95,'Aceite de girasol','Nacional',0,'2027-12-31'),(96,'Vinagre de vino','Nacional',0,'2028-01-01'),(97,'Vinagre de sidra','Km0',0,'2028-01-01'),(98,'Sidra natural','Km0',0,'2027-06-30'),(99,'Tomate frito','Nacional',0,'2028-01-01'),(100,'Pimiento morrón conserva','Nacional',0,'2028-01-01'),(101,'Sal','Nacional',0,'2035-01-01'),(102,'Pimienta negra','Global',0,'2028-01-01'),(103,'Pimentón dulce','Nacional',0,'2028-01-01'),(104,'Pimentón picante','Nacional',0,'2028-01-01'),(105,'Azafrán','Nacional',0,'2028-01-01'),(106,'Laurel','Km0',0,'2027-12-31'),(107,'Perejil','Km0',0,'2026-06-22'),(108,'Tomillo','Nacional',0,'2027-12-31'),(109,'Romero','Nacional',0,'2027-12-31'),(110,'Orégano','Nacional',0,'2027-12-31'),(111,'Albahaca','Nacional',0,'2026-06-22'),(112,'Comino','Global',0,'2028-01-01'),(113,'Canela','Global',0,'2028-01-01'),(114,'Nuez moscada','Global',0,'2028-01-01'),(115,'Guindilla','Km0',0,'2027-12-31'),(116,'Cebollino','Km0',0,'2026-06-22'),(117,'Manzana','Km0',0,'2026-07-15'),(118,'Pera','Km0',0,'2026-07-15'),(119,'Limón','Nacional',0,'2026-08-28'),(120,'Naranja','Nacional',0,'2026-08-28'),(121,'Uva','Nacional',0,'2026-06-28'),(122,'Higos','Nacional',0,'2026-06-20'),(123,'Ciruelas','Km0',0,'2026-06-20'),(124,'Cerezas','Nacional',0,'2026-06-20'),(125,'Membrillo','Nacional',0,'2026-09-30'),(126,'Almendras','Nacional',0,'2027-12-31'),(127,'Nueces','Nacional',0,'2027-12-31'),(128,'Piñones','Nacional',0,'2027-12-31'),(129,'Avellanas','Nacional',0,'2027-12-31'),(130,'Pasas','Nacional',0,'2027-06-30'),(131,'Caldo de pescado','Km0',0,'2026-06-20'),(132,'Caldo de carne','Km0',0,'2026-06-20'),(133,'Salsa verde','Km0',0,'2026-06-20'),(134,'Txakoli','Km0',0,'2027-12-31'),(135,'Vino blanco','Nacional',0,'2027-12-31'),(136,'Vino tinto','Nacional',0,'2027-12-31'),(137,'Brandy','Nacional',0,'2035-01-01'),(138,'Chocolate negro','Global',0,'2027-12-31'),(139,'Azúcar','Global',0,'2035-01-01'),(140,'Miel','Km0',0,'2030-01-01');
/*!40000 ALTER TABLE `ingrediente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingrediente_alergeno`
--

DROP TABLE IF EXISTS `ingrediente_alergeno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingrediente_alergeno` (
  `id_ingrediente` int NOT NULL,
  `id_alergeno` int NOT NULL,
  PRIMARY KEY (`id_ingrediente`,`id_alergeno`),
  KEY `id_alergeno` (`id_alergeno`),
  CONSTRAINT `ingrediente_alergeno_ibfk_1` FOREIGN KEY (`id_ingrediente`) REFERENCES `ingrediente` (`id_ingrediente`) ON DELETE CASCADE,
  CONSTRAINT `ingrediente_alergeno_ibfk_2` FOREIGN KEY (`id_alergeno`) REFERENCES `alergeno` (`id_alergeno`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingrediente_alergeno`
--

LOCK TABLES `ingrediente_alergeno` WRITE;
/*!40000 ALTER TABLE `ingrediente_alergeno` DISABLE KEYS */;
INSERT INTO `ingrediente_alergeno` VALUES (35,1),(36,1),(37,1),(38,1),(95,1),(96,1),(98,1),(101,1),(102,1),(6,2),(7,2),(23,2),(24,2),(87,3),(1,4),(2,4),(3,4),(13,4),(14,4),(15,4),(16,4),(17,4),(18,4),(19,4),(20,4),(88,7),(89,7),(90,7),(91,7),(92,7),(93,7),(94,7),(133,8),(134,8),(135,8),(136,8),(35,12),(38,12),(4,14),(5,14),(8,14),(9,14),(10,14),(11,14),(12,14),(21,14),(22,14),(25,14);
/*!40000 ALTER TABLE `ingrediente_alergeno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `ingredientes_hipoalergenicos`
--

DROP TABLE IF EXISTS `ingredientes_hipoalergenicos`;
/*!50001 DROP VIEW IF EXISTS `ingredientes_hipoalergenicos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `ingredientes_hipoalergenicos` AS SELECT 
 1 AS `id_ingrediente`,
 1 AS `nombre_ingrediente`,
 1 AS `sostenibilidad_producto`,
 1 AS `cecliaco`,
 1 AS `caducidad`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `receta`
--

DROP TABLE IF EXISTS `receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta` (
  `id_receta` int NOT NULL AUTO_INCREMENT,
  `id_cli` int NOT NULL,
  `nombre_receta` varchar(50) DEFAULT NULL,
  `valor_nutricional` int DEFAULT NULL,
  `num_ingredientes` int DEFAULT NULL,
  `nutriscore` char(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id_receta`),
  KEY `id_cli` (`id_cli`),
  CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`id_cli`) REFERENCES `cliente` (`id_cli`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta`
--

LOCK TABLES `receta` WRITE;
/*!40000 ALTER TABLE `receta` DISABLE KEYS */;
/*!40000 ALTER TABLE `receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta_ingrediente`
--

DROP TABLE IF EXISTS `receta_ingrediente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta_ingrediente` (
  `id_receta` int NOT NULL,
  `id_ingrediente` int DEFAULT NULL,
  PRIMARY KEY (`id_receta`),
  KEY `id_ingrediente` (`id_ingrediente`),
  CONSTRAINT `receta_ingrediente_ibfk_1` FOREIGN KEY (`id_receta`) REFERENCES `receta` (`id_receta`) ON DELETE CASCADE,
  CONSTRAINT `receta_ingrediente_ibfk_2` FOREIGN KEY (`id_ingrediente`) REFERENCES `ingrediente` (`id_ingrediente`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_ingrediente`
--

LOCK TABLES `receta_ingrediente` WRITE;
/*!40000 ALTER TABLE `receta_ingrediente` DISABLE KEYS */;
/*!40000 ALTER TABLE `receta_ingrediente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `recetas_celiacos`
--

DROP TABLE IF EXISTS `recetas_celiacos`;
/*!50001 DROP VIEW IF EXISTS `recetas_celiacos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `recetas_celiacos` AS SELECT 
 1 AS `id_receta`,
 1 AS `id_cli`,
 1 AS `nombre_receta`,
 1 AS `valor_nutricional`,
 1 AS `nutriscore`,
 1 AS `fecha_creacion`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usu` int NOT NULL AUTO_INCREMENT,
  `nombre_usu` varchar(50) DEFAULT NULL,
  `apellido1_usu` varchar(50) DEFAULT NULL,
  `apellido2_usu` varchar(50) DEFAULT NULL,
  `mail_usu` varchar(255) DEFAULT NULL,
  `telefono` int DEFAULT NULL,
  `localidad` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_usu`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (200,'xabi',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `ingredientes_hipoalergenicos`
--

/*!50001 DROP VIEW IF EXISTS `ingredientes_hipoalergenicos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `ingredientes_hipoalergenicos` AS select `i`.`id_ingrediente` AS `id_ingrediente`,`i`.`nombre_ingrediente` AS `nombre_ingrediente`,`i`.`sostenibilidad_producto` AS `sostenibilidad_producto`,`i`.`cecliaco` AS `cecliaco`,`i`.`caducidad` AS `caducidad` from `ingrediente` `i` where `i`.`id_ingrediente` in (select `ia`.`id_ingrediente` from `ingrediente_alergeno` `ia`) is false */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `recetas_celiacos`
--

/*!50001 DROP VIEW IF EXISTS `recetas_celiacos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `recetas_celiacos` AS select `r`.`id_receta` AS `id_receta`,`r`.`id_cli` AS `id_cli`,`r`.`nombre_receta` AS `nombre_receta`,`r`.`valor_nutricional` AS `valor_nutricional`,`r`.`nutriscore` AS `nutriscore`,`r`.`fecha_creacion` AS `fecha_creacion` from `receta` `r` where `r`.`id_receta` in (select `ri`.`id_receta` from (`receta_ingrediente` `ri` join `ingrediente` `i` on((`ri`.`id_ingrediente` = `i`.`id_ingrediente`))) where (`i`.`cecliaco` = true)) is false */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-06 14:36:16
