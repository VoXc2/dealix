#!/usr/bin/env python3
"""
Database Backup Script for Dealix

Creates timestamped backups of the database with compression.
Supports local and Docker environments.

Usage:
    python scripts/backup_database.py [--output PATH] [--compress]
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def get_database_config():
    """Extract database configuration from environment."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)
    
    # Parse mysql://user:password@host:port/database
    try:
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        return {
            'user': parsed.username,
            'password': parsed.password,
            'host': parsed.hostname,
            'port': parsed.port or 3306,
            'database': parsed.path[1:],  # Remove leading /
        }
    except Exception as e:
        print(f"ERROR: Failed to parse DATABASE_URL: {e}")
        sys.exit(1)

def create_backup(config, output_dir='backups', compress=True):
    """Create a database backup."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = Path(output_dir) / f"dealix_backup_{timestamp}.sql"
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Check if running in Docker
    in_docker = os.path.exists('/.dockerenv')
    
    try:
        if in_docker:
            # Local MySQL
            cmd = [
                'mysqldump',
                f'-u{config["user"]}',
                f'-p{config["password"]}',
                f'-h{config["host"]}',
                f'-P{config["port"]}',
                config["database"]
            ]
        else:
            # Docker MySQL
            container_name = os.getenv('DB_CONTAINER_NAME', 'dealix-mysql')
            cmd = [
                'docker', 'exec', container_name,
                'mysqldump',
                f'-u{config["user"]}',
                f'-p{config["password"]}',
                config["database"]
            ]
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)
        
        if compress:
            # Compress with gzip
            compressed_file = backup_file.with_suffix('.sql.gz')
            subprocess.run(['gzip', '-f', str(backup_file)], check=True)
            backup_file = compressed_file
        
        print(f"✓ Backup created: {backup_file}")
        print(f"  Size: {backup_file.stat().st_size:,} bytes")
        return str(backup_file)
    
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Backup failed: {e.stderr.decode()}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"ERROR: Command not found: {e}")
        print("Hint: Ensure mysqldump is installed or Docker is running")
        sys.exit(1)

def cleanup_old_backups(output_dir='backups', keep_days=7):
    """Remove backups older than specified days."""
    cutoff = datetime.now().timestamp() - (keep_days * 86400)
    backup_path = Path(output_dir)
    
    if not backup_path.exists():
        return
    
    removed = 0
    for backup_file in backup_path.glob('dealix_backup_*.sql*'):
        if backup_file.stat().st_mtime < cutoff:
            backup_file.unlink()
            print(f"✓ Removed old backup: {backup_file.name}")
            removed += 1
    
    if removed > 0:
        print(f"✓ Cleaned up {removed} old backup(s)")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Dealix Database Backup')
    parser.add_argument('--output', default='backups', help='Output directory')
    parser.add_argument('--compress', action='store_true', default=True, help='Compress backup')
    parser.add_argument('--keep-days', type=int, default=7, help='Keep backups for N days')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Dealix Database Backup")
    print("=" * 60)
    
    config = get_database_config()
    print(f"Database: {config['database']}")
    print(f"Host: {config['host']}:{config['port']}")
    print()
    
    backup_file = create_backup(config, args.output, args.compress)
    cleanup_old_backups(args.output, args.keep_days)
    
    print()
    print("=" * 60)
    print("Backup completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
