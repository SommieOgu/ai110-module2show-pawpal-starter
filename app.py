import streamlit as st
from pawpal_system import Owner, Pet, Task, SchedulePlanner

st.set_page_config(page_title="PawPal+", layout="centered")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name="Jordan")

owner: Owner = st.session_state["owner"]


def format_task_rows(tasks: list[Task]) -> list[dict[str, str | int | bool]]:
    rows: list[dict[str, str | int | bool]] = []
    for pet in owner.pets:
        for task in pet.tasks:
            if task in tasks:
                rows.append(
                    {
                        "Pet": pet.name,
                        "Title": task.title,
                        "Duration": task.duration_minutes,
                        "Priority": task.priority,
                        "Preferred start": task.preferred_start_time or "N/A",
                        "Scheduled start": task.scheduled_start_time or "TBD",
                        "Due date": task.due_date.isoformat() if task.due_date else "N/A",
                        "Completed": task.completed,
                    }
                )
    return rows

st.title("PawPal+")

st.markdown(
    """
Welcome to PawPal+. This app uses a backend scheduler to manage owners, pets, and tasks.
"""
)

owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Add a pet")
with st.form(key="add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "fish", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=1)
    add_pet_button = st.form_submit_button("Add pet")

    if add_pet_button and pet_name:
        new_pet = Pet(name=pet_name, species=species, age=age)
        owner.add_pet(new_pet)
        st.success(f"Added pet {pet_name}.")

if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a task")
if owner.pets:
    selected_pet_name = st.selectbox(
        "Select pet to assign task",
        [pet.name for pet in owner.pets],
    )
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)

    with st.form(key="add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        description = st.text_area("Description", value="")
        add_task_button = st.form_submit_button("Add task")

        if add_task_button and task_title:
            new_task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                description=description,
            )
            selected_pet.add_task(new_task)
            st.success(f"Added task '{task_title}' to {selected_pet.name}.")

    if selected_pet.tasks:
        st.write(f"Tasks for {selected_pet.name}:")
        st.table(
            [
                {
                    "Title": task.title,
                    "Duration": task.duration_minutes,
                    "Priority": task.priority,
                    "Description": task.description,
                    "Completed": task.completed,
                }
                for task in selected_pet.tasks
            ]
        )
    else:
        st.info(f"No tasks yet for {selected_pet.name}.")
else:
    st.info("Add a pet first to enable task scheduling.")

st.divider()

st.subheader("Build Schedule")
planner = SchedulePlanner(owner=owner, available_minutes=480, employees=["Alex"])
unscheduled_tasks = planner.retrieve_all_tasks(completed=False)

if unscheduled_tasks:
    st.markdown("### Upcoming Task Queue")
    sorted_upcoming = planner.sort_tasks_by_time(unscheduled_tasks)
    st.table(format_task_rows(sorted_upcoming))
else:
    st.info("No unscheduled tasks are available to schedule.")

if st.button("Generate schedule"):
    scheduled = planner.generate_schedule()
    st.markdown("### Today's Schedule")
    if scheduled:
        st.success(planner.get_plan_summary())
        if planner.conflicts:
            for conflict in planner.conflicts:
                st.warning(conflict)
        st.table(format_task_rows(scheduled))
        st.write(planner.explain_plan())
    else:
        st.warning("No tasks could be scheduled with the current constraints.")
