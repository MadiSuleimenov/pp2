-- 1. Groups / categories
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Seed default groups
INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

-- 2 Contacts (core table)
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='contacts' AND column_name='email') THEN
        ALTER TABLE contacts ADD COLUMN email VARCHAR(100);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='contacts' AND column_name='birthday') THEN
        ALTER TABLE contacts ADD COLUMN birthday DATE;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name='contacts' AND column_name='group_id') THEN
        ALTER TABLE contacts ADD COLUMN group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL;
    END IF;
END $$;

-- 3 Phones
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20)  NOT NULL,
    type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
);

-- 4 Helpful indexes
CREATE INDEX IF NOT EXISTS idx_contacts_name    ON contacts (name);
CREATE INDEX IF NOT EXISTS idx_contacts_email   ON contacts (email);
CREATE INDEX IF NOT EXISTS idx_phones_contact   ON phones   (contact_id);
CREATE INDEX IF NOT EXISTS idx_phones_phone     ON phones   (phone);
