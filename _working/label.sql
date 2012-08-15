LOCK TABLES `spa_label` WRITE;
/*!40000 ALTER TABLE `spa_label` DISABLE KEYS */;
DELETE FROM `spa_label`;
INSERT INTO `spa_label` VALUES (1,'Test Label 1'),(2,'BEEF Recordings'),(3,'Rauschzeit'),(4,'Lost My Dog');
/*!40000 ALTER TABLE `spa_label` ENABLE KEYS */;
UNLOCK TABLES;
