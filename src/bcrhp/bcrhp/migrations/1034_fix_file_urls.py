from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from arches.app.models.graph import Graph
from arches.app.models.models import Node
from guardian.shortcuts import assign_perm, remove_perm


backup_images_table_sql = """
    create table heritage_site.backup_1034_site_images as
        select * from heritage_site.site_images
        where site_images->0->>'url' !~ '^/files';
    """

reverse_backup_images_table_sql = """
    drop table heritage_site.backup_1034_site_images;
    """

backup_document_table_sql = """
    create table heritage_site.backup_1034_site_document as
        select * from heritage_site.site_document
        where site_document->0->>'url' !~ '^/files';
    """

reverse_backup_document_table_sql = """
    drop table heritage_site.backup_1034_site_document;
    """

fix_images_sql = """
    update heritage_site.site_images
        set site_images = jsonb_set(site_images, '{0,url}', to_jsonb(regexp_replace(site_images->0->>'url', '^/bcrhp', '')))
    where site_images->0->>'url' !~ '^/files';
    """

reverse_fix_images_sql = """
    update heritage_site.site_images i
        set site_images = b.site_images
        from heritage_site.backup_1034_site_images b
    where b.tileid = i.tileid;
    """

fix_documents_sql = """
    update heritage_site.site_document
        set site_document = jsonb_set(site_document, '{0,url}', to_jsonb(regexp_replace(site_document->0->>'url', '^/bcrhp', '')))
    where site_document->0->>'url' !~ '^/files';
    """

reverse_fix_documents_sql = """
    update heritage_site.site_document i
        set site_document = b.site_document
        from heritage_site.backup_1034_site_document b
    where b.tileid = i.tileid;
    """


class Migration(migrations.Migration):
    dependencies = [
        ("bcrhp", "910_update_heritage_usernames"),
    ]

    operations = [
        migrations.RunSQL(
            backup_images_table_sql,
            reverse_backup_images_table_sql,
        ),
        migrations.RunSQL(
            backup_document_table_sql,
            reverse_backup_document_table_sql,
        ),
        migrations.RunSQL(
            fix_images_sql,
            reverse_fix_images_sql,
        ),
        migrations.RunSQL(
            fix_documents_sql,
            reverse_fix_documents_sql,
        ),
    ]
