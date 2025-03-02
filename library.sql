/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 50743
 Source Host           : localhost:3306
 Source Schema         : bmis

 Target Server Type    : MySQL
 Target Server Version : 50743
 File Encoding         : 65001

 Date: 08/01/2024 14:48:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books`  (
  `isbn` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `author` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `press` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `category` int(11) NULL DEFAULT NULL,
  `intro` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `location` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `cover` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`isbn`) USING BTREE,
  UNIQUE INDEX `isbn`(`isbn`) USING BTREE,
  INDEX `ix_books_author`(`author`) USING BTREE,
  INDEX `ix_books_name`(`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of books
-- ----------------------------
INSERT INTO `books` VALUES ('1247571522', '平凡的世界', '路遥', '北京十月文艺出版社', 5, '本书是一部全景式地表现中国当代城乡社会生活的长篇小说。', '103', 'http://127.0.0.1:5000/static/img/cover/pinfan21_03_05_01_38_09.jpg');
INSERT INTO `books` VALUES ('21321543546', 'Flask web 开发实战', '李辉', '机械工业出版社', 1, 'Flask开发入门', '102', 'http://127.0.0.1:5000/static/img/cover/书籍封面21_03_05_08_59_53.jpg');
INSERT INTO `books` VALUES ('32432565613', '信号与系统', '郑钧里', '清华大学出版社', 0, '通信基础知识', '102', 'http://127.0.0.1:5000/static/img/cover/xinhao21_03_05_09_02_42.jpg');
INSERT INTO `books` VALUES ('9787115257284', '好学、好用、好玩的Photoshop 写给初学者的入门书', '李金明', '人民邮电出版社', 7, 'PS入门书籍', '102', 'http://127.0.0.1:5000/static/img/cover/s680071321_03_05_09_05_07.jpg');
INSERT INTO `books` VALUES ('9787115447395', '超级网红', '于晓华', '人民邮电出版社', 5, '网红经济日益发酵...', '102', 'http://127.0.0.1:5000/static/img/cover/超级网红21_03_05_00_55_36.jpg');
INSERT INTO `books` VALUES ('9787516644188', '悦己', '郝言言', '新华出版社', 5, '在生活中，在爱情中，如何取悦自己，如何找到自己的价值？《悦己》是一本写给女性的励志书籍，旨在帮助那些迷失在生活、爱情中的女人找到自我，学会取悦自己、接纳自己、欣赏自己。', '103', 'http://127.0.0.1:5000/static/img/cover/悦己21_03_05_00_58_31.jpg');

-- ----------------------------
-- Table structure for librarys
-- ----------------------------
DROP TABLE IF EXISTS `librarys`;
CREATE TABLE `librarys`  (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn_id` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `location` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT NULL,
  `borrower_id` int(11) NULL DEFAULT NULL,
  `start_date` float NULL DEFAULT NULL,
  `end_date` float NULL DEFAULT NULL,
  `readyto_borrow` int(11) NULL DEFAULT NULL,
  `readyto_return` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`book_id`) USING BTREE,
  UNIQUE INDEX `book_id`(`book_id`) USING BTREE,
  INDEX `isbn_id`(`isbn_id`) USING BTREE,
  INDEX `borrower_id`(`borrower_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of librarys
-- ----------------------------

-- ----------------------------
-- Table structure for requests
-- ----------------------------
DROP TABLE IF EXISTS `requests`;
CREATE TABLE `requests`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NULL DEFAULT NULL,
  `opcode` int(11) NULL DEFAULT NULL,
  `requester` int(11) NULL DEFAULT NULL,
  `requestdate` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  INDEX `book_id`(`book_id`) USING BTREE,
  INDEX `requester`(`requester`) USING BTREE,
  CONSTRAINT `requests_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `librarys` (`book_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `requests_ibfk_2` FOREIGN KEY (`requester`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of requests
-- ----------------------------

-- ----------------------------
-- Table structure for statics
-- ----------------------------
DROP TABLE IF EXISTS `statics`;
CREATE TABLE `statics`  (
  `mon` int(11) NOT NULL AUTO_INCREMENT,
  `book_data` int(11) NULL DEFAULT NULL,
  `reader_data` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`mon`) USING BTREE,
  UNIQUE INDEX `mon`(`mon`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of statics
-- ----------------------------
INSERT INTO `statics` VALUES (1, 0, 0);
INSERT INTO `statics` VALUES (2, 0, 0);
INSERT INTO `statics` VALUES (3, 6, 3);
INSERT INTO `statics` VALUES (4, 0, 0);
INSERT INTO `statics` VALUES (5, 0, 0);
INSERT INTO `statics` VALUES (6, 0, 3);
INSERT INTO `statics` VALUES (7, 0, 0);
INSERT INTO `statics` VALUES (8, 0, 0);
INSERT INTO `statics` VALUES (9, 0, 0);
INSERT INTO `statics` VALUES (10, 0, 0);
INSERT INTO `statics` VALUES (11, 0, 0);
INSERT INTO `statics` VALUES (12, 0, 0);

-- ----------------------------
-- Table structure for sysinfo
-- ----------------------------
DROP TABLE IF EXISTS `sysinfo`;
CREATE TABLE `sysinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `maxuser` int(11) NULL DEFAULT NULL,
  `maxbook` int(11) NULL DEFAULT NULL,
  `maxtime` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sysinfo
-- ----------------------------
INSERT INTO `sysinfo` VALUES (1, 100, 5, 3);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `gender` int(11) NULL DEFAULT NULL,
  `depart` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `post` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `contact` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `room` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_type` int(11) NULL DEFAULT NULL,
  `avata` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  UNIQUE INDEX `ix_users_username`(`username`) USING BTREE,
  INDEX `ix_users_name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1000014 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', 'pbkdf2:sha256:150000$URQZbAn9$88f3f5df7b557f1166e7c939b66f9857984f912ea38afa849d9452f132b01a30', '管理员', 1, '办公室', '助理', '13567892132', '12栋201', 0, 'http://127.0.0.1:5000/static/img/avata/avata321_03_05_00_59_56.jpg');
INSERT INTO `users` VALUES (11111, '2', 'pbkdf2:sha256:150000$pbF0U7OJ$0d89907556012e7198a7b31f4e787c17a06fc288443008176bc918b93c4dc1e7', '李四', 1, '2', '', '110', '23', 1, 'http://127.0.0.1:5000/static/img/avata/周末【短的】-封面24_01_08_14_40_31.jpg');
INSERT INTO `users` VALUES (12345, '1', 'pbkdf2:sha256:150000$6406wdds$a77d7cc04129288524864723d9b9da01e46bc8e16fb10a97d90932edcac98962', '张三', 1, '1', '', '110', '1201', 1, 'http://127.0.0.1:5000/static/img/avata/周末【短的】-封面24_01_08_14_34_33.jpg');
INSERT INTO `users` VALUES (100001, 'liming', 'pbkdf2:sha256:150000$ImrK3CTJ$b5bfd84bf1c3d1bc8c684285e540481c946773589ae72cc8e711934aee25c1a6', '李明', 1, '计算机系', '硕士', '13626526733', '13栋203', 1, 'http://127.0.0.1:5000/static/img/avata/avata321_03_05_00_59_56.jpg');
INSERT INTO `users` VALUES (100002, 'peiqi', 'pbkdf2:sha256:150000$dISCVHTF$b345144cf9619c9c4e0f14fcee2c562a54f00ea9aa45cf3e3f35e6c8a19a5a14', '佩奇', 1, '经济系', '闲人', '14562652673', '16栋202', 1, 'http://127.0.0.1:5000/static/img/avata/peiqi21_03_05_01_16_22.jpg');
INSERT INTO `users` VALUES (100004, 'mayi', 'pbkdf2:sha256:150000$xHpzN8ir$537e971237d53f1cdb710dfa74ce534cc32e569761377a758bf6f7701c4d1f63', '蚂蚁', 1, '计算机系', '博士', '13626776733', '12栋203', 1, 'http://127.0.0.1:5000/static/img/avata/starwar21_03_05_01_39_11.jpg');
INSERT INTO `users` VALUES (1000013, 'tom', 'pbkdf2:sha256:150000$2k47cLyL$1b43c7a0d2a13c80f4aad5aec18ea65de2895ae0183dbffdf9bc347f7014802f', '汤姆', 1, '外语系', '本科', '13626523933', '16栋302', 1, 'http://127.0.0.1:5000/static/img/avata/avata221_03_06_22_47_38.jpg');

-- ----------------------------
-- Table structure for wants
-- ----------------------------
DROP TABLE IF EXISTS `wants`;
CREATE TABLE `wants`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `author` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `press` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `category` int(11) NULL DEFAULT NULL,
  `sale` float NULL DEFAULT NULL,
  `requester` int(11) NULL DEFAULT NULL,
  `date` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  INDEX `requester`(`requester`) USING BTREE,
  INDEX `ix_wants_name`(`name`) USING BTREE,
  INDEX `ix_wants_author`(`author`) USING BTREE,
  CONSTRAINT `wants_ibfk_1` FOREIGN KEY (`requester`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of wants
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
