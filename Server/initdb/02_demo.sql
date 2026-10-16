-- Fictional study data. Run once after GameForge_schema_en.sql.
-- Demonstration prices are not prices of the primary platform.
USE gameforge_course;
START TRANSACTION;

INSERT INTO `Roles` (`id`,`name`) VALUES (1,'Player'),(2,'Moderator'),(3,'Administrator');
INSERT INTO `Users` (`id`,`role_id`,`telegram_id`,`display_name`) VALUES
  (1,1,900000001,'Anna — game creator'),(2,1,900000002,'Boris — player'),
  (3,2,900000003,'Maria — moderator'),(4,3,900000004,'Ivan — administrator');
INSERT INTO `Credit_Accounts` (`user_id`,`balance`) VALUES (1,100),(2,50),(3,0),(4,0);
INSERT INTO `Genres` (`id`,`name`) VALUES (1,'Puzzle'),(2,'Adventure'),(3,'Arcade');
INSERT INTO `Tags` (`id`,`name`) VALUES (1,'Space'),(2,'Logic'),(3,'Single-player');
INSERT INTO `Credit_Packages` (`id`,`name`,`credits`,`stars_price`) VALUES (1,'Study package 100',100,50),(2,'Study package 500',500,200);
INSERT INTO `Lobbies` (`id`,`owner_id`,`genre_id`,`name`,`invite_code`,`status`) VALUES (1,1,1,'Space puzzle','STUDY01','playing');
INSERT INTO `Lobby_Members` (`lobby_id`,`user_id`) VALUES (1,1),(1,2);
INSERT INTO `Ideas` (`id`,`lobby_id`,`author_id`,`body`,`status`) VALUES (1,1,1,'The player connects stars to form constellations.','accepted'),(2,1,2,'Add a time limit and hints.','accepted');
INSERT INTO `Idea_Votes` (`idea_id`,`user_id`) VALUES (1,1),(1,2),(2,1);
INSERT INTO `Lobby_Messages` (`lobby_id`,`author_id`,`body`) VALUES (1,2,'Let’s add three difficulty levels.');
INSERT INTO `Generations` (`id`,`lobby_id`,`requester_id`,`ai_model`,`cost_credits`,`status`) VALUES (1,1,1,'Study AI model',50,'succeeded'),(2,1,1,'Study AI model',50,'failed');
INSERT INTO `Games` (`id`,`author_id`,`genre_id`,`lobby_id`,`name`,`description`,`publication_status`) VALUES
  (1,1,1,1,'Constellations','Connect stars and form constellations.','published'),
  (2,1,3,NULL,'Jump','A game uploaded by its creator.','draft');
INSERT INTO `Game_Versions` (`id`,`game_id`,`generation_id`,`version_number`,`html_file`,`source_type`) VALUES
  (1,1,1,1,'games/constellations_v1.html','ai'),(2,2,NULL,1,'games/jump_v1.html','upload');
INSERT INTO `Game_Tags` (`game_id`,`tag_id`) VALUES (1,1),(1,2),(1,3);
INSERT INTO `Game_Launches` (`user_id`,`game_id`) VALUES (2,1),(2,1),(1,1);
INSERT INTO `Reviews` (`id`,`user_id`,`game_id`,`rating`,`body`) VALUES (1,2,1,5,'A clear and engaging puzzle.');
INSERT INTO `Favorites` (`user_id`,`game_id`) VALUES (2,1);
INSERT INTO `Likes` (`user_id`,`game_id`) VALUES (2,1);
INSERT INTO `Moderation_Reviews` (`version_id`,`moderator_id`,`decision`,`comment`) VALUES (1,3,'approved','The game has been reviewed and is ready for publication.');
INSERT INTO `Content_Reports` (`reporter_id`,`game_id`,`moderator_id`,`reason`,`status`) VALUES (2,1,3,'The hint on the second level is hard to see.','investigating');
INSERT INTO `Payments` (`id`,`user_id`,`package_id`,`credits`,`stars_amount`,`status`,`telegram_receipt`) VALUES
  (1,1,1,100,50,'paid','DEMO-PAID-001'),(2,2,1,100,50,'refunded','DEMO-REFUND-002');
INSERT INTO `Payment_Refunds` (`payment_id`,`staff_id`,`reason`,`status`) VALUES (2,4,'Study example of a purchase refund.','completed');

-- Anna’s balance: +50 welcome bonus +100 purchase -50 generation -50 failed generation +50 refund = 100.
-- Boris’s balance: +50 welcome bonus +100 purchase -100 refund = 50.
INSERT INTO `Credit_Transactions` (`user_id`,`amount`,`reason`,`generation_id`,`payment_id`,`transaction_key`) VALUES
  (1,50,'welcome',NULL,NULL,'welcome:1'),
  (2,50,'welcome',NULL,NULL,'welcome:2'),
  (1,100,'purchase',NULL,1,'purchase:1'),
  (1,-50,'generating',1,NULL,'generation:1'),
  (1,-50,'generating',2,NULL,'generation:2'),
  (1,50,'generation_refund',2,NULL,'generation-refund:2'),
  (2,100,'purchase',NULL,2,'purchase:2'),
  (2,-100,'purchase_refund',NULL,2,'purchase-refund:2');
INSERT INTO `Referrals` (`invitee_id`,`inviter_id`,`bonus_credits`) VALUES (2,1,0);
INSERT INTO `Author_Subscriptions` (`subscriber_id`,`author_id`) VALUES (2,1);
INSERT INTO `Notifications` (`user_id`,`title`,`body`) VALUES (1,'Game published','Модератор одобрил игру «Constellations».');
INSERT INTO `Platform_News` (`author_id`,`title`,`body`) VALUES (4,'Study version','Example gaming platform announcement.');
INSERT INTO `Platform_Settings` (`setting_key`,`setting_value`,`description`) VALUES ('max_lobby_members',5,'Maximum lobby members'),('generation_cost',50,'Generation cost in credits'),('welcome_bonus',50,'New player bonus'),('referral_bonus',10,'Planned referral bonus');
COMMIT;

-- Example queries for a presentation.
SELECT p.`display_name`, r.`name` AS `role` FROM `Users` p JOIN `Roles` r ON r.`id`=p.`role_id`;
SELECT p.`display_name`, s.`balance`, COALESCE(SUM(o.`amount`),0) AS `balance_from_transactions`
FROM `Users` p JOIN `Credit_Accounts` s ON s.`user_id`=p.`id`
LEFT JOIN `Credit_Transactions` o ON o.`user_id`=p.`id`
GROUP BY p.`id`,p.`display_name`,s.`balance`;
SELECT g.`name`, p.`display_name` AS `creator`, j.`name` AS `genre`, g.`publication_status`
FROM `Games` g JOIN `Users` p ON p.`id`=g.`author_id` JOIN `Genres` j ON j.`id`=g.`genre_id`;
