# Rent a Book Application
Aa application for managing student book rental developed on Django

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Notes](#notes)
- [License](#license)

## Installation

### Prerequisites

- Python 3.10+
- Git

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/arunk-iq/rent-a-book.git
   cd rent-a-book
   ```
2. **Create and Activate Virtual Environment**(Optional) 

   ```bash
   python -m venv venv
   # On Linux: 
   source venv/bin/activate  
   # On Windows: 
   venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   Application 
   ```bash
   http://localhost:8000/ 
   ```
   Admin Site
   ```bash
   http://localhost:8000/admin/
   ```

## Usage

### Admin Actions:

- Log in to the admin site using your superuser credentials.
- Add students (users who are not having is_staff and is_superuser) who can rent books.

### Start Rental:

- Navigate to application. First time it will direct to login page.Login with admin/staff credentials
- User will be taken to landing page. From side menu select `Student list`
- The system fetches list of students we have options to list all rentals and add rental against each student

### New rental

