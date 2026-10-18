
const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");

let tasks = [];
let currentFilter = "all";

document.getElementById("today").textContent =
    new Date().toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric"
    });

// Get tasks from Python backend
async function loadTasks() {
    try {
        const response = await fetch("/api/tasks");

        if (!response.ok) {
            throw new Error("Could not load tasks");
        }

        tasks = await response.json();
        renderTasks();
    } catch (error) {
        list.textContent =
            "Backend connection failed. Please run python app.py";
        console.error(error);
    }
}

// Save task updates through Python backend
async function updateTask(index, completed) {
    try {
        const response = await fetch(`/api/tasks/${index}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ completed })
        });

        if (!response.ok) {
            throw new Error("Could not update task");
        }

        await loadTasks();
    } catch (error) {
        alert("Could not update task. Check the Python server.");
        console.error(error);
    }
}

// Add a new task
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = input.value.trim();

    if (!name) return;

    try {
        const response = await fetch("/api/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name })
        });

        if (!response.ok) {
            throw new Error("Could not add task");
        }

        input.value = "";
        currentFilter = "all";

        document.querySelectorAll(".filter").forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.filter === "all"
            );
        });

        await loadTasks();
        input.focus();
    } catch (error) {
        alert("Could not add task. Check the Python server.");
        console.error(error);
    }
});

// Delete a task
async function deleteTask(index) {
    try {
        const response = await fetch(`/api/tasks/${index}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Could not delete task");
        }

        await loadTasks();
    } catch (error) {
        alert("Could not delete task. Check the Python server.");
        console.error(error);
    }
}

// Update dashboard statistics
function updateStats() {
    const completed = tasks.filter(task => task.completed).length;

    document.getElementById("total").textContent = tasks.length;
    document.getElementById("completed").textContent = completed;
    document.getElementById("pending").textContent =
        tasks.length - completed;
}

// Display tasks
function renderTasks() {
    list.replaceChildren();

    const filtered = tasks
        .map((task, index) => ({ ...task, index }))
        .filter(task => {
            if (currentFilter === "pending") {
                return !task.completed;
            }

            if (currentFilter === "completed") {
                return task.completed;
            }

            return true;
        });

    if (filtered.length === 0) {
        const empty = document.createElement("div");
        empty.className = "empty-state";
        empty.textContent = tasks.length === 0
            ? "✨ No tasks yet. Add your first task above!"
            : "No tasks in this category.";

        list.appendChild(empty);
    }

    filtered.forEach(task => {
        const row = document.createElement("div");
        row.className =
            "task-item" + (task.completed ? " done" : "");

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.className = "task-check";
        checkbox.checked = task.completed;
        checkbox.setAttribute("aria-label", "Complete task");

        checkbox.addEventListener("change", () => {
            updateTask(task.index, checkbox.checked);
        });

        const name = document.createElement("span");
        name.className = "task-name";
        name.textContent = task.name;

        const status = document.createElement("span");
        status.className = "task-status";
        status.textContent = task.completed
            ? "Completed"
            : "Pending";

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-btn";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
            deleteTask(task.index);
        });

        row.append(checkbox, name, status, deleteButton);
        list.appendChild(row);
    });

    updateStats();
}

// Task filters
document.querySelectorAll(".filter").forEach(button => {
    button.addEventListener("click", () => {
        currentFilter = button.dataset.filter;

        document.querySelectorAll(".filter").forEach(item => {
            item.classList.toggle("active", item === button);
        });

        renderTasks();
    });
});

// Initial load
loadTasks();
