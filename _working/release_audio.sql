LOCK TABLES `spa_releaseaudio` WRITE;
/*!40000 ALTER TABLE `spa_releaseaudio` DISABLE KEYS */;
DELETE FROM `spa_releaseaudio`;
INSERT INTO `spa_releaseaudio` VALUES (1,'release-audio/52d0c44f-db22-11e1-a030-0011b10a15ae/Late Nite Tuff Guy - One Night In the Disco.mp3',1,'Test release from someone or something..');
/*!40000 ALTER TABLE `spa_releaseaudio` ENABLE KEYS */;
UNLOCK TABLES;
