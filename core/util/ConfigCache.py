

class ConfigCache:

    singleton = None
    def __init__(self):
        self.__fireproof_cache = {}

    @staticmethod
    def get_cache():
        if ConfigCache.singleton is None:
            ConfigCache.singleton = ConfigCache()
        return ConfigCache.singleton

    def set(self, key, value):
        if key in self.__fireproof_cache:
            raise Exception(f'Вставка не удалась. Ключ {key} в ConfigCache уже существует')
        self.__fireproof_cache[key] = value

    def get(self, key):
        if key not in self.__fireproof_cache:
            raise Exception(f'Изъятие не удалось. Ключа {key} в ConfigCache нет')
        return self.__fireproof_cache[key]