DROP TABLE IF EXISTS users;
CREATE TABLE users (
    userid INT(11) PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(255) NOT NULL,
    active INT(11) NOT NULL DEFAULT 1,
    standkey INT(11) NOT NULL DEFAULT 1,
    sitkey INT(11) NOT NULL DEFAULT 2,
    cond VARCHAR(255) NOT NULL,
    startdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


DROP TABLE IF EXISTS desks;
CREATE TABLE desks (
    deskid INT(11) PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    macaddress VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL
);


DROP TABLE IF EXISTS heights;
CREATE TABLE heights (
    heightid INT(11) PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    time INT(11) NOT NULL,
    userid INT(11) NOT NULL,
    height REAL NOT NULL
);


DROP TABLE IF EXISTS actions;
CREATE TABLE actions (
    actionid INT(11) PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    time INT(11) NOT NULL,
    userid INT(11) NOT NULL,
    action VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS commands;
CREATE TABLE commands (
    commandid INT(11) PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    userid INT(11) NOT NULL,
    command REAL NOT NULL,
    done INT(11) NOT NULL DEFAULT 0
    );

DROP TABLE IF EXISTS deskjoins;
CREATE TABLE deskjoins (
    deskjoinid INT(11) PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end TIMESTAMP,
    deskid INT(11) NOT NULL,
    userid INT(11) NOT NULL
);
