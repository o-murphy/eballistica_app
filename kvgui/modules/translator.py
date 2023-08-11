import json
import logging
import os
from datetime import datetime
from pathlib import Path

TRANSLATION_VERSION = '0.0.1'

GENERATED_TRANSLATION = {
    "meta": {
        "language": None,
        "author": None,
        "version": TRANSLATION_VERSION,
        "date": datetime.strftime(datetime.now(), "%d.%m.%Y")
    },
    "context": {

    }
}

TEMPLATE_PATH = Path('kvgui/translations/translation_template.json')
TEMPLATE_PATH = TEMPLATE_PATH.absolute().as_posix()


def translate(text: str = "", ctx: str = 'root'):
    global GENERATED_TRANSLATION
    # TODO: translator implementation
    context = GENERATED_TRANSLATION['context'].get(ctx)
    if context:
        translated_text = context.get(text)
        if translated_text:
            GENERATED_TRANSLATION['context'][ctx][text] = translated_text
            return translated_text
        else:
            # logging.warning(f'Translation for "{text}" not found in "{ctx}" context')
            GENERATED_TRANSLATION['context'][ctx][text] = text
            return text
    else:
        GENERATED_TRANSLATION['context'][ctx] = {}
        GENERATED_TRANSLATION['context'][ctx][text] = text
        # logging.warning(f'Translation for "{text}" not found in "{ctx}" context')
        return text


def create_translation_template():
    # Create the directories if they don'unit_temperature exist
    os.makedirs(os.path.dirname(TEMPLATE_PATH), exist_ok=True)

    # Save the file to the target path
    with open(TEMPLATE_PATH, "w", encoding='utf-8') as fp:
        json.dump(GENERATED_TRANSLATION, fp, ensure_ascii=False)

