# Campus Leave Management System (LMS)

A modern, full-stack, three-tier role-based Leave Management System designed for academic institutions to streamline student leave applications, tracking, approvals, and analytics.

---

## 🚀 Key Features

### 👨‍🎓 Student Portal
- **Secure Authentication**: Register and log in using student credentials (email, password, register number, department, address, phone number).
- **Apply for Leave**:
  - Apply for various leave types: **Casual**, **Sick (Medical)**, **On Duty (OD)**, and **Emergency**.
  - Dynamic Form validation prevents selecting past dates and ensures the leave duration is valid.
  - Supports document upload: attach official **OD forms** or **Medical certificates** (PDFs or images).
- **Status Tracker**: Track the real-time approval status across the multi-level workflow hierarchy (Tutor ➔ Advisor ➔ HOD).
- **Application Management**: Cancel/delete pending leave requests if they are no longer required.
- **Personal Profile**: View student academic and personal details in a beautifully designed profile card.

### 👩‍🏫 Staff Portal (Tutors, Advisors, & HODs)
- **Role-based Dashboards**: Customized reviews depending on the staff member's role:
  - **Tutor**: Initial review and approval tier.
  - **Advisor**: Mid-level review and verification tier.
  - **HOD**: Final authority approval tier.
- **Review & Inbox**: View incoming leave requests filtered by department, complete with download links for uploaded OD/medical forms.
- **Approve/Reject with Comments**: Approve or reject requests and leave feedback comments.
- **Leave Analytics**: Visualization dashboard displaying total applications and charts for leaves by department and leave reason (powered by Chart.js).
- **Academic Calendar**: View college events and academic holidays via embedded calendar support.
- **Staff Profile**: View detailed staff credentials and designations.

---

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3 (Vanilla Premium Styles), Bootstrap v5.3, JavaScript (ES6+), Chart.js
- **Backend Framework**: Django 5.2 (Python Web Framework)
- **Database**: MongoDB (NoSQL Database)
- **ORM / ODM**: MongoEngine (Python Object-Document Mapper for MongoDB)
- **File Storage**: GridFS (for storing and downloading uploaded PDF files and images in MongoDB)

---

## 📂 Project Structure

```text
Leave-Management/
├── app/                        # Django Project Directory
│   ├── app/                    # Configuration, ASGI, WSGI & Settings
│   │   ├── settings.py         # MongoDB & Django Settings
│   │   └── urls.py             # Global URL Routing
│   ├── main/                   # Core LMS App Directory
│   │   ├── templates/          # HTML Templates (login, signup, leave, teacher, profile, etc.)
│   │   ├── static/             # Static Assets (custom CSS and styles)
│   │   ├── models.py           # Standard Django Models
│   │   ├── mongo_models.py     # MongoEngine Collections & Schemas
│   │   ├── views.py            # Business Logic & Request Handlers
│   │   ├── urls.py             # App-specific Routing URLs
│   │   └── tests.py            # Automated Unit Tests
│   └── manage.py               # Django CLI management script
├── Hackathon.users.csv         # Seeding data for users
├── Hackathon.leave_applications.csv # Seeding data for leave requests
└── README.md                   # Project Documentation
```

---

## 📋 Prerequisites

To run this application locally, you will need:
- **Python** (version 3.10 or higher recommended)
- **MongoDB** running locally on port `27017`

---

## ⚙️ Installation & Setup

Follow these steps to run the application locally:

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/Leave-Management.git
cd Leave-Management
```

### 2. Set Up Virtual Environment & Dependencies
Create a virtual environment and install the required Python packages:
```bash
python -m venv env
source env/bin/activate
pip install -r app/requirements.txt  # Or manually install django and mongoengine
```
*Note: Make sure `mongoengine` is installed.*

### 3. Start MongoDB Server
Ensure your local MongoDB instance is running:
```bash
sudo systemctl start mongod  # Linux
# OR
brew services start mongodb-community  # macOS
```

### 4. Run Django Database Migrations (for session storage)
```bash
python app/manage.py migrate
```

### 5. Start the Development Server
Run the local server using `manage.py`:
```bash
python app/manage.py runserver
```
The application will be accessible at: **`http://127.0.0.1:8000/`**

---

## 🧪 Running Automated Tests

A comprehensive unit testing suite is provided in `app/main/tests.py` covering views, login authentication, user creation, leave application restrictions, staff approvals, and deletion workflows.

To execute the test suite:
```bash
python app/manage.py test main
```

---

## 👤 Sample Credentials for Testing

You can use the following default credentials to test the student and staff dashboards (all accounts share the default password: `12345678`):

| Email | Role | Staff Designation |
| :--- | :--- | :--- |
| `jaiathiyaa@gmail.com` | Student | N/A |
| `rishi1@gmail.com` | Staff | Tutor |
| `darshan@gmail.com` | Staff | Advisor |

---

## 🛡️ License

This project is licensed under the MIT License. See the `LICENSE` file for details.
