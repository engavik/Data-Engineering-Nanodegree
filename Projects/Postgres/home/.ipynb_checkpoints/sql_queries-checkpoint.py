# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = ("""
create table if not exists songplays (songplay_id text primary key not null, start_time timestamp not null, user_id text not null, level text, song_id text, artist_id text, session_id text not null, location text, user_agent text)
""")

user_table_create = ("""
create table users (user_id text primary key not null, first_name text, last_name text, gender text, level text)
""")

song_table_create = ("""
create table songs (song_id text primary key, title text, artist_id text, year int, duration int)
""")

artist_table_create = ("""
create table artists (artist_id text primary key, name text, location text, latitude float, longitude float)
""")

time_table_create = ("""
create table time (start_time timestamp primary key not null, hour int, day int, week text, month text, year int, weekday text)
""")


# INSERT RECORDS

songplay_table_insert = ("""
insert into songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
on conflict(songplay_id) do nothing
""")

user_table_insert = ("""
insert into users (user_id, first_name, last_name, gender, level)
values(%s, %s, %s, %s, %s)
on conflict(user_id) do update set level = excluded.level
""")

song_table_insert = ("""
insert into songs (song_id, title, artist_id, year, duration)
values(%s, %s, %s, %s, %s)
on conflict(song_id) do nothing
""")

artist_table_insert = ("""
insert into artists (artist_id, name, location, latitude, longitude)
values (%s, %s, %s, %s, %s)
on conflict (artist_id) do nothing
""")


time_table_insert = ("""
insert into time (start_time, hour, day, week, month, year, weekday)
values(%s, %s, %s, %s, %s)
on conflict (start_time) do nothing
""")

# FIND SONGS

song_select = ("""
SELECT ss.song_id, ss.artist_id FROM songs ss 
JOIN artists ars on ss.artist_id = ars.artist_id
WHERE ss.title = %s
AND ars.name = %s
AND ss.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]