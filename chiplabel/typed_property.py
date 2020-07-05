#!/usr/bin/env python3
# typed_property.py

def typedproperty(name, expected_type, strip=False, regex=None):
    private_name = '_' + name
    @property
    def prop(self):
        return getattr(self, private_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f'Expected {expected_type}')
        value = value.strip() if strip else value
        if regex and not regex.match(value): 
            raise TypeError('Invalid character in string')
        setattr(self, private_name, value)
    return prop

String = lambda name: typedproperty(name, str)
StrippedString = lambda name: typedproperty(name, str, strip=True)
RegexString = lambda name, regex: typedproperty(name, str, strip=True, regex=regex)
Integer  = lambda name: typedproperty(name, int)
Float  = lambda name: typedproperty(name, float)
