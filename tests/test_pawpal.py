from datetime import date

from pawpal_system import Owner, Pet, SchedulePlanner, Task


def test_task_completion_changes_status() -> None:
    task = Task(
        title="Feed",
        duration_minutes=10,
        priority="medium",
        description="Feed the pet.",
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Bubbles", species="fish", age=1)
    initial_count = len(pet.get_tasks())

    pet.add_task(
        Task(
            title="Feed flakes",
            duration_minutes=5,
            priority="high",
            description="Feed the fish.",
        )
    )

    assert len(pet.get_tasks()) == initial_count + 1


def test_mark_complete_creates_next_daily_occurrence() -> None:
    task = Task(
        title="Feed",
        duration_minutes=10,
        frequency="daily",
        due_date=date(2026, 3, 30),
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 3, 31)
    assert next_task.completed is False
    assert next_task.frequency == "daily"


def test_pet_complete_task_generates_next_occurrence() -> None:
    pet = Pet(name="Bubbles", species="fish", age=1)
    task = Task(
        title="Feed flakes",
        duration_minutes=5,
        priority="high",
        frequency="daily",
        due_date=date(2026, 3, 30),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is not None
    assert next_task in pet.get_tasks()
    assert next_task.due_date == date(2026, 3, 31)
    assert task.completed is True


def test_owner_task_filters_by_pet_and_status() -> None:
    owner = Owner(name="Jordan", availability_start="08:00", availability_end="17:00")
    dog = Pet(name="Buddy", species="dog")
    cat = Pet(name="Fish", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    walk = Task(title="Walk", duration_minutes=30, priority="high")
    feed = Task(title="Feed", duration_minutes=10, priority="low", completed=True)
    dog.add_task(walk)
    cat.add_task(feed)

    assert owner.get_tasks_by_pet("Buddy") == [walk]
    assert owner.get_tasks_by_status(True) == [feed]


def test_sort_tasks_by_time_respects_preferred_start() -> None:
    owner = Owner(name="Jordan", availability_start="08:00", availability_end="17:00")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    early = Task(
        title="Early task",
        duration_minutes=15,
        priority="medium",
        preferred_start_time="08:00",
    )
    later = Task(
        title="Later task",
        duration_minutes=15,
        priority="high",
        preferred_start_time="09:00",
    )
    pet.add_task(later)
    pet.add_task(early)

    planner = SchedulePlanner(owner=owner, available_minutes=120, employees=["Alex"])
    sorted_tasks = planner.sort_tasks_by_time()

    assert sorted_tasks[0] is early
    assert sorted_tasks[1] is later


def test_detect_conflicts_for_same_preferred_start_time() -> None:
    owner = Owner(name="Jordan", availability_start="08:00", availability_end="17:00")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    task1 = Task(title="Groom", duration_minutes=20, preferred_start_time="09:00")
    task2 = Task(title="Brush", duration_minutes=15, preferred_start_time="09:00")
    pet.add_task(task1)
    pet.add_task(task2)

    planner = SchedulePlanner(owner=owner, available_minutes=120, employees=["Alex"])
    conflicts = planner.detect_conflicts([task1, task2])

    assert any("same preferred start time" in conflict for conflict in conflicts)


def test_detect_conflicts_for_duplicate_scheduled_time() -> None:
    owner = Owner(name="Jordan", availability_start="08:00", availability_end="17:00")
    dog = Pet(name="Buddy", species="dog")
    cat = Pet(name="Whiskers", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    task1 = Task(title="Walk", duration_minutes=20, scheduled_start_time="09:00")
    task2 = Task(title="Groom", duration_minutes=15, scheduled_start_time="09:00")
    dog.add_task(task1)
    cat.add_task(task2)

    planner = SchedulePlanner(owner=owner, available_minutes=120, employees=["Alex"])
    conflicts = planner.detect_conflicts([task1, task2])

    assert any("scheduled at the same time 09:00" in conflict for conflict in conflicts)


def test_generate_schedule_assigns_scheduled_times() -> None:
    owner = Owner(name="Jordan", availability_start="08:00", availability_end="10:00")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    walk = Task(title="Walk", duration_minutes=30, preferred_start_time="08:30")
    feed = Task(title="Feed", duration_minutes=15, priority="high")
    pet.add_task(walk)
    pet.add_task(feed)

    planner = SchedulePlanner(owner=owner, available_minutes=90, employees=["Alex"])
    scheduled = planner.generate_schedule()

    assert walk.scheduled_start_time == "08:30"
    assert feed.scheduled_start_time == "09:00"
    assert len(scheduled) == 2
