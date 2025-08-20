-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: open_point
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bundle_items`
--

DROP TABLE IF EXISTS `bundle_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bundle_items` (
  `bundle_item_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `item_id` int NOT NULL,
  `quantity` int DEFAULT '1',
  `price` int NOT NULL,
  PRIMARY KEY (`bundle_item_id`),
  KEY `product_id` (`product_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `bundle_items_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE,
  CONSTRAINT `bundle_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bundle_items`
--

LOCK TABLES `bundle_items` WRITE;
/*!40000 ALTER TABLE `bundle_items` DISABLE KEYS */;
INSERT INTO `bundle_items` VALUES (1,27,3,10,1300),(2,28,5,2,350),(3,28,54,2,350);
/*!40000 ALTER TABLE `bundle_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cup_storage`
--

DROP TABLE IF EXISTS `cup_storage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cup_storage` (
  `cup_storage_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `item_id` int NOT NULL,
  `remaining_cups` int NOT NULL,
  PRIMARY KEY (`cup_storage_id`),
  UNIQUE KEY `item_id` (`item_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `cup_storage_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `cup_storage_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cup_storage`
--

LOCK TABLES `cup_storage` WRITE;
/*!40000 ALTER TABLE `cup_storage` DISABLE KEYS */;
INSERT INTO `cup_storage` VALUES (11,3,8,2),(12,3,9,1);
/*!40000 ALTER TABLE `cup_storage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `ch_name` varchar(255) NOT NULL,
  `size` enum('small','medium','large','extraLarge','noSize') DEFAULT NULL,
  `price` int NOT NULL,
  PRIMARY KEY (`item_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,1,'那堤','medium',120),(2,1,'那堤','large',135),(3,1,'那堤','extraLarge',150),(4,2,'美式咖啡','medium',110),(5,2,'美式咖啡','large',125),(6,2,'美式咖啡','extraLarge',140),(7,3,'焦糖瑪奇朵','medium',130),(8,3,'焦糖瑪奇朵','large',145),(9,3,'焦糖瑪奇朵','extraLarge',160),(10,4,'濃縮咖啡','small',90),(11,5,'卡布奇諾','medium',125),(12,5,'卡布奇諾','large',140),(13,5,'卡布奇諾','extraLarge',155),(14,6,'摩卡','medium',135),(15,6,'摩卡','large',150),(16,6,'摩卡','extraLarge',165),(17,7,'可可瑪奇朵','medium',140),(18,7,'可可瑪奇朵','large',155),(19,7,'可可瑪奇朵','extraLarge',170),(20,8,'經典紅茶那堤','medium',125),(21,8,'經典紅茶那堤','large',140),(22,8,'經典紅茶那堤','extraLarge',155),(23,9,'醇濃抹茶那堤','medium',130),(24,9,'醇濃抹茶那堤','large',145),(25,9,'醇濃抹茶那堤','extraLarge',160),(26,10,'伯爵茶那堤','medium',135),(27,10,'伯爵茶那堤','large',150),(28,10,'伯爵茶那堤','extraLarge',165),(29,11,'玫瑰蜜香茶那堤','medium',140),(30,11,'玫瑰蜜香茶那堤','large',155),(31,11,'玫瑰蜜香茶那堤','extraLarge',170),(32,12,'冰經典紅茶那堤','medium',120),(33,12,'冰經典紅茶那堤','large',135),(34,12,'冰經典紅茶那堤','extraLarge',150),(35,13,'英式早餐紅茶','medium',110),(36,13,'英式早餐紅茶','large',125),(37,13,'英式早餐紅茶','extraLarge',140),(38,14,'蜜柚紅茶','medium',120),(39,14,'蜜柚紅茶','large',135),(40,14,'蜜柚紅茶','extraLarge',150),(41,15,'阿里山烏龍茶','medium',130),(42,15,'阿里山烏龍茶','large',145),(43,15,'阿里山烏龍茶','extraLarge',160),(44,16,'冰搖檸檬紅茶','medium',125),(45,16,'冰搖檸檬紅茶','large',140),(46,16,'冰搖檸檬紅茶','extraLarge',155),(47,17,'菇菇濃湯法烤麵包','noSize',65),(48,18,'草莓起司麵包','noSize',70),(49,19,'巧克力雙色吐司','noSize',75),(50,20,'明太子起司貝果','noSize',80),(51,21,'培根起司軟歐麵包','noSize',85),(52,22,'藍莓果粒貝果','noSize',70),(53,23,'肉桂捲','noSize',60),(54,24,'蜂蜜牛奶麵包','noSize',65),(55,25,'軟法麵包','noSize',50),(56,26,'雙起司軟歐麵包','noSize',75);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `ch_name` varchar(255) NOT NULL,
  `type` enum('coffee','latte','tea','food','bundle') NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Caffe Latte','那堤','coffee','2025-01-01 17:28:46','2025-01-01 17:28:46'),(2,'Caffe Americano','美式咖啡','coffee','2025-01-01 17:28:46','2025-01-01 17:28:46'),(3,'Caramel Macchiato','焦糖瑪奇朵','coffee','2025-01-01 17:28:46','2025-01-01 17:28:46'),(4,'Espresso','濃縮咖啡','coffee','2025-01-01 17:28:46','2025-01-01 17:28:46'),(5,'Cappuccino','卡布奇諾','coffee','2025-01-01 17:28:46','2025-01-01 17:28:46'),(6,'Caffe Mocha','摩卡','coffee','2025-01-01 17:28:46','2025-01-01 17:28:46'),(7,'Cocoa Macchiato','可可瑪奇朵','coffee','2025-01-01 17:28:46','2025-01-01 17:28:46'),(8,'Black Tea Latte','經典紅茶那堤','latte','2025-01-01 17:28:46','2025-01-01 17:28:46'),(9,'Pure Matcha Latte','醇濃抹茶那堤','latte','2025-01-01 17:28:46','2025-01-01 17:28:46'),(10,'Earl Grey Tea Latte','伯爵茶那堤','latte','2025-01-01 17:28:46','2025-01-01 17:28:46'),(11,'Rose Fancy Tea Latte','玫瑰蜜香茶那堤','latte','2025-01-01 17:28:46','2025-01-01 17:28:46'),(12,'Iced Black Tea Latte','冰經典紅茶那堤','latte','2025-01-01 17:28:46','2025-01-01 17:28:46'),(13,'English Breakfast Tea','英式早餐紅茶','tea','2025-01-01 17:28:46','2025-01-01 17:28:46'),(14,'Black Tea with Ruby Grapefruit and Honey','蜜柚紅茶','tea','2025-01-01 17:28:46','2025-01-01 17:28:46'),(15,'Alishan Oolong Tea','阿里山烏龍茶','tea','2025-01-01 17:28:46','2025-01-01 17:28:46'),(16,'Iced Shaken Lemon Black Tea','冰搖檸檬紅茶','tea','2025-01-01 17:28:46','2025-01-01 17:28:46'),(17,'Mushroom Soup Flavored Bread','菇菇濃湯法烤麵包','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(18,'Strawberry Cheese Bread','草莓起司麵包','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(19,'Chocolate Toast','巧克力雙色吐司','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(20,'Mentaiko Cheese Bagel','明太子起司貝果','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(21,'Bacon & Cheese Bread','培根起司軟歐麵包','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(22,'Blueberry Bagel','藍莓果粒貝果','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(23,'Cinnamon Roll','肉桂捲','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(24,'Honey & Milk Bread','蜂蜜牛奶麵包','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(25,'Cheesy Bread','軟法麵包','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(26,'Double Cheese Bread','雙起司軟歐麵包','food','2025-01-01 17:28:46','2025-01-01 17:28:46'),(27,'Latte Lover Bundle','拿鐵愛好者套卷','bundle','2025-01-01 17:28:47','2025-01-01 17:28:47'),(28,'Morning Essentials Bundle','早晨必備套卷','bundle','2025-01-01 17:28:47','2025-01-01 17:28:47');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_detail`
--

DROP TABLE IF EXISTS `transaction_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_detail` (
  `transaction_detail_id` int NOT NULL AUTO_INCREMENT,
  `transaction_id` int NOT NULL,
  `product_id` int NOT NULL,
  `item_id` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`transaction_detail_id`),
  KEY `transaction_id` (`transaction_id`),
  KEY `product_id` (`product_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `transaction_detail_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`transaction_id`) ON DELETE CASCADE,
  CONSTRAINT `transaction_detail_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE,
  CONSTRAINT `transaction_detail_ibfk_3` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_detail`
--

LOCK TABLES `transaction_detail` WRITE;
/*!40000 ALTER TABLE `transaction_detail` DISABLE KEYS */;
INSERT INTO `transaction_detail` VALUES (10,9,1,3,1),(11,10,1,3,1),(12,11,1,3,1),(13,12,3,8,4),(14,13,3,8,1),(15,14,3,9,1),(16,15,3,8,1);
/*!40000 ALTER TABLE `transaction_detail` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = big5 */ ;
/*!50003 SET character_set_results = big5 */ ;
/*!50003 SET collation_connection  = big5_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_cup_storage_after_add` AFTER INSERT ON `transaction_detail` FOR EACH ROW BEGIN
DECLARE total_quantity INT DEFAULT 0;

IF (select type from transactions where transaction_id=NEW.transaction_id) = 'add' THEN
IF (select type from products where product_id=NEW.product_id ) = 'bundle' THEN
INSERT INTO cup_storage (user_id, item_id, remaining_cups)
SELECT (select user_id from transactions where transaction_id=NEW.transaction_id), item_id, quantity
FROM bundle_items
WHERE product_id = NEW.product_id
ON DUPLICATE KEY UPDATE remaining_cups = COALESCE(remaining_cups, 0) + VALUES(remaining_cups);
ELSE

SET total_quantity = NEW.quantity;
INSERT INTO cup_storage (user_id, item_id, remaining_cups)
VALUES ((select user_id from transactions where transaction_id=NEW.transaction_id), NEW.item_id, total_quantity)
ON DUPLICATE KEY UPDATE remaining_cups = remaining_cups + total_quantity;
END IF;
END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = big5 */ ;
/*!50003 SET character_set_results = big5 */ ;
/*!50003 SET collation_connection  = big5_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_cup_storage_after_reduce` AFTER INSERT ON `transaction_detail` FOR EACH ROW BEGIN
    DECLARE id INT;

    
    SELECT user_id INTO id FROM transactions WHERE transaction_id = NEW.transaction_id;
    
    IF (SELECT type FROM transactions WHERE transaction_id = NEW.transaction_id) = 'reduce' THEN
        
        IF (SELECT remaining_cups FROM cup_storage WHERE user_id = id AND item_id = NEW.item_id) < NEW.quantity THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Remaining cups cannot be negative.';
        ELSE
            
            UPDATE cup_storage SET remaining_cups = remaining_cups - NEW.quantity WHERE user_id = id AND item_id = NEW.item_id;
            
            IF (SELECT remaining_cups FROM cup_storage WHERE user_id = id AND item_id = NEW.item_id) <= 0 THEN
                DELETE FROM cup_storage WHERE user_id = id AND item_id = NEW.item_id;
            END IF;
        END IF;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `type` enum('add','reduce') NOT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (9,3,'add','2025-01-02 02:04:31'),(10,3,'reduce','2025-01-02 02:04:52'),(11,3,'reduce','2025-01-02 02:04:58'),(12,3,'add','2025-01-02 02:05:22'),(13,3,'reduce','2025-01-02 02:05:30'),(14,3,'add','2025-01-02 04:58:57'),(15,3,'reduce','2025-01-02 04:59:02');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(60) NOT NULL,
  `gender` enum('male','female') DEFAULT NULL,
  `number` varchar(10) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'11124138@nhu.edu.tw','$2b$12$pCuDkL6Y70VR58bRzMr7SuQSu95M1MeWh6jk1z2jYkJ1N.mfHGPA.','male','11124138','2025-01-01 17:38:05','2025-01-01 17:38:05'),(4,'11124134@nhu.edu.tw','$2b$12$EV3ymt/6EqGpsVXPZ33P0OC4KHWpXppqwzGGU6AchhrvsOxXuR6n.','male','1','2025-01-02 05:27:20','2025-01-02 05:27:20');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-20 16:28:50
