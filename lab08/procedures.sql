-- Upsert (insert или update)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- Массовая вставка с проверкой телефона
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names text[], p_phones text[])
LANGUAGE plpgsql AS $$
DECLARE
    i integer;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]+$' THEN
            IF EXISTS (SELECT 1 FROM contacts WHERE name = p_names[i]) THEN
                UPDATE contacts SET phone = p_phones[i] WHERE name = p_names[i];
            ELSE
                INSERT INTO contacts(name, phone) VALUES(p_names[i], p_phones[i]);
            END IF;
        ELSE
            RAISE NOTICE 'Некорректный телефон: % для %', p_phones[i], p_names[i];
        END IF;
    END LOOP;
END;
$$;

-- Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_value OR phone = p_value;
END;
$$;
