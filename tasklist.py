import twitchio
from task import Task
from typing import List


class TaskList:

    def __init__(self):
        self.task_list = []

    def task_exists(self, new_task: Task) -> bool:
        for task in self.task_list:
            if (task.owner_id == new_task.owner_id) and (task.task_desc == new_task.task_desc):
                return True
        return False

    def has_active_task(self, user: twitchio.Chatter) -> bool:
        for task in self.task_list:
            if (task.owner_id == user.id) and task.is_current_task:
                return True
        return False

    def add_task(self, new_task: Task) -> None:
        if not self.task_exists(new_task):
            self.task_list.append(new_task)

    def edit_current_task_desc(self, user: twitchio.Chatter, new_desc: str) -> bool:
        if self.has_active_task(user.id):
            for task in self.task_list:
                if (task.owner_id == user.id) and task.is_current_task:
                    task.task_desc = new_desc
                    return True
        return False

    def delete_active_task(self, user: twitchio.Chatter) -> bool:
        if self.has_active_task(user.id):
            for task in self.task_list:
                if (task.owner_id == user.id) and task.is_current_task:
                    task.is_deleted = True
                    task.is_current_task = False
                    return True
        return False

    def mark_task_done(self, user: twitchio.Chatter) -> bool:
        if self.has_active_task(user.id):
            for task in self.task_list:
                if (task.owner_id == user.id) and task.is_current_task:
                    task.is_complete = True
                    task.is_current_task = False
                    return True
        return False

    def get_current_task(self, user: twitchio.Chatter) -> str:
        if self.has_active_task(user.id):
            for task in self.task_list:
                if (task.owner_id == user.id) and task.is_current_task:
                    return task.get_current_task()
        return f"No active tasks found for {user.name}."

    def get_accumulated_time(self, user: twitchio.Chatter) -> str:
        if self.has_active_task(user.id):
            for task in self.task_list:
                if (task.owner_id == user.id) and task.is_current_task:
                    return f"{user.name}, you have been working on your current task for: {task.get_elapsed_time()}"
        return f"{user.name}, you have no active tasks."

    def list_tasks(self, user: twitchio.Chatter) -> List[Task]:
        completed_tasks = []
        for task in self.task_list:
            if (task.owner_id == user.id) and task.is_complete:
                completed_tasks.append(task)
        return completed_tasks
