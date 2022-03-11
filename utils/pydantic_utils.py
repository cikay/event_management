from typing import Optional

import pydantic


class AllOptional(pydantic.main.ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        self.make_allfields_optional(self, bases, namespaces)
        return super().__new__(self, name, bases, namespaces, **kwargs)


    def make_allfields_optional(self, bases, namespaces):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)

        for field, field_type in annotations.items():
            if not field.startswith('__'):
                annotations[field] = Optional[field_type]

        namespaces['__annotations__'] = annotations
