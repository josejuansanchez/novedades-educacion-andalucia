CREATE TABLE user (
	telegram_id INTEGER PRIMARY KEY UNIQUE,
	username VARCHAR(128) NOT NULL,
	first_name VARCHAR(128),
	last_name VARCHAR(128),
	language_code VARCHAR(16),
	is_bot INTEGER NOT NULL
);

CREATE TABLE news (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    title VARCHAR(1024) NOT NULL,
	link VARCHAR(1024) NOT NULL,
	date DATETIME NOT NULL,
	source_name VARCHAR(128) NOT NULL
);

CREATE TABLE receives (
	telegram_id INTEGER NOT NULL,
	new_id INTEGER NOT NULL,
	PRIMARY KEY (telegram_id, new_id),
	FOREIGN KEY (telegram_id) REFERENCES user(telegram_id),
	FOREIGN KEY (new_id) REFERENCES news(id)
)