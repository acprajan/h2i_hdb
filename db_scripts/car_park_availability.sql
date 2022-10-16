drop table if exists car_park_availability;

create table if not exists car_park_availability
(
  carpark_number    varchar(50),
  total_lots        numeric,
  total_free_lots   numeric,
  lot_type          varchar(10),
  update_time       timestamp,
  primary key (carpark_number, update_time)
);
