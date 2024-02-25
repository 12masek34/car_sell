create_cars = """
    CREATE TABLE IF NOT EXISTS cars (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT,
        user_login TEXT,
        user_name TEXT,
        mark TEXT,
        model TEXT,
        year TEXT,
        engine_volume TEXT,
        power TEXT,
        transmission TEXT,
        city TEXT,
        contacts TEXT,
        price TEXT,
        description TEXT,
        photo_ids TEXT[],
        document_ids TEXT[],
        video_ids TEXT[]
    );
"""

insert_car = """
    INSERT INTO cars (user_id, user_login, user_name) values ($1, $2, $3) RETURNING id
"""

insert_field = """
    UPDATE cars SET {field} = $2
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

insert_document = """
    UPDATE cars
    SET document_ids = array_append(document_ids, $2),
    photo_ids = array_append(photo_ids, $3),
    video_ids = array_append(video_ids, $4)
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

select_documents = """
    SELECT photo_ids, document_ids, video_ids FROM cars
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

select_summary = """
    SELECT
        user_login,
        user_name,
        mark,
        model,
        year,
        engine_volume,
        power,
        transmission,
        city,
        contacts,
        price,
        description
FROM cars
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""
