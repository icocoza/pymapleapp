CREATE TABLE IF NOT EXISTS  `board` (
  `boardId` varchar(64) NOT NULL,
  `userId` varchar(64) DEFAULT NULL,
  `userName` varchar(32) DEFAULT NULL,
  `title` varchar(128) NOT NULL,
  `shortContent` varchar(128) NOT NULL,
  `hasImage` tinyint(1) DEFAULT NULL,
  `hasFile` tinyint(1) DEFAULT NULL,
  `category` varchar(64) DEFAULT NULL,
  `contentType` enum('text','image','vote','audio','video','link','none') NOT NULL,
  `deletedAt` datetime DEFAULT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`boardId`),
  KEY `idx_category` (`category`),
  KEY `idx_createdAt` (`createdAt`),
  KEY `idx_userName` (`userName`),
  KEY `idx_contentType` (`contentType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `boardContent` (
  `boardId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `content` varchar(2048) NOT NULL,
  `deletedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`boardId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `boardCount` (
  `boardId` varchar(64) NOT NULL,
  `likes` int(11) DEFAULT '0',
  `dislikes` int(11) DEFAULT '0',
  `visit` int(11) DEFAULT '0',
  `reply` int(11) DEFAULT '0',
  `modifiedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`boardId`),
  KEY `likes` (`likes`,`dislikes`,`visit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `boardReply` (
  `replyId` varchar(64) NOT NULL,
  `parentId` varchar(64) DEFAULT NULL,
  `boardId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `userName` varchar(32) NOT NULL,
  `depth` smallint(6) NOT NULL,
  `body` varchar(1024) NOT NULL,
  `replyAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `deletedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`replyId`),
  KEY `boardId` (`boardId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `boardScrap` (
  `scrapId` varchar(64) NOT NULL,
  `boardId` varchar(64) NOT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`scrapId`),
  KEY `idx_boardId` (`boardId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `boardVoter` (
  `boardId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `userName` varchar(32) NOT NULL,
  `preferences` varchar(16) NOT NULL,
  `score` int(11) DEFAULT '0',
  `votedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`boardId`,`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `chatChannel` (
  `channelId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `attendees` varchar(1024) NOT NULL,
  `attendeeCount` smallint(6) NOT NULL,
  `lastMessage` varchar(128) DEFAULT '',
  `channelType` varchar(24) DEFAULT '',
  `createdAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifiedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`channelId`),
  KEY `INDEX` (`userId`,`modifiedAt`,`channelId`,`createdAt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `chatDelMessage` (
  `channelId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `messageId` varchar(64) NOT NULL,
  `deletedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userId`,`messageId`),
  KEY `channelId` (`channelId`,`deletedAt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `chatMessage` (
  `messageId` varchar(64) NOT NULL,
  `channelId` varchar(64) NOT NULL,
  `senderId` varchar(64) NOT NULL,
  `content` varchar(1024) NOT NULL,
  `messageType` enum('none','chat','online','push') DEFAULT NULL,
  `readCount` int(11) DEFAULT '0',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`messageId`),
  KEY `channelId` (`channelId`,`senderId`,`createdAt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `chatMyChannel` (
  `userId` varchar(64) NOT NULL,
  `channelId` varchar(64) NOT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modifiedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userId`,`channelId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `chatReadMessage` (
  `channelId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `messageId` varchar(64) NOT NULL,
  `readAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userId`,`messageId`),
  KEY `channelId` (`channelId`,`userId`,`messageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `friend` (
  `userId` varchar(64) NOT NULL,
  `friendId` varchar(64) NOT NULL,
  `friendName` varchar(32) DEFAULT NULL,
  `friendType` enum('none','friend','block','black','unknown') DEFAULT 'friend',
  `friendStatus` enum('none','normal','busy','offline','leave') DEFAULT NULL,
  `deleted` tinyint(4) DEFAULT NULL,
  `addedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deletedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`userId`,`friendId`),
  KEY `userId` (`userId`,`friendId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `scrap` (
  `scrapId` varchar(64) NOT NULL,
  `url` varchar(256) NOT NULL,
  `title` varchar(64) NOT NULL,
  `subTitle` varchar(64) NOT NULL,
  `fileName` varchar(32) DEFAULT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`scrapId`),
  KEY `idx_url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `scrapBody` (
  `scrapId` varchar(64) NOT NULL,
  `body` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`scrapId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `uploadFile` (
  `fildId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `boardId` varchar(64) NOT NULL,
  `fileName` varchar(128) NOT NULL,
  `fileType` varchar(32) NOT NULL,  
  `width` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `thumbWidth` int(11) NOT NULL,
  `thumbHeight` int(11) NOT NULL,
  `fileSize` bigint(20) NOT NULL,
  `uploaded` tinyint(1) DEFAULT '0',
  `enabled` tinyint(1) DEFAULT '0',
  `cropped` tinyint(1) DEFAULT '0',
  `comment` varchar(256) DEFAULT NULL,
  `uploadedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `deletedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`fildId`),
  KEY `idx_userId` (`userId`),
  KEY `idx_boardId` (`boardId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `user` (
  `userId` varchar(64) NOT NULL,
  `userName` varchar(64) NOT NULL,
  `anonymous` tinyint(1) DEFAULT '0',
  `osType` varchar(16) DEFAULT NULL,
  `osVersion` varchar(8) DEFAULT NULL,
  `appVersion` varchar(8) DEFAULT NULL,
  `inAppcode` varchar(16) DEFAULT NULL,
  `likes` int(11) DEFAULT '0',
  `dislikes` int(11) DEFAULT '0',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `leftAt` datetime DEFAULT NULL,
  `lastAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userId`),
  KEY `idx_userName` (`userName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `userAuth` (
  `userId` varchar(64) NOT NULL,  
  `userName` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT '',
  `mobileNo` varchar(64) DEFAULT '',
  `password` varchar(64) DEFAULT '',
  `emailCode` varchar(32) DEFAULT '',
  `smsCode` varchar(6) DEFAULT '',
  `registeredAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `leftAt` datetime DEFAULT NULL,
  `authType` varchar(12) NOT NULL,
  PRIMARY KEY (`userId`),
  KEY `idx_email` (`email`),
  KEY `idx_phone` (`mobileNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `userPush` (
  `userId` varchar(64) NOT NULL,
  `uuid` varchar(128) NOT NULL,
  `epid` varchar(256) NOT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modifiedAt` datetime DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`userId`,`uuid`),
  KEY `idx_epid` (`epid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `userToken` (
  `userId` varchar(64) NOT NULL,
  `uuid` varchar(64) DEFAULT NULL,
  `tokenId` varchar(64) NOT NULL,
  `token` varchar(256) NOT NULL,
  `enabled` tinyint(1) DEFAULT '0',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `expiredAt` datetime DEFAULT NULL,  
  PRIMARY KEY (`userId`,`tokenId`),
  KEY `idx_uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `vote` (
  `boardId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `userName` varchar(32) NOT NULL,
  `closed` tinyint(1) DEFAULT '0',
  `expiredAt` datetime DEFAULT NULL,
  PRIMARY KEY (`boardId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `voteItem` (
  `voteItemId` varchar(64) NOT NULL,
  `boardId` varchar(64) NOT NULL,
  `itemText` varchar(128) DEFAULT NULL,
  `selectCount` int(11) DEFAULT '0',
  PRIMARY KEY (`voteItemId`),
  KEY `boardId` (`boardId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `voteUser` (
  `boardId` varchar(64) NOT NULL,
  `userId` varchar(64) NOT NULL,
  `voteItemId` varchar(64) NOT NULL,
  `votedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`boardId`,`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
