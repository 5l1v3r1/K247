    drop table if exists video;
    create table video (
    id integer primary key autoincrement,
    url text not null,
    watched text not null,
    comment text not null,
    duration test not null
);
