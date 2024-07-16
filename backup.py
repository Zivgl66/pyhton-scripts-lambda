import os
import shutil
from datetime import datetime, timedelta
import time

# Configuration
SOURCE_DIR = '/home/ziv/git/tobackup/'
BACKUP_DIR = '/home/ziv/git/backup'
DAILY_DIR = os.path.join(BACKUP_DIR, 'daily')
WEEKLY_DIR = os.path.join(BACKUP_DIR, 'weekly')
MONTHLY_DIR = os.path.join(BACKUP_DIR, 'monthly')

def create_backup(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    dest_path = os.path.join(dest, f'backup_{timestamp}')
    shutil.copytree(src, dest_path)
    print(f'Backup created at {dest_path}')

def cleanup_old_backups(backup_dir, retention_days):
    now = time.time()
    for filename in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, filename)
        if os.stat(file_path).st_mtime < now - retention_days * 86400:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f'Removed old backup {file_path}')

def main():
    # Create daily backup
    create_backup(SOURCE_DIR, DAILY_DIR)
    
    # Create weekly backup (every Sunday)
    if datetime.now().weekday() == 6:  # 6 corresponds to Sunday
        create_backup(SOURCE_DIR, WEEKLY_DIR)
    
    # Create monthly backup (on the 1st of every month)
    if datetime.now().day == 1:
        create_backup(SOURCE_DIR, MONTHLY_DIR)

    # Cleanup old backups
    cleanup_old_backups(DAILY_DIR, 7)    # Keep daily backups for 7 days
    cleanup_old_backups(WEEKLY_DIR, 30)  # Keep weekly backups for 30 days
    cleanup_old_backups(MONTHLY_DIR, 365) # Keep monthly backups for 365 days

if __name__ == '__main__':
    main()