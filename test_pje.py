from enum import Enum
import json
from pje import PropertyJSONEncoder
import unittest

class MyEnum(Enum):
    FIRST = 1
    SECOND = 2

class MyClass():
    def __init__(self, name, val, e: MyEnum) -> None:
        self._name = name
        self._val = val
        self._e = e

    @property
    def name(self):
        return self._name

    @property
    def val(self):
        return self._val

    @property
    def position(self):
        return self._e

class MyClassContainer():
    def __init__(self,name, val, content) -> None:
        self._name = name
        self._val = val
        self._content=content
        
    @property
    def name(self):
        return self._name

    @property
    def val(self):
        return self._val

    @property
    def content(self):
        return self._content   

class EncoderTest(unittest.TestCase):
    
    def testSerializeSingleValue(self):
        st = json.dumps(MyClassContainer("Container1", 1, MyClass("Class1", 11, MyEnum.FIRST)), cls=PropertyJSONEncoder, separators=(',',':'))
        self.assertEqual(st, '{"content":{"name":"Class1","position":"FIRST","val":11},"name":"Container1","val":1}')
        
    def testSerializeArray(self):
        st = json.dumps([MyClassContainer("Container2", 2, MyClass("Class2", 12, MyEnum.SECOND)),
        MyClassContainer("Container3", 3, MyClass("Class3", 13, MyEnum.FIRST))], cls=PropertyJSONEncoder)
        self.assertEqual(st, '[{"content": {"name": "Class2", "position": "SECOND", "val": 12}, "name": "Container2", "val": 2}, {"content": {"name": "Class3", "position": "FIRST", "val": 13}, "name": "Container3", "val": 3}]')

       

if __name__ == '__main__':
    unittest.main()

