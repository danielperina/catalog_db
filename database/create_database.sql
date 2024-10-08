-- MySQL Script generated by MySQL Workbench
-- Tue Jul 16 21:57:48 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema catalog
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema catalog
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `catalog` DEFAULT CHARACTER SET utf8 ;
USE `catalog` ;

-- -----------------------------------------------------
-- Table `catalog`.`Planta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `catalog`.`Planta` (
  `idPlanta` INT NOT NULL AUTO_INCREMENT,
  `nomeCientifico` VARCHAR(45) NOT NULL,
  `nomePopular` VARCHAR(45) NOT NULL,
  `descricaoBotanica` VARCHAR(100) NOT NULL,
  `imagem` MEDIUMBLOB NOT NULL,
  PRIMARY KEY (`idPlanta`),
  UNIQUE INDEX `nomeCientifico_UNIQUE` (`nomeCientifico` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `catalog`.`Comunidade`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `catalog`.`Comunidade` (
  `idComunidade` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `bioma` ENUM('Amazônia', 'Caatinga', 'Cerrado', 'Mata Atlântica', 'Pampas', 'Pantanal') NOT NULL,
  `localizacao` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idComunidade`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `catalog`.`Condicao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `catalog`.`Condicao` (
  `idCondicao` INT NOT NULL AUTO_INCREMENT,
  `descricao` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idCondicao`),
  UNIQUE INDEX `descricao_UNIQUE` (`descricao` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `catalog`.`Tratamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `catalog`.`Tratamento` (
  `Planta_idPlanta` INT NOT NULL,
  `Comunidade_idComunidade` INT NOT NULL,
  `Condicao_idCondicao` INT NOT NULL,
  `parteUtilizada` VARCHAR(45) NOT NULL,
  `preparacao` VARCHAR(45) NOT NULL,
  `aplicacao` VARCHAR(45) NOT NULL,
  `eficacia` ENUM('Não comprovada', '<=10%', '<=20%', '<=30%', '<=40%', '<=50%', '<=60%', '<=70%', '<=80%', '<=90%') NOT NULL,
  PRIMARY KEY (`Planta_idPlanta`, `Comunidade_idComunidade`, `Condicao_idCondicao`),
  INDEX `fk_Planta_has_Comunidade_Comunidade1_idx` (`Comunidade_idComunidade` ASC) ,
  INDEX `fk_Planta_has_Comunidade_Planta_idx` (`Planta_idPlanta` ASC) ,
  INDEX `fk_Planta_has_Comunidade_Condicao1_idx` (`Condicao_idCondicao` ASC) ,
  CONSTRAINT `fk_Planta_has_Comunidade_Planta`
    FOREIGN KEY (`Planta_idPlanta`)
    REFERENCES `catalog`.`Planta` (`idPlanta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Planta_has_Comunidade_Comunidade1`
    FOREIGN KEY (`Comunidade_idComunidade`)
    REFERENCES `catalog`.`Comunidade` (`idComunidade`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Planta_has_Comunidade_Condicao1`
    FOREIGN KEY (`Condicao_idCondicao`)
    REFERENCES `catalog`.`Condicao` (`idCondicao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `catalog`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `catalog`.`Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `cpf` VARCHAR(11) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE INDEX `cpf_UNIQUE` (`cpf` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `catalog`.`Privilegio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `catalog`.`Privilegio` (
  `idPrivilegio` INT NOT NULL AUTO_INCREMENT,
  `codigo` INT NOT NULL,
  PRIMARY KEY (`idPrivilegio`),
  UNIQUE INDEX `codigo_UNIQUE` (`codigo` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `catalog`.`Acesso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `catalog`.`Acesso` (
  `Usuario_idUsuario` INT NOT NULL,
  `Privilegio_idPrivilegio` INT NOT NULL,
  PRIMARY KEY (`Usuario_idUsuario`, `Privilegio_idPrivilegio`),
  INDEX `fk_Usuario_has_Privilegio_Privilegio1_idx` (`Privilegio_idPrivilegio` ASC) ,
  INDEX `fk_Usuario_has_Privilegio_Usuario1_idx` (`Usuario_idUsuario` ASC) ,
  CONSTRAINT `fk_Usuario_has_Privilegio_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `catalog`.`Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Usuario_has_Privilegio_Privilegio1`
    FOREIGN KEY (`Privilegio_idPrivilegio`)
    REFERENCES `catalog`.`Privilegio` (`idPrivilegio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
