from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    notes: str = ""
    selected: bool = True

    def update_title(self, title: str) -> None:
        raise NotImplementedError

    def update_duration(self, minutes: int) -> None:
        raise NotImplementedError

    def update_priority(self, priority: str) -> None:
        raise NotImplementedError

    def describe(self) -> str:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    owner_name: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        raise NotImplementedError

    def get_tasks(self) -> List[Task]:
        raise NotImplementedError


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
        raise NotImplementedError

    def set_availability(self, start: str, end: str) -> None:
        raise NotImplementedError

    def update_preferences(self, preferences: Dict[str, str]) -> None:
        raise NotImplementedError


class SchedulePlanner:
    def __init__(
        self,
        owner: Owner,
        pet: Pet,
        tasks: Optional[List[Task]] = None,
        available_minutes: int = 480,
    ) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks = tasks or []
        self.planned_tasks: List[Task] = []
        self.available_minutes = available_minutes

    def generate_schedule(self) -> None:
        raise NotImplementedError

    def sort_tasks_by_priority(self) -> List[Task]:
        raise NotImplementedError

    def fit_tasks_into_time(self) -> List[Task]:
        raise NotImplementedError

    def explain_plan(self) -> str:
        raise NotImplementedError

    def get_plan_summary(self) -> str:
        raise NotImplementedError
