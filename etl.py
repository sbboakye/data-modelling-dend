import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
cur = conn.cursor()
conn.set_session(autocommit=True)


def process_song_file(cur, filepath):
    """
    Extract data from the song folder and insert
    input into database
    
    :param cur: cursor from database connection
    :param filepath: path to datasets
    """
    data = pd.read_json(filepath, lines=True)
    # open song file
    df = data[['song_id', 'title', 'artist_id', 'year', 'duration']]

    # insert song record
    song_data = df.values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_df = data[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    
    artist_data = artist_df.values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Extract data from the log folder and insert
    input into database
    
    :param cur: cursor from database connection
    :param filepath: path to datasets
    """
    
    data = pd.read_json(filepath, lines=True)
    # open log file
    df = data

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = []

    time_data.append(df.ts.tolist())
    time_data.append(df.ts.dt.day.tolist())
    time_data.append(df.ts.dt.weekofyear.tolist())
    time_data.append(df.ts.dt.month.tolist())
    time_data.append(df.ts.dt.year.tolist())
    time_data.append(df.ts.dt.weekday.tolist())
    
    column_labels = ['timestamp', 'hour', 'day', 'week_of_year',
                'month', 'year', 'weekday']
    dict_data = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame(dict_data)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = data[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = user_df.copy()
    user_df.dropna(inplace=True)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Extract data from the song folder and insert
    input into database
    
    :param cur: cursor from database connection
    :param conn: connection to database
    :param filepath: path to datasets
    :param func: function to be used to process/insert data
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
