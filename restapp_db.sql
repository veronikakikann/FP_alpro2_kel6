-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 24, 2025 at 02:29 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restapp_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `daily_logs`
--

CREATE TABLE `daily_logs` (
  `log_id` varchar(29) NOT NULL,
  `username` varchar(20) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  `sleep_duration` decimal(4,2) NOT NULL,
  `sleep_quality` tinyint(4) NOT NULL CHECK (`sleep_quality` between 1 and 10),
  `systolic_bp` smallint(6) NOT NULL,
  `diastolic_bp` smallint(6) NOT NULL,
  `heart_rate` smallint(6) NOT NULL,
  `daily_steps` smallint(6) NOT NULL,
  `sleep_disorder` enum('Apnea','Insomnia','None') NOT NULL,
  `stress_level` enum('Low','Medium','High') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `daily_logs`
--

INSERT INTO `daily_logs` (`log_id`, `username`, `timestamp`, `sleep_duration`, `sleep_quality`, `systolic_bp`, `diastolic_bp`, `heart_rate`, `daily_steps`, `sleep_disorder`, `stress_level`) VALUES
('a_20251124', 'a', '2025-11-24 20:14:10', 6.00, 7, 115, 80, 70, 3000, 'None', 'Low'),
('player1_20251021070000', 'player1', '2025-10-21 07:00:00', 5.50, 4, 134, 88, 85, 4200, 'Insomnia', 'High'),
('player1_20251022070000', 'player1', '2025-10-22 07:00:00', 7.40, 8, 118, 77, 72, 8400, 'None', 'Low'),
('player1_20251023070000', 'player1', '2025-10-23 07:00:00', 6.90, 7, 121, 78, 74, 7100, 'None', 'Medium'),
('player1_20251024070000', 'player1', '2025-10-24 07:00:00', 5.70, 5, 131, 86, 83, 4500, 'Insomnia', 'High'),
('player1_20251025070000', 'player1', '2025-10-25 07:00:00', 8.30, 9, 113, 74, 66, 10800, 'None', 'Low'),
('player1_20251026070000', 'player1', '2025-10-26 07:00:00', 8.60, 9, 112, 73, 64, 11800, 'None', 'Low'),
('player1_20251027070000', 'player1', '2025-10-27 07:00:00', 7.80, 8, 116, 76, 69, 9500, 'None', 'Low'),
('player1_20251028070000', 'player1', '2025-10-28 07:00:00', 6.60, 7, 123, 79, 75, 6200, 'None', 'Medium'),
('player1_20251029070000', 'player1', '2025-10-29 07:00:00', 5.00, 3, 136, 89, 87, 3500, 'Apnea', 'High'),
('player1_20251030070000', 'player1', '2025-10-30 07:00:00', 7.30, 8, 117, 77, 71, 8800, 'None', 'Low'),
('player1_20251031070000', 'player1', '2025-10-31 07:00:00', 6.10, 6, 126, 83, 79, 5400, 'None', 'Medium'),
('player1_20251101070000', 'player1', '2025-11-01 07:00:00', 8.40, 9, 113, 72, 65, 11200, 'None', 'Low'),
('player1_20251102070000', 'player1', '2025-11-02 07:00:00', 8.10, 9, 114, 73, 66, 9800, 'None', 'Low'),
('player1_20251103070000', 'player1', '2025-11-03 07:00:00', 5.20, 4, 132, 87, 86, 3900, 'Insomnia', 'High'),
('player1_20251104070000', 'player1', '2025-11-04 07:00:00', 7.00, 7, 121, 79, 73, 7500, 'None', 'Low'),
('player1_20251105070000', 'player1', '2025-11-05 07:00:00', 7.50, 8, 119, 77, 71, 8200, 'None', 'Low'),
('player1_20251106070000', 'player1', '2025-11-06 07:00:00', 6.50, 6, 124, 80, 76, 6000, 'None', 'Medium'),
('player1_20251107070000', 'player1', '2025-11-07 07:00:00', 5.80, 5, 130, 85, 82, 4800, 'Insomnia', 'High'),
('player1_20251108070000', 'player1', '2025-11-08 07:00:00', 8.80, 9, 111, 72, 64, 10500, 'None', 'Low'),
('player1_20251109070000', 'player1', '2025-11-09 07:00:00', 9.00, 10, 110, 70, 62, 11000, 'None', 'Low'),
('player1_20251110070000', 'player1', '2025-11-10 07:00:00', 7.20, 8, 118, 76, 70, 9100, 'None', 'Low'),
('player1_20251111070000', 'player1', '2025-11-11 07:00:00', 6.00, 5, 128, 84, 80, 5500, 'None', 'Medium'),
('player1_20251112070000', 'player1', '2025-11-12 07:00:00', 4.50, 3, 138, 90, 88, 3200, 'Apnea', 'High'),
('player1_20251113070000', 'player1', '2025-11-13 07:00:00', 7.00, 7, 120, 78, 74, 7800, 'None', 'Low'),
('player1_20251114070000', 'player1', '2025-11-14 07:00:00', 6.80, 6, 122, 80, 75, 6700, 'None', 'Medium'),
('player1_20251115070000', 'player1', '2025-11-15 07:00:00', 8.50, 9, 112, 74, 65, 12500, 'None', 'Low'),
('player1_20251116070000', 'player1', '2025-11-16 07:00:00', 8.20, 9, 115, 75, 68, 10200, 'None', 'Low'),
('player1_20251117070000', 'player1', '2025-11-17 07:00:00', 5.50, 4, 135, 88, 85, 4100, 'Insomnia', 'High'),
('player1_20251118070000', 'player1', '2025-11-18 07:00:00', 6.20, 5, 125, 82, 78, 5200, 'None', 'Medium'),
('player1_20251119070000', 'player1', '2025-11-19 07:00:00', 7.50, 8, 118, 78, 72, 8500, 'None', 'Low'),
('player1_20251119120258', 'player1', '2025-11-19 12:02:58', 4.00, 3, 110, 80, 70, 4000, 'None', 'Medium'),
('player1_20251119120355', 'player1', '2025-11-19 12:03:55', 8.00, 10, 80, 50, 80, 10000, 'None', 'Low'),
('player1_20251119135157', 'player1', '2025-11-19 13:51:57', 6.00, 7, 110, 90, 77, 7000, 'Apnea', 'Medium'),
('player1_20251119135719', 'player1', '2025-11-19 13:57:19', 8.00, 7, 110, 90, 80, 6000, 'None', 'Low'),
('player1_20251119140155', 'player1', '2025-11-19 14:01:55', 8.00, 4, 100, 90, 80, 4000, 'None', 'Medium'),
('player1_20251119140225', 'player1', '2025-11-19 14:02:25', 9.00, 4, 100, 70, 80, 12000, 'Insomnia', 'Medium'),
('player_20251021', 'player', '2025-10-21 00:00:00', 7.75, 10, 116, 70, 68, 9435, 'None', 'Low'),
('player_20251022', 'player', '2025-10-22 00:00:00', 8.18, 8, 117, 70, 62, 10207, 'None', 'Low'),
('player_20251023', 'player', '2025-10-23 00:00:00', 6.06, 7, 126, 85, 80, 7197, 'None', 'Medium'),
('player_20251024', 'player', '2025-10-24 00:00:00', 6.05, 7, 128, 81, 80, 7359, 'None', 'Medium'),
('player_20251025', 'player', '2025-10-25 00:00:00', 7.07, 6, 124, 85, 77, 5000, 'None', 'Medium'),
('player_20251026', 'player', '2025-10-26 00:00:00', 8.82, 8, 116, 80, 60, 8721, 'None', 'Low'),
('player_20251027', 'player', '2025-10-27 00:00:00', 7.00, 5, 122, 82, 85, 7236, 'None', 'Medium'),
('player_20251028', 'player', '2025-10-28 00:00:00', 5.17, 4, 144, 91, 86, 2610, 'Insomnia', 'High'),
('player_20251029', 'player', '2025-10-29 00:00:00', 4.05, 3, 142, 92, 97, 4720, 'Apnea', 'High'),
('player_20251030', 'player', '2025-10-30 00:00:00', 7.69, 8, 118, 72, 67, 10975, 'None', 'Low'),
('player_20251031', 'player', '2025-10-31 00:00:00', 8.31, 9, 112, 75, 63, 9016, 'None', 'Low'),
('player_20251101', 'player', '2025-11-01 00:00:00', 7.34, 6, 124, 83, 79, 5015, 'None', 'Medium'),
('player_20251102', 'player', '2025-11-02 00:00:00', 8.66, 9, 115, 75, 63, 11356, 'None', 'Low'),
('player_20251103', 'player', '2025-11-03 00:00:00', 8.65, 9, 114, 72, 73, 11017, 'None', 'Low'),
('player_20251104', 'player', '2025-11-04 00:00:00', 7.16, 5, 121, 82, 82, 7831, 'None', 'Medium'),
('player_20251105', 'player', '2025-11-05 00:00:00', 7.97, 9, 114, 77, 73, 9733, 'None', 'Low'),
('player_20251106', 'player', '2025-11-06 00:00:00', 8.88, 10, 118, 74, 63, 11978, 'None', 'Low'),
('player_20251107', 'player', '2025-11-07 00:00:00', 8.48, 10, 115, 70, 68, 10963, 'None', 'Low'),
('player_20251108', 'player', '2025-11-08 00:00:00', 6.16, 7, 127, 82, 77, 5602, 'None', 'Medium'),
('player_20251109', 'player', '2025-11-09 00:00:00', 7.74, 10, 118, 71, 64, 11296, 'None', 'Low'),
('player_20251110', 'player', '2025-11-10 00:00:00', 5.13, 5, 135, 95, 92, 2368, 'Insomnia', 'High'),
('player_20251111', 'player', '2025-11-11 00:00:00', 7.64, 9, 119, 74, 67, 11325, 'None', 'Low'),
('player_20251112', 'player', '2025-11-12 00:00:00', 7.03, 7, 127, 85, 81, 6136, 'None', 'Medium'),
('player_20251113', 'player', '2025-11-13 00:00:00', 4.64, 3, 142, 87, 87, 4754, 'Insomnia', 'High'),
('player_20251114', 'player', '2025-11-14 00:00:00', 6.13, 5, 123, 81, 76, 7409, 'None', 'Medium'),
('player_20251115', 'player', '2025-11-15 00:00:00', 8.09, 10, 113, 71, 72, 9287, 'None', 'Low'),
('player_20251116', 'player', '2025-11-16 00:00:00', 6.75, 7, 126, 85, 83, 7561, 'None', 'Medium'),
('player_20251117', 'player', '2025-11-17 00:00:00', 8.95, 9, 116, 77, 74, 11661, 'None', 'Low'),
('player_20251118', 'player', '2025-11-18 00:00:00', 6.82, 6, 129, 85, 77, 7151, 'None', 'Medium'),
('player_20251119', 'player', '2025-11-19 00:00:00', 7.31, 7, 129, 81, 77, 6987, 'None', 'Medium'),
('player_20251120', 'player', '2025-11-20 21:26:12', 6.00, 1, 110, 85, 85, 3000, 'Insomnia', 'High'),
('player_20251121', 'player', '2025-11-21 00:26:49', 6.00, 7, 115, 80, 70, 3000, 'Insomnia', 'Medium'),
('player_20251124', 'player', '2025-11-24 19:55:57', 10.00, 6, 110, 85, 75, 1000, 'None', 'Low'),
('ulartangga_20251120205341', 'ulartangga', '2025-11-20 20:53:41', 8.00, 6, 100, 70, 70, 2000, 'None', 'Low');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(20) NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `gender` enum('M','F') NOT NULL,
  `birthdate` datetime NOT NULL,
  `occupation` varchar(50) NOT NULL,
  `bmi_category` enum('Normal','Overweight','Obese') NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `profile_picture`, `first_name`, `last_name`, `gender`, `birthdate`, `occupation`, `bmi_category`, `password_hash`, `created_at`) VALUES
('a', NULL, 'Raja', 'Mamamia', 'F', '2005-02-02 00:00:00', 'Housewife', 'Overweight', '$2b$12$rdN1Qg5EWL7e7iYTKtBXLOTqG8GvInrA4nOqt9xt8Q1mkbmYK7na6', '2025-11-24 13:05:46'),
('gagahberani', NULL, 'Raja', 'Lautan', 'M', '2002-05-22 00:00:00', 'Student', 'Normal', '$2b$12$vr.dt1o/ircEgRhYgZ8raON2rs4tWRC13tisHcsOyl6RlQRrGZpta', '2025-11-20 13:41:47'),
('mamamia', NULL, 'Mama', 'Mamamia', 'F', '2000-11-06 00:00:00', 'Housewife', 'Overweight', '$2b$12$pLOhnZ6LcyCRLsgzd/264OUbBWUMjWR4fVFwHWl6UyW0fDrHOIK2e', '2025-11-20 15:43:51'),
('player', NULL, 'Ilmiawan', 'Taufan Al Faris', 'M', '2010-10-10 00:00:00', 'Student', 'Normal', '$2b$12$Dxw7PQuHg9XDwzK6q9ZtgeTxV357Q9QsOw88P5LO59D3rPh2oMzYK', '2025-11-20 14:02:12'),
('player1', NULL, 'Ilmiawan', 'Taufan Al Faris', 'M', '2002-11-11 00:00:00', 'Student', 'Normal', 'scrypt:32768:8:1$2mH9BRABVkOET5MP$f990a741869a357896f2090ed7a84780ea31973be9e88fe4a061b39fd57b1ec0de1801edfa6e6b65cfe285cfe113e5f2627587066d48f03cbc7ea12f9f150e13', '2025-11-19 05:01:17'),
('ulartangga', NULL, 'Bahlil', 'Banget', 'M', '1999-06-05 00:00:00', 'Student', 'Overweight', '$2b$12$1CZWjdUbd9jH1fv863cmSOLbyTllkRi4yyZtk.xW95utxtkCXJMau', '2025-11-20 13:51:04');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `daily_logs`
--
ALTER TABLE `daily_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `idx_username` (`username`),
  ADD KEY `idx_timestamp` (`timestamp`),
  ADD KEY `idx_username_timestamp` (`username`,`timestamp`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `daily_logs`
--
ALTER TABLE `daily_logs`
  ADD CONSTRAINT `daily_logs_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
