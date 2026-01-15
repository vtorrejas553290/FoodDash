-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 15, 2026 at 12:20 PM
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
-- Database: `food_dash_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `staff_name` varchar(100) NOT NULL,
  `staff_id` varchar(20) NOT NULL,
  `action` varchar(255) NOT NULL,
  `details` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `staff_name`, `staff_id`, `action`, `details`, `created_at`) VALUES
(1, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 15:32:59'),
(2, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 15:34:47'),
(3, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 16:33:37'),
(4, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-06 16:34:05'),
(5, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 16:34:24'),
(6, 'System Admin', 'ADM00001', 'Added menu item', 'Classic Burger (₱159) - Burgers', '2026-01-06 16:36:00'),
(7, 'System Admin', 'ADM00001', 'Added menu item', 'Crispy Fries (₱79) - Sides', '2026-01-06 16:36:36'),
(8, 'System Admin', 'ADM00001', 'Added menu item', 'Fried Chicken (₱189) - Chicken', '2026-01-06 16:37:06'),
(9, 'System Admin', 'ADM00001', 'Added menu item', 'Milk Tea (₱99) - Drinks', '2026-01-06 16:37:35'),
(10, 'System Admin', 'ADM00001', 'Added menu item', 'Pepperoni Pizza (₱275) - Pizza', '2026-01-06 16:38:02'),
(11, 'System Admin', 'ADM00001', 'Updated customer', 'John Doe → John Does', '2026-01-06 16:38:11'),
(12, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-06 16:38:15'),
(13, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 16:40:07'),
(14, 'System Admin', 'ADM00001', 'Added new staff', 'c (c@.com)', '2026-01-06 16:41:13'),
(15, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-06 16:41:16'),
(16, 'c', 'EMP00002', 'Staff logged in', '', '2026-01-06 16:41:28'),
(17, 'c', 'EMP00002', 'Staff logged out', '', '2026-01-06 16:41:36'),
(18, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 16:43:10'),
(19, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-20260106233146-5: Completed', '2026-01-06 16:43:27'),
(20, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-20260106233122-3: Completed', '2026-01-06 16:43:29'),
(21, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-06 16:52:37'),
(22, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 17:43:36'),
(23, 'System Admin', 'ADM00001', 'Exported overview to PDF', 'File saved as: Admin_Dashboard_Overview_20260107_014341.pdf', '2026-01-06 17:43:44'),
(24, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 17:56:03'),
(25, 'System Admin', 'ADM00001', 'Exported overview to PDF', 'File saved as: Admin_Dashboard_Overview_20260107_015610.pdf', '2026-01-06 17:56:11'),
(26, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-06 18:03:35'),
(27, 'System Admin', 'ADM00001', 'Exported overview to PDF', 'File saved as: Admin_Dashboard_Overview_20260107_020337.pdf', '2026-01-06 18:03:38'),
(28, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-07 08:06:46'),
(29, 'System Admin', 'ADM00001', 'Updated menu item', 'Pepperoni Pizzas: Name: Pepperoni Pizza → Pepperoni Pizzas', '2026-01-07 08:07:39'),
(30, 'System Admin', 'ADM00001', 'Updated menu item', 'Pepperoni Pizza: Name: Pepperoni Pizzas → Pepperoni Pizza', '2026-01-07 08:07:45'),
(31, 'System Admin', 'ADM00001', 'Updated customer', 'John Does → John Doe', '2026-01-07 08:07:51'),
(32, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-07 08:08:43'),
(33, 'c', 'EMP00002', 'Staff logged in', '', '2026-01-07 08:08:51'),
(34, 'c', 'EMP00002', 'Staff logged out', '', '2026-01-07 08:08:58'),
(35, 'c', 'EMP00002', 'Staff logged in', '', '2026-01-12 04:37:55'),
(36, 'c', 'EMP00002', 'Updated order status', 'Order #ORD-20260112123700-9: Preparing', '2026-01-12 04:38:09'),
(37, 'c', 'EMP00002', 'Staff logged out', '', '2026-01-12 04:38:14'),
(38, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-12 04:38:33'),
(39, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-20260112123700-9: Completed', '2026-01-12 04:38:52'),
(40, 'System Admin', 'ADM00001', 'Exported overview to PDF', 'File saved as: Admin_Dashboard_Overview_20260112_124220.pdf', '2026-01-12 04:42:23'),
(41, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-11-20251110: Completed', '2026-01-12 04:44:36'),
(42, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-12-20251220: Completed', '2026-01-12 04:44:42'),
(43, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-12-20251215: Completed', '2026-01-12 04:44:45'),
(44, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-12 04:45:48'),
(45, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-12 04:47:07'),
(46, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-12 16:00:08'),
(47, 'System Admin', 'ADM00001', 'Updated customer', 'John Doe → John Doeaw', '2026-01-12 16:00:47'),
(48, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-12 16:01:21'),
(49, 'c', 'EMP00002', 'Staff logged in', '', '2026-01-12 16:02:08'),
(50, 'c', 'EMP00002', 'Updated order status', 'Order #ORD-20260113000151-3: Completed', '2026-01-12 16:02:12'),
(51, 'c', 'EMP00002', 'Staff logged out', '', '2026-01-12 16:02:16'),
(52, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-12 16:02:38'),
(53, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-14 15:22:07'),
(54, 'System Admin', 'ADM00001', 'Updated menu item', 'Pepperoni Pizza: Category: Pizza → Drinks', '2026-01-14 15:49:48'),
(55, 'System Admin', 'ADM00001', 'Updated menu item', 'Pepperoni Pizza: Category: Drinks → Pizza', '2026-01-14 15:49:57'),
(56, 'System Admin', 'ADM00001', 'Added new staff', 'Haris Usman (h@.com)', '2026-01-14 15:51:07'),
(57, 'System Admin', 'ADM00001', 'Updated staff', 'c → Clarence Mongas', '2026-01-14 15:51:21'),
(58, 'System Admin', 'ADM00001', 'Added menu item', 'aaddadad ada (₱03) - Burgers', '2026-01-14 15:52:03'),
(59, 'System Admin', 'ADM00001', 'Deleted menu item', 'aaddadad ada', '2026-01-14 15:52:07'),
(60, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-14 15:52:22'),
(61, 'Haris Usman', 'EMP00003', 'Staff logged in', '', '2026-01-14 15:54:13'),
(62, 'Haris Usman', 'EMP00003', 'Updated order status', 'Order #ORD-20260114235352-5: Completed', '2026-01-14 15:54:17'),
(63, 'Haris Usman', 'EMP00003', 'Staff logged out', '', '2026-01-14 15:54:20'),
(64, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-14 15:54:33'),
(65, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-12-20251225: Completed', '2026-01-14 15:54:58'),
(66, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-12-20251210: Completed', '2026-01-14 15:55:03'),
(67, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-12-20251205: Completed', '2026-01-14 15:55:05'),
(68, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-11-20251125: Completed', '2026-01-14 15:55:07'),
(69, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-11-20251115: Completed', '2026-01-14 15:55:10'),
(70, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-10-20251020: Completed', '2026-01-14 15:55:14'),
(71, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-10-20251005: Completed', '2026-01-14 15:55:17'),
(72, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-09-20250925: Completed', '2026-01-14 15:55:22'),
(73, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-09-20250920: Completed', '2026-01-14 15:55:24'),
(74, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-09-20250915: Completed', '2026-01-14 15:55:26'),
(75, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-09-20250905: Completed', '2026-01-14 15:55:28'),
(76, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-08-20250825: Completed', '2026-01-14 15:55:30'),
(77, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-08-20250815: Completed', '2026-01-14 15:55:33'),
(78, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-08-20250810: Completed', '2026-01-14 15:55:36'),
(79, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-08-20250805: Completed', '2026-01-14 15:55:38'),
(80, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-07-20250725: Completed', '2026-01-14 15:55:40'),
(81, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-07-20250705: Completed', '2026-01-14 15:55:44'),
(82, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-06-20250625: Completed', '2026-01-14 15:55:46'),
(83, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-06-20250620: Completed', '2026-01-14 15:55:49'),
(84, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-05-20250520: Completed', '2026-01-14 15:55:52'),
(85, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-04-20250420: Completed', '2026-01-14 15:55:56'),
(86, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-04-20250415: Completed', '2026-01-14 15:55:59'),
(87, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-03-20250320: Completed', '2026-01-14 15:56:02'),
(88, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-03-20250305: Completed', '2026-01-14 15:56:05'),
(89, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-02-20250225: Completed', '2026-01-14 15:56:07'),
(90, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-02-20250220: Completed', '2026-01-14 15:56:09'),
(91, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-02-20250210: Completed', '2026-01-14 15:56:11'),
(92, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-01-20250115: Completed', '2026-01-14 15:56:15'),
(93, 'System Admin', 'ADM00001', 'Updated order status', 'Order #ORD-2025-01-20250105: Completed', '2026-01-14 15:56:18'),
(94, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-14 15:59:35'),
(95, 'Clarence Mongas', 'EMP00002', 'Staff logged in', '', '2026-01-15 09:06:51'),
(96, 'Clarence Mongas', 'EMP00002', 'Staff logged out', '', '2026-01-15 09:07:03'),
(97, 'Clarence Mongas', 'EMP00002', 'Staff logged in', '', '2026-01-15 09:07:49'),
(98, 'Clarence Mongas', 'EMP00002', 'Updated order status', 'Order #ORD-20260115170723-7: Preparing', '2026-01-15 09:07:57'),
(99, 'Clarence Mongas', 'EMP00002', 'Updated order status', 'Order #ORD-20260115170723-7: Delivering', '2026-01-15 09:08:01'),
(100, 'Clarence Mongas', 'EMP00002', 'Staff logged out', '', '2026-01-15 09:08:15'),
(101, 'System Admin', 'ADM00001', 'Admin logged in', '', '2026-01-15 09:08:34'),
(102, 'System Admin', 'ADM00001', 'Admin logged out', '', '2026-01-15 09:09:37');

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `admin_id` varchar(10) DEFAULT NULL,
  `admin_name` varchar(100) NOT NULL,
  `admin_email` varchar(100) NOT NULL,
  `admin_phone` varchar(20) NOT NULL,
  `admin_address` text NOT NULL,
  `admin_password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `admin_id`, `admin_name`, `admin_email`, `admin_phone`, `admin_address`, `admin_password`, `created_at`, `updated_at`) VALUES
(1, 'ADM00001', 'System Admin', 'admin@fooddash.com', '1234567890', 'Main Office, Food Dash HQ', 'da23de9275cc7411bae1d33ca88ea5045a1cc9b36d577f3b886bc5eb3fb618e0', '2026-01-06 15:29:07', '2026-01-06 15:29:07');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` text NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `full_name`, `email`, `phone`, `address`, `password`, `created_at`, `updated_at`) VALUES
(1, 'John Doeaw', 'customer@email.com', '09171234567', '123 Sample Street, Manila', 'cdb310effa527556369ee3ed41d4ac094e95c2523d1a0e73d7d1d49fac2eeca0', '2026-01-06 15:29:07', '2026-01-12 16:00:47'),
(2, 'Vincent', 'v@.com', '09999991282', 'sand', '6b58bf58e7940c4fb2071628e140d65d509fea6c8b4915f68f461c07dae7a536', '2026-01-06 15:30:54', '2026-01-15 09:06:37'),
(3, 'Luna Santos', 'luna.santos2025@email.com', '09171232025', '25 Moon Street, Manila 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(4, 'Kai Rodriguez', 'kai.rod2025@email.com', '09282342025', '45 Ocean Avenue, Quezon City 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(5, 'Zara Chen', 'zara.chen2025@email.com', '09393452025', '65 Mountain Road, Makati 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(6, 'Leo Martinez', 'leo.martinez2025@email.com', '09404562025', '85 Star Lane, Taguig 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(7, 'Maya Kumar', 'maya.kumar2025@email.com', '09515672025', '105 Sun Drive, Pasig 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(9, 'Nova Tan', 'nova.tan2025@email.com', '09737892025', '145 Galaxy Street, Paranaque 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(10, 'Rio Lee', 'rio.lee2025@email.com', '09848902025', '165 River Avenue, Las Pinas 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(11, 'Skye Park', 'skye.park2025@email.com', '09959012025', '185 Sky Road, Muntinlupa 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19'),
(12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', 'a71e4fa7ec25fa364af74da64eedab14e6ebb7218ef70202e6929fbbe1e50d45', '2026-01-12 04:39:19', '2026-01-12 04:39:19');

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`id`, `name`, `description`, `price`, `category`, `image_url`, `created_at`) VALUES
(11, 'Classic Burger', 'Juicy beef patty with fresh veggies', 159.00, 'Burgers', 'picture/burger.png', '2026-01-06 16:36:00'),
(12, 'Crispy Fries', 'Golden crispy potato fries', 79.00, 'Sides', 'picture/fries.png', '2026-01-06 16:36:36'),
(13, 'Fried Chicken', 'Crispy fried chicken pieces', 189.00, 'Chicken', 'picture/chicken.png', '2026-01-06 16:37:06'),
(14, 'Milk Tea', 'Classic milk tea with pearls', 99.00, 'Drinks', 'picture/milktea.png', '2026-01-06 16:37:35'),
(15, 'Pepperoni Pizza', 'Loaded with pepperoni slices', 275.00, 'Pizza', 'picture/pizza.png', '2026-01-06 16:38:02');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `order_number` varchar(20) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `customer_name` varchar(100) NOT NULL,
  `customer_email` varchar(100) NOT NULL,
  `customer_phone` varchar(20) NOT NULL,
  `customer_address` text NOT NULL,
  `items` text NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `delivery_fee` decimal(10,2) DEFAULT 50.00,
  `total_amount` decimal(10,2) NOT NULL,
  `status` varchar(50) DEFAULT 'pending',
  `payment_method` varchar(50) DEFAULT 'Cash on Delivery',
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `order_number`, `customer_id`, `customer_name`, `customer_email`, `customer_phone`, `customer_address`, `items`, `subtotal`, `delivery_fee`, `total_amount`, `status`, `payment_method`, `notes`, `created_at`, `updated_at`) VALUES
(1, 'ORD-20260106233122-3', 2, 'v', 'v@.com', '09999991282', 'sand', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"img\": \"picture/burger.png\", \"qty\": 2}]', 318.00, 50.00, 368.00, 'Completed', 'Cash on Delivery', '', '2026-01-06 15:31:22', '2026-01-06 16:43:29'),
(2, 'ORD-20260106233146-5', 2, 'v', 'v@.com', '09999991282', 'sand', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"img\": \"picture/burger.png\", \"qty\": 3}]', 477.00, 50.00, 527.00, 'Completed', 'Cash on Delivery', '', '2026-01-06 15:31:46', '2026-01-06 16:43:27'),
(3, 'ORD-20260112123700-9', 2, 'Vincent', 'v@.com', '09999991282', 'sand', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275.00\", \"img\": \"picture/pizza.png\", \"qty\": 1}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159.00\", \"img\": \"picture/burger.png\", \"qty\": 1}]', 434.00, 50.00, 484.00, 'Completed', 'Cash on Delivery', '', '2026-01-12 04:37:00', '2026-01-12 04:38:52'),
(4, 'ORD-2025-01-20250105', 6, 'Leo Martinez', 'leo.martinez2025@email.com', '09404562025', '85 Star Lane, Taguig 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 3}]', 1689.00, 50.00, 1739.00, 'Completed', 'Cash on Delivery', '2025 fresh start order', '2025-01-05 05:01:00', '2026-01-14 15:56:18'),
(5, 'ORD-2025-01-20250110', 5, 'Zara Chen', 'zara.chen2025@email.com', '09393452025', '65 Mountain Road, Makati 2025', '[{\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 1}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}]', 1294.00, 50.00, 1344.00, 'completed', 'Cash on Delivery', 'January resolution meal 2025', '2025-01-10 03:32:00', '2026-01-12 04:39:19'),
(6, 'ORD-2025-01-20250115', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}]', 773.00, 50.00, 823.00, 'Completed', 'Cash on Delivery', '2025 fresh start order', '2025-01-15 03:20:00', '2026-01-14 15:56:15'),
(7, 'ORD-2025-01-20250120', 11, 'Skye Park', 'skye.park2025@email.com', '09959012025', '185 Sky Road, Muntinlupa 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}]', 910.00, 50.00, 960.00, 'completed', 'Cash on Delivery', '2025 fresh start order', '2025-01-20 08:27:00', '2026-01-12 04:39:19'),
(8, 'ORD-2025-01-20250125', 4, 'Kai Rodriguez', 'kai.rod2025@email.com', '09282342025', '45 Ocean Avenue, Quezon City 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}]', 1749.00, 50.00, 1799.00, 'completed', 'Cash on Delivery', 'Happy New Year 2025!', '2025-01-25 08:38:00', '2026-01-12 04:39:19'),
(9, 'ORD-2025-02-20250205', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}]', 1122.00, 50.00, 1172.00, 'completed', 'Cash on Delivery', 'February hearts 2025', '2025-02-05 06:10:00', '2026-01-12 04:39:19'),
(10, 'ORD-2025-02-20250210', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}]', 576.00, 50.00, 626.00, 'Completed', 'Cash on Delivery', 'Love month 2025 celebration', '2025-02-10 10:15:00', '2026-01-14 15:56:11'),
(11, 'ORD-2025-02-20250215', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}]', 1578.00, 50.00, 1628.00, 'completed', 'Cash on Delivery', 'February hearts 2025', '2025-02-15 06:27:00', '2026-01-12 04:39:19'),
(12, 'ORD-2025-02-20250220', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}]', 277.00, 50.00, 327.00, 'Completed', 'Cash on Delivery', 'February hearts 2025', '2025-02-20 09:04:00', '2026-01-14 15:56:09'),
(13, 'ORD-2025-02-20250225', 3, 'Luna Santos', 'luna.santos2025@email.com', '09171232025', '25 Moon Street, Manila 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}]', 615.00, 50.00, 665.00, 'Completed', 'Cash on Delivery', 'February hearts 2025', '2025-02-25 02:57:00', '2026-01-14 15:56:07'),
(14, 'ORD-2025-03-20250305', 4, 'Kai Rodriguez', 'kai.rod2025@email.com', '09282342025', '45 Ocean Avenue, Quezon City 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}]', 277.00, 50.00, 327.00, 'Completed', 'Cash on Delivery', 'March graduation 2025', '2025-03-05 06:27:00', '2026-01-14 15:56:05'),
(15, 'ORD-2025-03-20250310', 5, 'Zara Chen', 'zara.chen2025@email.com', '09393452025', '65 Mountain Road, Makati 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}]', 838.00, 50.00, 888.00, 'completed', 'Cash on Delivery', 'Summer prep 2025', '2025-03-10 12:02:00', '2026-01-12 04:39:19'),
(16, 'ORD-2025-03-20250315', 3, 'Luna Santos', 'luna.santos2025@email.com', '09171232025', '25 Moon Street, Manila 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}]', 555.00, 50.00, 605.00, 'completed', 'Cash on Delivery', 'Summer prep 2025', '2025-03-15 05:19:00', '2026-01-12 04:39:19'),
(17, 'ORD-2025-03-20250320', 11, 'Skye Park', 'skye.park2025@email.com', '09959012025', '185 Sky Road, Muntinlupa 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}]', 790.00, 50.00, 840.00, 'Completed', 'Cash on Delivery', 'March graduation 2025', '2025-03-20 04:40:00', '2026-01-14 15:56:02'),
(18, 'ORD-2025-03-20250325', 10, 'Rio Lee', 'rio.lee2025@email.com', '09848902025', '165 River Avenue, Las Pinas 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}]', 852.00, 50.00, 902.00, 'completed', 'Cash on Delivery', 'Spring begins 2025', '2025-03-25 05:02:00', '2026-01-12 04:39:19'),
(19, 'ORD-2025-04-20250405', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}]', 614.00, 50.00, 664.00, 'completed', 'Cash on Delivery', 'Easter celebration 2025', '2025-04-05 02:32:00', '2026-01-12 04:39:19'),
(20, 'ORD-2025-04-20250410', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}]', 696.00, 50.00, 746.00, 'completed', 'Cash on Delivery', 'Holy Week 2025', '2025-04-10 03:00:00', '2026-01-12 04:39:19'),
(21, 'ORD-2025-04-20250415', 11, 'Skye Park', 'skye.park2025@email.com', '09959012025', '185 Sky Road, Muntinlupa 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}]', 354.00, 50.00, 404.00, 'Completed', 'Cash on Delivery', 'April vacation 2025', '2025-04-15 12:17:00', '2026-01-14 15:55:59'),
(22, 'ORD-2025-04-20250420', 4, 'Kai Rodriguez', 'kai.rod2025@email.com', '09282342025', '45 Ocean Avenue, Quezon City 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}]', 709.00, 50.00, 759.00, 'Completed', 'Cash on Delivery', 'April vacation 2025', '2025-04-20 02:08:00', '2026-01-14 15:55:56'),
(23, 'ORD-2025-04-20250425', 10, 'Rio Lee', 'rio.lee2025@email.com', '09848902025', '165 River Avenue, Las Pinas 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 1}]', 1036.00, 50.00, 1086.00, 'completed', 'Cash on Delivery', 'Easter celebration 2025', '2025-04-25 06:26:00', '2026-01-12 04:39:19'),
(24, 'ORD-2025-05-20250505', 11, 'Skye Park', 'skye.park2025@email.com', '09959012025', '185 Sky Road, Muntinlupa 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}]', 1400.00, 50.00, 1450.00, 'completed', 'Cash on Delivery', 'Mother\'s Day 2025 treat', '2025-05-05 05:14:00', '2026-01-12 04:39:19'),
(25, 'ORD-2025-05-20250510', 5, 'Zara Chen', 'zara.chen2025@email.com', '09393452025', '65 Mountain Road, Makati 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 1}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}]', 977.00, 50.00, 1027.00, 'completed', 'Cash on Delivery', 'Flores de Mayo 2025', '2025-05-10 12:14:00', '2026-01-12 04:39:19'),
(26, 'ORD-2025-05-20250515', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}]', 989.00, 50.00, 1039.00, 'completed', 'Cash on Delivery', 'Mother\'s Day 2025 treat', '2025-05-15 04:40:00', '2026-01-12 04:39:19'),
(27, 'ORD-2025-05-20250520', 11, 'Skye Park', 'skye.park2025@email.com', '09959012025', '185 Sky Road, Muntinlupa 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}]', 631.00, 50.00, 681.00, 'Completed', 'Cash on Delivery', 'Flores de Mayo 2025', '2025-05-20 03:43:00', '2026-01-14 15:55:52'),
(28, 'ORD-2025-05-20250525', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 3}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}]', 1298.00, 50.00, 1348.00, 'completed', 'Cash on Delivery', 'May flowers festival 2025', '2025-05-25 12:14:00', '2026-01-12 04:39:19'),
(29, 'ORD-2025-06-20250605', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}]', 714.00, 50.00, 764.00, 'completed', 'Cash on Delivery', 'Mid-year review 2025', '2025-06-05 02:02:00', '2026-01-12 04:39:19'),
(30, 'ORD-2025-06-20250610', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}]', 1427.00, 50.00, 1477.00, 'completed', 'Cash on Delivery', 'Independence Day 2025', '2025-06-10 06:39:00', '2026-01-12 04:39:19'),
(31, 'ORD-2025-06-20250615', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}]', 556.00, 50.00, 606.00, 'completed', 'Cash on Delivery', 'Rainy season starts 2025', '2025-06-15 08:06:00', '2026-01-12 04:39:19'),
(32, 'ORD-2025-06-20250620', 5, 'Zara Chen', 'zara.chen2025@email.com', '09393452025', '65 Mountain Road, Makati 2025', '[{\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 1}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}]', 387.00, 50.00, 437.00, 'Completed', 'Cash on Delivery', 'Rainy season starts 2025', '2025-06-20 05:55:00', '2026-01-14 15:55:49'),
(33, 'ORD-2025-06-20250625', 5, 'Zara Chen', 'zara.chen2025@email.com', '09393452025', '65 Mountain Road, Makati 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}]', 1181.00, 50.00, 1231.00, 'Completed', 'Cash on Delivery', 'Mid-year review 2025', '2025-06-25 08:56:00', '2026-01-14 15:55:46'),
(34, 'ORD-2025-07-20250705', 5, 'Zara Chen', 'zara.chen2025@email.com', '09393452025', '65 Mountain Road, Makati 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}]', 649.00, 50.00, 699.00, 'Completed', 'Cash on Delivery', 'July monsoon season', '2025-07-05 05:25:00', '2026-01-14 15:55:44'),
(35, 'ORD-2025-07-20250710', 7, 'Maya Kumar', 'maya.kumar2025@email.com', '09515672025', '105 Sun Drive, Pasig 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}]', 257.00, 50.00, 307.00, 'completed', 'Cash on Delivery', 'Nutrition month 2025', '2025-07-10 12:02:00', '2026-01-12 04:39:19'),
(36, 'ORD-2025-07-20250715', 9, 'Nova Tan', 'nova.tan2025@email.com', '09737892025', '145 Galaxy Street, Paranaque 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 3}]', 1392.00, 50.00, 1442.00, 'completed', 'Cash on Delivery', 'July monsoon season', '2025-07-15 03:22:00', '2026-01-12 04:39:19'),
(37, 'ORD-2025-07-20250720', 10, 'Rio Lee', 'rio.lee2025@email.com', '09848902025', '165 River Avenue, Las Pinas 2025', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 1}]', 666.00, 50.00, 716.00, 'completed', 'Cash on Delivery', 'Nutrition month 2025', '2025-07-20 09:28:00', '2026-01-12 04:39:19'),
(38, 'ORD-2025-07-20250725', 9, 'Nova Tan', 'nova.tan2025@email.com', '09737892025', '145 Galaxy Street, Paranaque 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}]', 1132.00, 50.00, 1182.00, 'Completed', 'Cash on Delivery', 'Nutrition month 2025', '2025-07-25 04:39:00', '2026-01-14 15:55:40'),
(39, 'ORD-2025-08-20250805', 3, 'Luna Santos', 'luna.santos2025@email.com', '09171232025', '25 Moon Street, Manila 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}]', 1620.00, 50.00, 1670.00, 'Completed', 'Cash on Delivery', 'August typhoon preparation', '2025-08-05 08:06:00', '2026-01-14 15:55:38'),
(40, 'ORD-2025-08-20250810', 4, 'Kai Rodriguez', 'kai.rod2025@email.com', '09282342025', '45 Ocean Avenue, Quezon City 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}]', 1102.00, 50.00, 1152.00, 'Completed', 'Cash on Delivery', 'Buwan ng Wika 2025', '2025-08-10 09:34:00', '2026-01-14 15:55:36'),
(41, 'ORD-2025-08-20250815', 6, 'Leo Martinez', 'leo.martinez2025@email.com', '09404562025', '85 Star Lane, Taguig 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 2}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}]', 1340.00, 50.00, 1390.00, 'Completed', 'Cash on Delivery', 'August typhoon preparation', '2025-08-15 04:46:00', '2026-01-14 15:55:33'),
(42, 'ORD-2025-08-20250820', 3, 'Luna Santos', 'luna.santos2025@email.com', '09171232025', '25 Moon Street, Manila 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}]', 1003.00, 50.00, 1053.00, 'completed', 'Cash on Delivery', 'Back-to-school 2025', '2025-08-20 10:06:00', '2026-01-12 04:39:19'),
(43, 'ORD-2025-08-20250825', 9, 'Nova Tan', 'nova.tan2025@email.com', '09737892025', '145 Galaxy Street, Paranaque 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}]', 714.00, 50.00, 764.00, 'Completed', 'Cash on Delivery', 'Buwan ng Wika 2025', '2025-08-25 05:03:00', '2026-01-14 15:55:30'),
(44, 'ORD-2025-09-20250905', 10, 'Rio Lee', 'rio.lee2025@email.com', '09848902025', '165 River Avenue, Las Pinas 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}]', 1161.00, 50.00, 1211.00, 'Completed', 'Cash on Delivery', 'September chill 2025', '2025-09-05 03:53:00', '2026-01-14 15:55:28'),
(45, 'ORD-2025-09-20250910', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}]', 1165.00, 50.00, 1215.00, 'completed', 'Cash on Delivery', 'Ber months begin 2025!', '2025-09-10 12:38:00', '2026-01-12 04:39:19'),
(46, 'ORD-2025-09-20250915', 3, 'Luna Santos', 'luna.santos2025@email.com', '09171232025', '25 Moon Street, Manila 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}]', 788.00, 50.00, 838.00, 'Completed', 'Cash on Delivery', 'Christmas countdown 2025 starts', '2025-09-15 10:49:00', '2026-01-14 15:55:26'),
(47, 'ORD-2025-09-20250920', 4, 'Kai Rodriguez', 'kai.rod2025@email.com', '09282342025', '45 Ocean Avenue, Quezon City 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}]', 1518.00, 50.00, 1568.00, 'Completed', 'Cash on Delivery', 'Ber months begin 2025!', '2025-09-20 09:00:00', '2026-01-14 15:55:24'),
(48, 'ORD-2025-09-20250925', 6, 'Leo Martinez', 'leo.martinez2025@email.com', '09404562025', '85 Star Lane, Taguig 2025', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}]', 1302.00, 50.00, 1352.00, 'Completed', 'Cash on Delivery', 'Christmas countdown 2025 starts', '2025-09-25 09:20:00', '2026-01-14 15:55:22'),
(49, 'ORD-2025-10-20251005', 11, 'Skye Park', 'skye.park2025@email.com', '09959012025', '185 Sky Road, Muntinlupa 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}]', 1207.00, 50.00, 1257.00, 'Completed', 'Cash on Delivery', 'Spooky season 2025', '2025-10-05 02:27:00', '2026-01-14 15:55:17'),
(50, 'ORD-2025-10-20251010', 9, 'Nova Tan', 'nova.tan2025@email.com', '09737892025', '145 Galaxy Street, Paranaque 2025', '[{\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}]', 885.00, 50.00, 935.00, 'completed', 'Cash on Delivery', 'Pre-Christmas rush 2025', '2025-10-10 07:29:00', '2026-01-12 04:39:19'),
(51, 'ORD-2025-10-20251015', 10, 'Rio Lee', 'rio.lee2025@email.com', '09848902025', '165 River Avenue, Las Pinas 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 1}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}]', 623.00, 50.00, 673.00, 'completed', 'Cash on Delivery', 'Spooky season 2025', '2025-10-15 10:02:00', '2026-01-12 04:39:19'),
(52, 'ORD-2025-10-20251020', 4, 'Kai Rodriguez', 'kai.rod2025@email.com', '09282342025', '45 Ocean Avenue, Quezon City 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}]', 456.00, 50.00, 506.00, 'Completed', 'Cash on Delivery', 'Halloween 2025 party!', '2025-10-20 12:34:00', '2026-01-14 15:55:14'),
(53, 'ORD-2025-10-20251025', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}]', 1112.00, 50.00, 1162.00, 'completed', 'Cash on Delivery', 'Spooky season 2025', '2025-10-25 09:42:00', '2026-01-12 04:39:19'),
(54, 'ORD-2025-11-20251105', 8, 'Eli Wilson', 'eli.wilson2025@email.com', '09626782025', '125 Cloud Court, Mandaluyong 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}]', 1165.00, 50.00, 1215.00, 'completed', 'Cash on Delivery', 'November sale 2025', '2025-11-05 07:43:00', '2026-01-12 04:39:19'),
(55, 'ORD-2025-11-20251110', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 3}]', 726.00, 50.00, 776.00, 'Completed', 'Cash on Delivery', 'November sale 2025', '2025-11-10 02:06:00', '2026-01-12 04:44:36'),
(56, 'ORD-2025-11-20251115', 5, 'Zara Chen', 'zara.chen2025@email.com', '09393452025', '65 Mountain Road, Makati 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}]', 354.00, 50.00, 404.00, 'Completed', 'Cash on Delivery', 'Christmas shopping 2025', '2025-11-15 05:12:00', '2026-01-14 15:55:10'),
(57, 'ORD-2025-11-20251120', 11, 'Skye Park', 'skye.park2025@email.com', '09959012025', '185 Sky Road, Muntinlupa 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 2}]', 1129.00, 50.00, 1179.00, 'completed', 'Cash on Delivery', 'November sale 2025', '2025-11-20 09:01:00', '2026-01-12 04:39:19'),
(58, 'ORD-2025-11-20251125', 9, 'Nova Tan', 'nova.tan2025@email.com', '09737892025', '145 Galaxy Street, Paranaque 2025', '[{\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 2}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}]', 1108.00, 50.00, 1158.00, 'Completed', 'Cash on Delivery', 'November sale 2025', '2025-11-25 05:17:00', '2026-01-14 15:55:07'),
(59, 'ORD-2025-12-20251205', 9, 'Nova Tan', 'nova.tan2025@email.com', '09737892025', '145 Galaxy Street, Paranaque 2025', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 2}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 1}]', 1186.00, 50.00, 1236.00, 'Completed', 'Cash on Delivery', 'Noche Buena feast 2025', '2025-12-05 07:35:00', '2026-01-14 15:55:05'),
(60, 'ORD-2025-12-20251210', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 1}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 3}]', 1286.00, 50.00, 1336.00, 'Completed', 'Cash on Delivery', 'Year-end celebration 2025', '2025-12-10 06:11:00', '2026-01-14 15:55:03'),
(61, 'ORD-2025-12-20251215', 12, 'Orion Kim', 'orion.kim2025@email.com', '09160122025', '205 Constellation Lane, San Juan 2025', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199\", \"qty\": 3}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179\", \"qty\": 1}]', 376.00, 50.00, 426.00, 'Completed', 'Cash on Delivery', 'Noche Buena feast 2025', '2025-12-15 10:56:00', '2026-01-12 04:44:45'),
(62, 'ORD-2025-12-20251220', 9, 'Nova Tan', 'nova.tan2025@email.com', '09737892025', '145 Galaxy Street, Paranaque 2025', '[{\"title\": \"Pepperoni Pizza\", \"price\": \"\\u20b1275\", \"qty\": 3}, {\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}]', 1302.00, 50.00, 1352.00, 'Completed', 'Cash on Delivery', 'Noche Buena feast 2025', '2025-12-20 10:25:00', '2026-01-12 04:44:42'),
(63, 'ORD-2025-12-20251225', 6, 'Leo Martinez', 'leo.martinez2025@email.com', '09404562025', '85 Star Lane, Taguig 2025', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159\", \"qty\": 3}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189\", \"qty\": 1}]', 666.00, 50.00, 716.00, 'Completed', 'Cash on Delivery', 'Merry Christmas 2025!', '2025-12-25 12:56:00', '2026-01-14 15:54:58'),
(64, 'ORD-20260113000151-3', 2, 'Vincent', 'v@.com', '09999991282', 'sand', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159.00\", \"img\": \"picture/burger.png\", \"qty\": 2}, {\"title\": \"Crispy Fries\", \"price\": \"\\u20b179.00\", \"img\": \"picture/fries.png\", \"qty\": 2}, {\"title\": \"Milk Tea\", \"price\": \"\\u20b199.00\", \"img\": \"picture/milktea.png\", \"qty\": 1}, {\"title\": \"Fried Chicken\", \"price\": \"\\u20b1189.00\", \"img\": \"picture/chicken.png\", \"qty\": 1}]', 764.00, 50.00, 814.00, 'Completed', 'Cash on Delivery', '', '2026-01-12 16:01:51', '2026-01-12 16:02:12'),
(65, 'ORD-20260114235352-5', 2, 'Vincent', 'v@.com', '09999991282', 'sand', '[{\"title\": \"Classic Burger\", \"price\": \"\\u20b1159.00\", \"img\": \"picture/burger.png\", \"qty\": 1}]', 159.00, 50.00, 209.00, 'Completed', 'Cash on Delivery', '', '2026-01-14 15:53:52', '2026-01-14 15:54:17'),
(66, 'ORD-20260115170723-7', 2, 'Vincent', 'v@.com', '09999991282', 'sand', '[{\"title\": \"Milk Tea\", \"price\": \"\\u20b199.00\", \"img\": \"picture/milktea.png\", \"qty\": 1}]', 99.00, 50.00, 149.00, 'Delivering', 'Cash on Delivery', '', '2026-01-15 09:07:23', '2026-01-15 09:08:01');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `order_number` varchar(20) DEFAULT NULL,
  `menu_item_id` int(11) DEFAULT NULL,
  `menu_item_name` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `order_number`, `menu_item_id`, `menu_item_name`, `quantity`, `price`, `total_price`, `created_at`) VALUES
(1, 3, 'ORD-20260112123700-9', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2026-01-12 04:37:00'),
(2, 3, 'ORD-20260112123700-9', 11, 'Classic Burger', 1, 159.00, 159.00, '2026-01-12 04:37:00'),
(3, 4, 'ORD-2025-01-20250105', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-01-05 05:01:00'),
(4, 4, 'ORD-2025-01-20250105', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-01-05 05:01:00'),
(5, 4, 'ORD-2025-01-20250105', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-01-05 05:01:00'),
(6, 5, 'ORD-2025-01-20250110', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-01-10 03:32:00'),
(7, 5, 'ORD-2025-01-20250110', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-01-10 03:32:00'),
(8, 5, 'ORD-2025-01-20250110', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-01-10 03:32:00'),
(9, 5, 'ORD-2025-01-20250110', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-01-10 03:32:00'),
(10, 6, 'ORD-2025-01-20250115', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-01-15 03:20:00'),
(11, 6, 'ORD-2025-01-20250115', 11, 'Classic Burger', 2, 159.00, 318.00, '2025-01-15 03:20:00'),
(12, 6, 'ORD-2025-01-20250115', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-01-15 03:20:00'),
(13, 7, 'ORD-2025-01-20250120', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-01-20 08:27:00'),
(14, 7, 'ORD-2025-01-20250120', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-01-20 08:27:00'),
(15, 7, 'ORD-2025-01-20250120', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-01-20 08:27:00'),
(16, 7, 'ORD-2025-01-20250120', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-01-20 08:27:00'),
(17, 8, 'ORD-2025-01-20250125', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-01-25 08:38:00'),
(18, 8, 'ORD-2025-01-20250125', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-01-25 08:38:00'),
(19, 8, 'ORD-2025-01-20250125', 13, 'Fried Chicken', 3, 189.00, 567.00, '2025-01-25 08:38:00'),
(20, 8, 'ORD-2025-01-20250125', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-01-25 08:38:00'),
(21, 9, 'ORD-2025-02-20250205', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-02-05 06:10:00'),
(22, 9, 'ORD-2025-02-20250205', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-02-05 06:10:00'),
(23, 10, 'ORD-2025-02-20250210', 13, 'Fried Chicken', 3, 189.00, 567.00, '2025-02-10 10:15:00'),
(24, 10, 'ORD-2025-02-20250210', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-02-10 10:15:00'),
(25, 11, 'ORD-2025-02-20250215', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-02-15 06:27:00'),
(26, 11, 'ORD-2025-02-20250215', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-02-15 06:27:00'),
(27, 11, 'ORD-2025-02-20250215', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-02-15 06:27:00'),
(28, 11, 'ORD-2025-02-20250215', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-02-15 06:27:00'),
(29, 12, 'ORD-2025-02-20250220', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-02-20 09:04:00'),
(30, 12, 'ORD-2025-02-20250220', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-02-20 09:04:00'),
(31, 13, 'ORD-2025-02-20250225', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-02-25 02:57:00'),
(32, 13, 'ORD-2025-02-20250225', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-02-25 02:57:00'),
(33, 14, 'ORD-2025-03-20250305', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-03-05 06:27:00'),
(34, 14, 'ORD-2025-03-20250305', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-03-05 06:27:00'),
(35, 15, 'ORD-2025-03-20250310', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-03-10 12:02:00'),
(36, 15, 'ORD-2025-03-20250310', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-03-10 12:02:00'),
(37, 15, 'ORD-2025-03-20250310', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-03-10 12:02:00'),
(38, 16, 'ORD-2025-03-20250315', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-03-15 05:19:00'),
(39, 16, 'ORD-2025-03-20250315', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-03-15 05:19:00'),
(40, 17, 'ORD-2025-03-20250320', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-03-20 04:40:00'),
(41, 17, 'ORD-2025-03-20250320', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-03-20 04:40:00'),
(42, 17, 'ORD-2025-03-20250320', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-03-20 04:40:00'),
(43, 17, 'ORD-2025-03-20250320', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-03-20 04:40:00'),
(44, 18, 'ORD-2025-03-20250325', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-03-25 05:02:00'),
(45, 18, 'ORD-2025-03-20250325', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-03-25 05:02:00'),
(46, 18, 'ORD-2025-03-20250325', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-03-25 05:02:00'),
(47, 19, 'ORD-2025-04-20250405', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-04-05 02:32:00'),
(48, 19, 'ORD-2025-04-20250405', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-04-05 02:32:00'),
(49, 19, 'ORD-2025-04-20250405', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-04-05 02:32:00'),
(50, 20, 'ORD-2025-04-20250410', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-04-10 03:00:00'),
(51, 20, 'ORD-2025-04-20250410', 13, 'Fried Chicken', 2, 189.00, 378.00, '2025-04-10 03:00:00'),
(52, 21, 'ORD-2025-04-20250415', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-04-15 12:17:00'),
(53, 21, 'ORD-2025-04-20250415', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-04-15 12:17:00'),
(54, 22, 'ORD-2025-04-20250420', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-04-20 02:08:00'),
(55, 22, 'ORD-2025-04-20250420', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-04-20 02:08:00'),
(56, 23, 'ORD-2025-04-20250425', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-04-25 06:26:00'),
(57, 23, 'ORD-2025-04-20250425', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-04-25 06:26:00'),
(58, 23, 'ORD-2025-04-20250425', 13, 'Fried Chicken', 3, 189.00, 567.00, '2025-04-25 06:26:00'),
(59, 24, 'ORD-2025-05-20250505', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-05-05 05:14:00'),
(60, 24, 'ORD-2025-05-20250505', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-05-05 05:14:00'),
(61, 24, 'ORD-2025-05-20250505', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-05-05 05:14:00'),
(62, 24, 'ORD-2025-05-20250505', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-05-05 05:14:00'),
(63, 25, 'ORD-2025-05-20250510', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-05-10 12:14:00'),
(64, 25, 'ORD-2025-05-20250510', 13, 'Fried Chicken', 2, 189.00, 378.00, '2025-05-10 12:14:00'),
(65, 25, 'ORD-2025-05-20250510', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-05-10 12:14:00'),
(66, 25, 'ORD-2025-05-20250510', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-05-10 12:14:00'),
(67, 26, 'ORD-2025-05-20250515', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-05-15 04:40:00'),
(68, 26, 'ORD-2025-05-20250515', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-05-15 04:40:00'),
(69, 26, 'ORD-2025-05-20250515', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-05-15 04:40:00'),
(70, 27, 'ORD-2025-05-20250520', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-05-20 03:43:00'),
(71, 27, 'ORD-2025-05-20250520', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-05-20 03:43:00'),
(72, 27, 'ORD-2025-05-20250520', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-05-20 03:43:00'),
(73, 28, 'ORD-2025-05-20250525', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-05-25 12:14:00'),
(74, 28, 'ORD-2025-05-20250525', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-05-25 12:14:00'),
(75, 28, 'ORD-2025-05-20250525', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-05-25 12:14:00'),
(76, 28, 'ORD-2025-05-20250525', 11, 'Classic Burger', 2, 159.00, 318.00, '2025-05-25 12:14:00'),
(77, 29, 'ORD-2025-06-20250605', 13, 'Fried Chicken', 2, 189.00, 378.00, '2025-06-05 02:02:00'),
(78, 29, 'ORD-2025-06-20250605', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-06-05 02:02:00'),
(79, 29, 'ORD-2025-06-20250605', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-06-05 02:02:00'),
(80, 30, 'ORD-2025-06-20250610', 13, 'Fried Chicken', 3, 189.00, 567.00, '2025-06-10 06:39:00'),
(81, 30, 'ORD-2025-06-20250610', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-06-10 06:39:00'),
(82, 30, 'ORD-2025-06-20250610', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-06-10 06:39:00'),
(83, 30, 'ORD-2025-06-20250610', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-06-10 06:39:00'),
(84, 31, 'ORD-2025-06-20250615', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-06-15 08:06:00'),
(85, 31, 'ORD-2025-06-20250615', 13, 'Fried Chicken', 3, 189.00, 567.00, '2025-06-15 08:06:00'),
(86, 31, 'ORD-2025-06-20250615', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-06-15 08:06:00'),
(87, 32, 'ORD-2025-06-20250620', 13, 'Fried Chicken', 3, 189.00, 567.00, '2025-06-20 05:55:00'),
(88, 32, 'ORD-2025-06-20250620', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-06-20 05:55:00'),
(89, 33, 'ORD-2025-06-20250625', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-06-25 08:56:00'),
(90, 33, 'ORD-2025-06-20250625', 13, 'Fried Chicken', 2, 189.00, 378.00, '2025-06-25 08:56:00'),
(91, 33, 'ORD-2025-06-20250625', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-06-25 08:56:00'),
(92, 33, 'ORD-2025-06-20250625', 11, 'Classic Burger', 2, 159.00, 318.00, '2025-06-25 08:56:00'),
(93, 34, 'ORD-2025-07-20250705', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-07-05 05:25:00'),
(94, 34, 'ORD-2025-07-20250705', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-07-05 05:25:00'),
(95, 35, 'ORD-2025-07-20250710', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-07-10 12:02:00'),
(96, 35, 'ORD-2025-07-20250710', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-07-10 12:02:00'),
(97, 36, 'ORD-2025-07-20250715', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-07-15 03:22:00'),
(98, 36, 'ORD-2025-07-20250715', 13, 'Fried Chicken', 3, 189.00, 567.00, '2025-07-15 03:22:00'),
(99, 37, 'ORD-2025-07-20250720', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-07-20 09:28:00'),
(100, 37, 'ORD-2025-07-20250720', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-07-20 09:28:00'),
(101, 38, 'ORD-2025-07-20250725', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-07-25 04:39:00'),
(102, 38, 'ORD-2025-07-20250725', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-07-25 04:39:00'),
(103, 38, 'ORD-2025-07-20250725', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-07-25 04:39:00'),
(104, 38, 'ORD-2025-07-20250725', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-07-25 04:39:00'),
(105, 39, 'ORD-2025-08-20250805', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-08-05 08:06:00'),
(106, 39, 'ORD-2025-08-20250805', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-08-05 08:06:00'),
(107, 39, 'ORD-2025-08-20250805', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-08-05 08:06:00'),
(108, 39, 'ORD-2025-08-20250805', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-08-05 08:06:00'),
(109, 40, 'ORD-2025-08-20250810', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-08-10 09:34:00'),
(110, 40, 'ORD-2025-08-20250810', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-08-10 09:34:00'),
(111, 40, 'ORD-2025-08-20250810', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-08-10 09:34:00'),
(112, 41, 'ORD-2025-08-20250815', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-08-15 04:46:00'),
(113, 41, 'ORD-2025-08-20250815', 11, 'Classic Burger', 2, 159.00, 318.00, '2025-08-15 04:46:00'),
(114, 41, 'ORD-2025-08-20250815', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-08-15 04:46:00'),
(115, 41, 'ORD-2025-08-20250815', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-08-15 04:46:00'),
(116, 42, 'ORD-2025-08-20250820', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-08-20 10:06:00'),
(117, 42, 'ORD-2025-08-20250820', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-08-20 10:06:00'),
(118, 42, 'ORD-2025-08-20250820', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-08-20 10:06:00'),
(119, 43, 'ORD-2025-08-20250825', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-08-25 05:03:00'),
(120, 43, 'ORD-2025-08-20250825', 13, 'Fried Chicken', 3, 189.00, 567.00, '2025-08-25 05:03:00'),
(121, 43, 'ORD-2025-08-20250825', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-08-25 05:03:00'),
(122, 44, 'ORD-2025-09-20250905', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-09-05 03:53:00'),
(123, 44, 'ORD-2025-09-20250905', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-09-05 03:53:00'),
(124, 44, 'ORD-2025-09-20250905', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-09-05 03:53:00'),
(125, 45, 'ORD-2025-09-20250910', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-09-10 12:38:00'),
(126, 45, 'ORD-2025-09-20250910', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-09-10 12:38:00'),
(127, 45, 'ORD-2025-09-20250910', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-09-10 12:38:00'),
(128, 46, 'ORD-2025-09-20250915', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-09-15 10:49:00'),
(129, 46, 'ORD-2025-09-20250915', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-09-15 10:49:00'),
(130, 46, 'ORD-2025-09-20250915', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-09-15 10:49:00'),
(131, 47, 'ORD-2025-09-20250920', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-09-20 09:00:00'),
(132, 47, 'ORD-2025-09-20250920', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-09-20 09:00:00'),
(133, 47, 'ORD-2025-09-20250920', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-09-20 09:00:00'),
(134, 47, 'ORD-2025-09-20250920', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-09-20 09:00:00'),
(135, 48, 'ORD-2025-09-20250925', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-09-25 09:20:00'),
(136, 48, 'ORD-2025-09-20250925', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-09-25 09:20:00'),
(137, 49, 'ORD-2025-10-20251005', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-10-05 02:27:00'),
(138, 49, 'ORD-2025-10-20251005', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-10-05 02:27:00'),
(139, 49, 'ORD-2025-10-20251005', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-10-05 02:27:00'),
(140, 49, 'ORD-2025-10-20251005', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-10-05 02:27:00'),
(141, 50, 'ORD-2025-10-20251010', 13, 'Fried Chicken', 2, 189.00, 378.00, '2025-10-10 07:29:00'),
(142, 50, 'ORD-2025-10-20251010', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-10-10 07:29:00'),
(143, 51, 'ORD-2025-10-20251015', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-10-15 10:02:00'),
(144, 51, 'ORD-2025-10-20251015', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-10-15 10:02:00'),
(145, 51, 'ORD-2025-10-20251015', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-10-15 10:02:00'),
(146, 52, 'ORD-2025-10-20251020', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-10-20 12:34:00'),
(147, 52, 'ORD-2025-10-20251020', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-10-20 12:34:00'),
(148, 53, 'ORD-2025-10-20251025', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-10-25 09:42:00'),
(149, 53, 'ORD-2025-10-20251025', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-10-25 09:42:00'),
(150, 53, 'ORD-2025-10-20251025', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-10-25 09:42:00'),
(151, 53, 'ORD-2025-10-20251025', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-10-25 09:42:00'),
(152, 54, 'ORD-2025-11-20251105', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-11-05 07:43:00'),
(153, 54, 'ORD-2025-11-20251105', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-11-05 07:43:00'),
(154, 54, 'ORD-2025-11-20251105', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-11-05 07:43:00'),
(155, 55, 'ORD-2025-11-20251110', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-11-10 02:06:00'),
(156, 55, 'ORD-2025-11-20251110', 13, 'Fried Chicken', 2, 189.00, 378.00, '2025-11-10 02:06:00'),
(157, 56, 'ORD-2025-11-20251115', 15, 'Pepperoni Pizza', 1, 275.00, 275.00, '2025-11-15 05:12:00'),
(158, 56, 'ORD-2025-11-20251115', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-11-15 05:12:00'),
(159, 57, 'ORD-2025-11-20251120', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-11-20 09:01:00'),
(160, 57, 'ORD-2025-11-20251120', 13, 'Fried Chicken', 2, 189.00, 378.00, '2025-11-20 09:01:00'),
(161, 57, 'ORD-2025-11-20251120', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-11-20 09:01:00'),
(162, 57, 'ORD-2025-11-20251120', 11, 'Classic Burger', 2, 159.00, 318.00, '2025-11-20 09:01:00'),
(163, 58, 'ORD-2025-11-20251125', 12, 'Crispy Fries', 3, 79.00, 237.00, '2025-11-25 05:17:00'),
(164, 58, 'ORD-2025-11-20251125', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-11-25 05:17:00'),
(165, 58, 'ORD-2025-11-20251125', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-11-25 05:17:00'),
(166, 58, 'ORD-2025-11-20251125', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-11-25 05:17:00'),
(167, 59, 'ORD-2025-12-20251205', 11, 'Classic Burger', 1, 159.00, 159.00, '2025-12-05 07:35:00'),
(168, 59, 'ORD-2025-12-20251205', 13, 'Fried Chicken', 1, 189.00, 189.00, '2025-12-05 07:35:00'),
(169, 59, 'ORD-2025-12-20251205', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-12-05 07:35:00'),
(170, 59, 'ORD-2025-12-20251205', 14, 'Milk Tea', 1, 99.00, 99.00, '2025-12-05 07:35:00'),
(171, 60, 'ORD-2025-12-20251210', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-12-10 06:11:00'),
(172, 60, 'ORD-2025-12-20251210', 14, 'Milk Tea', 3, 99.00, 297.00, '2025-12-10 06:11:00'),
(173, 60, 'ORD-2025-12-20251210', 15, 'Pepperoni Pizza', 2, 275.00, 550.00, '2025-12-10 06:11:00'),
(174, 60, 'ORD-2025-12-20251210', 12, 'Crispy Fries', 2, 79.00, 158.00, '2025-12-10 06:11:00'),
(175, 61, 'ORD-2025-12-20251215', 14, 'Milk Tea', 2, 99.00, 198.00, '2025-12-15 10:56:00'),
(176, 61, 'ORD-2025-12-20251215', 12, 'Crispy Fries', 1, 79.00, 79.00, '2025-12-15 10:56:00'),
(177, 62, 'ORD-2025-12-20251220', 15, 'Pepperoni Pizza', 3, 275.00, 825.00, '2025-12-20 10:25:00'),
(178, 62, 'ORD-2025-12-20251220', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-12-20 10:25:00'),
(179, 63, 'ORD-2025-12-20251225', 11, 'Classic Burger', 3, 159.00, 477.00, '2025-12-25 12:56:00'),
(180, 63, 'ORD-2025-12-20251225', 13, 'Fried Chicken', 2, 189.00, 378.00, '2025-12-25 12:56:00'),
(181, 64, 'ORD-20260113000151-3', 11, 'Classic Burger', 2, 159.00, 318.00, '2026-01-12 16:01:51'),
(182, 64, 'ORD-20260113000151-3', 12, 'Crispy Fries', 2, 79.00, 158.00, '2026-01-12 16:01:51'),
(183, 64, 'ORD-20260113000151-3', 14, 'Milk Tea', 1, 99.00, 99.00, '2026-01-12 16:01:51'),
(184, 64, 'ORD-20260113000151-3', 13, 'Fried Chicken', 1, 189.00, 189.00, '2026-01-12 16:01:51'),
(185, 65, 'ORD-20260114235352-5', 11, 'Classic Burger', 1, 159.00, 159.00, '2026-01-14 15:53:52'),
(186, 66, 'ORD-20260115170723-7', 14, 'Milk Tea', 1, 99.00, 99.00, '2026-01-15 09:07:23');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `id` int(11) NOT NULL,
  `staff_id` varchar(10) DEFAULT NULL,
  `staff_name` varchar(100) NOT NULL,
  `staff_email` varchar(100) NOT NULL,
  `staff_phone` varchar(20) NOT NULL,
  `staff_address` text NOT NULL,
  `staff_password` varchar(255) NOT NULL,
  `role` varchar(50) DEFAULT 'staff',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`id`, `staff_id`, `staff_name`, `staff_email`, `staff_phone`, `staff_address`, `staff_password`, `role`, `created_at`, `updated_at`) VALUES
(1, 'EMP00001', 'Staff User', 'staff@fooddash.com', '0987654321', 'Staff Office', 'bcb913566fdd31673f307af000e69ccb3568166e0b5f72bf9de41e54b1809739', 'staff', '2026-01-06 15:29:07', '2026-01-06 15:29:07'),
(2, 'EMP00002', 'Clarence Mongas', 'c@.com', '091223511', 'Calinan', '6b58bf58e7940c4fb2071628e140d65d509fea6c8b4915f68f461c07dae7a536', 'staff', '2026-01-06 16:41:13', '2026-01-14 15:51:21'),
(3, 'EMP00003', 'Haris Usman', 'h@.com', '09224545226', 'Cotabato', '6b58bf58e7940c4fb2071628e140d65d509fea6c8b4915f68f461c07dae7a536', 'staff', '2026-01-14 15:51:07', '2026-01-14 15:51:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_staff_name` (`staff_name`),
  ADD KEY `idx_staff_id` (`staff_id`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `admin_email` (`admin_email`),
  ADD UNIQUE KEY `admin_id` (`admin_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `menu_item_id` (`menu_item_id`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `staff_email` (`staff_email`),
  ADD UNIQUE KEY `staff_id` (`staff_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=187;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_items` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
