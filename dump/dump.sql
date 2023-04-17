CREATE TABLE gebruikers (
    id int NOT NULL AUTO_INCREMENT,
    username varchar(20) NOT NULL,
    name varchar(200) NOT NULL,
    email varchar(120) NOT NULL,
    favo_kl varchar(120),
    dates datetime,
    pw_hash varchar(244),
    PRIMARY KEY (id),
    UNIQUE (email, username)
);
CREATE TABLE posts (
    id int NOT NULL AUTO_INCREMENT,
    author varchar(200) NOT NULL,
    title varchar(200) NOT NULL,
    content text NOT NULL,
    slug varchar(200) NOT NULL,
    date_posted datetime,
    PRIMARY KEY (id)
);