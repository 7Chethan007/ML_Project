
CREATE TABLE `ml` (
  `company_id` VARCHAR(255) NOT NULL PRIMARY KEY,
  `company_name` VARCHAR(255),
  `pros` JSON,
  `cons` JSON,
  `analysis_json` JSON,
  `last_updated` DATETIME,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;