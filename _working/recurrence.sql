LOCK TABLES `spa_recurrence` WRITE;
DELETE FROM `spa_recurrence`;
/*!40000 ALTER TABLE `spa_recurrence` DISABLE KEYS */;
INSERT INTO `spa_recurrence` VALUES (1),(2),(3);
/*!40000 ALTER TABLE `spa_recurrence` ENABLE KEYS */;
UNLOCK TABLES;