-- MySQL dump 10.13  Distrib 5.5.12, for Win64 (x86)
--
-- Host: localhost    Database: deepsouthsounds
-- ------------------------------------------------------
-- Server version	5.5.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `www_mix`
--

DROP TABLE IF EXISTS `www_mix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `www_mix` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `upload_date` datetime NOT NULL,
  `mix_image` varchar(100) NOT NULL,
  `local_file` varchar(100) NOT NULL,
  `download_url` varchar(255) NOT NULL,
  `stream_url` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `www_mix_403f60f` (`user_id`),
  CONSTRAINT `user_id_refs_id_281ef78f` FOREIGN KEY (`user_id`) REFERENCES `www_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `www_mix`
--

LOCK TABLES `www_mix` WRITE;
/*!40000 ALTER TABLE `www_mix` DISABLE KEYS */;
INSERT INTO `www_mix` VALUES (1,'Andre Lodemann \"Fragments\"','01. Latecomer - Cosmic Cart - Faces Records','2012-05-06 23:03:51','mix-images/Deepsouthsounds/lodemann.jpg','mixes/Deepsouthsounds/Andre Lodemann - Fragments Podcast.mp3','NOTHING','NOTHING',1,1),(2,'June 2010','Marbert Rocell - Beats Like Birds','2012-04-17 17:46:26','mix-images/fergalmoran/crazymix.jpg','mixes/June2010.mp3','NOTHING','NOTHING',1,1);
/*!40000 ALTER TABLE `www_mix` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-07-26 15:44:39
