from pawpal_system import CareTask, Owner, Pet, Scheduler


def test_mark_complete_changes_task_status():
	task = CareTask(
		title="Feed the cat",
		duration_minutes=10,
		priority="high",
		task_type="daily",
		is_required=True,
	)

	assert task.is_completed is False

	task.mark_complete()

	assert task.is_completed is True


def test_adding_task_to_pet_increases_task_count():
	owner = Owner(name="Alex", daily_time_available=120, preferences="feeding")
	pet = Pet(name="Mochi", species="cat", age=3, notes="")
	task = CareTask(
		title="Brush fur",
		duration_minutes=15,
		priority="medium",
		task_type="daily",
		is_required=False,
	)

	initial_task_count = len(pet.tasks)

	owner.add_task(task, pet)

	assert len(pet.tasks) == initial_task_count + 1
	assert task in pet.tasks


def test_sort_by_time_simple():
	scheduler = Scheduler(strategy_name="test")
	times = ["09:00", "08:30", "12:45", "08:00", "10:15"]
	expected = ["08:00", "08:30", "09:00", "10:15", "12:45"]

	assert scheduler.sort_by_time(times) == expected


def test_sort_by_time_with_ranges():
	scheduler = Scheduler(strategy_name="test")
	times = ["09:00-09:30", "08:00-08:15", "10:00-10:30", "08:30-08:45"]
	expected = ["08:00-08:15", "08:30-08:45", "09:00-09:30", "10:00-10:30"]

	assert scheduler.sort_by_time(times) == expected
