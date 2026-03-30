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
        )
    )
    fish.add_task(
        Task(
            title="Feed flakes",
            duration_minutes=5,
            priority="high",
            frequency="daily",
            description=f"Feed {fish.name} fish flakes.",
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


if __name__ == "__main__":
    main()
