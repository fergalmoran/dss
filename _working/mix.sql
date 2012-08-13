-- MySQL dump 10.13  Distrib 5.5.24, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: deepsouthsounds
-- ------------------------------------------------------
-- Server version	5.5.24-0ubuntu0.12.04.1

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
  `user_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `www_mix_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_d7e10871` FOREIGN KEY (`user_id`) REFERENCES `www_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `www_mix`
--

LOCK TABLES `www_mix` WRITE;
/*!40000 ALTER TABLE `www_mix` DISABLE KEYS */;
INSERT INTO `www_mix` VALUES (1,'June 2010','Marbert Rocell - Beats Like Birds\r\nMoto Clara - Silently\r\nBroad Bean Band - OkiDoki (Fish Go Deep Mix)\r\nJay Shepheard - Umzug\r\nThe Juan MacLean - Happy House\r\nScope - Runnin\' The Game\r\nJayson Brothers - The Game\r\nSezer Uysal & Everen Ulosoy - Singing In The Bathtub\r\nLatour - Blue\r\nPol_On - Toga\r\nArmando - Don\'t Take It\r\nDaniel Paul - Outta Space\r\nFlight Facilities feat Giselle - Crave You\r\nPhonique feat Erlend Oye - Casualties (Morgan Geist remix)','2012-04-17 17:46:26','mix-images/fergalmoran/crazymix.jpg','mixes/June2010.mp3','mixes/June2010.mp3','mixes/June2010.mp3',1,1),(9,'Andre Lodemann \"Fragments\"','01. Latecomer - Cosmic Cart - Faces Records\r\n02. Andre Lodemann - Going To The Core feat. Nathalie Claude - BWR\r\n03. Prommer & Barck - Sleeping Beauty (Broken Reform Rmx) - Derwin\r\n04. Franck Roger - Hustling Peoples - Real Tone\r\n05. Acos Coolkas - Dont Fly Away (Jimpster Dub) - Audio Tonic\r\n06. Manuel Tur - About To Fall - Mild Pitch\r\n07. Kevin Saunderson feat. Inner City - Future (Kenny Larkin Tension Mix) AL Edit\r\n08. Paul Loraine - Envy (Funk DVoid Remix) - Bigger Deer\r\n09. Magic Mountain High - Schnitzel Box 1 - Untitled 1 - Workshop\r\n10. Ian Pooley - Indigo - Pokerflat\r\n11. Charles Webster feat. Thandi Draai - Fight For Freedom (Atjazz Astro Remix) - Miso','2012-05-06 23:03:51','mix-images/Deepsouthsounds/lodemann.jpg','mixes/Deepsouthsounds/Andre Lodemann - Fragments Podcast.mp3','NOTHING','NOTHING',1,1),(11,'Brawther \"back to basics\"','taken from back to basics podcast1','2012-05-13 19:45:57','mix-images/Deepsouthsounds/brawther.jpg','mixes/Deepsouthsounds/Brawther - BackToBasics Podcast 01.mp3','/','/',1,1),(12,'Robert Bruen \"chilled\"','1.tom midleton - optimysic\r\n2.digby jones - pina colada\r\n3.crazy p - you\'ve lost that loving feeling\r\n4.jakatta - one fine day\r\n5.st.germain - sure thing\r\n6.moby - porcelain\r\n7.max melvin - whatever\r\n8.bliss - dontlook back (fug mix)\r\n9.ulrich schnauss - passing by\r\n10.groove armada - fireside favorite\r\n11.bullitnuts - heavy air\r\n12.aim - just passin thru\r\n13.crazy p - play it cool\r\n','2012-05-14 22:09:30','mix-images/Deepsouthsounds/chillout mix 1 Album Art.jpg','mixes/Deepsouthsounds/chillout mix - Bruen.mp3','/','/',1,1),(16,'tigerskin','mp3','2012-05-24 18:00:22','','mixes/Deepsouthsounds/deep love tigerskin.mp3','/','/',1,1),(17,'Test','teste','2012-05-27 10:02:31','','mixes/Deepsouthsounds/house_lo.mp3','','',1,1);
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

-- Dump completed on 2012-08-13 19:14:50
