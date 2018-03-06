create table records (
	id int AUTO_INCREMENT primary key,
    recorder varchar(100),
    score int,
    created timestamp DEFAULT CURRENT_TIMESTAMP
)

