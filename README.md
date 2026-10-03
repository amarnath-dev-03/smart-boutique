# 🧵 Smart Boutique

## Smart Tailoring & Boutique Management System

**Smart Boutique** is a full-stack Django web application designed to help tailoring and boutique businesses manage their daily operations from a single platform.

The system provides modules for customer management, measurements, products, inventory, orders, payments, expenses, invoices, dashboards, and business reports.

## 🌐 Live Demo

**Live Website:**
https://smart-boutique-29cq.onrender.com/

**GitHub Repository:**
https://github.com/amarnath-dev-03/smart-boutique

> The application is deployed using Render with PostgreSQL as the production database.

## ✨ Features

### 🔐 Authentication

* User Login & Logout
* Password visibility toggle
* Forgot Password
* Email OTP verification
* OTP expiry validation
* Password reset
* Protected dashboard access
* Secure password hashing

### 👥 Customer Management

* Add customers
* View customer details
* Edit customer information
* Delete customers
* Search customers

### 📏 Measurement Management

* Add customer measurements
* View measurement details
* Edit measurements
* Delete measurements
* Search measurements
* Connect measurements with customers

### 👕 Product Management

* Add products
* View product details
* Edit products
* Delete products
* Product categories
* Product pricing

### 📦 Inventory Management

* Add inventory items
* View inventory details
* Edit inventory
* Delete inventory
* Search inventory
* Stock tracking

### 🧾 Order Management

* Create orders
* Edit orders
* View order details
* Manage order items
* Edit order items
* Delete order items
* Automatic item totals
* Automatic order total calculation
* Order status tracking

### 💳 Payment Management

* Record customer payments
* Link payments with orders
* Cash / UPI / Card / Bank Transfer
* Payment history
* Payment status
* Paid amount tracking
* Pending balance calculation

### 💰 Expense Management

* Add expenses
* Edit expenses
* Delete expenses
* Expense categories
* Expense tracking

### 📄 Invoice & Reports

* Generate professional PDF invoices
* Customer details
* Order details
* Product details
* Quantity and price
* Total amount
* Business reports
* Financial summaries
* Monthly business reports
* Payment summaries
* Expense summaries

### 📊 Dashboard

The dashboard provides an overview of the business with:

* Customer statistics
* Product statistics
* Inventory statistics
* Order statistics
* Measurement statistics
* Payment statistics
* Expense statistics
* Charts and reports
* Order status information
* Recent orders
* Quick actions

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

### Backend

* Python
* Django

### Database

* PostgreSQL

### PDF

* ReportLab

### Email

* Brevo API
* Email OTP

### Deployment

* Render
* Gunicorn

### Version Control

* Git
* GitHub

## 📂 Project Structure

```text
Smart Boutique
│
├── boutique
├── customers
├── dashboard
├── expenses
├── inventory
├── measurements
├── orders
├── payments
├── products
├── userlogin
│
├── manage.py
├── requirements.txt
└── README.md
```

## 🗄️ Database

The application uses **PostgreSQL** as the production database.

Main data areas include:

* Customers
* Measurements
* Products
* Inventory
* Orders
* Order Items
* Payments
* Expenses
* Users

## 🔄 Application Workflow

```text
Login
   ↓
Dashboard
   ↓
Customer
   ↓
Measurement
   ↓
Product / Inventory
   ↓
Order
   ↓
Order Items
   ↓
Payment
   ↓
Invoice
   ↓
Reports
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/amarnath-dev-03/smart-boutique.git
```

### 2. Open the project

```bash
cd smart-boutique
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create an admin user

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 🔑 Environment Variables

Sensitive configuration should be stored using environment variables and should not be committed to GitHub.

Example:

```text
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-postgresql-database-url
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
```

## 🚀 Deployment

The application is deployed using:

* GitHub for source code
* Render Web Service for the Django application
* Render PostgreSQL for the production database
* Gunicorn as the production application server
* Brevo API for Email OTP delivery

### Production Services

**Web Service**

```text
smart-boutique
```

**Database**

```text
smart-boutique-db
```

## 📱 Responsive Design

The application has been tested on desktop and mobile screen sizes.

The interface is designed to provide a usable experience across different screen sizes.

## 🔒 Security

The project includes:

* Django authentication
* Password hashing
* Session-based OTP verification
* OTP expiry
* Protected dashboard pages
* Environment variables for production secrets
* PostgreSQL production database
* API-based email delivery

Sensitive credentials and environment variables are not stored in the GitHub repository.

## 👨‍💻 Developer

**Amarnath P**

GitHub:
https://github.com/amarnath-dev-03/

## 📜 License

This project was created for learning, development, and portfolio purposes.
