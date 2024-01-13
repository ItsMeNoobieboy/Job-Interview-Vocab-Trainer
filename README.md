## Inspiration
The inspiration for this project came when we were thinking about the struggles that ESL speakers face when attempting to get a job. Our group realized that many ESL speakers know general vocabulary in English, but their vocabulary might not include words relevant to their careers. In order for them to learn this, we thought that having a simulator for a job interview where they can review vocabulary would be helpful interviews and in their careers. Additionally, having the opportunity to practice a job interview would allow them to be more confident that they know how to answer the questions that they might encounter in a real interview.

## What it does
Our application starts by asking the user to input their native language, which will be used as the reference language for the translations. The simulated interview starts with a general question regarding the person’s job interests. The person responds to the questions as if they are in a professional interview, and the “interviewer” replies with AI-generated answers. After asking a maximum of eight questions, the chatbot ends the conversation. As the interview continues, the user can click on words they do not recognize in English. These words are added to a list of words on the left side of the screen. The user is also allowed to manually enter words they want to translate. The application generates a table of these words and their translations so the user can review. Then, it generates a memory association game using the recorded words. This allows the interviewee to identify industry-specific words in English to help them prepare for real-life interviews.

## How we built it
We used a shared coding environment on Visual Studio Code. For the backend, we used Python to combine a ChatGPT and language translation API that one of our team members had access to. For the frontend, we used a combination of CSS, JavaScript, and HTML with Svelte  


## Challenges we ran into
Our main challenges were integrating the Python code into the website and making the "Words to Learn" list save everything given to it. We managed to overcome these challenges by splitting up the work between people who understood different aspects of it, allowing us to efficiently work on the project.

## Accomplishments that we're proud of
There are three main accomplishments in this project that we are proud of. The first and biggest one is the smooth integration of ChatGPT into the interview program, which we did using websockets. Our second main accomplishment was coding a secondary Flashcards mode that allows the interviewee to study the words they do not know in a fun, engaging manner. Lastly, four out of the five of us learned Svelte for the first time! We had not seen the language before today, but we all picked it up fast and implemented it effectively.


## What we learned
We learned how to integrate the ChatGPT API into a web application and combine different programming languages to develop a user interface as well as how to improve the stylistic components of our application. Mainly, though, most of our group learned Svelte and how to integrate Python with it.

## What's next for Job Interview Simulator
If we were to continue this project, we’d like to refine the visuals and features of the website. It’s a bit laggy (on OpenAI’s end) which makes it more difficult to use and we’d like to use a better translation service which gives more nuance to the translations. Additionally, we’d like to add a feature so the user can enter words in their native language to the “Words to Learn” list. Finally, we believe it would also be helpful for learners to have an audio feature where they speak to the website and listen to the responses out loud, so they’re more confident in their ability to understand the interviewer and be understood.

## Instructions for Use

To use this website, make sure to add your OpenAI API key to backend/api_key_storage.py!