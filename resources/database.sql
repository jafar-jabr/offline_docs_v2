DROP TABLE IF EXISTS 'app_pref';

CREATE TABLE `app_pref` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`current_version`	TEXT,
	`regular_size`	INTEGER,
	`big_size`	INTEGER,
	`font_color`	TEXT,
	`release_date`	TEXT
);

DROP TABLE IF EXISTS 'category';

CREATE TABLE `category` (
	`id`	INTEGER NOT NULL,
	`cat_name`	TEXT NOT NULL,
	`desc`	TEXT,
	`user_id`	INTEGER NOT NULL,
	`created_at`	TEXT,
	`updated_at`	TEXT,
	PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS 'docs';

CREATE TABLE `docs` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`doc_name`	TEXT,
	`details`	TEXT NOT NULL,
	`doc_type`	TEXT NOT NULL,
	`category_id`	INTEGER NOT NULL,
	`created_at`	DATETIME NOT NULL,
	`updated_at`	DATETIME,
	FOREIGN KEY(`category_id`) REFERENCES `category`(`id`)
);

DROP TABLE IF EXISTS 'remember_me';

CREATE TABLE `remember_me` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`user_name`	varchar ( 255 ),
	`pass_word`	varchar ( 255 )
);

DROP TABLE IF EXISTS 'tags';

CREATE TABLE `tags` (
	`id`	INTEGER NOT NULL,
	`tag_name`	TEXT,
	`doc_id`	INTEGER,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`doc_id`) REFERENCES `docs`(`id`)
);
DROP TABLE IF EXISTS 'users';

CREATE TABLE `users` (
	`id`	INTEGER NOT NULL,
	`firstname`	VARCHAR ( 255 ) NOT NULL,
	`lastname`	VARCHAR ( 255 ) NOT NULL,
	`email`	VARCHAR ( 255 ) NOT NULL UNIQUE,
	`phone`	TEXT,
	`password`	VARCHAR ( 255 ) NOT NULL,
	`created_at`	TEXT,
	`status`	INTEGER,
	PRIMARY KEY(`id`)
	);

DROP TABLE IF EXISTS 'sticky_notes';

CREATE TABLE "sticky_notes" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"note_date"	DATETIME,
	"details"	TEXT NOT NULL,
	"x_pos"	INTEGER NOT NULL DEFAULT 400,
	"y_pos"	INTEGER NOT NULL DEFAULT 250,
	"the_width"	INTEGER NOT NULL DEFAULT 200,
	"the_height"	INTEGER NOT NULL DEFAULT 300,
	"created_at"	DATETIME NOT NULL,
	"updated_at"	DATETIME
);

