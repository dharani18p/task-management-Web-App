# Task Management Web Application

A full-stack, scalable web application designed to manage tasks efficiently for a large user base. This project provides a complete solution from user authentication to task analytics, built with a robust backend API and a dynamic frontend.

**Live Demo:** [Link to your deployed application] *(You can add this later when you host it)*

---

## 📸 Screenshots & Demo

[GIF of the Task Management application in action]
*(A short GIF showing user login, task creation, and updating is highly recommended)*


*(Screenshot of the main dashboard showing tasks, filters, and analytics)*

---

## ✨ Key Features

This application is packed with features designed for a seamless user experience and powerful functionality:

* **Secure User Authentication:** Users can register and log in via a secure system using JWT (JSON Web Tokens) stored in `HttpOnly` cookies, complete with CSRF (Cross-Site Request Forgery) protection.
* **Full Task Management (CRUD):** Users have complete control to **C**reate, **R**ead, **U**pdate, and **D**elete their tasks.
* **Dynamic Filtering & Pagination:** The task list can be easily filtered by status and priority, with a pagination system to handle large numbers of tasks efficiently.
* **Real-time Analytics & Leaderboard:** The dashboard displays key stats (total, pending, completed tasks) and features a live leaderboard of top-performing users.
* **Responsive User Interface:** A clean, modern UI built with vanilla JavaScript that provides instant feedback through non-blocking "toast" notifications.

---

## 🛠️ Technology Stack & Architecture

This project was designed for scale and performance, capable of handling **100,000 users** and **1,000,000 tasks**.

### **System Architecture**
The backend is built on a scalable architecture using stateless API servers, a high-performance relational database, and an in-memory caching layer for analytics.



### **Technologies Used**

| Backend | Frontend | Database & Cache |
| :--- | :--- | :--- |
| Python | Vanilla JavaScript (ES6+) | PostgreSQL |
| Flask | HTML5 | Redis |
| SQLAlchemy | CSS3 | |
| Flask-JWT-Extended | | |

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### **Prerequisites**
* Python 3.x
* Git

### **Installation & Setup**

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/task-management-Web-App.git](https://github.com/your-username/task-management-Web-App.git)
    cd task-management-Web-App
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    *(You need to create this file by running `pip freeze > requirements.txt` in your terminal)*
    ```sh
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5.  **Run the Flask server:**
    ```sh
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

---

## 📋 API Endpoints

The core of the application is a well-defined RESTful API.

<details>
  <summary>Click to view API Endpoint Summary</summary>
  
  | Method | Endpoint | Description |
  | :--- | :--- | :--- |
  | `POST` | `/api/users/register` | Register a new user. |
  | `POST` | `/api/users/login` | Log in a user and set auth cookies. |
  | `GET` | `/api/tasks` | Get all tasks for the logged-in user. |
  | `POST` | `/api/tasks` | Create a new task. |
  | `PUT` | `/api/tasks/<task_id>` | Update a specific task. |
  | `DELETE`| `/api/tasks/<task_id>` | Delete a specific task. |
  | `GET` | `/api/analytics/leaderboard` | Get the user leaderboard. |
</details>
