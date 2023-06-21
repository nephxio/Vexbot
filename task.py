import datetime


class Task:

    def __init__(self, owner_id: int, owner_nick: str, task_desc: str,
                 is_current_task: bool = True, is_complete: bool = False, is_deleted: bool = False,
                 timestamp: datetime.datetime = datetime.datetime.now()) -> None:
        self.owner_id: int = owner_id
        self.owner_nick: str = owner_nick
        self.task_desc: str = task_desc
        self.is_current_task: bool = is_current_task
        self.is_complete: bool = is_complete
        self.is_deleted: bool = is_deleted
        self.timestamp: datetime.datetime = timestamp

    def get_elapsed_time(self) -> str:
        elapsed_time: datetime.timedelta = datetime.datetime.now() - self.timestamp

        return str(datetime.timedelta(seconds=elapsed_time.total_seconds()))

    def edit_task_desc(self, new_desc: str) -> None:
        self.task_desc = new_desc

    def mark_as_done(self) -> None:
        self.is_complete = True

    def delete_task(self) -> None:
        self.is_deleted = True

    def get_current_task(self) -> str:
        return f"Current task for {self.owner_nick}: {self.task_desc}"
