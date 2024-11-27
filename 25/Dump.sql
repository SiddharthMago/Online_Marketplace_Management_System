-- MySQL dump 10.13  Distrib 8.0.40, for macos15.0 (arm64)
--
-- Host: localhost    Database: online_marketplace_management
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
-- Table structure for table `Category`
--

DROP TABLE IF EXISTS `Category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Category` (
  `category_id` varchar(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `parent_category_id` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  KEY `parent_category_id` (`parent_category_id`),
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`parent_category_id`) REFERENCES `Category` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Category`
--

LOCK TABLES `Category` WRITE;
/*!40000 ALTER TABLE `Category` DISABLE KEYS */;
INSERT INTO `Category` VALUES ('C0001','Electronics',NULL),('C0002','Mobile Phones','C0001'),('C0003','Laptops','C0001'),('C0004','Home Appliances',NULL),('C0005','Kitchen Appliances','C0004');
/*!40000 ALTER TABLE `Category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customer` (
  `customer_id` varchar(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `street` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip` varchar(10) DEFAULT NULL,
  `join_date` date NOT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES ('CUST001','Siddharth Mago','john.doe@example.com','108 New York','New York','NY','10001','2023-01-01'),('CUST002','Jane Smith','jane.smith@example.com','202 Second St','San Francisco','CA','94101','2023-02-15'),('CUST003','Sam Wilson','sam.wilson@example.com','303 Third St','Chicago','IL','60601','2023-03-20'),('CUST004','Lucy Brown','lucy.brown@example.com','404 Fourth St','Austin','TX','73301','2023-04-10'),('CUST005','Mike Green','mike.green@example.com','505 Fifth St','Seattle','WA','98101','2023-05-05');
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Discount_Code`
--

DROP TABLE IF EXISTS `Discount_Code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Discount_Code` (
  `promotion_id` varchar(10) NOT NULL,
  `code` varchar(20) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `value` float DEFAULT NULL,
  `expiry` date NOT NULL,
  PRIMARY KEY (`promotion_id`,`code`),
  CONSTRAINT `discount_code_ibfk_1` FOREIGN KEY (`promotion_id`) REFERENCES `Promotion` (`promotion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Discount_Code`
--

LOCK TABLES `Discount_Code` WRITE;
/*!40000 ALTER TABLE `Discount_Code` DISABLE KEYS */;
INSERT INTO `Discount_Code` VALUES ('PRM001','SEASON20','Flat Discount',20,'2023-06-30'),('PRM002','NEWYEAR25','Flat Discount',25,'2023-12-31'),('PRM003','CLEAR30','Flat Discount',30,'2023-07-15'),('PRM004','FESTIVE15','Percentage Discount',15,'2023-10-15'),('PRM005','BLACKFRIDAY50','Percentage Discount',50,'2023-11-24');
/*!40000 ALTER TABLE `Discount_Code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order_Item`
--

DROP TABLE IF EXISTS `Order_Item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Order_Item` (
  `order_id` int NOT NULL,
  `transaction_id` varchar(20) NOT NULL,
  `item_number` int NOT NULL,
  `product_id` varchar(10) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `unit_price` float DEFAULT NULL,
  PRIMARY KEY (`order_id`,`item_number`,`transaction_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `Orders` (`order_id`),
  CONSTRAINT `order_item_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`) ON DELETE CASCADE,
  CONSTRAINT `order_item_chk_1` CHECK ((`quantity` > 0)),
  CONSTRAINT `order_item_chk_2` CHECK ((`unit_price` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order_Item`
--

LOCK TABLES `Order_Item` WRITE;
/*!40000 ALTER TABLE `Order_Item` DISABLE KEYS */;
INSERT INTO `Order_Item` VALUES (1,'T0001',1,'P0001',1,999.99),(2,'T0002',1,'P0003',1,849.99),(3,'T0003',1,'P0004',1,499.99),(4,'T0004',1,'P0005',1,129.99),(5,'T0005',1,'P0002',1,1999.99);
/*!40000 ALTER TABLE `Order_Item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `transaction_id` varchar(20) NOT NULL,
  `ordered_by` varchar(10) NOT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `order_date` date NOT NULL,
  `order_status` enum('DELIVERED','PENDING','OUT FOR DELIVERY') NOT NULL,
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `transaction_id` (`transaction_id`),
  KEY `ordered_by` (`ordered_by`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`ordered_by`) REFERENCES `Customer` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` VALUES (1,'T0001','CUST001',4.5,'2023-06-15','DELIVERED'),(2,'T0002','CUST002',3.8,'2023-07-10','PENDING'),(3,'T0003','CUST003',5.0,'2023-07-20','OUT FOR DELIVERY'),(4,'T0004','CUST004',4.0,'2023-08-01','DELIVERED'),(5,'T0005','CUST005',NULL,'2023-08-15','PENDING');
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Premium_Seller`
--

DROP TABLE IF EXISTS `Premium_Seller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Premium_Seller` (
  `seller_id` varchar(10) NOT NULL,
  `premium_since` date NOT NULL,
  `tier` varchar(10) DEFAULT NULL,
  `commission_rate` decimal(3,2) DEFAULT NULL,
  PRIMARY KEY (`seller_id`),
  CONSTRAINT `premium_seller_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `Seller` (`seller_id`),
  CONSTRAINT `premium_seller_chk_1` CHECK ((`tier` in (_utf8mb4'SILVER',_utf8mb4'GOLD',_utf8mb4'PLATINUM'))),
  CONSTRAINT `premium_seller_chk_2` CHECK ((`commission_rate` between 0.01 and 0.10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Premium_Seller`
--

LOCK TABLES `Premium_Seller` WRITE;
/*!40000 ALTER TABLE `Premium_Seller` DISABLE KEYS */;
INSERT INTO `Premium_Seller` VALUES ('S0001','2023-06-01','PLATINUM',0.07),('S0002','2024-08-08','PLATINUM',0.03),('S0003','2023-07-07','SILVER',0.03),('S0004','2023-07-01','PLATINUM',0.03);
/*!40000 ALTER TABLE `Premium_Seller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product` (
  `product_id` varchar(10) NOT NULL,
  `SKU` varchar(50) NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` float DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `seller_id` varchar(10) NOT NULL,
  `category_id` varchar(10) NOT NULL,
  PRIMARY KEY (`product_id`,`SKU`),
  UNIQUE KEY `SKU_2` (`SKU`),
  KEY `seller_id` (`seller_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `Seller` (`seller_id`),
  CONSTRAINT `product_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `Category` (`category_id`),
  CONSTRAINT `product_chk_1` CHECK ((`price` > 0)),
  CONSTRAINT `product_chk_2` CHECK ((`stock` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product`
--

LOCK TABLES `Product` WRITE;
/*!40000 ALTER TABLE `Product` DISABLE KEYS */;
INSERT INTO `Product` VALUES ('P0001','SKU001','iPhone 14',999.99,14,'S0001','C0002'),('P0002','SKU002','Macbook Pro',2499.99,3,'S0001','C0003'),('P0003','SKU003','Samsung Galaxy S23',849.99,15,'S0002','C0002'),('P0004','SKU004','Dyson Vacuum',499.99,8,'S0003','C0004'),('P0005','SKU005','Air Fryer',129.99,20,'S0004','C0005'),('P0006','SKU006','Water Bottle',24.99,12,'S0002','C0005');
/*!40000 ALTER TABLE `Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product_Images`
--

DROP TABLE IF EXISTS `Product_Images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product_Images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `product_id` varchar(10) DEFAULT NULL,
  `image` longblob NOT NULL,
  PRIMARY KEY (`image_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product_Images`
--

LOCK TABLES `Product_Images` WRITE;
/*!40000 ALTER TABLE `Product_Images` DISABLE KEYS */;
INSERT INTO `Product_Images` VALUES (1,'P0001',_binary 'awfaLongfaefeaftextfaefeaaforfaefafImageh5eg1'),(2,'P0002',_binary 'longfeafatextaefaeforfaeeahyimagejnbst2');
/*!40000 ALTER TABLE `Product_Images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product_Review`
--

DROP TABLE IF EXISTS `Product_Review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product_Review` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` varchar(10) NOT NULL,
  `product_id` varchar(10) NOT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `comment` text,
  `review_date` date NOT NULL,
  PRIMARY KEY (`review_id`),
  UNIQUE KEY `customer_id` (`customer_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_review_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`),
  CONSTRAINT `product_review_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`),
  CONSTRAINT `product_review_chk_1` CHECK ((`rating` between 0.0 and 5.0))
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product_Review`
--

LOCK TABLES `Product_Review` WRITE;
/*!40000 ALTER TABLE `Product_Review` DISABLE KEYS */;
INSERT INTO `Product_Review` VALUES (1,'CUST001','P0001',4.5,'Great phone!','2023-06-16'),(2,'CUST002','P0003',4.0,'Good value for the price.','2023-07-11'),(3,'CUST003','P0004',5.0,'Excellent vacuum cleaner!','2023-07-21'),(4,'CUST004','P0005',4.0,'Works as advertised.','2023-08-02'),(5,'CUST005','P0002',4.5,'Powerful laptop!','2023-08-16'),(16,'CUST001','P0002',4.0,'Solid performance, a bit pricey.','2023-06-17'),(17,'CUST002','P0001',4.5,'Excellent design and features.','2023-07-12'),(18,'CUST003','P0003',3.5,'Average experience, could be better.','2023-07-22'),(19,'CUST004','P0004',4.8,'Very reliable and easy to use.','2023-08-03'),(20,'CUST005','P0005',5.0,'Highly recommended for everyone.','2023-08-17'),(21,'CUST001','P0003',3.9,'Good but not exceptional.','2023-08-01'),(22,'CUST002','P0004',4.2,'Works as expected.','2023-08-02'),(23,'CUST003','P0005',5.0,'Absolutely worth the price.','2023-08-05'),(24,'CUST004','P0001',4.7,'Another great product.','2023-08-08');
/*!40000 ALTER TABLE `Product_Review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Promotion`
--

DROP TABLE IF EXISTS `Promotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Promotion` (
  `promotion_id` varchar(10) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `discount_amount` int DEFAULT NULL,
  `provided_by` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`promotion_id`),
  KEY `provided_by` (`provided_by`),
  CONSTRAINT `promotion_ibfk_1` FOREIGN KEY (`provided_by`) REFERENCES `Seller` (`seller_id`),
  CONSTRAINT `promotion_chk_1` CHECK ((`discount_amount` between 0 and 100))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Promotion`
--

LOCK TABLES `Promotion` WRITE;
/*!40000 ALTER TABLE `Promotion` DISABLE KEYS */;
INSERT INTO `Promotion` VALUES ('PRM001','Seasonal Sale','2023-06-01','2023-06-30',0,'S0001'),('PRM002','New Year Sale','2023-12-01','2023-12-31',0,'S0002'),('PRM003','Clearance Sale','2023-07-01','2023-07-15',0,'S0003'),('PRM004','Festive Offer','2023-10-01','2023-10-15',0,'S0004'),('PRM005','Black Friday','2023-11-24','2023-11-24',1,'S0005');
/*!40000 ALTER TABLE `Promotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Seller`
--

DROP TABLE IF EXISTS `Seller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Seller` (
  `seller_id` varchar(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `street` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip` varchar(10) DEFAULT NULL,
  `join_date` date NOT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `referred_by` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`seller_id`),
  KEY `referred_by` (`referred_by`),
  CONSTRAINT `seller_ibfk_1` FOREIGN KEY (`referred_by`) REFERENCES `Seller` (`seller_id`),
  CONSTRAINT `seller_chk_1` CHECK ((`rating` between 0.0 and 5.0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Seller`
--

LOCK TABLES `Seller` WRITE;
/*!40000 ALTER TABLE `Seller` DISABLE KEYS */;
INSERT INTO `Seller` VALUES ('S0001','Alice','123 Main St','New York','NY','10001','2023-01-15',4.5,NULL),('S0002','Bob','456 Elm St','Los Angeles','CA','90001','2023-02-10',3.8,'S0001'),('S0003','Charlie','789 Maple Ave','Chicago','IL','60601','2023-03-12',4.2,'S0001'),('S0004','Diana','321 Oak St','Houston','TX','77001','2023-04-05',4.9,NULL),('S0005','Eva','653 Pine Rd','Phoenix','AZ','85003','2023-05-20',4.6,NULL);
/*!40000 ALTER TABLE `Seller` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-27  7:14:23
