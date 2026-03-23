# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. Press enter to apply did not actually work
2. I have to click 'Submit Guess' button 2x
3. The hint was wrong. It always said 'Go Higher' but that wasn't the case
4. When I click the 'New Game' button after winning, it doesn't actually start a new game welp. It just resets the attempts number. It no longer stores the history of the input in that new game
5. In the middle of the game and before winning, when I try to do 'new game', it still stores the old history
   1. This also makes the game go out of attempts earlier than expected
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

I used Claude Opus 4.5

**Example of correct AI suggestion:** It correctly pointed out where the bug for incorrect guess was

**Example of misleading suggestion:** When the pytest was not working because of path import error, it suggested I create a conftest.py file and then set the path. 
I questioned this suggestion because it adds an unnecessary file to the codebase. Instead, it can be helpful to just add the path there



## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I played the game again to check whether the 2 bugs (incorrect hints and 2 tries to submit one guess) were fixed or not. I ran both manual and pytest. 

AI helped me in understanding the issue with my tests because initially it was just result == "win". But the output returned by check_guess is actually an array
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit is a python library that creates interactive web pages from python scripts. 

Reruns are when a user interacts with the app. Each button click or interaction makes the app re-execute from top to bottom

Because these reruns happen, the session state is important to preserve the value of variables from one state to the next

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

1. One strategy => Question the LLM back about its suggestion. Like do I really need to implement it this way? And most likely, the following discussion leads to a more optimal understanding than the first session
2. One thing to do differently => Slow down and review its refactoring suggestion line by line. This was a simpler codebase so it didn't matter as much. But in bigger codebases, it absolutely matters.
3. It didn't change the way I think about AI generated code, but it taught me better ways to collaborate with it and slow down when learning from AI. I still want to learn how to get over its wall of text response and digest the info.

