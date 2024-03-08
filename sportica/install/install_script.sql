CREATE TABLE `auth-accounts` (
  `id`         INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `first_name` VARCHAR(16)  NOT NULL,
  `last_name`  VARCHAR(16)  NOT NULL,
  `password`   VARCHAR(64)  NOT NULL,
  `email`      VARCHAR(128) NOT NULL UNIQUE,
  `role`       INT          NOT NULL DEFAULT 2,
  `valid`      BOOLEAN      NOT NULL DEFAULT FALSE,
  `active`     BOOLEAN      NOT NULL DEFAULT TRUE
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

CREATE TABLE `auth-roles` (
  `role` INT         NOT NULL PRIMARY KEY,
  `name` VARCHAR(64) NOT NULL
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

CREATE TABLE `auth-challenge` (
  `id`        INT         NOT NULL,
  `challenge` VARCHAR(32) NOT NULL
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

CREATE TABLE `email-config` (
  `id`           INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username`     VARCHAR(32)  NOT NULL,
  `password`     VARCHAR(64)  NOT NULL,
  `host`         VARCHAR(32)  NOT NULL UNIQUE,
  `port`         INT          NOT NULL,
  `smtp_auth`    BOOLEAN               DEFAULT TRUE,
  `smtp_secure`  VARCHAR(3)   NOT NULL,
  `display_name` VARCHAR(128) NOT NULL,
  `email`        VARCHAR(128) NOT NULL UNIQUE,
  `active`       BOOLEAN      NOT NULL,
  CONSTRAINT chk_smtp_secure CHECK (smtp_secure IN ('ssl', 'tls'))
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

CREATE TABLE `captcha-key` (
  `id`         INT         NOT NULL  AUTO_INCREMENT PRIMARY KEY,
  `site_key`   VARCHAR(64) NOT NULL,
  `secret_key` VARCHAR(64) NOT NULL
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

CREATE TABLE `content-config` (
  `id`          INT           NOT NULL AUTO_INCREMENT,
  `destination` VARCHAR(1024) NOT NULL,
  `maxFileSize` INT           NOT NULL,
  `thumbType`   VARCHAR(8)    NOT NULL,
  `thumbWidth`  INT           NOT NULL,
  `thumbHeight` INT           NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

CREATE TABLE `content-details` (
  `id`                INT           NOT NULL AUTO_INCREMENT,
  `fileName`          VARCHAR(1024) NOT NULL,
  `mimeFileName`      VARCHAR(32)   NOT NULL,
  `typeFileName`      VARCHAR(16)   NOT NULL,
  `imageFileName`     VARCHAR(1024) NOT NULL,
  `imageMimeFileName` VARCHAR(32)   NOT NULL,
  `imageTypeFileName` VARCHAR(16)   NOT NULL,
  `thumbFileName`     VARCHAR(1024) NOT NULL,
  `thumbMimeFileName` VARCHAR(32)   NOT NULL,
  `thumbTypeFileName` VARCHAR(16)   NOT NULL,
  `title`             VARCHAR(32)   NOT NULL,
  `description`       VARCHAR(512)  NOT NULL,
  `tags`              VARCHAR(512)  NOT NULL,
  `publisher`         INT           NOT NULL,
  `pubDate`           DATE          NOT NULL,
  `state`             INT           NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

CREATE TABLE `content-comments` (
  `pubDate`   DATE          NOT NULL,
  `publisher` INT           NOT NULL,
  `contents`  VARCHAR(2048) NOT NULL,
  `contentId` INT           NOT NULL,
  `commentId` INT           NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`commentId`),
  FOREIGN KEY (`contentId`) REFERENCES `content-details` (`id`)
    ON DELETE CASCADE
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

CREATE TABLE `content-states` (
  `state` INT         NOT NULL PRIMARY KEY,
  `name`  VARCHAR(64) NOT NULL
)
  ENGINE = InnoDB
  CHARACTER SET utf8
  COLLATE utf8_unicode_ci;

INSERT INTO `auth-roles` (`role`, `name`) VALUES ('1', 'manager');
INSERT INTO `auth-roles` (`role`, `name`) VALUES ('2', 'user');

INSERT INTO `auth-accounts` (`first_name`, `last_name`, `password`, `email`, `role`, `valid`, `active`)
VALUES ('Ricardo', 'Frade', 'admin', 'admin@sportica.com', 1, 1, 1);

INSERT INTO `email-config`
(`username`, `password`, `host`, `port`, `smtp_auth`, `smtp_secure`, `display_name`, `email`, `active`) VALUES
  ('', 'nzwgyobvrinkvxkb', 'smtp-mail.outlook.com', 587, TRUE, 'tls', 'Sportica', '',
   TRUE);

INSERT INTO `captcha-key` (`site_key`, `secret_key`)
VALUES ('6LcxByATAAAAABzVzx6dKS4QfotFT30MJUbjru0J', '6LcxByATAAAAAH2X_wuShA6efLzeibtNgoWIEZpe');

INSERT INTO `content-config`
(`destination`, `maxFileSize`, `thumbType`, `thumbWidth`, `thumbHeight`) VALUES
  ('C:\\Temp\\upload\\contents', '52428800', 'png', '80', '80');

INSERT INTO `content-states` (`state`, `name`) VALUES ('1', 'public');
INSERT INTO `content-states` (`state`, `name`) VALUES ('2', 'private');
