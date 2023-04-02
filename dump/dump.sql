CREATE TABLE gebruikers (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(200) NOT NULL,
    email varchar(120) NOT NULL,
    favo_kl varchar(120),
    dates datetime,
    pw_hash varchar(244),
    PRIMARY KEY (id),
    UNIQUE (email)
)
