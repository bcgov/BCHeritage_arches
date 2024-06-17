import socket
import time
import urllib
from urllib import request, parse
from urllib.error import HTTPError, URLError
import json
import psycopg2
import ssl
from http.client import InvalidURL
import csv

csv_filename = "./all_urls.csv"
validated_csv_filename = "./validated_urls.csv"

db_user="<bcrhp username>"
db_password="<bcrhp user password>"
db_host="localhost"
db_port="5432"
db_database="<bcrhp database>"

get_urls=False

class UrlValidator:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # max_rows = 30000
    max_rows = 10000
    #max_rows = 30
    current_row = 0

    def get_connection(self):
        conn =  psycopg2.connect(user=db_user,
                                 password=db_password,
                                 host=db_host,
                                 port=db_port,
                                 database=db_database)
        conn.set_session(readonly=True)
        return conn

    def validate_all_urls(self):
        if get_urls:
            file1 = open(csv_filename, "w")
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("""select distinct external_url->>'url' from heritage_site.external_url order by 1 limit %s""" % self.max_rows)
            url_rows = cursor.fetchall()
            file1.write(self.get_header())
            for row in url_rows:
                file1.write('"%s", "%s"\n' % (row[0], ""))
            file1.close()
        with open(csv_filename, "r") as csvfile:
            with open(validated_csv_filename, "w") as csv_output_file:
                csv_output_file.write(self.get_header())
                reader = csv.reader(csvfile, delimiter=",", quotechar="\"", skipinitialspace=True,)
                for row1 in reader:
                    if row1[1]:
                        print("Already Validated %s" % row1[1])
                        csv_output_file.write('"%s", "%s"\n' % (row1[0],row1[1]))
                    else:
                        print("Need to validate %s" % row1[1])
                        self.validate_url(row1[0], csv_output_file)

    def get_header(self):
        return '"URL", ' \
               '"Valid"\n'

    def validate_url(self, url, file):
        response = None
        try:
            self.current_row += 1
            parsed_url = parse.urlparse(url)
            if "bcarchives" in url:
                print("Bypassing")
                file.write('"%s", "%s"\n' % (url, "Bypassing - has rate limiter"))
            elif " " in url.strip():
                print("Bypassing")
                file.write('"%s", "%s"\n' % (url, "Bypassing - invalid URL format"))
            else:
                socket.gethostbyname(str(parsed_url.hostname))
                print("%s: %s" %(self.current_row, url))
                response = urllib.request.urlopen(url, context=self.ctx)
                file.write('"%s", "%s"\n' % (url, 'Valid %s' % response.getcode()))
        except socket.error as e:
            print(e)
            file.write('"%s", "%s"\n' % (url, str(e)))
        except HTTPError as e:
            print(e.getcode())
            print(response.info())
            file.write('"%s", "%s"\n' % (url, str(e.getcode())))
        except InvalidURL as e:
            print(e)
            print(response.info())
            file.write('"%s", "%s"\n' % (url, str(e)))
        except Exception as e:
            print(e)
            file.write('"%s", "%s"\n' % (url, str(e)))


if __name__ == '__main__':
    # creates an instance of the class
    start_time = time.time()
    validator = UrlValidator()
    validator.validate_all_urls()
    end_time = time.time()
    print("%s:%s:%s" % (int((end_time - start_time)/3600), int((end_time - start_time)/60), int((end_time - start_time)%60)))
