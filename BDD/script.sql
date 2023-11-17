create table type
(
    name varchar(20) not null,
    id   int auto_increment
        primary key
);

create table skill
(
    name           varchar(50) not null,
    description    text        null,
    power          int         null,
    accuracy       int         null,
    max_life_point int         null,
    type_name      varchar(20) null,
    id             int auto_increment
        primary key,
    constraint skill_type_name_fk
        foreign key (type_name) references type (name)
);

create table pokemon
(
    name       varchar(20) not null,
    size       float       null,
    weight     float       null,
    stats      int         null,
    image      text        null,
    types      int         null,
    skills     int         null,
    id_pokedex int auto_increment
        primary key,
    constraint pokemon_skill_id_fk
        foreign key (skills) references skill (id),
    constraint pokemon_type_id_fk
        foreign key (types) references type (id)
);

create index pokemon_name_index
    on pokemon (name);

create index skill_name_index
    on skill (name);

create index type_id_index
    on type (id);

create index type_name_index
    on type (name);


