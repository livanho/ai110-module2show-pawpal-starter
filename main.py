from __future__ import annotations

from datetime import date

from pawpal_system import CareTask, Owner, Pet, Scheduler


def build_demo_plan() -> str:
	owner = Owner(name="Jordan", daily_time_available=120, preferences="walk feeding grooming")

	dog = Pet(name="Mochi", species="dog", age=4, notes="Energetic morning walker")
	cat = Pet(name="Luna", species="cat", age=2, notes="Likes quiet evening routines")
	owner.add_pet(dog)
	owner.add_pet(cat)

	task_1 = CareTask(
		title="Morning walk",
		duration_minutes=30,
		priority="high",
		task_type="daily",
		is_required=True,
		pet=dog,
	)
	task_2 = CareTask(
		title="Breakfast feeding",
		duration_minutes=15,
		priority="high",
		task_type="daily",
		is_required=True,
		pet=cat,
	)
	task_3 = CareTask(
		title="Evening brushing",
		duration_minutes=20,
		priority="medium",
		task_type="daily",
		is_required=False,
		pet=dog,
	)

	owner.add_task(task_1)
	owner.add_task(task_2)
	owner.add_task(task_3)

	scheduler = Scheduler(strategy_name="priority_first")
	plan = owner.request_daily_plan(for_date=date.today(), scheduler=scheduler)

	return plan.summarize()


if __name__ == "__main__":
	print("Today's Schedule")
	print(build_demo_plan())
