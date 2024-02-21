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
        price INTEGER,
        description TEXT,
        photo_ids TEXT[],
        document_ids TEXT[]
    );
"""

insert_car = """
    INSERT INTO cars (user_id, user_login, user_name) values ($1, $2, $3) RETURNING id
"""

insert_field = """
    UPDATE cars SET {field} = $2
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

# insert_model = """
#     UPDATE cars SET model = $2
#     WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
# """

# insert_year = """
#     UPDATE cars SET year = $2
#     WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
# """

# insert_engine_volume = """
#     UPDATE cars SET engine_volume = $2
#     WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
# """
# insert_engine_power = """
#     UPDATE cars SET engine_power = $2
#     WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
# """


# insert_document = """
#     UPDATE cars
#     SET document_ids = array_append(document_ids, $2),
#     photo_ids = array_append(photo_ids, $3)
#     WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
# """

# select_documents = """
#     SELECT photo_ids, document_ids FROM cars
#     WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
# """

# select_summary = """
#     SELECT restriction, number_of_keys, tire, drive_type, user_login, user_name FROM cars
#     WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
# """
