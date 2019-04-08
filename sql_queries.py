# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL PRIMARY KEY, timestamp timestamp, 
    user_id int, level varchar, song_id text, artist_id text, 
    session_id int, location varchar, user_agent varchar);
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (user_id int NOT NULL PRIMARY KEY, first_name text,
    last_name text, gender text, level text);
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (song_id text NOT NULL PRIMARY KEY, title text, artist_id text, year int, duration decimal);
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (artist_id text NOT NULL PRIMARY KEY, name text,
    location text, latitude decimal, longitude decimal);
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (id SERIAL PRIMARY KEY, timestamp timestamp, hour int, day int, 
    week_of_year int, month int, year int);
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (timestamp, 
    user_id, level, song_id, artist_id, 
    session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO NOTHING;
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = ("""
    INSERT INTO time (timestamp, hour, day, week_of_year, month, year)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
""")

# FIND SONGS

song_select = ("""
    SELECT s.song_id, a.artist_id
    FROM songs s
    JOIN artists a
    ON s.artist_id = a.artist_id
    WHERE s.title = (%s)
    AND a.name = (%s)
    AND s.duration = (%s);
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]