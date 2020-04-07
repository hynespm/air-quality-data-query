CREATE TABLE `airquality` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `Date` varchar(255) COLLATE utf8_bin NOT NULL,
    `Time` varchar(255) COLLATE utf8_bin NOT NULL,
    `CO(GT)` varchar(255) COLLATE utf8_bin NOT NULL,
    `PT08.S1(CO)` varchar(255) COLLATE utf8_bin NOT NULL,
    `C6H6(GT)` varchar(255) COLLATE utf8_bin NOT NULL,
    `PT08.S2(NMHC)` varchar(255) COLLATE utf8_bin NOT NULL,
    `NOx(GT)` varchar(255) COLLATE utf8_bin NOT NULL,
    `PT08.S3(NOx)` varchar(255) COLLATE utf8_bin NOT NULL,
    `NO2(GT)` varchar(255) COLLATE utf8_bin NOT NULL,
    `PT08.S4(NO2)` varchar(255) COLLATE utf8_bin NOT NULL,
    `PT08.S5(O3)` varchar(255) COLLATE utf8_bin NOT NULL,
    `T` varchar(255) COLLATE utf8_bin NOT NULL,
    `RH` varchar(255) COLLATE utf8_bin NOT NULL,
    `AH` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;
