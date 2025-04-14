# ⛪️ ST.MARY'S MUNJITI CHURCH BACKEND
![Python](https://img.shields.io/badge/Python-3.8-blue)
![Flask-RESTful](https://img.shields.io/badge/Framework-Flask--RESTful-orange)
![Database](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-blue)
![Deployment](https://img.shields.io/badge/Deployed-Render-success)
![License](https://img.shields.io/badge/License-MIT-green)

## Description
This is a project for the backend for a church website. It helps to access various data for the church.

It uses:
   - Python 3.8
   - Flask-Restful
   - SQLAlchemy
   - SQLite and Postgre 

The website is maintained by church administrators, while any visitor can access the public data through the frontend.

The project majorly depends on these files under the Server directory;
   - models.py: Contains models 
   - seed.py: Contains the sample data stored on the database
   - app.py: Contains the CRUD methods for the data on database

## Installation and usage
   1. Deployed version
      You can access the backend using the following link;
          https://munjiti-backend.onrender.com/

      This uses PostgreSQL for the database

   2. Locally
      - You first fork and clone here on Github
      - You go to the terminal on your computer then install the dependancies using pipenv install && pipenv shell
      - When successful to access the endpoints, you can either use:

              - python app.py
              OR
              - flask run

## 🧾 License
This project is licensed under the [MIT License](./LICENSE).

        
    
