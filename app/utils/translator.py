from googletrans import Translator, LANGUAGES

translator = Translator()

def detect_and_translate(text):
    """Returns (translated_text, original_lang_name)"""
    try:
        detected = translator.detect(text)
        lang_code = detected.lang
        lang_name = LANGUAGES.get(lang_code, lang_code).title()

        if lang_code == 'en':
            return text, 'English'

        result = translator.translate(text, dest='en')
        return result.text, lang_name
    except Exception:
        return text, 'Unknown'