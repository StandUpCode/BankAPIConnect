class Singleton(type):
    _instance = {}

    def __call(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        else:
            assert not args and not kwargs

        return cls._instance[cls]
