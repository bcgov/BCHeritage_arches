# BC Fossil Management System
BC Fossil Management Office implementation of Arches
![Lifecycle:Maturing](https://img.shields.io/badge/Lifecycle-Maturing-007EC6)

### Running in Docker
**These steps assume that the base directory is ~/git.**
1. Start Docker Desktop
2. Create the Arches Dependency Containers:
``` shell
cd ~/git
git clone https://github.com/bcgov/arches-dependency-containers
cd arches-dependency-containers/arches-7-5-2
docker compose up
```
This should result in a set of docker containers that have the base dependency software to run
Arches (Postgres, Elasticsearch, Redis, etc).

3. Clone BCGov Arches Core at the same level as this directory. Assuming that all dependencies
   are installed in ~/git/bcfms/ by running `git clone  https://github.com/bcgov/BCHeritage_arches bcfms`.
``` shell
cd git/bcfms/src
git clone https://github.com/bcgov/arches
git clone https://github.com/bcgov/arches_common
cd arches && git checkout stable/7.6.4.1_bcgov
# This should result in a directory structure like the below:
~/git/bcfms/
     /bcfms/src/arches/         # <- This is a clone of the arches bcgov/arches repo
     /bcfms/src/bcfms/          # <- This directory
     /bcfms/src/arches_common/   # <- This is a clone of the bcgov/arches_common repo
```


4. Change back to the src/bcfms directory and create the test user data file at
   `bcfms/management/data/test_user_list.py`:

    1. the password is only a dummy password so it can be left as is. OIDC is used so when
       authenticating you will use your IDIR username and password.
    2. the `@idir` suffix is necessary
    3. tht `<idir username>` must be in lower case
``` python
def get_user_list():
   return (
   {"name": "<idir username>@idir", "email": "<email>", "password": "Test12345!", "is_superuser": True,
   "is_staff": True, "first_name": "<first name>", "last_name": "<last name>",
   "groups": ["Resource Editor", "Resource Reviewer", "FMO", "Resource Exporter"]},
   )
```

5. Create the `git/bcfms/src/bcfms/.env` file using the dot.env.j2 as a template.
- The AUTH_BYPASS_HOSTS should include the webpack container name and IP address, `localhost` and the bcfms container
name and IP address. This is typically not available until after creating the container in the next step, so the 
webpack build will fail. After creating the container add the 2 IP addresses to the `AUTH_BYPASS_HOSTS` parameter and
restart the containers. The webpack build should work the second time around
- Fill in all .env variables with `{{ }}` values, substituting the appropriate values.

6. Create the BCFMS containers (this will fail the first time):
```shell
cd git/bcfms/src/bcfms
docker compose up
```

You should now be able to access BCFMS at http://localhost:81/bc-fossil-management

6. After logging into BCFMS, the map will initially be blank. Navigate to the system settings in the LHS
   menu and enter your Mapbox token there.