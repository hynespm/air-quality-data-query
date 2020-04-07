create table airquality
(
    id                 int auto_increment
        primary key,
    date               varchar(255) not null,
    time               varchar(255) not null,
    co                 varchar(255) not null,
    tin_oxide          varchar(255) not null,
    metanic_hydro      varchar(255) not null,
    benzene_conc       varchar(255) not null,
    titania            varchar(255) not null,
    nox                varchar(255) not null,
    tungsten_oxide_nox varchar(255) not null,
    average_no2        varchar(255) not null,
    tungsten_oxide_no2 varchar(255) not null,
    indium_oxide       varchar(255) not null,
    temp               varchar(255) not null,
    relative_humidity  varchar(255) not null,
    absolute_humidity  varchar(255) not null
)
    collate = utf8_bin;