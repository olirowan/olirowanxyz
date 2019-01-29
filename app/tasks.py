import os
import time
import pipes
import pathlib
from app import app, task_schedule

backup_path = app.config['BACKUP_PATH']
mysql_backup_db = app.config['MYSQL_DB_NAME']
mysql_backup_user = app.config['MYSQL_BACKUP_USER']
mysql_backup_pass = app.config['MYSQL_BACKUP_PASS']

@task_schedule.scheduled_job('cron', day_of_week='sat', hour=23)
def create_database_backup():

    backup_time = time.strftime('%Y%m%d-%H%M%S')
    db_backup_path = backup_path + '/database/' + backup_time + '/'
    pathlib.Path(db_backup_path).mkdir(parents=True, exist_ok=True)

    app.logger.info("Starting database backup at: " + backup_time)
    mysqldump_process = "mysqldump" + " -u " + mysql_backup_user + " -p" + mysql_backup_pass + " " + mysql_backup_db\
                        + " > " + pipes.quote(db_backup_path) + mysql_backup_db + ".sql"
    os.system(mysqldump_process)

    compress_backup_process = "gzip " + pipes.quote(db_backup_path) + db_backup_path + ".sql"
    os.system(compress_backup_process)

    backup_complete_time = time.strftime('%Y%m%d-%H%M%S')
    app.logger.info("Completed database backup at: " + backup_complete_time)