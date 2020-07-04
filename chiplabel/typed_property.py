#!/usr/bin/env python3
# typed_property.py

def typedproperty(name, expected_type, strip=False):
    private_name = '_' + name
    @property
    def prop(self):
        return getattr(self, private_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f'Expected {expected_type}')
        setattr(self, private_name, value.strip())

    return prop

String = lambda name: typedproperty(name, str)
StrippedString = lambda name: typedproperty(name, str, strip=True)
Integer  = lambda name: typedproperty(name, int)
Float  = lambda name: typedproperty(name, float)
