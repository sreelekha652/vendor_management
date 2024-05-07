Vendor Management System with Performance Metrics

Develop a Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics


Features
Feature 1: Vendor Profile Management
Feature 2:Purchase Order Tracking .
Feature 3:Vendor Performance Evaluation

Installation

1. Clone the repository: `git clone https://github.com/sreelekha652/vendor_management.git
2. Navigate to the project directory: `cd project_name`
3. Create a virtual environment: `python3 -m venv env`
4. Activate the virtual environment:
   - On Windows: `env\Scripts\activate`
   - On macOS and Linux: `source env/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Set up the database: `python manage.py migrate`
7. Run the development server: `python manage.py runserver`.

Usage
- Make sure the development server is running (`python manage.py runserver`).
- Navigate to the API endpoints using a web browser or API client like Postman.
- API documentation can be found at following link

https://docs.google.com/spreadsheets/d/1xeO2UTuq6NiJiDtx3SH8fUxiGxsTMXnVRS4NrsJV6Hc/edit?usp=sharing

Authentication


This API uses token-based authentication. To obtain a token, send a POST request to http://localhost:8000/vendor/loginapi/ with your username . Include the token in the Authorization header of subsequent requests.
  
