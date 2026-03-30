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
		pass

	def estimate_score(self, preferences: str) -> int:
		pass


@dataclass
class Pet:
	name: str
	species: str
	age: int
	notes: str
	tasks: list[CareTask] = field(default_factory=list)

	def get_tasks(self) -> list[CareTask]:
		pass

	def update_notes(self, notes: str) -> None:
		pass


@dataclass
class DailyPlan:
	date: date
	scheduled_items: list[ScheduledItem] = field(default_factory=list)
	total_minutes: int = 0
	explanations: list[str] = field(default_factory=list)

	def add_item(self, task: CareTask, time_slot: str) -> None:
		pass

	def summarize(self) -> str:
		pass

	def get_todays_tasks(self) -> list[CareTask]:
		pass


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
		pass

	def add_task(self, task: CareTask, pet: Pet | None = None) -> None:
		pass

	def request_daily_plan(self, for_date: date, scheduler: Scheduler | None = None) -> DailyPlan:
		pass


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
		pass

	def explain_choice(self, task: CareTask) -> str:
		pass

