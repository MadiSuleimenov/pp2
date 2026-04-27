CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- Find contact
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(name) = LOWER(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    -- Validate type
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home, work, or mobile. Got: %', p_type;
    END IF;

    -- Avoid exact duplicates for same contact
    IF EXISTS (
        SELECT 1 FROM phones
        WHERE contact_id = v_contact_id AND phone = p_phone
    ) THEN
        RAISE NOTICE 'Phone % already exists for contact %.', p_phone, p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);

    RAISE NOTICE 'Phone % (%) added to contact %.', p_phone, p_type, p_contact_name;
END;
$$;

--2. move_to_group
--  Moves a contact to a group; creates the group if missing.
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- Ensure group exists (create if not)
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    -- Find contact
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(name) = LOWER(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;

    RAISE NOTICE 'Contact "%" moved to group "%".', p_contact_name, p_group_name;
END;
$$;

--3 search_contacts

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id  INTEGER,
    name        VARCHAR,
    email       VARCHAR,
    birthday    DATE,
    group_name  VARCHAR,
    phones_list TEXT,
    created_at  TIMESTAMP
)
LANGUAGE plpgsql AS $$
DECLARE
    v_pattern TEXT := '%' || p_query || '%';
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name          AS group_name,
        STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
                        AS phones_list,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE
        c.name  ILIKE v_pattern OR
        c.email ILIKE v_pattern OR
        p.phone ILIKE v_pattern
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    ORDER BY c.name;
END;
$$;

--4 get_contacts_page
CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit    INTEGER DEFAULT 10,
    p_offset   INTEGER DEFAULT 0,
    p_group    VARCHAR DEFAULT NULL,
    p_sort_by  VARCHAR DEFAULT 'name'
)
RETURNS TABLE (
    contact_id  INTEGER,
    name        VARCHAR,
    email       VARCHAR,
    birthday    DATE,
    group_name  VARCHAR,
    phones_list TEXT,
    created_at  TIMESTAMP
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Validate sort column to prevent SQL injection
    IF p_sort_by NOT IN ('name', 'birthday', 'created_at') THEN
        RAISE EXCEPTION 'Invalid sort column: %', p_sort_by;
    END IF;

    RETURN QUERY EXECUTE format(
        'SELECT DISTINCT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name          AS group_name,
            STRING_AGG(p.phone || %L || COALESCE(p.type,%L) || %L, %L)
                            AS phones_list,
            c.created_at
         FROM contacts c
         LEFT JOIN groups g ON g.id = c.group_id
         LEFT JOIN phones p ON p.contact_id = c.id
         WHERE ($1 IS NULL OR g.name ILIKE $1)
         GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
         ORDER BY c.%I NULLS LAST
         LIMIT $2 OFFSET $3',
        ' (', '?', ')', ', ',
        p_sort_by
    ) USING p_group, p_limit, p_offset;
END;
$$;
