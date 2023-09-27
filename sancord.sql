SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";
CREATE DATABASE IF NOT EXISTS `SanCord` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `SanCord`;

CREATE TABLE `guilds` (
  `serial` int(24) NOT NULL,
  `guild_id` bigint(64) DEFAULT NULL,
  `guild_name` varchar(48) DEFAULT NULL,
  `status_channel` bigint(64) DEFAULT NULL,
  `joining_date` datetime DEFAULT NULL,
  `ip` varchar(48) DEFAULT NULL,
  `port` int(24) DEFAULT NULL,
  `set_ip` int(1) DEFAULT 0,
  `status` int(1) DEFAULT 0,
  `sg_channel` bigint(64) DEFAULT NULL,
  `sg_logC` bigint(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `suggestions`(
  `sid` int(24) DEFAULT 0,
  `key` int(128) DEFAULT NULL,
  `guild_id` bigint(64) DEFAULT NULL,
  `author` bigint(64) DEFAULT NULL,
  `title` varchar(256) DEFAULT NULL,
  `suggestion` varchar(2048) DEFAULT NULL,
  `s_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Indexes for table `guilds`
--

ALTER TABLE `guilds`
  ADD PRIMARY KEY (`serial`);
--
-- AUTO_INCREMENT for table `guilds`
--
ALTER TABLE `guilds`
  MODIFY `serial` int(24) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- Indexes for table `guilds`
--

ALTER TABLE `suggestions`
  ADD PRIMARY KEY(`sid`);

--
-- AUTO_INCREMENT for table `guilds`
--

ALTER TABLE `suggestions`
  MODIFY `sid` int(24) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;
