CREATE TABLE IF NOT EXISTS `admin`.`adminUser` (
  `userId` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `adminStatus` enum('none','normal','pending','block','leave') DEFAULT 'pending',
  `userRole` enum('none','user','adminUser','adminMaster','anonymous') DEFAULT NULL,
  `userName` varchar(64) DEFAULT NULL,
  `nationality` varchar(8) DEFAULT NULL,
  `lastPassword` varchar(64) DEFAULT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `lastAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `leftAt` datetime DEFAULT NULL,
  `passwordAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `admin`.`adminToken` (
  `userId` varchar(64) NOT NULL,
  `token` varchar(256) NOT NULL,
  `remoteIp` varchar(32) DEFAULT '',
  `reserved` varchar(64) DEFAULT NULL,
  `issuedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `admin`.`adminApp` (
  `appId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `scode` varchar(32) NOT NULL,
  `title` varchar(64) NOT NULL,
  `token` varchar(512) NOT NULL,
  `version` varchar(8) DEFAULT '',
  `description` varchar(64) DEFAULT '',
  `status` enum('ready','block','deleted','pending','stop') NOT NULL DEFAULT 'ready',
  `fcmid` varchar(32) DEFAULT NULL,
  `fcmkey` varchar(256) DEFAULT NULL,
  `storeUrl` varchar(512) DEFAULT '',
  `updateForce` tinyint(1) DEFAULT '0',
  `dbHost` varchar(64) DEFAULT NULL,
  `dbPort` SMALLINT DEFAULT 3306,
  `dbOptions` varchar(128) DEFAULT NULL,
  `dbUserId` varchar(32) DEFAULT NULL,
  `dbPassword` varchar(32) DEFAULT NULL,
  `dbInitConn` int(11) NOT NULL DEFAULT '4',
  `dbMaxConn` int(11) NOT NULL DEFAULT '8',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `statusAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appId`),
  KEY `idx_scode` (`scode`),
  KEY `idx_userId` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
