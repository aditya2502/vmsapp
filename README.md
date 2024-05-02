# Vendor Management System API

This is a Vendor Management System API built using Django and Django REST Framework. It allows you to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd vendor-management-system
2. Install Dependencies:
pip install -r requirements.txt
3. Configure the Database:
Update the database settings in settings.py to use your preferred database (SQLite, PostgreSQL, MySQL, etc.).
Run migrations to create database schema:
python manage.py migrate
4. Create Superuser (Optional):
Create a superuser to access the Django admin interface:
python manage.py createsuperuser
5. Run the Django Development Server:
   python manage.py runserver
6. Access the API:
Open your web browser and go to http://127.0.0.1:8000/api/ to access the API root.
Use the Django admin interface at http://127.0.0.1:8000/admin/ to manage database records (if applicable).

API Endpoints
Vendor Profile Management
POST /api/vendors/
Create a new vendor profile.
Request Body: JSON object containing vendor details.
Response: JSON object representing the newly created vendor profile.


GET /api/vendors/
List all vendor profiles.
Response: JSON array containing details of all vendor profiles.Vendor Performance Endpoint

GET /api/vendors/{vendor_id}/performance/
Retrieve performance metrics for a specific vendor.
Parameters: vendor_id - ID of the vendor.
Response: JSON object containing performance metrics.
