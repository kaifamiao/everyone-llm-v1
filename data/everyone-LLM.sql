CREATE TABLE setting (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ParaName VARCHAR(200) NOT NULL,
    ParaValue VARCHAR(2000) NOT NULL,
    ParaIndex INTEGER NOT NULL,
    user_role VARCHAR(200) NOT NULL
);
select *from setting;
insert into setting (ParaName, ParaValue, ParaIndex, user_role) values ('version', 'alpha-0.0.1', 1001, 'system');
insert into setting (ParaName, ParaValue, ParaIndex, user_role) values ('title', 'everyone-LLM', 1002, 'system');
insert into setting (ParaName, ParaValue, ParaIndex, user_role) values ('author', 'kaifamiao', 1003, 'system');
insert into setting (ParaName, ParaValue, ParaIndex, user_role) values ('github', 'https://github.com/kaifamiao/everyone-LLM', 1004, 'system');

insert into setting (ParaName, ParaValue, ParaIndex, user_role) values ('version', 'alpha-0.0.1', 2001, 'guest');
insert into setting (ParaName, ParaValue, ParaIndex, user_role) values ('title', 'everyone-LLM', 2002, 'guest');
insert into setting (ParaName, ParaValue, ParaIndex, user_role) values ('author', 'kaifamiao', 2003, 'guest');
insert into setting (ParaName, ParaValue, ParaIndex, user_role) values ('github', 'https://github.com/kaifamiao/everyone-LLM', 2004, 'guest');


CREATE TABLE sidebar_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL
);

INSERT INTO sidebar_items (item_name) VALUES ('Item 1'), ('Item 2'), ('Item 3');


CREATE TABLE sidebar_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL
);

INSERT INTO sidebar_items (item_name) VALUES ('Item 1'), ('Item 2'), ('Item 3');

select *
from sidebar_items;
