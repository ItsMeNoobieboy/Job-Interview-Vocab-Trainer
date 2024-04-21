from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

class GPT:
    def __init__(self, api_key=API_KEY):
        self.memory = ["Hello, thank you for coming in today. I understand that you're interested in working at our company. Can you please start by telling me which position you are applying for?"]
        self.client = OpenAI(api_key=api_key)

    def get_completion(self, prompt="", model="gpt-3.5-turbo",role_prompt=None):
        if role_prompt is None:
            role_prompt = "Act like an interviewer for a job. The person you're talking to wants to work at your company. DO NOT RESPOND AS THE INTERVIEWEE. YOU ARE THE INTERVIEWER. DO NOT RESPOND TO ANYTHING UNRELATED TO THE INTERVIEW. END EVERY RESPONSE WITH A QUESTION. ONLY RESPOND IN ENGLISH. do not thank the interviewee in every response. ask the first interview question. The interview will end after 8 questions, so talk to the user accordingly."
        
        self.memory.append(prompt)
        messages = [{"role": "user", "content": prompt}, {"role": "assistant", "content": ''.join(self.memory)+role_prompt}]
        
        msg = ""
        for chunk in self.client.chat.completions.create(model = model, messages = messages, temperature = 0, stream=True):
            chunk = chunk.choices[0].delta.content
            if chunk is None:
                continue
            yield chunk
            msg += chunk
            # print(chunk)

        self.memory.append(msg)

        # return msg


if __name__ == "__main__":

    gpt = GPT()#api_key, job)
    for _ in range(5):
        prompt = input("Enter your prompt: ")
        
        response = gpt.get_completion(prompt)
        print(response)

