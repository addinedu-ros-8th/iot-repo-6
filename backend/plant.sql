CREATE TABLE plant
(
    plant_id int auto_increment PRIMARY key,
    plant_name varchar(16),
    temperature_min float,
    temperature_max float,
    humidity_min float,
    humidity_max float,
    soil_moisture_min float,
    soil_moisture_max float,
    light_intensity_min float,
    light_intensity_max float,
    growing_date datetime,
    harvest_date datetime
);