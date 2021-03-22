from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.http_download_operations import HttpDownloadOperator
from airflow.operators.zip_file_operations import UnzipFileOperator
from airflow.operators.hdfs_operations import HdfsPutFileOperator, HdfsGetFileOperator, HdfsMkdirFileOperator
from airflow.operators.filesystem_operations import CreateDirectoryOperator
from airflow.operators.filesystem_operations import ClearDirectoryOperator
from airflow.operators.hive_operator import HiveOperator


args = {
    'owner': 'airflow'
}

dag = DAG('xkcd', default_args=args, description='xkcd practical exam',
          schedule_interval='56 18 * * *',
          start_date=datetime(2019, 10, 16), catchup=False, max_active_runs=1)


create_local_import_dir = CreateDirectoryOperator(
    task_id='create_import_dir',
    path='/home/xkcd',
    directory='imdb',
    dag=dag,
)

clear_local_import_dir = ClearDirectoryOperator(
    task_id='clear_import_dir',
    directory='/home/airflow/xkcd',
    pattern='*',
    dag=dag,
)

download_xkcd_latest = HttpDownloadOperator(
    task_id='download_xkcd_latest',
    download_uri='https://xkcd.com//info.0.json',
    save_to='/home/airflow/xkcd/latest_xkcd.json',
    dag=dag,
)

create_local_import_dir >> clear_local_import_dir >> download_title_ratings