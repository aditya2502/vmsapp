Completed Project

# Vendor Management System

## Overview
This is a Vendor Management System (VMS) that allows vendors to manage their associated products and to track their related Purchase orders It also provides matrics which gives insightful analysis of their Purchase Orders :-

 Vendor Metrics:
1. On-Time Delivery Rate: Percentage of orders delivered by the promised date.
2. Quality Rating: Average of quality ratings given to a vendorfs purchase orders.
3. Response Time: Average time taken by a vendor to acknowledge or respond to purchase orders .
4. Fulfilment Rate: Percentage of purchase orders fulfilled without issues.

```Admin Username: admin```
```Admin Password: admin```  

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/aditya2502/VendorManagementSystem.git

## Configuration

1. **Open a Command Prompt:**

- On Windows, you can use Command Prompt or PowerShell.

2. **Navigate to Your Project Directory:**
   ```bash
   cd path/to/your/project

3. **Create a Virtual Environment:**
   ```bash
   python -m venv venv

4. **Activate the Virtual Environment:**
   ```bash
   venv\Scripts\activate

5. **Install Packages from requirements.txt:**
   ```bash
   pip install -r requirements.txt

## Usage

1. **Run The Django Server:**

   ```bash
   python manage.py runserver
   
2. **API Endpoints For Vendors:**

   - POST ```/api/vendors/```: Create a new vendor.
   - GET ```/api/vendors/```: List all vendors.
   - GET ```/api/vendors/{vendor_id}/```: Retrieve a specific vendor's details.
   - PUT ```/api/vendors/{vendor_id}/```: Replace a vendor's details.
   - PATCH ```/api/vendors/{vendor_id}/```: Update a vendor's details.
   - DELETE ```/api/vendors/{vendor_id}/```: Delete a vendor.
   - GET ```/api/vendors/{vendor_id}/performance/```: Retrieve a vendor's performance metrics.

3. **API Endpoints For Purchase Orders:**

    - POST ```/api/purchase_orders/```: Create a purchase order.
    - GET ```/api/purchase_orders/```: List all purchase orders
    - GET ```/api/purchase_orders/?vendor=1```: List all purchase orders filtered by vendor
    - GET ```/api/purchase_orders/{po_id}/```: Retrieve details of a specific purchase order.
    - PUT ```/api/purchase_orders/{po_id}/```: Replace a purchase order.
    - PATCH ```/api/purchase_orders/{po_id}/```: Update a purchase order.
    - DELETE ```/api/purchase_orders/{po_id}/```: Delete a purchase order.
    - GET ```/api/purchase_orders/{po_id}/acknowledge/```: for vendors to acknowledge

