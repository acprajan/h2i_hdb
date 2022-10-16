drop table if exists car_park_information;

create table if not exists car_park_information
(
  short_term_parking      varchar(50),
  car_park_type           varchar(100),
  y_coord                 numeric,
  x_coord                 numeric,
  free_parking            varchar(100),
  gantry_height           numeric,
  car_park_basement       varchar(50),
  address                 varchar(500),
  car_park_decks          numeric,
  _id                     numeric,
  carpark_number          varchar(50),
  type_of_parking_system  varchar(50),
  primary key (carpark_number)
);
