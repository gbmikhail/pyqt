class Port:
    def __set_name__(self, owner, name):
        self.attr_name = name

    def __set__(self, instance, value):
        if value <= 0 or value >= 65536:
            raise ValueError('Порт может быть числом от 1 до 65535')
        instance.__dict__[self.attr_name] = value
