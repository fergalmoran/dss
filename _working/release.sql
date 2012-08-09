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
-- Table structure for table `www_release`
--

DROP TABLE IF EXISTS `www_release`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `www_release` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `release_artist` varchar(100) NOT NULL,
  `release_title` varchar(100) NOT NULL,
  `release_description` longtext NOT NULL,
  `release_image` varchar(100) NOT NULL,
  `release_label_id` int(11) NOT NULL,
  `release_date` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `www_release_1a9c1def` (`release_label_id`),
  KEY `www_release_403f60f` (`user_id`),
  CONSTRAINT `release_label_id_refs_id_318351e2` FOREIGN KEY (`release_label_id`) REFERENCES `www_label` (`id`),
  CONSTRAINT `user_id_refs_id_606833aa` FOREIGN KEY (`user_id`) REFERENCES `www_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `www_release`
--

LOCK TABLES `www_release` WRITE;
/*!40000 ALTER TABLE `www_release` DISABLE KEYS */;
INSERT INTO `www_release` VALUES (1,'Test Release Artist 1','Test Release Artist 1','Test Release Artist 1','',1,'2012-07-30',1,1);
/*!40000 ALTER TABLE `www_release` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-07-31 16:32:30
