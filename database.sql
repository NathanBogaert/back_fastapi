-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 17 mai 2023 à 12:09
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `back-python-bogaert`
--

-- --------------------------------------------------------

--
-- Structure de la table `activity`
--

CREATE TABLE `activity` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `startTime` datetime NOT NULL,
  `endTime` datetime NOT NULL,
  `created_by` int(11) NOT NULL,
  `id_planning` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `activity`
--

INSERT INTO `activity` (`id`, `name`, `startTime`, `endTime`, `created_by`, `id_planning`) VALUES
(15, 'Finir le backend', '2023-05-17 09:53:27', '2023-05-17 13:00:27', 34, 13),
(16, 'Réunion avec les investisseurs', '2023-05-17 09:53:27', '2023-05-17 13:00:27', 34, 16),
(17, 'Lancer de papier dans la poubelle', '2023-05-17 09:53:27', '2023-05-17 13:00:27', 28, 1),
(18, 'Faire la pub du produit', '2023-05-17 09:53:27', '2023-05-17 13:00:27', 32, 15),
(19, 'Contactez les acheteurs', '2023-05-17 09:53:27', '2023-05-17 13:00:27', 31, 15),
(20, 'Regardez les retours des clients', '2023-05-17 09:53:27', '2023-05-17 13:00:27', 31, 16),
(21, 'Faire passer la réforme', '2023-05-17 09:59:12', '2023-05-17 09:59:12', 35, 17),
(22, 'Essayer de ne pas utiliser le 49-3', '2023-05-17 09:59:12', '2023-05-17 09:59:12', 36, 17),
(23, 'Lancer la nouvelle émission rêve en cuisine', '2023-05-17 09:59:12', '2023-05-17 09:59:12', 29, 14),
(24, 'Faire des pâtes', '2023-05-17 09:59:12', '2023-05-17 09:59:12', 29, 1);

-- --------------------------------------------------------

--
-- Structure de la table `company`
--

CREATE TABLE `company` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `company`
--

INSERT INTO `company` (`id`, `name`) VALUES
(1, 'Ubibug'),
(3, 'Popstar Games'),
(10, 'Drama Games');

-- --------------------------------------------------------

--
-- Structure de la table `participant`
--

CREATE TABLE `participant` (
  `id_user` int(11) DEFAULT NULL,
  `id_activity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `participant`
--

INSERT INTO `participant` (`id_user`, `id_activity`) VALUES
(29, 23),
(29, 24),
(36, 22),
(36, 21),
(35, 21),
(32, 18),
(32, 19),
(32, 20),
(31, 20),
(31, 18),
(28, 15),
(28, 17),
(28, 23),
(34, 15),
(34, 17);

-- --------------------------------------------------------

--
-- Structure de la table `planning`
--

CREATE TABLE `planning` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `id_company` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `planning`
--

INSERT INTO `planning` (`id`, `name`, `id_company`) VALUES
(1, 'Semaine 1', 1),
(13, 'Semaine 2', 1),
(14, 'Semaine 3', 1),
(15, 'Semaine 1', 3),
(16, 'Semaine 2', 3),
(17, 'Semaine 1', 10);

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` text NOT NULL,
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `password` text NOT NULL,
  `email` text NOT NULL,
  `rights` enum('MAINTAINER','ADMIN','USER') NOT NULL,
  `id_company` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id`, `username`, `firstname`, `lastname`, `password`, `email`, `rights`, `id_company`) VALUES
(28, 'admin', 'gAAAAABkZJi6kxr6JcklJFeMyhAf4q6CkR1CJfGstJQzLkL5O0MHIJXHA96sOwrvTs_kz9nr7GQRWPkvgqulCqxndCoGxTlokg==', 'gAAAAABkZJi6g_51PG4ZAxS_H_4IjGH1kGt9B_9z74mhjaYH74laeYgfJLyoupaC2s3LYodMyUo_ywkSBrVM4qXceGTCyMyK2A==', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'gAAAAABkZJi6YmIV0sdW-YdQz4YMhiw3yvAxbt0DXBMYOvlDseZhtKbuAeF-ItOwh4ab_imvCkfgyLVm_EHazPu9cjUZv56NXA==', 'ADMIN', 1),
(29, 'petchebest', 'gAAAAABkZJrKs9rylqaRA5r7UQVAjiarNPoGicy7rh2xIMnh79yIzgL2NoJqu8iRK5BnrspsDlxY14K43h8ocpxQqygDM2gw6Q==', 'gAAAAABkZJrKNLBS45dDsvYrWEn8PCawlwgzv0z9_RIlrPjC26mwVXFTteP56biJ8GsaX0Yijzy26VAfeG6uUGLatJW1LvMYgg==', '26231dad668048925946f9217009a02eddf5a13e2709e50353041e12757a4a5b', 'gAAAAABkZJrKnK6XoSUOc4wKljjtBeCVQnT9ewA0JscoAmXde3aiVyxVMBEx9pYSd00ksK-kPsrLSFvaw19Ord6X54iPWbmNpK78WR2rY92_kjIGYZvo7ow=', 'USER', 1),
(31, 'jelhorloge', 'gAAAAABkZJwmehQC0ElhY7j4P4Fg_aseIcmxBssEd3y-9NLraB42OwCQbvEu45JqW57HzJSzFJ4EDwbx-kuC_Mu7FCyeo4NCzQ==', 'gAAAAABkZJwmseNdRGkGMG6nW7t2z8V8rdXi7SP2W9oW8id6Gti9wqlAxyhfhDY6U0VmGVjgdb6fPHnkve02PrIoT1TD_3xOTg==', 'aa3d2fe4f6d301dbd6b8fb2d2fddfb7aeebf3bec53ffff4b39a0967afa88c609', 'gAAAAABkZJwmn_SfEmCUcD9GRGWw4CUf8eBMZHJJHDjm4YI_DXqqrE6aGQLUBLjpjsMmLtp7PA0dbMrX6RheY0gPSyyohdTS1WI_JscaLZ8JS33CLNnic68=', 'USER', 3),
(32, 'therock', 'gAAAAABkZJyH7Onw-Bx52EffeiYyZTS9yzcPN7YqEMLDXUJbfbYRH_-thqr8IsDAip-IGp2pB8-M4R0_yEMCaka7-B3SARb2ow==', 'gAAAAABkZJyH15ff937563JOKqyjWSZXUeJRrZuT1_qKMpnaZGD-udj9e-grWJQSA0PHro41b7-fv1QrF7JHF4H9QnfH4EspQw==', 'a1159e9df3670d549d04524532629f5477ceb7deec9b45e47e8c009506ecb2c8', 'gAAAAABkZJyHLx2iqvSeLvBNpkBXUIK0rDNz78XLtXqXBmbdXhknz3dmRe8AtcMUMaozKwZz7JtfhsDGtAVqf6KrBt1T3yod8AbZbMAXhsBoLNVxn0lqJ-A=', 'ADMIN', 3),
(34, 'boss', 'gAAAAABkZKL8rEAirJyk-XmBDQuYWbmhqD22meaBvjNtwA48nDjDfydjPL-aeymtxdG2njrfG9Ez_LljNMWcoYM2rE-cMdE2DQ==', 'gAAAAABkZKL84YsHUyyAopcf0O5lIaA5VOMHZJPBWP28EyQI0wDLDO8OXpmqqYyMttQ7xPp7npcYD9-ZBjYoRj3M1wWVAqB_7A==', 'a1159e9df3670d549d04524532629f5477ceb7deec9b45e47e8c009506ecb2c8', 'gAAAAABkZKL8FJw8LY0e9odJZjO95LZMh_CS7tcYw42SKjxyw1dNKIt6aJDwKSfoUBTe64c1vT9b9s1VYHv7zpuzvNTdZAcIsg==', 'MAINTAINER', 1),
(35, 'Manu', 'gAAAAABkZKOMu2SCK4MU0Dul6ON7z42pHhfqcl_tbEa5VbeyuhlQLwKCOSzDWwTIQTY_Uor3RO8yynq5MFVncjFEe0lpHWdlQg==', 'gAAAAABkZKOMQ4JaoTvJ8MhBtoD4czaSbqz1SZ1uH2ryfXY0HKzhQiqNPLw4nEYPGPkFaGdrp_jFYaEg31Ajp0_h0vhvrUShcQ==', 'a1159e9df3670d549d04524532629f5477ceb7deec9b45e47e8c009506ecb2c8', 'gAAAAABkZKOMDUTPyYMJ066Wnblyhig6TZXEFO3MUylwgDRWr7pY5Z2uF5H-p33wHZfVL2Q1lkrBobty6XoSXLwqDV65vfKed2pRIJLBNfH2WRO32PYDN-0=', 'ADMIN', 10),
(36, 'eborne', 'gAAAAABkZKO877pHusKitpTui2s6CojiimdqEHiQGyWjbYcFmXj_pVwiQ-ou_OZihsMRg2lUAWpF4MKGVwR60jhIBCZyDDrm4w==', 'gAAAAABkZKO8ypQkzd1X0wjthlt3TuBZiWDbUbNmulHqBqnsXZMNFRzvJ3waUCcUET-11PgpR5VWkvkbI8004x19irYO5ymSnQ==', '560aa3e6e94314c78236109e209ac79e15e05ec8bf2dcb78300ae65e720edf9e', 'gAAAAABkZKO8pPkJmp2ePwXcuWTQEZLroalTb1pR1Xd6KONvqWNgEVJnSGMs_AWLwvlUalcy386ls9gK_YEXDo4Xn0sjytF0I9t8II9JmmQFdN7Y_7gL9To=', 'USER', 10);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `activity`
--
ALTER TABLE `activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_planning` (`id_planning`),
  ADD KEY `created_by` (`created_by`);

--
-- Index pour la table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `participant`
--
ALTER TABLE `participant`
  ADD KEY `id_activity` (`id_activity`),
  ADD KEY `id_user` (`id_user`);

--
-- Index pour la table `planning`
--
ALTER TABLE `planning`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_company` (`id_company`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_company` (`id_company`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `activity`
--
ALTER TABLE `activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT pour la table `company`
--
ALTER TABLE `company`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `planning`
--
ALTER TABLE `planning`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `activity`
--
ALTER TABLE `activity`
  ADD CONSTRAINT `activity_ibfk_3` FOREIGN KEY (`id_planning`) REFERENCES `planning` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `activity_ibfk_4` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Contraintes pour la table `participant`
--
ALTER TABLE `participant`
  ADD CONSTRAINT `participant_ibfk_2` FOREIGN KEY (`id_activity`) REFERENCES `activity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `participant_ibfk_3` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `planning`
--
ALTER TABLE `planning`
  ADD CONSTRAINT `planning_ibfk_1` FOREIGN KEY (`id_company`) REFERENCES `company` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`id_company`) REFERENCES `company` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
