import json
import logging
import os
from datetime import datetime
from pathlib import Path
from kvgui.modules import signals as sig

TRANSLATION_VERSION = '0.0.1'

# TEMPLATE_PATH = Path('kvgui/translations/translation_template.json')
# TEMPLATE_PATH = TEMPLATE_PATH.absolute().as_posix()


DEFAULT_TRANSLATION = {
    "meta": {
        "language": None,
        "author": None,
        "version": TRANSLATION_VERSION,
        "date": datetime.strftime(datetime.now(), "%d.%m.%Y")
    },
    "context": {

    }
}


class Translator:
    def __init__(self):
        self._lang = DEFAULT_TRANSLATION
        self.translations = list(lang.stem for lang in Path('kvgui', 'translations').iterdir())
        print(self.translations)
        sig.set_lang.connect(self.load_lang)

    def load_lang(self, lang='English', **kwargs):
        # if lang == 'English':
        #     self._lang = DEFAULT_TRANSLATION
        #     return
        try:
            path = Path('kvgui', 'translations', f'{lang}.json').absolute().as_posix()
            with open(path, 'r', encoding='utf-8') as fp:
                self._lang = json.load(fp)['context']
        except Exception as exc:
            logging.warning(exc)
        sig.translator_update.emit()

    def translate(self, text: str = "", ctx: str = 'root'):
        context = self._lang.get(ctx)
        if context:
            translated_text = context.get(text)
            if translated_text:
                return translated_text
            else:
                return text
        else:
            return text


app_translator = Translator()
translate = app_translator.translate


# try:
#     with open(Path('kvgui/translations/Ukrainian.json').absolute().as_posix(), 'r', encoding='utf-8') as fp:
#         GENERATED_TRANSLATION = json.load(fp)
# except Exception as exc:
#     GENERATED_TRANSLATION = DEFAULT_TRANSLATION


# def translate(text: str = "", ctx: str = 'root'):
#     global GENERATED_TRANSLATION
#     # TODO: translator implementation
#     context = GENERATED_TRANSLATION['context'].get(ctx)
#     if context:
#         translated_text = context.get(text)
#         if translated_text:
#             GENERATED_TRANSLATION['context'][ctx][text] = translated_text
#             return translated_text
#         else:
#             # logging.warning(f'Translation for "{text}" not found in "{ctx}" context')
#             GENERATED_TRANSLATION['context'][ctx][text] = text
#             return text
#     else:
#         GENERATED_TRANSLATION['context'][ctx] = {}
#         GENERATED_TRANSLATION['context'][ctx][text] = text
#         # logging.warning(f'Translation for "{text}" not found in "{ctx}" context')
#         return text
#
#
# def create_translation_template():
#     # Create the directories if they don'unit_temperature exist
#     os.makedirs(os.path.dirname(TEMPLATE_PATH), exist_ok=True)
#
#     # Save the file to the target path
#     with open(TEMPLATE_PATH, "w", encoding='utf-8') as fp:
#         json.dump(GENERATED_TRANSLATION, fp, ensure_ascii=False)

