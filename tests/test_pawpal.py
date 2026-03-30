from pawpal_system import Pet, Task


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
