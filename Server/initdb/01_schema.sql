-- Separate GameForge study database. MySQL 8.0.16+. The primary database is not modified.
CREATE SCHEMA IF NOT EXISTS gameforge_course DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE gameforge_course;

-- Platform roles: player, moderator, administrator
CREATE TABLE `Roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_1_1 (`name`)
) ENGINE=InnoDB COMMENT='Platform roles: player, moderator, administrator';

-- Player, creator, and staff accounts
CREATE TABLE `Users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `role_id` INT NOT NULL,
  `telegram_id` BIGINT NOT NULL,
  `display_name` VARCHAR(60) NOT NULL,
  `is_blocked` BOOLEAN NOT NULL DEFAULT FALSE,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_2_1 (`telegram_id`),
  CONSTRAINT fk_2_1 FOREIGN KEY (`role_id`) REFERENCES `Roles` (`id`)
) ENGINE=InnoDB COMMENT='Player, creator, and staff accounts';

-- Main game genres
CREATE TABLE `Genres` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_3_1 (`name`)
) ENGINE=InnoDB COMMENT='Main game genres';

-- Rooms for collaborative game creation
CREATE TABLE `Lobbies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `owner_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `invite_code` VARCHAR(20) NOT NULL,
  `status` VARCHAR(25) NOT NULL DEFAULT 'collecting',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_4_1 (`invite_code`),
  CONSTRAINT fk_4_1 FOREIGN KEY (`owner_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_4_2 FOREIGN KEY (`genre_id`) REFERENCES `Genres` (`id`),
  CONSTRAINT ck_4_1 CHECK (`status` IN ('collecting','generating','playing','closed'))
) ENGINE=InnoDB COMMENT='Rooms for collaborative game creation';

-- User membership in a lobby
CREATE TABLE `Lobby_Members` (
  `lobby_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `joined_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`lobby_id`, `user_id`),
  CONSTRAINT fk_5_1 FOREIGN KEY (`lobby_id`) REFERENCES `Lobbies` (`id`),
  CONSTRAINT fk_5_2 FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB COMMENT='User membership in a lobby';

-- Participant suggestions for a future game
CREATE TABLE `Ideas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `lobby_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  `body` VARCHAR(500) NOT NULL,
  `status` VARCHAR(25) NOT NULL DEFAULT 'proposed',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT fk_6_1 FOREIGN KEY (`lobby_id`, `author_id`) REFERENCES `Lobby_Members` (`lobby_id`, `user_id`),
  CONSTRAINT ck_6_1 CHECK (`status` IN ('proposed','accepted','rejected'))
) ENGINE=InnoDB COMMENT='Participant suggestions for a future game';

-- One vote per user for a selected idea
CREATE TABLE `Idea_Votes` (
  `idea_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`idea_id`, `user_id`),
  CONSTRAINT fk_7_1 FOREIGN KEY (`idea_id`) REFERENCES `Ideas` (`id`),
  CONSTRAINT fk_7_2 FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB COMMENT='One vote per user for a selected idea';

-- Game discussion among room participants
CREATE TABLE `Lobby_Messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `lobby_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  `body` VARCHAR(1000) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT fk_8_1 FOREIGN KEY (`lobby_id`, `author_id`) REFERENCES `Lobby_Members` (`lobby_id`, `user_id`)
) ENGINE=InnoDB COMMENT='Game discussion among room participants';

-- AI requests to create and revise games
CREATE TABLE `Generations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `lobby_id` INT NOT NULL,
  `requester_id` INT NOT NULL,
  `ai_model` VARCHAR(60) NOT NULL,
  `cost_credits` INT NOT NULL,
  `status` VARCHAR(25) NOT NULL DEFAULT 'queued',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_9_1 (`id`, `requester_id`),
  CONSTRAINT fk_9_1 FOREIGN KEY (`lobby_id`) REFERENCES `Lobbies` (`id`),
  CONSTRAINT fk_9_2 FOREIGN KEY (`requester_id`) REFERENCES `Users` (`id`),
  CONSTRAINT ck_9_1 CHECK (`cost_credits` >= 0),
  CONSTRAINT ck_9_2 CHECK (`status` IN ('queued','running','succeeded','failed'))
) ENGINE=InnoDB COMMENT='AI requests to create and revise games';

-- Games in a personal library and public catalog
CREATE TABLE `Games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `author_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  `lobby_id` INT NULL,
  `name` VARCHAR(120) NOT NULL,
  `description` VARCHAR(1000) NOT NULL,
  `publication_status` VARCHAR(25) NOT NULL DEFAULT 'draft',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT fk_10_1 FOREIGN KEY (`author_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_10_2 FOREIGN KEY (`genre_id`) REFERENCES `Genres` (`id`),
  CONSTRAINT fk_10_3 FOREIGN KEY (`lobby_id`) REFERENCES `Lobbies` (`id`),
  CONSTRAINT ck_10_1 CHECK (`publication_status` IN ('draft','pending_review','published','rejected','hidden'))
) ENGINE=InnoDB COMMENT='Games in a personal library and public catalog';

-- Game file history: AI output or creator upload
CREATE TABLE `Game_Versions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `generation_id` INT NULL,
  `version_number` INT NOT NULL,
  `html_file` VARCHAR(255) NOT NULL,
  `source_type` VARCHAR(25) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_11_1 (`game_id`, `version_number`),
  UNIQUE KEY uq_11_2 (`generation_id`),
  CONSTRAINT fk_11_1 FOREIGN KEY (`game_id`) REFERENCES `Games` (`id`),
  CONSTRAINT fk_11_2 FOREIGN KEY (`generation_id`) REFERENCES `Generations` (`id`),
  CONSTRAINT ck_11_1 CHECK (`version_number` > 0),
  CONSTRAINT ck_11_2 CHECK ((`source_type` = 'ai' AND `generation_id` IS NOT NULL) OR (`source_type` = 'upload' AND `generation_id` IS NULL)),
  CONSTRAINT ck_11_3 CHECK (`source_type` IN ('ai','upload'))
) ENGINE=InnoDB COMMENT='Game file history: AI output or creator upload';

-- Additional game tags
CREATE TABLE `Tags` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_12_1 (`name`)
) ENGINE=InnoDB COMMENT='Additional game tags';

-- Many-to-many relationship between games and tags
CREATE TABLE `Game_Tags` (
  `game_id` INT NOT NULL,
  `tag_id` INT NOT NULL,
  PRIMARY KEY (`game_id`, `tag_id`),
  CONSTRAINT fk_13_1 FOREIGN KEY (`game_id`) REFERENCES `Games` (`id`),
  CONSTRAINT fk_13_2 FOREIGN KEY (`tag_id`) REFERENCES `Tags` (`id`)
) ENGINE=InnoDB COMMENT='Many-to-many relationship between games and tags';

-- One review per player per game, with a rating from 1 to 5
CREATE TABLE `Reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  `rating` TINYINT NOT NULL,
  `body` VARCHAR(1000) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_14_1 (`user_id`, `game_id`),
  CONSTRAINT fk_14_1 FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_14_2 FOREIGN KEY (`game_id`) REFERENCES `Games` (`id`),
  CONSTRAINT ck_14_1 CHECK (`rating` BETWEEN 1 AND 5)
) ENGINE=InnoDB COMMENT='One review per player per game, with a rating from 1 to 5';

-- Personal collection of favorite games
CREATE TABLE `Favorites` (
  `user_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `game_id`),
  CONSTRAINT fk_15_1 FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_15_2 FOREIGN KEY (`game_id`) REFERENCES `Games` (`id`)
) ENGINE=InnoDB COMMENT='Personal collection of favorite games';

-- Likes, independent of favorites
CREATE TABLE `Likes` (
  `user_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `game_id`),
  CONSTRAINT fk_16_1 FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_16_2 FOREIGN KEY (`game_id`) REFERENCES `Games` (`id`)
) ENGINE=InnoDB COMMENT='Likes, independent of favorites';

-- Game launch history for statistics
CREATE TABLE `Game_Launches` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT fk_17_1 FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_17_2 FOREIGN KEY (`game_id`) REFERENCES `Games` (`id`)
) ENGINE=InnoDB COMMENT='Game launch history for statistics';

-- Staff decisions on a specific game version
CREATE TABLE `Moderation_Reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `version_id` INT NOT NULL,
  `moderator_id` INT NOT NULL,
  `decision` VARCHAR(25) NOT NULL,
  `comment` VARCHAR(500) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT fk_18_1 FOREIGN KEY (`version_id`) REFERENCES `Game_Versions` (`id`),
  CONSTRAINT fk_18_2 FOREIGN KEY (`moderator_id`) REFERENCES `Users` (`id`),
  CONSTRAINT ck_18_1 CHECK (`decision` IN ('approved','отклонено','changes_requested','blocked'))
) ENGINE=InnoDB COMMENT='Staff decisions on a specific game version';

-- A report about a game or review and its handling
CREATE TABLE `Content_Reports` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `reporter_id` INT NOT NULL,
  `game_id` INT NULL,
  `review_id` INT NULL,
  `moderator_id` INT NULL,
  `reason` VARCHAR(500) NOT NULL,
  `status` VARCHAR(25) NOT NULL DEFAULT 'new',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT fk_19_1 FOREIGN KEY (`reporter_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_19_2 FOREIGN KEY (`game_id`) REFERENCES `Games` (`id`),
  CONSTRAINT fk_19_3 FOREIGN KEY (`review_id`) REFERENCES `Reviews` (`id`),
  CONSTRAINT fk_19_4 FOREIGN KEY (`moderator_id`) REFERENCES `Users` (`id`),
  CONSTRAINT ck_19_1 CHECK ((`game_id` IS NOT NULL AND `review_id` IS NULL) OR (`game_id` IS NULL AND `review_id` IS NOT NULL)),
  CONSTRAINT ck_19_2 CHECK (`status` IN ('new','investigating','closed'))
) ENGINE=InnoDB COMMENT='A report about a game or review and its handling';

-- One wallet per user: balance and debt
CREATE TABLE `Credit_Accounts` (
  `user_id` INT NOT NULL,
  `balance` INT NOT NULL DEFAULT 0,
  `debt` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`),
  CONSTRAINT fk_20_1 FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT ck_20_1 CHECK (`balance` >= 0),
  CONSTRAINT ck_20_2 CHECK (`debt` >= 0)
) ENGINE=InnoDB COMMENT='One wallet per user: balance and debt';

-- Credit purchase options using Telegram Stars
CREATE TABLE `Credit_Packages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `credits` INT NOT NULL,
  `stars_price` INT NOT NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`),
  CONSTRAINT ck_21_1 CHECK (`credits` > 0),
  CONSTRAINT ck_21_2 CHECK (`stars_price` > 0)
) ENGINE=InnoDB COMMENT='Credit purchase options using Telegram Stars';

-- Purchase order with the original price and credit amount
CREATE TABLE `Payments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `package_id` INT NOT NULL,
  `credits` INT NOT NULL,
  `stars_amount` INT NOT NULL,
  `status` VARCHAR(25) NOT NULL DEFAULT 'created',
  `telegram_receipt` VARCHAR(120) NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_22_1 (`telegram_receipt`),
  UNIQUE KEY uq_22_2 (`id`, `user_id`),
  CONSTRAINT fk_22_1 FOREIGN KEY (`user_id`) REFERENCES `Credit_Accounts` (`user_id`),
  CONSTRAINT fk_22_2 FOREIGN KEY (`package_id`) REFERENCES `Credit_Packages` (`id`),
  CONSTRAINT ck_22_1 CHECK (`credits` > 0),
  CONSTRAINT ck_22_2 CHECK (`stars_amount` > 0),
  CONSTRAINT ck_22_3 CHECK (`status` IN ('created','paid','refund_pending','refunded'))
) ENGINE=InnoDB COMMENT='Purchase order with the original price and credit amount';

-- Purchase refund request and outcome
CREATE TABLE `Payment_Refunds` (
  `payment_id` INT NOT NULL,
  `staff_id` INT NULL,
  `reason` VARCHAR(300) NOT NULL,
  `status` VARCHAR(25) NOT NULL DEFAULT 'pending',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_id`),
  CONSTRAINT fk_23_1 FOREIGN KEY (`payment_id`) REFERENCES `Payments` (`id`),
  CONSTRAINT fk_23_2 FOREIGN KEY (`staff_id`) REFERENCES `Users` (`id`),
  CONSTRAINT ck_23_1 CHECK (`status` IN ('pending','completed'))
) ENGINE=InnoDB COMMENT='Purchase refund request and outcome';

-- Ledger of credit grants, charges, and refunds
CREATE TABLE `Credit_Transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `amount` INT NOT NULL,
  `reason` VARCHAR(25) NOT NULL,
  `generation_id` INT NULL,
  `payment_id` INT NULL,
  `transaction_key` VARCHAR(100) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY uq_24_1 (`transaction_key`),
  CONSTRAINT fk_24_1 FOREIGN KEY (`user_id`) REFERENCES `Credit_Accounts` (`user_id`),
  CONSTRAINT fk_24_2 FOREIGN KEY (`generation_id`, `user_id`) REFERENCES `Generations` (`id`, `requester_id`),
  CONSTRAINT fk_24_3 FOREIGN KEY (`payment_id`, `user_id`) REFERENCES `Payments` (`id`, `user_id`),
  CONSTRAINT ck_24_1 CHECK (`amount` <> 0),
  CONSTRAINT ck_24_2 CHECK (`generation_id` IS NULL OR `payment_id` IS NULL),
  CONSTRAINT ck_24_3 CHECK ((`reason` IN ('generating','generation_refund') AND `generation_id` IS NOT NULL AND `payment_id` IS NULL) OR (`reason` IN ('purchase','purchase_refund') AND `payment_id` IS NOT NULL AND `generation_id` IS NULL) OR (`reason` IN ('welcome','referral','admin_adjustment') AND `generation_id` IS NULL AND `payment_id` IS NULL)),
  CONSTRAINT ck_24_4 CHECK ((`reason` IN ('welcome','generation_refund','purchase','referral') AND `amount` > 0) OR (`reason` IN ('generating','purchase_refund') AND `amount` < 0) OR `reason` = 'admin_adjustment'),
  CONSTRAINT ck_24_5 CHECK (`reason` IN ('welcome','generating','generation_refund','purchase','purchase_refund','referral','admin_adjustment'))
) ENGINE=InnoDB COMMENT='Ledger of credit grants, charges, and refunds';

-- Who invited a new user and the bonus amount
CREATE TABLE `Referrals` (
  `invitee_id` INT NOT NULL,
  `inviter_id` INT NOT NULL,
  `bonus_credits` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`invitee_id`),
  CONSTRAINT fk_25_1 FOREIGN KEY (`invitee_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_25_2 FOREIGN KEY (`inviter_id`) REFERENCES `Users` (`id`),
  CONSTRAINT ck_25_1 CHECK (`invitee_id` <> `inviter_id`),
  CONSTRAINT ck_25_2 CHECK (`bonus_credits` >= 0)
) ENGINE=InnoDB COMMENT='Who invited a new user and the bonus amount';

-- Player subscription to another creator’s releases
CREATE TABLE `Author_Subscriptions` (
  `subscriber_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  PRIMARY KEY (`subscriber_id`, `author_id`),
  CONSTRAINT fk_26_1 FOREIGN KEY (`subscriber_id`) REFERENCES `Users` (`id`),
  CONSTRAINT fk_26_2 FOREIGN KEY (`author_id`) REFERENCES `Users` (`id`),
  CONSTRAINT ck_26_1 CHECK (`subscriber_id` <> `author_id`)
) ENGINE=InnoDB COMMENT='Player subscription to another creator’s releases';

-- Platform messages for a specific user
CREATE TABLE `Notifications` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(120) NOT NULL,
  `body` VARCHAR(500) NOT NULL,
  `is_read` BOOLEAN NOT NULL DEFAULT FALSE,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT fk_27_1 FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB COMMENT='Platform messages for a specific user';

-- Platform staff announcements
CREATE TABLE `Platform_News` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `author_id` INT NOT NULL,
  `title` VARCHAR(120) NOT NULL,
  `body` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT fk_28_1 FOREIGN KEY (`author_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB COMMENT='Platform staff announcements';

-- Configurable limits and action costs
CREATE TABLE `Platform_Settings` (
  `setting_key` VARCHAR(60) NOT NULL,
  `setting_value` INT NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`setting_key`),
  CONSTRAINT ck_29_1 CHECK (`setting_value` >= 0)
) ENGINE=InnoDB COMMENT='Configurable limits and action costs';
