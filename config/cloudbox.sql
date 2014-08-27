CREATE DATABASE IF NOT EXISTS `cloudbox` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `cloudbox`;


-- Dumping structure for table cloudbox.cb_bans
CREATE TABLE IF NOT EXISTS `cb_bans` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `userID` bigint(20) unsigned NOT NULL,
  `bannerUserID` bigint(20) unsigned NOT NULL,
  `type` smallint(6) NOT NULL,
  `recordID` bigint(20) unsigned NOT NULL COMMENT 'The type of the record is determined by the type.',
  `startTime` int(10) unsigned NOT NULL,
  `endTime` int(10) unsigned NOT NULL,
  `reason` varchar(500) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_bans: ~0 rows (approximately)
/*!40000 ALTER TABLE `cb_bans` DISABLE KEYS */;
/*!40000 ALTER TABLE `cb_bans` ENABLE KEYS */;


-- Dumping structure for table cloudbox.cb_global_metadata
CREATE TABLE IF NOT EXISTS `cb_global_metadata` (
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `value` text COLLATE utf8_unicode_ci NOT NULL,
  `defaultValue` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_global_metadata: ~1 rows (approximately)
/*!40000 ALTER TABLE `cb_global_metadata` DISABLE KEYS */;
INSERT INTO `cb_global_metadata` (`name`, `value`, `defaultValue`) VALUES
	('databaseVersion', '1000011', '1000011');
/*!40000 ALTER TABLE `cb_global_metadata` ENABLE KEYS */;


-- Dumping structure for table cloudbox.cb_users
CREATE TABLE IF NOT EXISTS `cb_users` (
  `id` binary(16) NOT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `firstseen` int(11) NOT NULL,
  `lastseen` int(11) NOT NULL,
  `primaryUserGroup` int(11) NOT NULL DEFAULT '1',
  `secondaryUserGroups` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `password` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_users: ~0 rows (approximately)
/*!40000 ALTER TABLE `cb_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `cb_users` ENABLE KEYS */;


-- Dumping structure for table cloudbox.cb_user_groups
CREATE TABLE IF NOT EXISTS `cb_user_groups` (
  `id` binary(16) NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `displayStylePriority` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `userGroupID` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_user_groups: ~0 rows (approximately)
/*!40000 ALTER TABLE `cb_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `cb_user_groups` ENABLE KEYS */;


-- Dumping structure for table cloudbox.cb_user_group_user_assoc
CREATE TABLE IF NOT EXISTS `cb_user_group_user_assoc` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userID` binary(16) NOT NULL,
  `groupID` varbinary(16) NOT NULL,
  UNIQUE KEY `id` (`id`),
  KEY `userID` (`userID`,`groupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_user_group_user_assoc: ~0 rows (approximately)
/*!40000 ALTER TABLE `cb_user_group_user_assoc` DISABLE KEYS */;
/*!40000 ALTER TABLE `cb_user_group_user_assoc` ENABLE KEYS */;


-- Dumping structure for table cloudbox.cb_user_ip
CREATE TABLE IF NOT EXISTS `cb_user_ip` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userID` binary(16) NOT NULL,
  `logDate` int(10) unsigned NOT NULL,
  `ip` varbinary(16) NOT NULL,
  `action` smallint(5) unsigned NOT NULL,
  `subActionType` int(10) unsigned NOT NULL,
  `subActionID` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `logDate` (`logDate`),
  KEY `ip_logDate` (`ip`,`logDate`),
  KEY `actions` (`action`,`subActionType`,`subActionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_user_ip: ~0 rows (approximately)
/*!40000 ALTER TABLE `cb_user_ip` DISABLE KEYS */;
/*!40000 ALTER TABLE `cb_user_ip` ENABLE KEYS */;


-- Dumping structure for table cloudbox.cb_user_service_assoc
CREATE TABLE IF NOT EXISTS `cb_user_service_assoc` (
  `userID` bigint(20) NOT NULL,
  `service` tinyint(4) NOT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT '0',
  UNIQUE KEY `userID_service` (`userID`,`service`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_user_service_assoc: ~0 rows (approximately)
/*!40000 ALTER TABLE `cb_user_service_assoc` DISABLE KEYS */;
/*!40000 ALTER TABLE `cb_user_service_assoc` ENABLE KEYS */;


-- Dumping structure for table cloudbox.cb_worlds
CREATE TABLE IF NOT EXISTS `cb_worlds` (
  `id` binary(16) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `worldServerID` int(11) NOT NULL,
  `path` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
  `format` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
  `isDefault` tinyint(1) NOT NULL,
  `preloadAtServerStart` tinyint(1) NOT NULL,
  `lastAccessed` int(10) unsigned NOT NULL,
  `lastModified` int(10) unsigned NOT NULL,
  `timeCreated` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_worlds: ~1 rows (approximately)
/*!40000 ALTER TABLE `cb_worlds` DISABLE KEYS */;
INSERT INTO `cb_worlds` (`id`, `name`, `worldServerID`, `path`, `type`, `format`, `isDefault`, `preloadAtServerStart`, `lastAccessed`, `lastModified`, `timeCreated`) VALUES
	(_binary 0x65356466366465383431303335333064, 'default', 1, 'data/worlds/server1/default.cw', 'classic', 'cw', 1, 1, 0, 0, 0);
/*!40000 ALTER TABLE `cb_worlds` ENABLE KEYS */;


-- Dumping structure for table cloudbox.cb_worldservers
CREATE TABLE IF NOT EXISTS `cb_worldservers` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table cloudbox.cb_worldservers: ~1 rows (approximately)
/*!40000 ALTER TABLE `cb_worldservers` DISABLE KEYS */;
INSERT INTO `cb_worldservers` (`id`, `name`) VALUES
	(1, 'server1');
/*!40000 ALTER TABLE `cb_worldservers` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
