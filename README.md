"" 🧵 Smart Boutique""

" Smart Tailoring & Boutique Management System "

**Smart Boutique** is a full-stack Django web application designed to help tailoring and boutique businesses manage their daily operations from a single platform.

The system provides modules for customer management, measurements, products, inventory, orders, payments, expenses, invoices, dashboards, and business reports.



 🌐 Live Demo

**Live Website:**
https://smart-boutique-29cq.onrender.com

**GitHub Repository:**
https://github.com/amarnath-dev-03/smart-boutique

> The application is deployed using Render with PostgreSQL as the production database.


✨ Features 

🔐 Authentication

* User Login & Logout
* Forgot Password
* Email OTP verification
* OTP expiry validation
* Password reset
* Secure password hashing

👥 Customer Management

* Add customers
* View customer details
* Edit customer information
* Delete customers
* Search customers

📏 Measurement Management

* Add customer measurements
* View measurement details
* Edit measurements
* Delete measurements
* Search measurements

👕 Product Management

* Add products
* Edit products
* Delete products
* View product details
* Product categories
* Product pricing
* Stock management

📦 Inventory Management

* Add inventory items
* Edit inventory
* Delete inventory
* Search inventory
* Stock tracking
* Product and inventory synchronization

🧾 Order Management

* Create orders
* Edit orders
* Delete orders
* View order details
* Manage order items
* Automatic item totals
* Automatic order total calculation
* Order status tracking

💳 Payment Management

* Record payments
* Payment history
* Payment methods
* Payment status
* Paid amount tracking
* Pending balance calculation

💰 Expense Management

* Add expenses
* Edit expenses
* Delete expenses
* Expense categories
* Expense search
* Expense tracking

📄 Invoice & Reports

* Generate professional Invoice PDFs
* Business reports
* Financial summaries
* Monthly business reports
* Order status reports
* Payment summaries
* Expense summaries
* Net balance calculation

📊 Dashboard

* Customer statistics
* Product statistics
* Inventory statistics
* Order statistics
* Payment statistics
* Expense statistics
* Order status charts
* Monthly business charts
* Payment status
* Low stock alerts
* Recent orders
* Quick actions



🛠️ Technologies Used

# Backend

* Python
* Django

# Database

* PostgreSQL

# Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

# PDF

* ReportLab

# Email

* Brevo API
* Email OTP

# Deployment

* Render

# Version Control

* Git
* GitHub


 📁 Project Modules

`text
Smart Boutique
│
├── Authentication
├── Customers
├── Measurements
├── Products
├── Inventory
├── Orders
├── Payments
├── Expenses
├── Dashboard
├── Reporting
└── Invoice PDF

 🗄️ Database

The application uses "" PostgreSQL"" as the production database.

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


🔄 Application Workflow

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

🚀 Deployment

The application is deployed on "" Render "".

 Production Stack

```text
Django
   ↓
Gunicorn
   ↓
Render
   ↓
PostgreSQL
```

Email OTP is handled through the "" Brevo API "".

🎯 Project Purpose

The main purpose of Smart Boutique is to provide a simple digital management system for tailoring and boutique businesses.

It helps manage:

* Customer information
* Customer measurements
* Products
* Inventory
* Orders
* Payments
* Expenses
* Invoices
* Business reports

from one centralized application.

---

## 🔒 Security

The project includes:

* Django authentication
* Password hashing
* Session-based OTP verification
* OTP expiry
* Environment variables for production secrets
* PostgreSQL production database
* API-based email delivery

Sensitive credentials and environment variables are not stored in the GitHub repository.


 👨‍💻 Author

""" Amarnath P """


📜 License

This project was created for "" learning, development, and portfolio purposes "".
