# ftf-re-api
## API Setup Steps
1. Clone the repo
2. Make sure you have python3 installed and this is the version you are using
3. In the terminal:
  - After cloning the repo, navigate to its directory (ftf-re-api) and create a virtual environment (make sure that the environment is called 'venv')
    - Run: `python3 -m venv venv`
  - Activate the environment by running Mac: `source venv/bin/activate`, Windows: `.\venv\scripts\activate`
  - Install dependencies with pip
    - `pip install -r requirements.txt`
4. Setup MySql to run in local machine and setup credentials in .env file (steps below adapted from: https://codeburst.io/installing-and-configuring-mysql-with-django-a7b54b0f27ce)
  - Mac users:
    - MySQL install with homebrew: `brew install mysql`
    - Start MySQL with homebrew: `brew services start mysql`
    - Open MySQL Workbench
  - Windows users:
    - Download MySQLInstaller: https://dev.mysql.com/downloads/installer/
    - If you installed MySQLWorkbench before MySQLInstaller, remove MySQLWorkbench with MySQLInstaller
    - Click "Add.." in MySQLInstaller
    - Select the developer kit, leave defaults as is and install
    - Once everything is installed, click "reconfigure" on the MySQLServer install
    - Give a name to the MySQL Server and start it
    - Open MySQL Workbench
  - In MySQL Workbench, under connections, right click and rescan servers
  - Double click on the local instance connection just created
  - Create a new Schema
    - Click the Schema tab
    - Right-click in the Schema list and select Create Schema
    - Give it a name and follow the prompts to create it
  - Setup a database user
    - Select the Administration tab
    - Select Users and Privileges
    - Click Add Account
    - Give your user a name and password
    - Assign Administrative Roles and Schema Privileges
    - ![alt text](https://miro.medium.com/max/875/1*02UwfaPiNr8mWqSqb3akdg.png)
    
    *If you press on the DBA checkmark it should check all of them, and you're good to go*
5. Create a file inside 'ftf-re-api/reporting_engine/' called '.env'
     - Add these lines to the file:
     ```
      DB_NAME='[db name you assigned to the schema you created in workbench]'
      DB_USER='[db user name you created]'
      DB_PW='[db user password you created]'
      DB_HOST='127.0.0.1'
      DB_PORT='3306'
       
      SOURCE_DB_HOST='freshtrak-focus.cnw8nooqdydn.us-east-2.rds.amazonaws.com'
      SOURCE_DB_USER='[username for source db]'
      SOURCE_DB_PW='[password for source db]'
      SOURCE_DB_NAME='[name for source db]'
      SOURCE_DB_PORT='3306'
      PYTHONPATH =  [path of the reporting engine folder; something like C:\myname\ftf-re-api\reporting_engine]

      ```
     *Replace what's in square brackets, including the square brackets - example: '[db name...]' -> 'reports_beta'*
6. Connect Django to DB and start Django Server
  - Navigate to 'ftf-re-api/reporting_engine/'
  - Make sure MySQL server is running
  - Create migrations: `python manage.py makemigrations`
  - Run migrations: `python manage.py migrate`
  - Load source data: `python manage.py loaddata data.json`
  - Start django server: `python manage.py runserver`
7. If everything was successful, you should be able to navigate to http://localhost:8000 and see django's default index page
8. To navigate to the admin site visit: 'http://localhost:8000/admin'
  - Create your own admin superuser
    - Run: `python manage.py createsuperuser`
    - With the username and password you specify here, you can access the django admin
  - The Django admin is a user interface to see the entries in the database and manage them (modify, delete, add, etc...)
  
**After these steps are finished, all you have to do when coming back to work on the project is to activate the python environment: `source ./venv/bin/activate` (Mac) or `.\venv\scripts\activate` (Windows) and then you can start the django server: `python manage.py runserver`**

## Swagger Documentation
Swager docs may be accessed by going to the url */api/doc*  

If you would like to add a model to Swagger, you must create a serializer as seen in api/serializers.py




## VSCode Setup tips

- To get VSCode to recognize python packages we create:
  1. Go to File->Preferences->Settings
  2. In the Settings window, switch to the Workspace Tab
  3. Expand the extensions pane and select python
  4. For Env File put the path as `${workspaceFolder}/reporting_engine/.env`
  5. Explanation: This will have VSCode load the .env file into its own environment variables. Since we specified the PYTHONPATH in the .env file, VSCode will know where to look for our packages. Otherwise you will get warnings in the IDE when referencing custom packages, like the services package in transform_layer.
