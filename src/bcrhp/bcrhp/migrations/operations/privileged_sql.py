from django.db.migrations.operations.special import RunSQL
from django.db.backends.postgresql.base import DatabaseWrapper
from arches.app.models.system_settings import settings


class RunPrivilegedSQL(RunSQL):
    #
    # Version of the base RunSQL operation that tries to pick up the credentials
    # from the PG_SUPERUSER and PG_SUPERUSER_PW settings. This is used to perform
    # database migrations that require higher level permissions than the application
    # owner role. Replaces the connection in the 
    def __get_connection_settings(self):
        db = dict(settings.DATABASES["default"])

        # Attempt to use extra credentials from settings. If these don't exist
        # or are blank, revert to the default user/password credentials.
        try:
            if settings.PG_SUPERUSER != "" and settings.PG_SUPERUSER_PW != "":
                print("Picking up username %s from PG_SUPERUSER" % settings.PG_SUPERUSER)
                db["USER"] = settings.PG_SUPERUSER
                db["PASSWORD"] = settings.PG_SUPERUSER_PW
            else:
                print("Using default username/password")
                
        except AttributeError:
            pass

        return db

    def database_forwards(self, app_label, schema_editor, from_state, to_state):

        database_wrapper = DatabaseWrapper(settings_dict=self.__get_connection_settings())
        schema_editor.connection = database_wrapper
        super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        database_wrapper = DatabaseWrapper(settings_dict=self.__get_connection_settings())
        schema_editor.connection = database_wrapper
        return super().database_backwards(app_label, schema_editor, from_state, to_state)



