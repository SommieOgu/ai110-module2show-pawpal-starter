from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple


PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}


@dataclass
class Task:
    title: str
    duration_minutes: int
    frequency: str = "daily"
    priority: str = "medium"
    description: str = ""
    completed: bool = False
    preferred_start_time: Optional[str] = None
    scheduled_start_time: Optional[str] = None
    due_date: Optional[date] = None

    def update_title(self, title: str) -> None:
        """Update the task title."""
        self.title = title

    def update_duration(self, minutes: int) -> None:
        """Update how long the task takes."""
        self.duration_minutes = minutes

    def update_priority(self, priority: str) -> None:
        """Change the task priority."""
        self.priority = priority

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as completed and create the next occurrence if recurring."""
        self.completed = True
        if not self.is_recurring():
            return None

        next_due = self._compute_next_due_date()
        if next_due is None:
            return None

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            description=self.description,
            preferred_start_time=self.preferred_start_time,
            due_date=next_due,
        )

    def _compute_next_due_date(self) -> Optional[date]:
        """Return the next due date based on frequency."""
        base_date = self.due_date or date.today()
        if self.frequency == "daily":
            return base_date + timedelta(days=1)
        if self.frequency == "weekly":
            return base_date + timedelta(weeks=1)
        return None

    def is_recurring(self) -> bool:
        """Return whether this task should repeat on a schedule."""
        return self.frequency != "one-time"

    def is_due(self, current_day: Optional[str] = None) -> bool:
        """Determine whether the task should be scheduled for the current day."""
        if self.frequency == "daily":
            return True

        if self.frequency == "weekly":
            if current_day is None:
                return True
            return current_day.lower() in {
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            }

        if self.frequency == "monthly":
            if current_day is None:
                return True
            return current_day.lower() in {"1", "01", "first", "month_start"}

        return True

    def describe(self) -> str:
        """Return a short text description of the task."""
        schedule_info = (
            f" starting at {self.scheduled_start_time}" if self.scheduled_start_time else ""
        )
        due_info = f" due {self.due_date.isoformat()}" if self.due_date else ""
        return (
            f"{self.title}: {self.description} "
            f"({self.duration_minutes} min, {self.priority}, {self.frequency})"
            f"{schedule_info}{due_info}"
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    owner: Optional[Owner] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        self.tasks = [existing for existing in self.tasks if existing is not task]

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and automatically queue the next occurrence if recurring."""
        if task not in self.tasks:
            return None
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
        return next_task

    def get_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """Return the current task list for this pet."""
        if completed is None:
            return self.tasks
        return [task for task in self.tasks if task.completed is completed]


class Owner:
    def __init__(
        self,
        name: str,
        availability_start: str = "",
        availability_end: str = "",
        preferences: Optional[Dict[str, str]] = None,
    ) -> None:
        self.name = name
        self.availability_start = availability_start
        self.availability_end = availability_end
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet to this owner."""
        pet.owner = self
        self.pets.append(pet)

    def set_availability(self, start: str, end: str) -> None:
        """Set the owner's available hours."""
        self.availability_start = start
        self.availability_end = end

    def update_preferences(self, preferences: Dict[str, str]) -> None:
        """Update the owner's scheduling preferences."""
        self.preferences.update(preferences)

    def get_all_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """Collect every task from all owned pets, optionally filtering by pet or completion."""
        tasks: List[Task] = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            tasks.extend(pet.get_tasks(completed))
        return tasks

    def get_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks that belong to a specific pet."""
        return self.get_all_tasks(pet_name=pet_name)

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return self.get_all_tasks(completed=completed)


class SchedulePlanner:
    def __init__(
        self,
        owner: Owner,
        available_minutes: int = 480,
        employees: Optional[List[str]] = None,
        worker_count: Optional[int] = None,
    ) -> None:
        self.owner = owner
        self.available_minutes = available_minutes
        self.employees = employees or []
        self.worker_count = len(self.employees) if self.employees else (worker_count or 1)
        self.planned_tasks: List[Task] = []
        self.conflicts: List[str] = []

    def retrieve_all_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        current_day: Optional[str] = None,
    ) -> List[Task]:
        """Get all tasks from the owner and their pets, with optional filters."""
        tasks = self.owner.get_all_tasks(pet_name=pet_name, completed=completed)
        if current_day is not None:
            return [task for task in tasks if task.is_due(current_day)]
        return [task for task in tasks if task.is_due()]

    def sort_tasks_by_priority(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by priority, completion, and duration."""
        tasks = tasks if tasks is not None else self.retrieve_all_tasks()
        return sorted(
            tasks,
            key=lambda task: (
                PRIORITY_ORDER.get(task.priority, 99),
                task.completed,
                task.duration_minutes,
            ),
        )

    def sort_tasks_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by preferred start time and priority."""
        tasks = tasks if tasks is not None else self.retrieve_all_tasks()
        return sorted(
            tasks,
            key=lambda task: (
                self._parse_time(task.preferred_start_time)
                if task.preferred_start_time
                else 24 * 60,
                PRIORITY_ORDER.get(task.priority, 99),
                task.completed,
                task.duration_minutes,
            ),
        )

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """Return tasks filtered by pet name or completion status."""
        return self.retrieve_all_tasks(pet_name=pet_name, completed=completed)

    def filter_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Return only tasks for the named pet."""
        return self.retrieve_all_tasks(pet_name=pet_name)

    def filter_tasks_by_status(self, completed: bool) -> List[Task]:
        """Return only tasks matching the completion status."""
        return self.retrieve_all_tasks(completed=completed)

    def fit_tasks_into_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Pack as many tasks as possible into available minutes."""
        tasks = tasks if tasks is not None else self.sort_tasks_by_priority()
        adjusted_minutes = self._adjusted_available_minutes()
        scheduled: List[Task] = []
        total = 0

        for task in tasks:
            if task.completed:
                continue
            if total + task.duration_minutes <= adjusted_minutes:
                scheduled.append(task)
                total += task.duration_minutes

        return scheduled

    def generate_schedule(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = False,
        current_day: Optional[str] = None,
    ) -> List[Task]:
        """Build the final schedule and store the selected tasks."""
        tasks = self.retrieve_all_tasks(
            pet_name=pet_name,
            completed=completed,
            current_day=current_day,
        )
        tasks = [task for task in tasks if not task.completed]
        tasks = self.sort_tasks_by_time(tasks)
        self.planned_tasks = self.fit_tasks_into_time(tasks)
        self._assign_schedule_times(self.planned_tasks)
        self.detect_conflicts(self.planned_tasks)
        return self.planned_tasks

    def explain_plan(self) -> str:
        """Return a text summary of the current schedule."""
        if not self.planned_tasks:
            return "No tasks could be scheduled with the current constraints."

        lines = [
            f"Schedule for {self.owner.name}:",
            f"Available minutes: {self._adjusted_available_minutes()} (workers: {self._effective_worker_count()})",
        ]
        if self.employees:
            lines.append("Employees: " + ", ".join(self.employees))
        if self.conflicts:
            lines.append("Issues: " + "; ".join(self.conflicts))
        for task in self.planned_tasks:
            lines.append(f"- {task.describe()}")
        return "\n".join(lines)

    def get_plan_summary(self) -> str:
        """Return a short summary of the generated schedule."""
        return (
            f"Scheduled {len(self.planned_tasks)} tasks "
            f"for {self.owner.name} across {len(self.owner.pets)} pet(s)."
        )

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Detect scheduling issues such as overlapping preferred times or too much work."""
        tasks = tasks if tasks is not None else self.sort_tasks_by_time()
        conflicts: List[str] = []

        if not self.employees:
            conflicts.append("No external employees assigned; owner will manage tasks alone.")

        if self.worker_count > 4:
            conflicts.append("More than 4 workers assigned; effective capacity is capped at 4.")

        same_start_times: Dict[str, List[Task]] = {}
        for task in tasks:
            if task.preferred_start_time:
                same_start_times.setdefault(task.preferred_start_time, []).append(task)

        for start_time, task_group in same_start_times.items():
            if len(task_group) > 1:
                conflicts.append(
                    f"{len(task_group)} tasks want the same preferred start time {start_time}."
                )

        scheduled_time_groups: Dict[str, List[Task]] = {}
        for task in tasks:
            if task.scheduled_start_time:
                scheduled_time_groups.setdefault(task.scheduled_start_time, []).append(task)

        for start_time, task_group in scheduled_time_groups.items():
            if len(task_group) > 1:
                conflicts.append(
                    f"{len(task_group)} tasks are scheduled at the same time {start_time}."
                )

        total_minutes = sum(task.duration_minutes for task in tasks)
        if total_minutes > self._adjusted_available_minutes():
            conflicts.append(
                f"Task workload exceeds capacity by "
                f"{total_minutes - self._adjusted_available_minutes()} minutes."
            )

        self.conflicts = conflicts
        return conflicts

    def _assign_schedule_times(self, tasks: List[Task]) -> None:
        """Assign actual start times for scheduled tasks."""
        window_start = self._parse_time(self.owner.availability_start or "08:00")
        window_end = self._parse_time(self.owner.availability_end or "17:00")
        if window_end <= window_start:
            window_end = window_start + self.available_minutes

        used_slots: List[Tuple[int, int]] = []
        next_available = window_start

        for task in tasks:
            preferred_start = (
                self._parse_time(task.preferred_start_time)
                if task.preferred_start_time
                else None
            )

            if preferred_start is not None:
                preferred_end = preferred_start + task.duration_minutes
                if (
                    preferred_start >= window_start
                    and preferred_end <= window_end
                    and not self._slot_conflicts(preferred_start, task.duration_minutes, used_slots)
                ):
                    task.scheduled_start_time = self._format_time(preferred_start)
                    used_slots.append((preferred_start, preferred_end))
                    next_available = max(next_available, preferred_end)
                    continue

            if next_available + task.duration_minutes <= window_end:
                task.scheduled_start_time = self._format_time(next_available)
                used_slots.append((next_available, next_available + task.duration_minutes))
                next_available += task.duration_minutes
            else:
                task.scheduled_start_time = None

    def _slot_conflicts(
        self,
        start: int,
        duration: int,
        scheduled: List[Tuple[int, int]],
    ) -> bool:
        end = start + duration
        return any(not (end <= existing_start or start >= existing_end) for existing_start, existing_end in scheduled)

    def _parse_time(self, time_str: str) -> int:
        """Turn an HH:MM string into minutes since midnight."""
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    def _format_time(self, minutes: int) -> str:
        """Turn minutes since midnight into an HH:MM string."""
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    def _effective_worker_count(self) -> int:
        """Return the effective number of workers for this schedule."""
        return max(1, min(self.worker_count, 4))

    def _available_window_minutes(self) -> int:
        """Return the owner's availability window in minutes."""
        if not self.owner.availability_start or not self.owner.availability_end:
            return self.available_minutes
        return max(
            0,
            self._parse_time(self.owner.availability_end)
            - self._parse_time(self.owner.availability_start),
        )

    def _adjusted_available_minutes(self) -> int:
        """Calculate available minutes considering worker count and owner availability."""
        capacity = min(self.available_minutes, self._available_window_minutes())
        return int(capacity * self._effective_worker_count())
