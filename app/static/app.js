const API_PREFIX = "/api";

// Helper function to get a cookie by name
const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
};

// Helper function to show toast notifications
let toastTimeout;
const showToast = (message, type = 'success') => {
    const toast = document.getElementById('toast-notification');
    if (!toast) return;
    clearTimeout(toastTimeout);
    toast.textContent = message;
    toast.className = `toast-show ${type}`;
    toastTimeout = setTimeout(() => {
        toast.className = toast.className.replace('toast-show', '');
    }, 3000);
};

// Helper function to handle API responses
const handleApiResponse = async (response, context = '') => {
    const responseText = await response.text();
    if (!response.ok) {
        let errorMsg = `API Error: ${response.statusText}`;
        try {
            const errorJson = JSON.parse(responseText);
            errorMsg = errorJson.error || errorJson.msg || "An unknown error occurred.";
        } catch (e) {
            // The response was not JSON, could be HTML error page
            console.error(`[${context}] Raw non-JSON response:`, responseText.substring(0, 500));
        }
        throw new Error(errorMsg);
    }
    try {
        const data = JSON.parse(responseText);
        return { response, data };
    } catch (parseErr) {
        throw new Error(`Invalid JSON response from server.`);
    }
};

// Main application logic starts after the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Get all DOM elements
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const addTaskForm = document.getElementById('addTaskForm');
    const tasksListContainer = document.getElementById('tasks-list');
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const currentPageSpan = document.getElementById('current-page');

    let currentPage = 1;
    const perPage = 5;

    const getUserId = () => localStorage.getItem("user_id");

    const formatDueDateTime = (dueDate) => {
        if (!dueDate) return '-';
        const dt = new Date(dueDate);
        return isNaN(dt.getTime()) ? '-' : dt.toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' });
    };

    // ===== AUTHENTICATION =====
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const res = await fetch(`${API_PREFIX}/users/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                await handleApiResponse(res, 'REGISTER');
                showToast("Registration successful! Please log in.");
                setTimeout(() => window.location.href = "/login-page", 1000);
            } catch (err) {
                showToast(err.message, 'error');
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const res = await fetch(`${API_PREFIX}/users/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const { data: responseData } = await handleApiResponse(res, 'LOGIN');
                localStorage.setItem('user_id', responseData.user_id);
                window.location.href = "/tasks-page";
            } catch (err) {
                showToast(err.message, 'error');
            }
        });
    }

    // ===== TASK MANAGEMENT =====

    // Load all tasks for the current user
    const loadTasks = async (page = 1) => {
        if (!tasksListContainer) return;

        let url = `${API_PREFIX}/tasks?page=${page}&per_page=${perPage}`;
        if (statusFilter?.value) url += `&status=${statusFilter.value}`;
        if (priorityFilter?.value) url += `&priority=${priorityFilter.value}`;

        try {
            const res = await fetch(url);
            const { data } = await handleApiResponse(res, 'LOAD_TASKS');

            tasksListContainer.innerHTML = "";
            if (!data.tasks || data.tasks.length === 0) {
                tasksListContainer.innerHTML = "<p>No tasks found for the selected filters.</p>";
            } else {
                data.tasks.forEach(task => {
                    const card = document.createElement("div");
                    card.className = `task-card status-${task.status}`;
                    card.innerHTML = `
                        <h3>${task.title}</h3>
                        <p>${task.description || 'No description.'}</p>
                        <div class="task-meta">
                            <span>Status: <strong>${task.status}</strong></span>
                            <span>Priority: <strong>${task.priority}</strong></span>
                        </div>
                        <div class="task-actions">
                            <button class="update-status-btn" data-task-id="${task.task_id}" ${task.status === 'completed' ? 'disabled' : ''}>
                                Mark Completed
                            </button>
                            <button class="delete-task-btn" data-task-id="${task.task_id}">Delete</button>
                        </div>
                    `;
                    tasksListContainer.appendChild(card);
                });
            }

            currentPage = data.pagination.current_page;
            if (currentPageSpan) currentPageSpan.innerText = currentPage;
            if (prevPageBtn) prevPageBtn.disabled = !data.pagination.has_prev;
            if (nextPageBtn) nextPageBtn.disabled = !data.pagination.has_next;

        } catch (err) {
            if (err.message.includes('Unauthorized')) {
                window.location.href = '/login-page';
            }
            showToast(err.message, 'error');
        }
    };

    // Add a new task
    if (addTaskForm) {
        addTaskForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addTaskForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const csrfToken = getCookie("csrf_access_token");
                const res = await fetch(`${API_PREFIX}/tasks`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRF-TOKEN": csrfToken
                    },
                    body: JSON.stringify(data)
                });
                await handleApiResponse(res, 'ADD_TASK');
                showToast("Task added successfully!");
                addTaskForm.reset();
                loadTasks();
                loadAnalytics();
            } catch (err) {
                showToast(err.message, 'error');
            }
        });
    }

    // Handle clicks for Update and Delete buttons
    if (tasksListContainer) {
        tasksListContainer.addEventListener('click', async (e) => {
            const taskId = e.target.dataset.taskId;
            if (!taskId) return;

            const csrfToken = getCookie("csrf_access_token");

            // Handle Update Clicks
            if (e.target.classList.contains('update-status-btn')) {
                try {
                    const res = await fetch(`${API_PREFIX}/tasks/${taskId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-TOKEN': csrfToken
                        },
                        body: JSON.stringify({ status: 'completed' })
                    });
                    await handleApiResponse(res, 'UPDATE_TASK');
                    showToast("Task marked as completed!");
                    loadTasks(currentPage);
                    loadAnalytics();
                } catch (err) {
                    showToast(err.message, 'error');
                }
            }

            // Handle Delete Clicks
            if (e.target.classList.contains('delete-task-btn')) {
                if (!confirm("Are you sure you want to delete this task?")) return;
                try {
                    const res = await fetch(`${API_PREFIX}/tasks/${taskId}`, {
                        method: 'DELETE',
                        headers: { 'X-CSRF-TOKEN': csrfToken }
                    });
                    await handleApiResponse(res, 'DELETE_TASK');
                    showToast("Task deleted.");
                    e.target.closest('.task-card').remove();
                    loadAnalytics();
                } catch (err) {
                    showToast(err.message, 'error');
                }
            }
        });
    }

    // ===== ANALYTICS & LEADERBOARD =====
    const loadAnalytics = async () => {
        try {
            const res = await fetch(`${API_PREFIX}/analytics`);
            const { data } = await handleApiResponse(res, 'ANALYTICS');
            document.getElementById("total-tasks").innerText = data.total_tasks || 0;
            document.getElementById("pending-tasks").innerText = data.tasks_by_status?.pending || 0;
            document.getElementById("in-progress-tasks").innerText = data.tasks_by_status['in-progress'] || 0;
            document.getElementById("completed-tasks").innerText = data.tasks_by_status?.completed || 0;
        } catch (err) {
            console.error("Analytics error:", err);
        }
    };

    const loadLeaderboard = async () => {
        const leaderboardList = document.getElementById('leaderboard-list');
        if (!leaderboardList) return;
        try {
            const res = await fetch(`${API_PREFIX}/analytics/leaderboard`);
            const { data } = await handleApiResponse(res, 'LEADERBOARD');
            leaderboardList.innerHTML = '';
            if (!data.leaderboard || data.leaderboard.length === 0) {
                leaderboardList.innerHTML = '<li>No data yet.</li>';
                return;
            }
            data.leaderboard.forEach(user => {
                const li = document.createElement('li');
                li.innerHTML = `${user.name} <span>${user.completed_tasks} tasks</span>`;
                leaderboardList.appendChild(li);
            });
        } catch (err) {
            console.error("Leaderboard error:", err);
            leaderboardList.innerHTML = '<li>Could not load data.</li>';
        }
    };

    // ===== FILTERS & PAGINATION CONTROLS =====
    applyFiltersBtn?.addEventListener("click", () => loadTasks(1));
    prevPageBtn?.addEventListener("click", () => { if (currentPage > 1) loadTasks(currentPage - 1); });
    nextPageBtn?.addEventListener("click", () => loadTasks(currentPage + 1));

    // ===== INITIAL PAGE LOAD =====
    if (tasksListContainer) {
        loadTasks();
        loadAnalytics();
        loadLeaderboard();
    }
});