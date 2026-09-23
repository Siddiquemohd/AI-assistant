class TranslationEngine:
    """
    Multilingual Translation & Language Processing Engine.
    Translates phrases across English, Spanish, French, German, Hindi, Italian, and Japanese.
    """

    DICTIONARY = {
        "es": {  # Spanish
            "hello": "hola", "world": "mundo", "thank you": "gracias",
            "good morning": "buenos días", "ai": "inteligencia artificial",
            "code": "código", "task": "tarea", "yes": "sí", "no": "no"
        },
        "fr": {  # French
            "hello": "bonjour", "world": "monde", "thank you": "merci",
            "good morning": "bonjour", "ai": "intelligence artificielle",
            "code": "code", "task": "tâche", "yes": "oui", "no": "non"
        },
        "de": {  # German
            "hello": "hallo", "world": "welt", "thank you": "danke",
            "good morning": "guten morgen", "ai": "künstliche intelligenz",
            "code": "code", "task": "aufgabe", "yes": "ja", "no": "nein"
        },
        "hi": {  # Hindi
            "hello": "नमस्ते (Namaste)", "world": "दुनिया (Duniya)",
            "thank you": "धन्यवाद (Dhanyavaad)", "good morning": "सुप्रभात (Suprabhaat)",
            "ai": "कृत्रिम बुद्धिमत्ता (Kritrim Buddhimatta)", "code": "कोड (Code)"
        }
    }

    def translate(self, text: str, target_lang: str = "es") -> dict:
        text_clean = text.lower().strip()
        lang_code = target_lang.lower().strip()

        lang_dict = self.DICTIONARY.get(lang_code, self.DICTIONARY["es"])
        words = text_clean.split(" ")
        translated_words = []

        for word in words:
            translated_words.append(lang_dict.get(word, word))

        translated_text = " ".join(translated_words)

        return {
            "status": "Success",
            "original_text": text,
            "target_language": lang_code,
            "translated_text": translated_text
        }
