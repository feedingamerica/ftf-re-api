# ftf-re-api
## API Setup Steps
1. Clone the repo
2. Make sure you have python3 installed and this is the version you are using
3. In the terminal:
  - After cloning the repo, navigate to its directory (ftf-re-api) and create a virtual environment (make sure that the environment is called 'venv')
    - Run: `python3 -m venv venv`
  - Activate the environment by running `source venv/bin/activate`
  - Install dependencies with pip
    - `pip install -r requirements.txt`
4. Setup MySql to run in local machine and setup credentials in .env file
  - **Important: In (b) only follow instructions up to "Setup a database user"**
  - Follow the steps found here: https://codeburst.io/installing-and-configuring-mysql-with-django-a7b54b0f27ce
  - Installation and running instructions are for Mac, lookup installation instructions for Windows
  - To rescan servers, right click on MySQL Workbench
  - Create a .env file inside 'ftf-re-api/reporting_engine/'
     - Add these lines to the file:
     ```
       export DB_NAME='[db name you assigned to the schema in step (b)]'
       export DB_USER='[db user name you created]'
       export DB_PW='[db user password you created]'
       export DB_HOST='127.0.0.1'
       export DB_PORT='3306' ```
       *Replace what's in square brackets - example: '[db name...]' -> 'reports_beta'*
5. Connect Django to DB and start Django Server
  - Navigate to 'ftf-re-api/reporting-engine/'
  - Make sure MySQL server is running
  - Run: `python manage.py migrate`
  - Start django server: `python manage.py runserver`
6. If everything was successful, you should be able to navigate to http://localhost:8000 and see django's default index page
7. To navigate to the admin site visit: 'http://localhost:8000/admin'
  - Josean Martinez has the credentials for the super user, let him know to see how he can get that to you.
  - If not, you could also create your own admin superuser
    - Run: `python manage.py createsuperuser`
    - With the username and password you specify here, you can access the django admin
  - The Django admin is a user interface to see the entries in the database and manage them (modify, delete, add, etc...)
  
**After these steps are finished, all you have to do when coming back to work on the project is to activate the python environment: `source ./venv/bin/activate` and then you can start the django server**

  
  
  
