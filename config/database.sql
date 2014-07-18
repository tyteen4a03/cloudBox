SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `cb_global_metadata` (
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `value` text COLLATE utf8_unicode_ci NOT NULL,
  `defaultValue` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `cb_global_metadata` (`name`, `value`, `defaultValue`) VALUES
('databaseVersion', '1000011', '1000011');

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

CREATE TABLE IF NOT EXISTS `cb_user_groups` (
  `id` binary(16) NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `displayStylePriority` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `userGroupID` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `cb_user_group_user_assoc` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userID` binary(16) NOT NULL,
  `groupID` varbinary(16) NOT NULL,
  UNIQUE KEY `id` (`id`),
  KEY `userID` (`userID`,`groupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `cb_user_service_assoc` (
  `userID` bigint(20) NOT NULL,
  `service` tinyint(4) NOT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT '0',
  UNIQUE KEY `userID_service` (`userID`,`service`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `cb_worlds` (
  `id` binary(16) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `worldServerID` int(11) NOT NULL,
  `path` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
  `format` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
  `isDefault` tinyint(1) NOT NULL,
  `preloadAtServerStart` tinyint(1) NOT NULL,
  `lastAccessed` int(11) DEFAULT NULL,
  `lastModified` int(11) DEFAULT NULL,
  `timeCreated` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `cb_worldservers` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;