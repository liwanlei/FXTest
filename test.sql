/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2019-04-22 10:43:57
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `actions`
-- ----------------------------
DROP TABLE IF EXISTS `actions`;
CREATE TABLE `actions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `name` varchar(252) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `style` int(11) DEFAULT NULL,
  `sleepnum` int(11) DEFAULT NULL,
  `sql` varchar(252) DEFAULT NULL,
  `testevent` int(11) DEFAULT NULL,
  `caseid` int(11) DEFAULT NULL,
  `requestsurl` varchar(252) DEFAULT NULL,
  `requestsparame` varchar(252) DEFAULT NULL,
  `requestmethod` varchar(8) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_actions_name` (`name`),
  KEY `user` (`user`),
  KEY `testevent` (`testevent`),
  CONSTRAINT `actions_ibfk_1` FOREIGN KEY (`user`) REFERENCES `users` (`id`),
  CONSTRAINT `actions_ibfk_2` FOREIGN KEY (`testevent`) REFERENCES `ceshihuanjing` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of actions
-- ----------------------------

-- ----------------------------
-- Table structure for `alembic_version`
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------

-- ----------------------------
-- Table structure for `caseactions`
-- ----------------------------
DROP TABLE IF EXISTS `caseactions`;
CREATE TABLE `caseactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case` int(11) DEFAULT NULL,
  `action` int(11) DEFAULT NULL,
  `actiontype` int(11) DEFAULT NULL,
  `filed` varchar(252) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `case` (`case`),
  KEY `action` (`action`),
  CONSTRAINT `caseactions_ibfk_1` FOREIGN KEY (`case`) REFERENCES `interfacetests` (`id`),
  CONSTRAINT `caseactions_ibfk_2` FOREIGN KEY (`action`) REFERENCES `actions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of caseactions
-- ----------------------------

-- ----------------------------
-- Table structure for `casegenerals`
-- ----------------------------
DROP TABLE IF EXISTS `casegenerals`;
CREATE TABLE `casegenerals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case` int(11) DEFAULT NULL,
  `general` int(11) DEFAULT NULL,
  `filed` varchar(252) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `case` (`case`),
  KEY `general` (`general`),
  CONSTRAINT `casegenerals_ibfk_1` FOREIGN KEY (`case`) REFERENCES `interfacetests` (`id`),
  CONSTRAINT `casegenerals_ibfk_2` FOREIGN KEY (`general`) REFERENCES `generalconfigurations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of casegenerals
-- ----------------------------

-- ----------------------------
-- Table structure for `ceshihuanjing`
-- ----------------------------
DROP TABLE IF EXISTS `ceshihuanjing`;
CREATE TABLE `ceshihuanjing` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `make_user` int(11) DEFAULT NULL,
  `url` varchar(252) DEFAULT NULL,
  `desc` varchar(252) DEFAULT NULL,
  `database` varchar(252) DEFAULT NULL,
  `dbport` varchar(252) DEFAULT NULL,
  `dbhost` varchar(252) DEFAULT NULL,
  `databaseuser` varchar(32) DEFAULT NULL,
  `databasepassword` varchar(32) DEFAULT NULL,
  `project` int(11) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `make_user` (`make_user`),
  KEY `project` (`project`),
  CONSTRAINT `ceshihuanjing_ibfk_1` FOREIGN KEY (`make_user`) REFERENCES `users` (`id`),
  CONSTRAINT `ceshihuanjing_ibfk_2` FOREIGN KEY (`project`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ceshihuanjing
-- ----------------------------
INSERT INTO `ceshihuanjing` VALUES ('8', '1', '阿萨德撒的', '萨达萨达', null, null, null, null, null, null, '0');
INSERT INTO `ceshihuanjing` VALUES ('9', '1', 'ss  ', 'asdasdasd', 'None', 'ddd', 'ddd', 'None', null, '6', '0');
INSERT INTO `ceshihuanjing` VALUES ('10', '1', 'dasdasdasd  ', 'ssssssasa', 'None', 'asdas', 'asdsad', 'None', null, '6', '0');
INSERT INTO `ceshihuanjing` VALUES ('11', '1', '萨达萨达   ', '萨达萨达', '阿萨德撒的', 'ddd', 'dd', '萨达萨达', '萨达萨达', '6', '0');
INSERT INTO `ceshihuanjing` VALUES ('12', '1', 'http:127.0.0.1 ', '本地测试环境', 'testtuling', 'sadsad', 'sadsad', 'root', 'testurl', null, '1');
INSERT INTO `ceshihuanjing` VALUES ('13', '1', 'dasdasdasd', 'dasdasdasd', 'dasdasdasd', 'dasdasdasd', 'dasdasdasd', 'dasdasdasd', 'dasdasdasd', null, '1');

-- ----------------------------
-- Table structure for `emailreports`
-- ----------------------------
DROP TABLE IF EXISTS `emailreports`;
CREATE TABLE `emailreports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_re_user_id` int(11) DEFAULT NULL,
  `send_email` varchar(64) DEFAULT NULL,
  `send_email_password` varchar(64) DEFAULT NULL,
  `stmp_email` varchar(64) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `to_email` varchar(64) DEFAULT NULL,
  `default_set` tinyint(1) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `email_re_user_id` (`email_re_user_id`),
  CONSTRAINT `emailreports_ibfk_1` FOREIGN KEY (`email_re_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of emailreports
-- ----------------------------
INSERT INTO `emailreports` VALUES ('3', '1', 'dd@qq.com', 'dwer', null, null, '[\'dsfsdf\']', '1', '0');
INSERT INTO `emailreports` VALUES ('4', '1', 'sdfsdf@qq.tyuty', 'sdfsdf', null, null, '[\'asdasd\']', '0', '1');
INSERT INTO `emailreports` VALUES ('5', '1', 'asdasd@qq.bb', 'sadasdas', null, null, '[\'sadasd\']', '1', '1');

-- ----------------------------
-- Table structure for `generalconfigurations`
-- ----------------------------
DROP TABLE IF EXISTS `generalconfigurations`;
CREATE TABLE `generalconfigurations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `name` varchar(252) NOT NULL,
  `style` int(11) DEFAULT NULL,
  `key` varchar(252) DEFAULT NULL,
  `token_parame` varchar(252) DEFAULT NULL,
  `token_url` varchar(252) DEFAULT NULL,
  `token_method` varchar(16) DEFAULT NULL,
  `sqlurl` varchar(252) DEFAULT NULL,
  `request_url` varchar(252) DEFAULT NULL,
  `request_parame` varchar(252) DEFAULT NULL,
  `request_method` varchar(252) DEFAULT NULL,
  `testevent` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_generalconfigurations_name` (`name`),
  KEY `user` (`user`),
  KEY `testevent` (`testevent`),
  CONSTRAINT `generalconfigurations_ibfk_1` FOREIGN KEY (`user`) REFERENCES `users` (`id`),
  CONSTRAINT `generalconfigurations_ibfk_2` FOREIGN KEY (`testevent`) REFERENCES `ceshihuanjing` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of generalconfigurations
-- ----------------------------

-- ----------------------------
-- Table structure for `interfaces`
-- ----------------------------
DROP TABLE IF EXISTS `interfaces`;
CREATE TABLE `interfaces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_id` int(11) DEFAULT NULL,
  `projects_id` int(11) DEFAULT NULL,
  `Interface_name` varchar(252) DEFAULT NULL,
  `Interface_url` varchar(252) DEFAULT NULL,
  `Interface_meth` varchar(252) DEFAULT NULL,
  `Interface_headers` varchar(252) DEFAULT NULL,
  `Interface_user_id` int(11) DEFAULT NULL,
  `interfacetype` varchar(32) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `model_id` (`model_id`),
  KEY `projects_id` (`projects_id`),
  KEY `Interface_user_id` (`Interface_user_id`),
  CONSTRAINT `interfaces_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `models` (`id`),
  CONSTRAINT `interfaces_ibfk_2` FOREIGN KEY (`projects_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `interfaces_ibfk_3` FOREIGN KEY (`Interface_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of interfaces
-- ----------------------------
INSERT INTO `interfaces` VALUES ('1', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('2', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('4', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('5', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('7', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('8', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('10', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('11', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('13', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('14', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('16', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('17', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('19', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('20', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('22', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('23', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('25', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('26', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('28', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('29', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('31', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('32', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('34', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('35', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('37', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('38', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('40', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('41', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('43', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('44', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('46', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('47', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('49', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('50', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('52', '2', '9', '阿萨德撒的', '萨达萨达', '萨达萨达', null, '1', 'http', '0');
INSERT INTO `interfaces` VALUES ('53', '2', null, 'asdasdasdasdasdasd', 'http://www.tuling123.com/openapi/api', 'POST', 'asdfasdfadsf', '1', 'http', '0');

-- ----------------------------
-- Table structure for `interfacetests`
-- ----------------------------
DROP TABLE IF EXISTS `interfacetests`;
CREATE TABLE `interfacetests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_id` int(11) DEFAULT NULL,
  `projects_id` int(11) DEFAULT NULL,
  `interface_id` int(11) DEFAULT NULL,
  `bian_num` varchar(252) DEFAULT NULL,
  `interface_type` varchar(16) DEFAULT NULL,
  `Interface_name` varchar(252) DEFAULT NULL,
  `Interface_url` varchar(252) DEFAULT NULL,
  `Interface_meth` varchar(252) DEFAULT NULL,
  `Interface_pase` varchar(252) DEFAULT NULL,
  `Interface_assert` varchar(252) DEFAULT NULL,
  `Interface_headers` varchar(252) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `getattr_p` varchar(252) DEFAULT NULL,
  `Interface_is_tiaoshi` tinyint(1) DEFAULT NULL,
  `Interface_tiaoshi_shifou` tinyint(1) DEFAULT NULL,
  `Interface_user_id` int(11) DEFAULT NULL,
  `saveresult` tinyint(1) DEFAULT NULL,
  `is_database` tinyint(1) DEFAULT NULL,
  `chaxunshujuku` varchar(252) DEFAULT NULL,
  `databaseziduan` varchar(252) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `model_id` (`model_id`),
  KEY `projects_id` (`projects_id`),
  KEY `interface_id` (`interface_id`),
  KEY `pid` (`pid`),
  KEY `Interface_user_id` (`Interface_user_id`),
  CONSTRAINT `interfacetests_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `models` (`id`),
  CONSTRAINT `interfacetests_ibfk_2` FOREIGN KEY (`projects_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `interfacetests_ibfk_3` FOREIGN KEY (`interface_id`) REFERENCES `interfaces` (`id`),
  CONSTRAINT `interfacetests_ibfk_4` FOREIGN KEY (`pid`) REFERENCES `interfacetests` (`id`),
  CONSTRAINT `interfacetests_ibfk_5` FOREIGN KEY (`Interface_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of interfacetests
-- ----------------------------

-- ----------------------------
-- Table structure for `mockserver`
-- ----------------------------
DROP TABLE IF EXISTS `mockserver`;
CREATE TABLE `mockserver` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `make_uers` int(11) DEFAULT NULL,
  `name` varchar(55) DEFAULT NULL,
  `path` varchar(252) DEFAULT NULL,
  `methods` varchar(50) DEFAULT NULL,
  `headers` varchar(500) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `fanhui` varchar(500) DEFAULT NULL,
  `params` varchar(500) DEFAULT NULL,
  `rebacktype` varchar(32) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `delete` tinyint(1) DEFAULT NULL,
  `ischeck` tinyint(1) DEFAULT NULL,
  `is_headers` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `make_uers` (`make_uers`),
  CONSTRAINT `mockserver_ibfk_1` FOREIGN KEY (`make_uers`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of mockserver
-- ----------------------------

-- ----------------------------
-- Table structure for `models`
-- ----------------------------
DROP TABLE IF EXISTS `models`;
CREATE TABLE `models` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_name` varchar(256) DEFAULT NULL,
  `model_user_id` int(11) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `model_user_id` (`model_user_id`),
  CONSTRAINT `models_ibfk_1` FOREIGN KEY (`model_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of models
-- ----------------------------
INSERT INTO `models` VALUES ('1', '添加', '1', '1');
INSERT INTO `models` VALUES ('2', '登录', '1', '1');
INSERT INTO `models` VALUES ('3', '的订单', '1', '0');
INSERT INTO `models` VALUES ('4', '添加阿萨德撒的', '1', '0');
INSERT INTO `models` VALUES ('5', '添加', '1', '1');
INSERT INTO `models` VALUES ('6', '登录', '1', '1');
INSERT INTO `models` VALUES ('7', '的订单', '1', '0');
INSERT INTO `models` VALUES ('8', '添加阿萨德撒的', '1', '0');
INSERT INTO `models` VALUES ('9', '添加', '1', '1');
INSERT INTO `models` VALUES ('10', '登录', '1', '1');
INSERT INTO `models` VALUES ('11', '的订单', '1', '0');
INSERT INTO `models` VALUES ('12', '添加阿萨德撒的', '1', '0');
INSERT INTO `models` VALUES ('13', '添加', '1', '1');
INSERT INTO `models` VALUES ('14', '登录', '1', '1');
INSERT INTO `models` VALUES ('15', '的订单', '1', '0');
INSERT INTO `models` VALUES ('16', '添加阿萨德撒的', '1', '0');
INSERT INTO `models` VALUES ('17', '添加', '1', '1');
INSERT INTO `models` VALUES ('18', '登录', '1', '1');
INSERT INTO `models` VALUES ('19', '的订单', '1', '0');
INSERT INTO `models` VALUES ('20', '添加阿萨德撒的', '1', '0');
INSERT INTO `models` VALUES ('21', '添加', '1', '1');
INSERT INTO `models` VALUES ('22', '登录', '1', '1');
INSERT INTO `models` VALUES ('23', '的订单', '1', '0');
INSERT INTO `models` VALUES ('24', '添加阿萨德撒的', '1', '0');
INSERT INTO `models` VALUES ('25', '添加', '1', '1');
INSERT INTO `models` VALUES ('26', '登录', '1', '1');
INSERT INTO `models` VALUES ('27', '的订单', '1', '0');
INSERT INTO `models` VALUES ('28', '添加阿萨德撒的', '1', '0');

-- ----------------------------
-- Table structure for `parames`
-- ----------------------------
DROP TABLE IF EXISTS `parames`;
CREATE TABLE `parames` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interface_id` int(11) DEFAULT NULL,
  `parameter_type` varchar(64) DEFAULT NULL,
  `parameter_name` varchar(64) DEFAULT NULL,
  `necessary` tinyint(1) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `default` varchar(63) DEFAULT NULL,
  `desc` varchar(252) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `interface_id` (`interface_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `parames_ibfk_1` FOREIGN KEY (`interface_id`) REFERENCES `interfaces` (`id`),
  CONSTRAINT `parames_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of parames
-- ----------------------------

-- ----------------------------
-- Table structure for `projects`
-- ----------------------------
DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_user_id` int(11) DEFAULT NULL,
  `project_name` varchar(252) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_name` (`project_name`),
  KEY `project_user_id` (`project_user_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`project_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of projects
-- ----------------------------
INSERT INTO `projects` VALUES ('1', '1', '昨夜西风凋碧树', '0');
INSERT INTO `projects` VALUES ('2', '1', 'asdasd', '0');
INSERT INTO `projects` VALUES ('3', '1', '啊实打实的萨达萨达', '0');
INSERT INTO `projects` VALUES ('4', '1', 'dasdasdsad', '1');
INSERT INTO `projects` VALUES ('5', '1', 'asdsad', '0');
INSERT INTO `projects` VALUES ('6', '1', 'asdasdasdasd', '1');
INSERT INTO `projects` VALUES ('7', '1', 'sadf ', '0');
INSERT INTO `projects` VALUES ('8', '7', 'dd', '0');
INSERT INTO `projects` VALUES ('9', '7', 'ddss', '1');
INSERT INTO `projects` VALUES ('10', '7', 'ddss1', '1');
INSERT INTO `projects` VALUES ('11', '7', 'ddss122', '1');
INSERT INTO `projects` VALUES ('12', '7', 'sdasd', '1');
INSERT INTO `projects` VALUES ('13', '7', 'sdasddsd', '1');

-- ----------------------------
-- Table structure for `quanxians`
-- ----------------------------
DROP TABLE IF EXISTS `quanxians`;
CREATE TABLE `quanxians` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rose` int(11) DEFAULT NULL,
  `project` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rose` (`rose`),
  KEY `project` (`project`),
  CONSTRAINT `quanxians_ibfk_1` FOREIGN KEY (`rose`) REFERENCES `roles` (`id`),
  CONSTRAINT `quanxians_ibfk_2` FOREIGN KEY (`project`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of quanxians
-- ----------------------------

-- ----------------------------
-- Table structure for `quanxianusers`
-- ----------------------------
DROP TABLE IF EXISTS `quanxianusers`;
CREATE TABLE `quanxianusers` (
  `user_id` int(11) DEFAULT NULL,
  `quanxians_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `quanxians_id` (`quanxians_id`),
  CONSTRAINT `quanxianusers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `quanxianusers_ibfk_2` FOREIGN KEY (`quanxians_id`) REFERENCES `quanxians` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of quanxianusers
-- ----------------------------

-- ----------------------------
-- Table structure for `registrations`
-- ----------------------------
DROP TABLE IF EXISTS `registrations`;
CREATE TABLE `registrations` (
  `task_id` int(11) DEFAULT NULL,
  `interfacetests_id` int(11) DEFAULT NULL,
  KEY `task_id` (`task_id`),
  KEY `interfacetests_id` (`interfacetests_id`),
  CONSTRAINT `registrations_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `registrations_ibfk_2` FOREIGN KEY (`interfacetests_id`) REFERENCES `interfacetests` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of registrations
-- ----------------------------

-- ----------------------------
-- Table structure for `roles`
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `default` tinyint(1) DEFAULT NULL,
  `permissions` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO `roles` VALUES ('1', 'User', '0', '7');
INSERT INTO `roles` VALUES ('2', 'Oneadmin', '0', '15');
INSERT INTO `roles` VALUES ('3', 'Administrator', '0', '255');

-- ----------------------------
-- Table structure for `tasks`
-- ----------------------------
DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `makeuser` int(11) DEFAULT NULL,
  `taskname` varchar(32) DEFAULT NULL,
  `taskstart` varchar(252) DEFAULT NULL,
  `taskmakedate` datetime DEFAULT NULL,
  `taskrepor_to` varchar(252) DEFAULT NULL,
  `taskrepor_cao` varchar(252) DEFAULT NULL,
  `task_make_email` varchar(252) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `yunxing_status` varchar(16) DEFAULT NULL,
  `prject` int(11) DEFAULT NULL,
  `testevent` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `makeuser` (`makeuser`),
  KEY `prject` (`prject`),
  KEY `testevent` (`testevent`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`makeuser`) REFERENCES `users` (`id`),
  CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`prject`) REFERENCES `projects` (`id`),
  CONSTRAINT `tasks_ibfk_3` FOREIGN KEY (`testevent`) REFERENCES `ceshihuanjing` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tasks
-- ----------------------------

-- ----------------------------
-- Table structure for `testcaseresults`
-- ----------------------------
DROP TABLE IF EXISTS `testcaseresults`;
CREATE TABLE `testcaseresults` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_id` int(11) DEFAULT NULL,
  `result` varchar(252) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `testevir` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `case_id` (`case_id`),
  KEY `testevir` (`testevir`),
  CONSTRAINT `testcaseresults_ibfk_1` FOREIGN KEY (`case_id`) REFERENCES `interfacetests` (`id`),
  CONSTRAINT `testcaseresults_ibfk_2` FOREIGN KEY (`testevir`) REFERENCES `ceshihuanjing` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of testcaseresults
-- ----------------------------

-- ----------------------------
-- Table structure for `tstresults`
-- ----------------------------
DROP TABLE IF EXISTS `tstresults`;
CREATE TABLE `tstresults` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Test_user_id` int(11) DEFAULT NULL,
  `test_num` int(11) DEFAULT NULL,
  `pass_num` int(11) DEFAULT NULL,
  `fail_num` int(11) DEFAULT NULL,
  `Exception_num` int(11) DEFAULT NULL,
  `can_num` int(11) DEFAULT NULL,
  `wei_num` int(11) DEFAULT NULL,
  `projects_id` int(11) DEFAULT NULL,
  `test_time` datetime DEFAULT NULL,
  `hour_time` int(11) DEFAULT NULL,
  `test_rep` varchar(252) DEFAULT NULL,
  `test_log` varchar(252) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Test_user_id` (`Test_user_id`),
  KEY `projects_id` (`projects_id`),
  CONSTRAINT `tstresults_ibfk_1` FOREIGN KEY (`Test_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tstresults_ibfk_2` FOREIGN KEY (`projects_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tstresults
-- ----------------------------

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(63) DEFAULT NULL,
  `password` varchar(252) DEFAULT NULL,
  `user_email` varchar(64) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `is_login` tinyint(1) DEFAULT NULL,
  `is_sper` tinyint(1) DEFAULT NULL,
  `work_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `user_email` (`user_email`),
  KEY `work_id` (`work_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`work_id`) REFERENCES `works` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', 'liwanlei', 'pbkdf2:sha256:50000$H2XVXtY6$06878e9c817c7a1dfba6caaa2e58256726f2fd4eafea8b493fddaa6236f74329', '952943386@qq.com', '0', '1', '1', '1');
INSERT INTO `users` VALUES ('2', 'eewrewr', 'pbkdf2:sha256:50000$4i6Pbd9N$037662ab9611088b2b6cded8fcad9ab09e5886ca6ea979817c68df954c398499', '99324432432', '0', null, '0', '1');
INSERT INTO `users` VALUES ('5', 'liwanleil', 'pbkdf2:sha256:50000$0OKoPwym$d41abf01a84d3b973103bd31ca3194633d4d3c04161d5e1d3d48e10d5ef291cc', '32423432', '0', null, '0', '2');
INSERT INTO `users` VALUES ('7', 'liwanlei123', 'pbkdf2:sha256:50000$wmfUrJpv$66d849c3b279ef8fe863ee3c84977f9f4787255110c867ea7a8e0abf12db824b', 'liwanlei', '0', null, '0', '1');
INSERT INTO `users` VALUES ('9', 'liwanlei11', 'pbkdf2:sha256:50000$215EW9H2$3904ebc2814d19d77d5b3410e9fc3ddd6b36be4ae8e65e6a5e6ce0ffcb1e1451', '12121212', '0', null, '0', '1');
INSERT INTO `users` VALUES ('10', 'admin', 'pbkdf2:sha256:50000$FMK2Wp13$d41783225ddc9057a6b78076cde6df2111a52ab83cbfc42238b19fb25e7e622a', 'slitobo@163.com', '1', null, '0', '1');
INSERT INTO `users` VALUES ('11', 'Test', 'pbkdf2:sha256:50000$85nqYzxM$853128989c4ca8854ba3cbc1792074338956c09d828c4e13ccc13c3eecd5970b', 'Test@qq.com', '0', null, '0', '1');
INSERT INTO `users` VALUES ('12', 'liwanlei345', 'pbkdf2:sha256:50000$Gcrd8CAG$16c48e5863596e6f42a764eecd94c6cc90801ce8e2ba25155f41ffb6f1f03823', 'liwanlei@qq.com', '0', null, '0', '1');
INSERT INTO `users` VALUES ('16', 'zhangyan', 'pbkdf2:sha256:50000$vnn1svKe$952ea026f8f2cae3c193254ca08ed11a7053ae294bea7c992f9f3e0b7592a401', '1392364470', '0', null, '0', '1');
INSERT INTO `users` VALUES ('17', 'james', 'pbkdf2:sha256:50000$k1Agosjm$c704984da17747c5d8dc41fab46ca00fc1eadb389c9da342bf5d32acf458150a', '984106718@qq.com', '0', null, '0', '1');
INSERT INTO `users` VALUES ('18', 'Ahre', 'pbkdf2:sha256:50000$GmY74OIM$c2bb446c0a09b27f968f9e81a14b03bb303027274cb2a0d935615be2584669ca', '121983006@qq.com', '0', null, '0', '1');
INSERT INTO `users` VALUES ('19', '1234', 'pbkdf2:sha256:50000$y6zq0qWy$e8766a9ce6ca0ae4c0da8627bd741ea3d0d193bfd4679144997edb67ab456151', '123', '0', null, '0', null);
INSERT INTO `users` VALUES ('20', '111111', 'pbkdf2:sha256:50000$wYgqrQQA$a36ee60eb57d61b7b31f1c30c6338e2dbd0ad7c57e133fccfea6a3298be5b393', '111', '0', null, '0', null);
INSERT INTO `users` VALUES ('21', 'sky216', 'pbkdf2:sha256:50000$e6JMhZi3$4aea5ddeac3937a24b869e88b5e53f78918fb694efe8d7d37d3ca39fb00cc9f6', '3358372183@qq.com', '0', null, '0', null);
INSERT INTO `users` VALUES ('22', 'test123', 'pbkdf2:sha256:50000$6RV2HjgA$4e1a7aec9190d770ba432f83b5472c4c51f1ee54c428f30e7e0a96216fcb87ed', 'test@test.com', '0', null, '0', null);

-- ----------------------------
-- Table structure for `works`
-- ----------------------------
DROP TABLE IF EXISTS `works`;
CREATE TABLE `works` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of works
-- ----------------------------
INSERT INTO `works` VALUES ('3', '测试主管');
INSERT INTO `works` VALUES ('1', '测试工程师');
INSERT INTO `works` VALUES ('4', '测试经理');
INSERT INTO `works` VALUES ('2', '自动化测试工程师');

-- ----------------------------
-- Table structure for `yilai`
-- ----------------------------
DROP TABLE IF EXISTS `yilai`;
CREATE TABLE `yilai` (
  `case_id` int(11) DEFAULT NULL,
  `cases_id` int(11) DEFAULT NULL,
  `attred` varchar(32) DEFAULT NULL,
  KEY `case_id` (`case_id`),
  KEY `cases_id` (`cases_id`),
  CONSTRAINT `yilai_ibfk_1` FOREIGN KEY (`case_id`) REFERENCES `interfacetests` (`id`),
  CONSTRAINT `yilai_ibfk_2` FOREIGN KEY (`cases_id`) REFERENCES `interfacetests` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of yilai
-- ----------------------------
