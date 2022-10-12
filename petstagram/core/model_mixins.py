class StrFromFieldMixin:
    str_fields = ()

    def __str__(self):
        fields = [(str_field, getattr(self, str_field)) for str_field in self.str_fields]

        return ', '.join(f"{name}={value}" for (name, value) in fields)
