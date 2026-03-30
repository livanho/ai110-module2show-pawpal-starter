from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class CareTask:
	title: str
	duration_minutes: int
	priority: str
	task_type: str
	is_required: bool
	pet: Pet | None = None

	def is_due_today(self, for_date: date) -> bool:
		if self.is_required:
			return True

		task_type_normalized = self.task_type.strip().lower()
		if task_type_normalized == "daily":
			return True
		if task_type_normalized == "weekday":
			return for_date.weekday() < 5
		if task_type_normalized == "weekend":
			return for_date.weekday() >= 5

		return True

	def estimate_score(self, preferences: str) -> int:
		priority_weights = {
			"high": 100,
			"medium": 60,
			"low": 30,
		}
		priority_score = priority_weights.get(self.priority.strip().lower(), 0)

		required_bonus = 40 if self.is_required else 0

		preferences_tokens = {
			token
			for token in preferences.lower().replace(",", " ").split()
			if token
		}
		title_tokens = {
			token
			for token in self.title.lower().replace(",", " ").split()
			if token
		}
		type_tokens = {
			token
			for token in self.task_type.lower().replace(",", " ").split()
			if token
		}
		preference_match_bonus = 15 if preferences_tokens & (title_tokens | type_tokens) else 0

		# Slightly favor shorter tasks so plans can fit more essential work.
		duration_penalty = min(self.duration_minutes // 15, 20)

		return priority_score + required_bonus + preference_match_bonus - duration_penalty


@dataclass
class Pet:
	name: str
	species: str
	age: int
	notes: str
	tasks: list[CareTask] = field(default_factory=list)

	def get_tasks(self) -> list[CareTask]:
		return list(self.tasks)

	def update_notes(self, notes: str) -> None:
		self.notes = notes.strip()


@dataclass
class DailyPlan:
	date: date
	scheduled_items: list[ScheduledItem] = field(default_factory=list)
	total_minutes: int = 0
	explanations: list[str] = field(default_factory=list)

	def add_item(self, task: CareTask, time_slot: str) -> None:
		self.scheduled_items.append(ScheduledItem(task=task, time_slot=time_slot))
		self.total_minutes += task.duration_minutes

	def summarize(self) -> str:
		if not self.scheduled_items:
			return f"No tasks scheduled for {self.date.isoformat()}."

		lines = [f"Plan for {self.date.isoformat()} ({self.total_minutes} min):"]
		for item in self.scheduled_items:
			pet_name = item.task.pet.name if item.task.pet else "General"
			lines.append(
				f"- {item.time_slot}: {item.task.title} ({item.task.duration_minutes} min, {item.task.priority}, {pet_name})"
			)

		if self.explanations:
			lines.append("Explanations:")
			for explanation in self.explanations:
				lines.append(f"- {explanation}")

		return "\n".join(lines)

	def get_todays_tasks(self) -> list[CareTask]:
		return [item.task for item in self.scheduled_items]


@dataclass
class ScheduledItem:
	task: CareTask
	time_slot: str


class Owner:
	def __init__(
		self,
		name: str,
		daily_time_available: int,
		preferences: str,
	) -> None:
		self.name = name
		self.daily_time_available = daily_time_available
		self.preferences = preferences
		self.pets: list[Pet] = []
		self.tasks: list[CareTask] = []
		self.scheduler: Scheduler | None = None

	def add_pet(self, pet: Pet) -> None:
		if pet not in self.pets:
			self.pets.append(pet)

	def add_task(self, task: CareTask, pet: Pet | None = None) -> None:
		target_pet = pet or task.pet
		if target_pet is not None:
			task.pet = target_pet
			if target_pet not in self.pets:
				self.pets.append(target_pet)
			if task not in target_pet.tasks:
				target_pet.tasks.append(task)

		if task not in self.tasks:
			self.tasks.append(task)

	def request_daily_plan(self, for_date: date, scheduler: Scheduler | None = None) -> DailyPlan:
		effective_scheduler = scheduler or self.scheduler or Scheduler(strategy_name="priority_first")
		self.scheduler = effective_scheduler
		return effective_scheduler.build_plan(
			owner=self,
			pets=self.pets,
			tasks=self.tasks,
			for_date=for_date,
		)


class Scheduler:
	def __init__(self, strategy_name: str) -> None:
		self.strategy_name = strategy_name

	def build_plan(
		self,
		owner: Owner,
		pets: list[Pet],
		tasks: list[CareTask],
		for_date: date,
	) -> DailyPlan:
		plan = DailyPlan(date=for_date)

		due_tasks = [task for task in tasks if task.is_due_today(for_date)]
		sorted_tasks = sorted(
			due_tasks,
			key=lambda task: (
				not task.is_required,
				-task.estimate_score(owner.preferences),
				task.duration_minutes,
				task.title.lower(),
			),
		)

		def minutes_to_hhmm(total_minutes: int) -> str:
			hours = total_minutes // 60
			minutes = total_minutes % 60
			return f"{hours:02d}:{minutes:02d}"

		used_minutes = 0
		day_start_minutes = 8 * 60
		for task in sorted_tasks:
			if used_minutes + task.duration_minutes > owner.daily_time_available:
				plan.explanations.append(
					f"Skipped '{task.title}' due to time limit ({owner.daily_time_available} min/day)."
				)
				continue

			start = day_start_minutes + used_minutes
			end = start + task.duration_minutes
			time_slot = f"{minutes_to_hhmm(start)}-{minutes_to_hhmm(end)}"
			plan.add_item(task=task, time_slot=time_slot)
			plan.explanations.append(self.explain_choice(task))
			used_minutes += task.duration_minutes

		if not plan.scheduled_items:
			plan.explanations.append("No due tasks fit within available time.")

		return plan

	def explain_choice(self, task: CareTask) -> str:
		required_note = "required" if task.is_required else "optional"
		pet_name = task.pet.name if task.pet else "general care"
		return (
			f"Selected '{task.title}' for {pet_name} because it is {required_note}, "
			f"priority={task.priority}, duration={task.duration_minutes} min."
		)

