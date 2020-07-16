import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']

"""Creates SparkSession
   Creates SparkSession and returns it. If SparkSession is already created it returns
   the currently running SparkSession."""


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark



def process_song_data(spark, input_data, output_data):
    
     """
        This function loads song_data from S3, processes songs and artist tables load them back to S3
        
        Parameters:
            spark       = Spark Session
            input_data  = location of song_data where the file is loaded to process
            output_data = location of the results stored
    """
    
    # get filepath to song data file
    song_data = os.path.join(input_data,"song_data/*/*/*/*.json")
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = spark.sql("""
                            select distinct s.song_id, s.title, 
                            s.artist_id, s.year, s.duration 
                            from songs_table s 
                            where song_id is not null """)
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy("year", "artist_id").parquet(output_data+'songs_table/')

    # extract columns to create artists table
    artists_table = spark.sql(""" select distinct a.artist_id, a.artist_name,
                                  a.artist_location, a.artist_latitude,
                                  a.artist_longitude
                                  from songs_table a
                                  where a.artist_id is not null """)
    
    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data+'artists_table/')

   

def process_log_data(spark, input_data, output_data):
    
    """
    This function loads log_data from S3, processes songs and artist tables and loaded them back to S3.
    Parameters:
            spark       = Spark Session
            input_data  = location of song_data where the file is loaded to process
            output_data = location of the results stored
    """
    
    # get filepath to log data file
    log_data = os.path.join(input_data, "log_data/*.json")

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    users_table = spark.sql(""" select distinct l.userId as user_id, 
    l.firstName as first_name, l.lastName as last_name, 
    l.gender as gender, l.level as level 
    from logs_table l
    where l.userId is not null """)
    
    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(output_data+'users_table/')
    
    # extract columns to create time table
    time_table = spark.sql("""
                            SELECT 
                            A.start_time_sub as start_time,
                            hour(A.start_time_sub) as hour,
                            dayofmonth(A.start_time_sub) as day,
                            weekofyear(A.start_time_sub) as week,
                            month(A.start_time_sub) as month,
                            year(A.start_time_sub) as year,
                            dayofweek(A.start_time_sub) as weekday
                            FROM
                            (SELECT to_timestamp(timeSt.ts/1000) as start_time_sub
                            FROM log_data_table timeSt
                            WHERE timeSt.ts IS NOT NULL
                            ) A
                        """)
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy("year", "month").parquet(output_data+'time_table/')

    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data+'songs_table/')

def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
