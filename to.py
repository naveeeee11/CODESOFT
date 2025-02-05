import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect("todo_list.db")
cursor = conn.cursor()

# Create tasks table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')),
    due_date TEXT,
    status TEXT CHECK(status IN ('Pending', 'Completed')) DEFAULT 'Pending'
)
''')
conn.commit()


def add_task():
    """Adds a new task to the database."""
    title = input("Enter task title: ")
    description = input("Enter task description (optional): ")
    priority = input("Set priority (Low/Medium/High): ").capitalize()
    due_date = input("Enter due date (YYYY-MM-DD) (optional): ")

    cursor.execute("INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
                   (title, description, priority, due_date))
    conn.commit()
    print("Task added successfully!")


def view_tasks():
    """Displays all tasks from the database."""
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(f"[{task[0]}] {task[1]} | {task[2]} | Priority: {task[3]} | Due: {task[4]} | Status: {task[5]}")


def update_task():
    """Updates task details based on task ID."""
    task_id = input("Enter Task ID to update: ")
    new_status = input("Mark as Completed? (yes/no): ").strip().lower()

    if new_status == "yes":
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
        conn.commit()
        print("Task updated successfully!")
    else:
        print("No changes made.")


def delete_task():
    """Deletes a task by ID."""
    task_id = input("Enter Task ID to delete: ")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print("Task deleted successfully!")


# Main menu loop
while True:
    print("\nTo-Do List Menu:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Select an option: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        update_task()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        print("Exiting... Have a productive day!")
        break
    else:
        print("Invalid choice! Please enter a valid option.")

# Close database connection
conn.close()
