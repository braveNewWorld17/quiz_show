create table quiz (
	id int AUTO_INCREMENT primary key,
    quiz_type_code int,
    quiz_type_desc varchar(32),
    quiz varchar(64),
    answer varchar(64),
    created timestamp DEFAULT CURRENT_TIMESTAMP
)

