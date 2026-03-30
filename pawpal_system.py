from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}


@dataclass
class Task:
    title: str
    duration_minutes: int
    frequency: str = "daily"
    priority: str = "medium"
    description: str = ""
    completed: bool = False

    def update_title(self, title: str) -> None:
        """Update the task title."""
        self.title = title

    def update_duration(self, minutes: int) -> None:
        """Update how long the task takes."""
        self.duration_minutes = minutes

    def update_priority(self, priority: str) -> None:
        """Change the task priority."""
        self.priority = priority

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def describe(self) -> str:
        """Return a short text description of the task."""
        return (
            f"{self.title}: {self.description} "
            f"({self.duration_minutes} min, {self.priority}, {self.frequency})"
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

    def get_tasks(self) -> List[Task]:
        """Return the current task list for this pet."""
        return self.tasks


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

    def get_all_tasks(self) -> List[Task]:
        """Collect every task from all owned pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


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

    def retrieve_all_tasks(self) -> List[Task]:
        """Get all tasks from the owner and their pets."""
        return self.owner.get_all_tasks()

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

    def generate_schedule(self) -> List[Task]:
        """Build the final schedule and store the selected tasks."""
        tasks = self.sort_tasks_by_priority()
        self.planned_tasks = self.fit_tasks_into_time(tasks)
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
        for task in self.planned_tasks:
            lines.append(f"- {task.describe()}")
        return "\n".join(lines)

    def get_plan_summary(self) -> str:
        """Return a short summary of the generated schedule."""
        return (
            f"Scheduled {len(self.planned_tasks)} tasks "
            f"for {self.owner.name} across {len(self.owner.pets)} pet(s)."
        )

    def _effective_worker_count(self) -> int:
        """Return the effective number of workers for this schedule."""
        return max(1, self.worker_count)

    def _adjusted_available_minutes(self) -> int:
        """Calculate available minutes considering worker count."""
        return int(self.available_minutes * min(self._effective_worker_count(), 4))
