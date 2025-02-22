CREATE TABLE rental_kit
(
    rental_kit_id int auto_increment PRIMARY key,
    rental_kit_status_id int,
    user_id int,
    user_card_id int,
    plant_id int,
    rental_startdate datetime,
    planting_date datetime
);