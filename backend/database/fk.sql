-- alter table user
-- ADD CONSTRAINT fk_user_card_id FOREIGN KEY (user_card_id)
-- REFERENCES user_card(user_card_id) ON DELETE CASCADE;

-- alter table user
-- ADD CONSTRAINT fk_farm_kiet_id FOREIGN KEY (farm_kit_id)
-- REFERENCES farm_kit(farm_kit_id) ON DELETE CASCADE;

alter table rental_kit
ADD CONSTRAINT fk_user_card_id_r FOREIGN KEY (user_card_id)
REFERENCES user_card(user_card_id) ON DELETE CASCADE;

alter table rental_kit
ADD CONSTRAINT fk_user_id_r FOREIGN KEY (user_id)
REFERENCES user(user_id) ON DELETE CASCADE;

alter table rental_kit
ADD CONSTRAINT fk_rental_kit_status_id_r FOREIGN KEY (rental_kit_status_id)
REFERENCES rental_kit_status(rental_kit_status_id) ON DELETE CASCADE;

alter table rental_kit
ADD CONSTRAINT fk_plant_id_r FOREIGN KEY (plant_id)
REFERENCES plant(plant_id) ON DELETE CASCADE;
