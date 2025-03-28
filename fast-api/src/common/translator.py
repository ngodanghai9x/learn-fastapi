import importlib
from typing import Any, Dict
# https://dev.to/whchi/simple-way-to-make-i18n-support-in-fastapi-27kd

class Translator:
    _instances: Dict[str, 'Translator'] = {}

    def __new__(cls, lang: str) -> 'Translator':
        if lang not in cls._instances:
            cls._instances[lang] = super(Translator, cls).__new__(cls)
        return cls._instances[lang]

    def __init__(self, lang: str):
        self.lang = lang

    def t(self, key: str, **kwargs: Dict[str, Any]) -> str:
        file_key, *translation_keys = key.split('.')

        locale_module = importlib.import_module(f'src.i18n.{self.lang}.{file_key}')

        translation = locale_module.locale
        for translation_key in translation_keys:
            translation = translation.get(translation_key, None)
            if translation is None:
                return f'Key {key} not found in {self.lang} locale'
        if kwargs.keys():
            translation = translation.format(**kwargs)
        return translation