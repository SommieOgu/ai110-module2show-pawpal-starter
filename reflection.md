# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

     My initial thoughts is that their would be a owner and pet with a has-relationship. I also assumed there would be a pet care task and schedule. where the task and their duration would dictate the schedule.

- What classes did you include, and what responsibilities did you assign to each?

 My initial thoughts is that their would be a owner class and pet class with a has-relationship. I also assumed there would be a pet care task and schedule class. The owner and pet class would be responsible for tracking names, which pet/which owner they belong to and what date they came in. In the owner class their would be a special attribute for time to pick up times. In the the other classes pet task and schedule they will have a shared attribute on durration and priority and they will point to each otehr and will have an is- a realationship with the pets. class task will include methods like shower wich will calulate the time it takes to wash a pet based on pet and owners needs



**b. Design changes**

- Did your design change during implementation?
    Yes it did, way more than expected

- If yes, describe at least one change and why you made it.
    I intially was thinking of the four classes and a few attributes. However, after AI help was was able to add more attributes and way more methods to the classes that was proposed. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    In my scheduler considers all of those. Time is a big thing with wanting to get as many clients per day while considering priority of the pets and the preferences. I would also say add aother contraint which is number of workers. if we only have 2 people in the schedule need to be less packed.

- How did you decide which constraints mattered most?
     Time is a primary! No schedule can exceed daily available minutes. Next was priority, if time is limited, choose the most important tasks first. Owners preferences after, use them to favor owner/pet needs once time and priority are respected. Lastly, worker_count adjusts capacity. if you have more workers, you can schedule more tasks overall. if you have fewer workers, keep the plan less packed. It prioritizes high-priority tasks first and fits as many of those tasks into the available minutes as possible. That means lower-priority tasks may be left unscheduled when time is limited. 



**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
   One tradeoff the scheduler makes is prioritizing preferred start times and task priority first, then greedily filling available minutes, which can leave small unused gaps or leave lower-priority tasks unscheduled.

- Why is that tradeoff reasonable for this scenario?
    This tradeoff is very reasonable because in a pet care/shop scenario, it is more important to complete urgent or owner-preferred tasks than to force every task into the day. It keeps the schedule practical and predictable for a busy owner or limited staff.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI for parts of this project: designing mermaid code, filling gaps in my brainstorming, turning phase 2 ideas into class code, debugging logic, and refining the Streamlit UI. It helped me understand each step and made it easier to translate my thoughts into working Python classes. I also used AI to explain sections of the code when I wanted to know why a particular approach worked or didn't work.

- What kinds of prompts or questions were most helpful?
     The most helpful prompts were action-oriented and included the relevant file names or code snippets. When I said exactly what I wanted to do and pointed to the file, the AI could focus on the task instead of guessing. Vague prompts were less productive, so I learned to keep requests specific and task-focused.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    In phase 2, the AI initially treated the owner as a worker on the schedule, which did not match the pet shop scenario. I did not accept that suggestion and instead added a separate randomized employee list for staffing. That change kept the owner and employee roles distinct and made the model more realistic.

- How did you evaluate or verify what the AI suggested?
     I evaluated suggestions by checking whether they matched the prompt, reading the actual code changes, and running the relevant behavior manually. I also used tests to verify that the new behavior worked correctly. For example, after a scheduling change, I checked that tasks were ordered by priority and time the way I expected in my phas 2 but order changed in phase 4, and I confirmed the code still passed the test cases.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested that completing a daily task marks it complete and creates the next occurrence, that tasks are sorted correctly by preferred start time and priority, and that duplicate preferred or scheduled start times are detected as conflicts. I also verified that task retrieval and filtering work by pet and completion status so the schedule only considers the right tasks.

- Why were these tests important?
    These tests validate the core scheduler logic: recurring tasks must continue automatically, time-sensitive work needs to be ordered correctly, and conflicting appointments should not silently pass through. That helps ensure the app produces a realistic daily plan instead of impossible or poorly ordered task lists.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am not that confident, maybe a 4 out of 5, because the test cases cover happy paths and important edge cases, but the demo still showed a lot of incomplete tasks with different priorities. The scheduler handles the basic behaviors I tested, yet the live demo suggests task ordering and completion handling can still be improved. I also feel testing can never be 100% complete, so it’s realistic to leave room for unknown cases. That’s why I keep the confidence level lower even though the core logic passed the tests.

- What edge cases would you test next if you had more time?
    Next I would test more edge cases around overloaded schedules, like when total task duration exceeds the available window. I’d also verify behavior with multiple workers, since a real shop should not rely on only one worker all day. Finally, I’d check how recurring tasks, due dates, and owner availability interact when tasks must be deferred or shifted.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I was most satisfied with seeing my original idea for four classes and their attributes come to life in working Python code. It felt good to turn the UML planning into real class and scheduler behavior. The design started on paper and then actually worked together in the app, which made the planning exercise feel worthwhile. That made the whole project feel more concrete and rewarding

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would spend more time on class brainstorming and refining the UML before coding. Right now the design feels a bit cluttered and some classes are doing too much, so I’d separate responsibilities more clearly. I’d also add more tests early, because better coverage would catch issues before they become messy. That would make the system cleaner and easier to extend.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    I learned to always double-check the AI’s suggestions instead of accepting them blindly. The best prompts were action-oriented and included file names or code snippets, because that let the AI focus on the exact task. Vague requests were less productive, so being specific made the work much smoother.
