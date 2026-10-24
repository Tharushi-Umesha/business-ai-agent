
from db import get_connection


def add_task(title: str) -> str:
    """Save a new task in PostgreSQL."""
    title = title.strip()

    if not title:
        return "Error: Task title cannot be empty."

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title)
                VALUES (%s)
                RETURNING id;
                """,
                (title,),
            )
            task_id = cur.fetchone()[0]

    return f"Task #{task_id} added successfully: {title}"


def get_all_tasks() -> list:
    """Retrieve tasks from PostgreSQL."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, status, created_at
                FROM tasks
                ORDER BY id DESC;
                """
            )
            return cur.fetchall()


def list_tasks() -> str:
    """Return all tasks in a readable format."""
    tasks = get_all_tasks()

    if not tasks:
        return "There are currently no tasks."

    return "\n".join(
        f"ID: {task[0]} | {task[1]} | Status: {task[2]}"
        for task in tasks
    )


def complete_task(task_id: int) -> str:
    """Mark a task as completed."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET status = 'completed'
                WHERE id = %s AND status = 'pending'
                RETURNING title;
                """,
                (task_id,),
            )
            task = cur.fetchone()

    if task:
        return f"Task #{task_id} completed: {task[0]}"

    return f"Task #{task_id} was not found as a pending task."


def delete_task(task_id: int) -> str:
    """Delete a task from PostgreSQL."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING title;",
                (task_id,),
            )
            task = cur.fetchone()

    if task:
        return f"Task #{task_id} deleted: {task[0]}"

    return f"Task #{task_id} was not found."
