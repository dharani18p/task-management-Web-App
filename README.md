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

### `POST /api/users/register` - Register a new user
<table>
  <tr>
    <td valign="top">
      <p>This endpoint allows a new user to create an account.</p>
      <strong>Request Body:</strong>
      <pre><code>{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}</code></pre>
      <strong>Success Response:</strong> <code>201 Created</code>
    </td>
    <td valign="top">
      <strong>Example in Postman:</strong><br>
      <a href="https://github.com/user-attachments/assets/645441aa-8278-4ff3-95d4-718566c9616b">
        <img src="https://github.com/user-attachments/assets/645441aa-8278-4ff3-95d4-718566c9616b" alt="Register User API Screenshot" width="400"/>
      </a>
      <br><em>Click image to enlarge</em>
    </td>
  </tr>
</table>

---

### `POST /api/users/login` - Log in a user
<table>
  <tr>
    <td valign="top">
      <p>Authenticates a user and sets the secure <code>access_token_cookie</code> and <code>csrf_access_token_cookie</code>.</p>
      <strong>Request Body:</strong>
      <pre><code>{
  "email": "test@example.com",
  "password": "password123"
}</code></pre>
      <strong>Success Response:</strong> <code>200 OK</code>
    </td>
    <td valign="top">
      <strong>Example in Postman:</strong><br>
      <a href="https://github.com/user-attachments/assets/29d6923d-26fc-4a75-9aa4-af1ef7459fad">
        <img src="https://github.com/user-attachments/assets/29d6923d-26fc-4a75-9aa4-af1ef7459fad" alt="Login API Screenshot" width="400"/>
      </a>
      <br><em>Click image to enlarge</em>
      <hr>
      <strong>Resulting Cookies:</strong><br>
      <a href="https://github.com/user-attachments/assets/e147c89e-eacc-4d8c-bcb9-a2d78f9529b5">
        <img src="https://github.com/user-attachments/assets/e147c89e-eacc-4d8c-bcb9-a2d78f9529b5" alt="Login Cookies Screenshot" width="400"/>
      </a>
      <br><em>Click image to enlarge</em>
    </td>
  </tr>
</table>

---

### `POST /api/tasks` - Create a new task
<table>
  <tr>
    <td valign="top">
      <p>Creates a new task for the authenticated user. Requires the <code>X-CSRF-TOKEN</code> header.</p>
      <strong>Request Body:</strong>
      <pre><code>{
  "title": "My New Task",
  "description": "Details about the task.",
  "priority": "high"
}</code></pre>
      <strong>Success Response:</strong> <code>201 Created</code>
    </td>
    <td valign="top">
      <strong>Example in Postman:</strong><br>
      <a href="https://github.com/user-attachments/assets/edce1601-6bb5-4740-b60f-b12ba269c067">
        <img src="https://github.com/user-attachments/assets/edce1601-6bb5-4740-b60f-b12ba269c067" alt="Create Task API Screenshot" width="400"/>
      </a>
      <br><em>Click image to enlarge</em>
    </td>
  </tr>
</table>

---

### `GET /api/tasks` - Get all tasks
<table>
  <tr>
    <td valign="top">
      <p>Retrieves a paginated and filterable list of tasks for the logged-in user.</p>
      <strong>Query Parameters:</strong>
      <ul>
        <li><code>page</code> (e.g., 1)</li>
        <li><code>limit</code> (e.g., 10)</li>
        <li><code>status</code> (e.g., "pending")</li>
        <li><code>priority</code> (e.g., "high")</li>
      </ul>
      <strong>Success Response:</strong> <code>200 OK</code>
    </td>
    <td valign="top">
      <strong>Example in Postman:</strong><br>
      <a href="https://github.com/user-attachments/assets/abf052db-a0de-41ad-adb5-f4bfa2845342">
        <img src="https://github.com/user-attachments/assets/abf052db-a0de-41ad-adb5-f4bfa2845342" alt="Get Tasks API Screenshot" width="400"/>
      </a>
      <br><em>Click image to enlarge</em>
    </td>
  </tr>
</table>

---

### `PUT /api/tasks/<task_id>` - Update a task
<table>
  <tr>
    <td valign="top">
      <p>Updates a specific task. Requires the <code>X-CSRF-TOKEN</code> header.</p>
      <strong>Request Body:</strong>
      <pre><code>{
  "status": "completed",
  "priority": "low"
}</code></pre>
      <strong>Success Response:</strong> <code>200 OK</code>
    </td>
    <td valign="top">
      <strong>Example in Postman:</strong><br>
      <a href="https://github.com/user-attachments/assets/4f4328e3-bc83-4fa4-8f56-f10af7fae7fe">
        <img src="https://github.com/user-attachments/assets/4f4328e3-bc83-4fa4-8f56-f10af7fae7fe" alt="Update Task API Screenshot" width="400"/>
      </a>
      <br><em>Click image to enlarge</em>
    </td>
  </tr>
</table>

---

### `DELETE /api/tasks/<task_id>` - Delete a task
<table>
  <tr>
    <td valign="top">
      <p>Deletes a specific task. Requires the <code>X-CSRF-TOKEN</code> header.</p>
      <strong>Success Response:</strong> <code>200 OK</code>
    </td>
    <td valign="top">
      <strong>Example in Postman:</strong><br>
      <a href="https://github.com/user-attachments/assets/f2eacd11-4f41-4488-bef9-5a849cf500a8">
        <img src="https://github.com/user-attachments/assets/f2eacd11-4f41-4488-bef9-5a849cf500a8" alt="Delete Task API Screenshot" width="400"/>
      </a>
      <br><em>Click image to enlarge</em>
    </td>
  </tr>
</table>

---

### `GET /api/analytics/leaderboard` - Get leaderboard
<table>
  <tr>
    <td valign="top">
      <p>Retrieves a list of top users based on the number of completed tasks.</p>
      <strong>Success Response:</strong> <code>200 OK</code>
    </td>
    <td valign="top">
      <strong>Example in Postman:</strong><br>
      <a href="https://github.com/user-attachments/assets/48bb4d70-cf19-4063-ab02-83b812edc288">
        <img src="https://github.com/user-attachments/assets/48bb4d70-cf19-4063-ab02-83b812edc288" alt="Leaderboard API Screenshot" width="400"/>
      </a>
      <br><em>Click image to enlarge</em>
    </td>
  </tr>
</table>
