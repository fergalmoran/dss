LOCK TABLES `socialaccount_socialapp` WRITE;
DELETE FROM `socialaccount_socialapp`;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
INSERT INTO `socialaccount_socialapp` VALUES (1,1,'facebook','Facebook','154504534677009','8eb42253ef42e3133ee76348255c2d78'),(2,1,'twitter','Twitter','qmvJ6tptgd8G9T9WYp6P3Q','ts6bYmZdnYxj7EscOvfz7YTwHu7r8OVGTkZWKhYqex8');
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;
