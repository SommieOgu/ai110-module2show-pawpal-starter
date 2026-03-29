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
