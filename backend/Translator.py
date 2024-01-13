import translate
from openai import OpenAI
from api_key_storage import API_KEY

client = OpenAI(api_key=API_KEY)

def convert_to_code(language_name, model="gpt-3.5-turbo-0301"):
    messages = [{"role": "user", "content": language_name}, {"role": "assistant", "content": 'You are converting the name of a language to its language code. Do not say anything except for the language code. If you dont understand the language name, say en.'}]
    response = client.chat.completions.create(model = model, messages = messages, temperature = 0)

    language_code = response.choices[0].message.content
    return language_code

class Translator:
    def __init__(self, native_lang, as_word=True):
        if as_word:
            native_lang = convert_to_code(native_lang)
        self.translator_en = translate.Translator(from_lang=native_lang, to_lang="en")
        self.translator_native = translate.Translator(from_lang="en", to_lang=native_lang)

    def translate_to_english(self, message):
        translation = self.translator_en.translate(message)

        return translation
    
    def translate_to_native(self, message):
        translation = self.translator_native.translate(message)

        return translation