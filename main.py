import random

from pawpal_system import Task, Pet, Owner, SchedulePlanner


def main() -> None:
    owner = Owner(name="Jordan", availability_start="08:00", availability_end="17:00")

    dog = Pet(name="HoneyComb", species="dog", age=3)
    fish = Pet(name="Gorilla", species="fish", age=1)

    owner.add_pet(dog)
    owner.add_pet(fish)

    dog.add_task(
        Task(
            title="Morning walk",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            description=f"Take {dog.name} for a walk.",
        )
    )
    dog.add_task(
        Task(
            title="Feed breakfast",
            duration_minutes=15,
            priority="medium",
            frequency="daily",
            description=f"Feed {dog.name} his morning meal.",
        )
    )

    fish.add_task(
        Task(
            title="Tank check",
            duration_minutes=10,
            priority="medium",
            frequency="daily",
            description=f"Check {fish.name}'s tank water and filter.",
            preferred_start_time="08:15",
        )
    )
    fish.add_task(
        Task(
            title="Feed flakes",
            duration_minutes=5,
            priority="high",
            frequency="daily",
            description=f"Feed {fish.name} fish flakes.",
            completed=True,
            preferred_start_time="08:15",
        )
    )

    # Add tasks out of order to demonstrate sorting by preferred_start_time.
    dog.add_task(
        Task(
            title="Evening play",
            duration_minutes=20,
            priority="low",
            frequency="daily",
            description=f"Play with {dog.name} before bedtime.",
            preferred_start_time="18:00",
        )
    )
    dog.add_task(
        Task(
            title="Breakfast treat",
            duration_minutes=10,
            priority="high",
            frequency="daily",
            description=f"Give {dog.name} a morning treat.",
            preferred_start_time="08:15",
        )
    )

    employee_names = ["Alex", "Taylor", "Morgan", "Riley", "Sam", "Jamie"]
    employees = random.sample(employee_names, k=random.randint(1, 3))

    planner = SchedulePlanner(owner=owner, available_minutes=240, employees=employees)
    planner.generate_schedule()

    print("Today's Schedule")
    print("----------------")
    print(planner.explain_plan())
    print()
    print(planner.get_plan_summary())
    print()

    print("All tasks sorted by preferred time:")
    for task in planner.sort_tasks_by_time(owner.get_all_tasks()):
        print(f"- {task.describe()}")

    print()
    print("Incomplete tasks:")
    for task in planner.filter_tasks(completed=False):
        print(f"- {task.describe()}")

    print()
    print("Tasks for HoneyComb:")
    for task in planner.filter_tasks(pet_name="HoneyComb"):
        print(f"- {task.describe()}")


if __name__ == "__main__":
    main()
