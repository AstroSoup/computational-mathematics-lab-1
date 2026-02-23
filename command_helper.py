class App:
    def __init__(self):
        self.commands: dict[str, callable] = {"help": self.help}

    def help(self, *args):
        """
        Справка.
        """
        for name, func in self.commands.items():
            if func.__doc__ is None:
                print(name)
            else:
                doc = func.__doc__
                print(f"{name}: {doc}")

    def command(self, name=None):
        g_name = name
        def wrap(func):
            def wrapper():
                func()
            name = func.__name__ if g_name is None else g_name
            self.commands[name] = func
            return wrapper
        return wrap




