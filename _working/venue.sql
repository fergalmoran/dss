LOCK TABLES `spa_venue` WRITE;
DELETE FROM `spa_venue`;
/*!40000 ALTER TABLE `spa_venue` DISABLE KEYS */;
INSERT INTO `spa_venue` VALUES (1,1,'The Pavillion','Carey\'s Lane','venue-images/5344256c-e2fc-11e1-a282-00163e1b2ddf/Pavilion_Upstairs_1-894x600.jpg');
/*!40000 ALTER TABLE `spa_venue` ENABLE KEYS */;
UNLOCK TABLES;
