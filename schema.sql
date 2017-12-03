    drop table if exists video;
    create table video (
    id integer primary key autoincrement,
    url text not null,
    votes text not null,
    comment text not null,
    duration test not null
);
