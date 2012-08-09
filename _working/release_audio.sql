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
-- Table structure for table `www_releaseaudio`
--

DROP TABLE IF EXISTS `www_releaseaudio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `www_releaseaudio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `local_file` varchar(100) NOT NULL,
  `release_id` int(11) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `www_releaseaudio_47d82a6c` (`release_id`),
  CONSTRAINT `release_id_refs_id_25bc9f64` FOREIGN KEY (`release_id`) REFERENCES `www_release` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `www_releaseaudio`
--

LOCK TABLES `www_releaseaudio` WRITE;
/*!40000 ALTER TABLE `www_releaseaudio` DISABLE KEYS */;
INSERT INTO `www_releaseaudio` VALUES (1,'release-audio/52d0c44f-db22-11e1-a030-0011b10a15ae/Late Nite Tuff Guy - One Night In the Disco.mp3',1,'Test release from someone or something..');
/*!40000 ALTER TABLE `www_releaseaudio` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-07-31 16:32:37
