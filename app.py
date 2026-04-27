import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, CareTask

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        daily_time_available=120,
        preferences="walk feeding",
    )

if "selected_pet_name" not in st.session_state:
    st.session_state.selected_pet_name = None

if "daily_plan" not in st.session_state:
    st.session_state.daily_plan = None

owner = st.session_state.owner


def find_pet_by_name(name: str) -> Pet | None:
    for pet in owner.pets:
        if pet.name == name:
            return pet
    return None


def task_to_row(task: CareTask) -> dict[str, str | int | bool]:
    return {
        "title": task.title,
        "duration_minutes": task.duration_minutes,
        "priority": task.priority,
        "task_type": task.task_type,
        "is_required": task.is_required,
        "pet": task.pet.name if task.pet else "General",
    }


st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=owner.name)
daily_time = st.number_input(
    "Daily time available (minutes)", min_value=15, max_value=1440, value=int(owner.daily_time_available), step=15
)
preferences = st.text_input("Owner preferences (keywords)", value=owner.preferences)

owner.name = owner_name.strip() or owner.name
owner.daily_time_available = int(daily_time)
owner.preferences = preferences.strip()

st.markdown("### Add a Pet")
pet_col1, pet_col2 = st.columns(2)
with pet_col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with pet_col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=3)
pet_notes = st.text_area("Pet notes", value="")

if st.button("Add pet"):
    normalized_name = pet_name.strip().lower()
    if not normalized_name:
        st.warning("Please enter a pet name.")
    elif any(existing.name.strip().lower() == normalized_name for existing in owner.pets):
        st.info("That pet already exists for this owner.")
    else:
        new_pet = Pet(
            name=pet_name.strip(),
            species=species,
            age=int(pet_age),
            notes=pet_notes.strip(),
        )
        owner.add_pet(new_pet)
        st.session_state.selected_pet_name = new_pet.name
        st.success(f"Added pet: {new_pet.name}")

if owner.pets:
    pet_rows = [
        {
            "name": pet.name,
            "species": pet.species,
            "age": pet.age,
            "notes": pet.notes,
            "tasks": len(pet.tasks),
        }
        for pet in owner.pets
    ]
    st.write("Current pets:")
    st.table(pet_rows)
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("### Tasks")
st.caption("Add care tasks and save them as CareTask objects for the selected pet.")

pet_names = [pet.name for pet in owner.pets]
if pet_names:
    if st.session_state.selected_pet_name not in pet_names:
        st.session_state.selected_pet_name = pet_names[0]
    selected_pet_name = st.selectbox(
        "Assign task to pet",
        pet_names,
        index=pet_names.index(st.session_state.selected_pet_name),
    )
    st.session_state.selected_pet_name = selected_pet_name
else:
    selected_pet_name = None
    st.caption("No pet selected. Add a pet first.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_col1, task_col2 = st.columns(2)
with task_col1:
    task_type = st.selectbox("Task type", ["daily", "weekday", "weekend"], index=0)
with task_col2:
    is_required = st.checkbox("Required task", value=True)

if st.button("Add task"):
    clean_title = task_title.strip()
    if not clean_title:
        st.warning("Please enter a task title.")
    elif selected_pet_name is None:
        st.warning("Add a pet before adding tasks.")
    else:
        selected_pet = find_pet_by_name(selected_pet_name)
        already_exists = any(
            existing.title.strip().lower() == clean_title.lower()
            and existing.duration_minutes == int(duration)
            and existing.pet is not None
            and existing.pet.name == selected_pet_name
            for existing in owner.tasks
        )
        if already_exists:
            st.info("That task already exists for the selected pet.")
        else:
            new_task = CareTask(
                title=clean_title,
                duration_minutes=int(duration),
                priority=priority,
                task_type=task_type,
                is_required=is_required,
                pet=selected_pet,
            )
            owner.add_task(new_task, selected_pet)
            st.success(f"Added task: {new_task.title}")

if owner.tasks:
    st.write("Current tasks:")
    st.table([task_to_row(task) for task in owner.tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule using Owner.request_daily_plan.")

if st.button("Generate schedule"):
    if not owner.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        st.session_state.daily_plan = owner.request_daily_plan(for_date=date.today())

if st.session_state.daily_plan is not None:
    plan = st.session_state.daily_plan
    st.write(plan.summarize())

    if plan.scheduled_items:
        plan_rows = [
            {
                "time_slot": item.time_slot,
                "task": item.task.title,
                "pet": item.task.pet.name if item.task.pet else "General",
                "duration_minutes": item.task.duration_minutes,
                "priority": item.task.priority,
            }
            for item in plan.scheduled_items
        ]
        st.table(plan_rows)

    if plan.explanations:
        st.markdown("### Why these tasks were chosen")
        for explanation in plan.explanations:
            st.write(f"- {explanation}")
