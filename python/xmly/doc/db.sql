--  订单表
CREATE TABLE `tb_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `status` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `resource_type,,,ll;/j tyu/.` int(11) NOT NULL,
  `parent_id` bigint(20) DEFAULT NULL,
  `timestamp` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FKovripa3rfs5f9qu2pvyhgo6xi` (`parent_id`),
  CONSTRAINT `FKovripa3rfs5f9qu2pvyhgo6xi` FOREIGN KEY (`parent_id`) REFERENCES `module` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;