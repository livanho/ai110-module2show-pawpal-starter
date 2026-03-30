# PawPal+ Project Reflection

## 1. System Design

### Core user actions

1. Add a pet profile.
2. Add a care task for a pet.
3. Generate and view today's plan.

### Main objects, attributes, and methods

#### Owner

- Attributes: `name`, `daily_time_available`, `preferences`
- Methods: `add_pet(pet)`, `add_task(task)`, `request_daily_plan(date)`

#### Pet

- Attributes: `name`, `species`, `age`, `notes`
- Methods: `get_tasks()`, `update_notes(notes)`

#### CareTask

- Attributes: `title`, `duration_minutes`, `priority`, `task_type`, `is_required`
- Methods: `is_due_today(date)`, `estimate_score(preferences)`

#### DailyPlan

- Attributes: `date`, `scheduled_items`, `total_minutes`, `explanations`
- Methods: `add_item(task, time_slot)`, `summarize()`, `get_todays_tasks()`

#### Scheduler

- Attributes: `strategy_name`
- Methods: `build_plan(owner, pets, tasks, date)`, `explain_choice(task)`

### Mermaid class diagram

```mermaid
classDiagram
	class Owner {
		+String name
		+int daily_time_available
		+String preferences
		+add_pet(pet)
		+add_task(task)
		+request_daily_plan(date)
	}

	class Pet {
		+String name
		+String species
		+int age
		+String notes
		+get_tasks()
		+update_notes(notes)
	}

	class CareTask {
		+String title
		+int duration_minutes
		+String priority
		+String task_type
		+bool is_required
		+is_due_today(date) bool
		+estimate_score(preferences) int
	}

	class DailyPlan {
		+String date
		+List scheduled_items
		+int total_minutes
		+List explanations
		+add_item(task, time_slot)
		+summarize() String
		+get_todays_tasks() List
	}

	class Scheduler {
		+String strategy_name
		+build_plan(owner, pets, tasks, date) DailyPlan
		+explain_choice(task) String
	}

	Owner "1" o-- "0..*" Pet : owns
	Pet "1" o-- "0..*" CareTask : needs
	Owner "1" o-- "0..*" CareTask : manages
	Scheduler ..> Owner : uses
	Scheduler ..> Pet : uses
	Scheduler ..> CareTask : ranks
	Scheduler --> DailyPlan : creates
	DailyPlan "1" o-- "0..*" CareTask : schedules
```

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
