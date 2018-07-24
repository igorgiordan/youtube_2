CREATE TABLE Usuario(
    username VARCHAR(255) UNIQUE,
    nome VARCHAR(255),
    senha VARCHAR(255),
    email VARCHAR(255), 
    PRIMARY KEY (username));

CREATE TABLE Video (
    nome VARCHAR(255),
    id serial,
    link VARCHAR(400),
    username VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES Usuario(username));

CREATE TABLE Curtir (
    id_video INTEGER,
    username VARCHAR(255),
    FOREIGN KEY (username) REFERENCES Usuario(username),
    FOREIGN KEY (id_video) REFERENCES Video(id));

CREATE TABLE Comentar (
    username VARCHAR(255),
    id_video INTEGER,
    texto TEXT,
    FOREIGN KEY (username) REFERENCES Usuario(username),
    FOREIGN KEY (id_video) REFERENCES Video(id));
