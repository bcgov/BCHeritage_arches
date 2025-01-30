### How to restore a database from a backup file
NB - This will apply any user permissions to the new instance. Verify the user permissions after performing the restore
if moving between instances.
1. Backup current database before dropping it.
2. Ensure the backup file is valid. If it is compressed, uncompress the file to ensure it is valid.
3. Ensure the users match the target database if exporting from one instance and back into a different one:
eg: `bcfms_dlvr`, `proxy_databc_dlvr` in DLVR database
4. Set the search path in the backup file, around line 13:
```
SELECT pg_catalog.set_config('search_path', 'public,databc', false);
```

5. Drop existing database:
```shell
psql -Upostgres << EOF
drop database bcfms_dlvr;
EOF
```
6. Recreate new database:
```shell
psql -Upostgres <<EOF
CREATE DATABASE bcfms_dlvr
    WITH OWNER = bcfms_dlvr
        ENCODING = 'UTF8'
        CONNECTION LIMIT=-1
        TEMPLATE = template_postgis;
EOF
```

7. Import backup file:
```shell
psql -Upostgres bcfms_dlvr < [backup file].sql
```
This should run cleanly.

8. Reindex Arches instance
```shell
sudo -uwwwadm /bin/bash
cd /apps_ux/apps_<env>
source bcfms_<env>_venv/bin/activate
cd bcfms
python manage.py bc_reindex_database
```

9. Compress or delete backup file.