import oracledb
import re
from django.conf import settings


class HriaDao:
    DEBUG = True
    HRIA_USER = 'BCRHP_ARCHES'

    def __init__(self):
        pass

    def __get_connection(self):
        hria_config = settings.HRIA_DATABASE
        print(hria_config)
        connection = oracledb.connect(user=hria_config["USER"], password=hria_config["PASSWORD"],
                                      host=hria_config["HOST"], port=hria_config["PORT"], service_name=hria_config["SERVICE_NAME"])
        if self.DEBUG:
            cursor = connection.cursor()
            for row in cursor.execute("select * from v$version"):
                print(row)

        return connection

    def get_next_borden_sequence(self, borden_grid):
        with self.__get_connection() as connection:
            with connection.cursor() as cursor:
                row = cursor.execute("""select nvl(max(max_seq) + 1,1) from 
                                        (select max(bordensequence) max_seq from sde.a101 where bordennumber like :borden_grid||'%' union 
                                        select max(bordensequence) from sde.tfm_site where bordennumber like :borden_grid||'%') a""", borden_grid=borden_grid).fetchone()
                print("Next ID: %s" % row[0])
                retval = "%s-%s" % (borden_grid, row[0])
                print(retval)
                return retval

    def borden_number_exists(self, borden_number):
        connection = self.__get_connection()
        cursor = connection.cursor()
        row = cursor.execute("""select count(*) from 
            (select 1 from sde.a101 where bordennumber = :borden_number union 
            select 1 from sde.tfm_site where bordennumber = :borden_number) a""", borden_number=borden_number).fetchone()
        print("Exists? %s" % (row[0] != 0))
        return row[0] != 0

    def reserve_borden_number(self, borden_number, is_heritage_site, resourceinstanceid):
        connection = self.__get_connection()
        with connection.cursor() as cursor:
            try:
                version_exists = cursor.execute("""SELECT COUNT (1) FROM sde.versions WHERE name = :bcrhp_user""", bcrhp_user=self.HRIA_USER).fetchone()
                print("Version exists? %s" % version_exists)
                if version_exists[0] == 0:
                    cursor.callproc('sde.version_user_ddl.create_version',
                                    ['SDE.DEFAULT',
                                     self.HRIA_USER,
                                     2,
                                     1,
                                     'Generate next borden number sequence'])

                cursor.callproc('sde.version_util.set_current_version', [self.HRIA_USER])
                cursor.callproc('sde.version_user_ddl.edit_version', [self.HRIA_USER, 1])
                cursor.execute("""insert into SDE.VMV_TFM_SITE(
                        --, --        OBJECTID                  NUMBER(38)
                        MODIFIEDBY, --                VARCHAR2(30)
                        MODIFIEDON, --               DATE
                        MODIFIEDUSING , --            VARCHAR2(30)
                        BORDENNUMBER, --             VARCHAR2(13)
                        BORDENUPPER, --              VARCHAR2(2)
                        BORDENLOWER, --              VARCHAR2(2)
                        BORDENSEQUENCE, --           NUMBER(10)
                        CREATIONDATE, --             DATE
                        SITEFORMUSERID, --           VARCHAR2(30)
                        -- FORMRECEIVED, --             DATE
                        REGISTRATIONSTATUS, --       VARCHAR2(20)
                        -- DOCUMENTKEY, --              NUMBER(10)
                        -- SITEPARENTOID, --            NUMBER(10)
                        -- XX_ARSI_ID, --               NUMBER(10)
                        -- SHAPE, --                    NUMBER(38)
                        APPROVALFLAG, --             VARCHAR2(20)
                        -- PACCUPDATEDDATE, --          DATE
                        -- PACCPROJOFFICER, --          VARCHAR2(40)
                        -- PACCFLAGFLIPPEDDATE, --      DATE
                        CREATEDON, --                DATE
                        CREATEDBY, --                VARCHAR2(30)
                        CREATEDUSING, --             VARCHAR2(30)
                        ISHERITAGESITE, --           VARCHAR2(1)
                        -- REGISTRATIONDATE, --         DATE
                        IMPORTPK --                 VARCHAR2(100)
                        -- IMPORTFK, --                 VARCHAR2(100)
                        -- SDE_STATE_ID, --             NUMBER
                    )
                    values (:bcrhp_user,
                        sysdate,
                        'SQL',
                        :borden_number,
                        :borden_upper,
                        :borden_lower,
                        :borden_sequence,
                        sysdate,
                        :bcrhp_user,
                        'Decision Pending',
                        'NEW',
                        sysdate,
                        :bcrhp_user,
                        'SQL',
                        :is_heritage_site,
                        :arches_uuid
                           )""", bcrhp_user=self.HRIA_USER,
                               borden_number=borden_number,
                               borden_upper= re.sub(r'(.)(.)(.)(.)-.*',r'\1\3',borden_number),
                               borden_lower= re.sub(r'(.)(.)(.)(.)-.*',r'\2\4',borden_number),
                               borden_sequence= re.sub(r'.*-',r'',borden_number),
                               is_heritage_site=is_heritage_site,
                               arches_uuid=resourceinstanceid)

                connection.commit()
            except oracledb.Error as tx_error:
                print("Unable to reserve borden number: %s" % str(tx_error))
                # Probably don't need to do this but making it explicit
                connection.rollback()
