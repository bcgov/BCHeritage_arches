import logging
import oracledb
import re
from django.conf import settings


logger = logging.getLogger(__name__)


class HriaDao:
    DEBUG = True

    def __init__(self):
        pass

    def __get_connection(self):
        hria_config = settings.HRIA_DATABASE
        connection = oracledb.connect(
            user=hria_config["USER"],
            password=hria_config["PASSWORD"],
            host=hria_config["HOST"],
            port=hria_config["PORT"],
            service_name=hria_config["SERVICE_NAME"],
        )
        if self.DEBUG:
            cursor = connection.cursor()
            for row in cursor.execute("select * from v$version"):
                logger.debug("Database version %s" % str(row))

        return connection

    def get_next_borden_sequence(self, borden_grid):
        with self.__get_connection() as connection:
            with connection.cursor() as cursor:
                row = cursor.execute(
                    """select nvl(max(max_seq) + 1,1) from 
                                        (select max(bordensequence) max_seq from sde.a101 where bordennumber like :borden_grid||'%' union 
                                         select max(bordensequence) from sde.tfm_site where bordennumber like :borden_grid||'%') a""",
                    borden_grid=borden_grid,
                ).fetchone()
                logger.debug("Next Borden Number %s-%s" % (borden_grid, row[0]))
                return "%s-%s" % (borden_grid, row[0])

    def validate_borden_number(self, borden_number, resourceinstanceid, conn=None):
        connection = conn if conn is not None else self.__get_connection()
        with connection.cursor() as cursor:
            row = cursor.execute(
                """select bordennumber, importpk from SDE.A101 where bordennumber = :borden_number 
                                    union select bordennumber, importpk from SDE.TFM_SITE where bordennumber = :borden_number""",
                borden_number=borden_number,
            ).fetchone()
            logger.debug("Exists? %s" % (row is not None))
            if row is not None and str(row[1]) != str(resourceinstanceid):
                raise ValueError(
                    "Borden Number %s already exists in HRIA" % borden_number
                )

            row = cursor.execute(
                """select bordennumber from SDE.A101 where IMPORTPK = :resource_id union 
                 select bordennumber from SDE.TFM_SITE where IMPORTPK = :resource_id""",
                resource_id=resourceinstanceid,
            ).fetchone()
            if row is not None and row[0] != borden_number:
                raise ValueError(
                    "Heritage Site %s is already associated with Borden Number %s in HRIA"
                    % (resourceinstanceid, row[0])
                )

    def reserve_borden_number(
        self, borden_number, is_heritage_site, resourceinstanceid
    ):
        # Checks
        hria_application_user = settings.HRIA_DATABASE["APPLICATION_USER"].upper()
        hria_schema = settings.HRIA_DATABASE["USER"].upper()
        logger.debug("HRIA user: %s, schema: %s" % (hria_application_user, hria_schema))
        logger.debug(
            "Borden number: %s, resourceinstanceid: %s, is_heritage_site: %s"
            % (borden_number, resourceinstanceid, is_heritage_site)
        )
        connection = self.__get_connection()
        with connection.cursor() as cursor:
            try:
                # Do one last validation prior to trying to reserve the borden number
                self.validate_borden_number(
                    borden_number, resourceinstanceid, connection
                )
                version_exists = cursor.execute(
                    """SELECT COUNT (1) FROM sde.versions WHERE name = :bcrhp_user""",
                    bcrhp_user=hria_application_user,
                ).fetchone()
                logger.debug("Version exists? %s" % version_exists)
                if version_exists[0] == 0:
                    cursor.callproc(
                        "sde.version_user_ddl.create_version",
                        [
                            "SDE.DEFAULT",
                            hria_application_user,
                            2,
                            1,
                            "Generate next borden number sequence",
                        ],
                    )

                cursor.callproc(
                    "sde.version_util.set_current_version", [hria_application_user]
                )
                cursor.callproc(
                    "sde.version_user_ddl.edit_version", [hria_application_user, 1]
                )
                cursor.execute(
                    """insert into SDE.VMV_TFM_SITE(
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
                           )""",
                    bcrhp_user=hria_application_user,
                    borden_number=borden_number,
                    borden_upper=re.sub(r"(.)(.)(.)(.)-.*", r"\1\3", borden_number),
                    borden_lower=re.sub(r"(.)(.)(.)(.)-.*", r"\2\4", borden_number),
                    borden_sequence=re.sub(r".*-", r"", borden_number),
                    is_heritage_site=is_heritage_site,
                    arches_uuid=resourceinstanceid,
                )

                # Add a row to the reconcile log to kick off the process
                # Here the version is <HRIA DB Schema>.<Version Name> - eg 'BFERGUSO.BCRHP_ARCHES'
                #   HRIA DB Schema: Oracle DB schema that created the version
                #   Version Name: Name of the version - using BCRHP_ARCHES
                cursor.execute(
                    """INSERT INTO SDE.TFM_SYS_RECONCILE_LOG
                                        (VERSION, 
                                        VERSION_PARENT, 
                                        RECONCILE_STATUS, 
                                        RECONCILE_SUBMIT, 
                                        DELETE_VERSION, 
                                        MODIFIEDBY, 
                                        MODIFIEDON, 
                                        MODIFIEDUSING)
                                    VALUES (
                                        :version, 
                                        'SDE.DEFAULT', 
                                        'SUBMITTED', 
                                        SYSDATE, 
                                        'Y', 
                                        'SQL', 
                                        SYSDATE, 
                                        'SQL'
                                      )""",
                    version="%s.%s" % (hria_schema, hria_application_user),
                )
                connection.commit()
            except oracledb.Error as tx_error:
                # Probably don't need to do this but making it explicit
                connection.rollback()
                logger.error("Unable to reserve borden number: %s" % str(tx_error))
                raise RuntimeError(
                    "Unable to reserve borden number. Please check logs for root cause."
                )
