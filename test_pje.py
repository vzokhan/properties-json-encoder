from enum import Enum
import json
from pje import PropertyJSONEncoder
import unittest
import uuid
from string import Template


class MyEnum(Enum):
    FIRST = 1
    SECOND = 2


class MyClass():
    def __init__(self, uid, name, val, e: MyEnum) -> None:
        self._uid = uid
        self._name = name
        self._val = val
        self._e = e

    @property
    def uid(self):
        return self._uid

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
    def __init__(self, name, val, content) -> None:
        self._name = name
        self._val = val
        self._content = content

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
        self.maxDiff = None

        uid = uuid.uuid4()

        actual = json.dumps(MyClassContainer("Container1", 1, MyClass(
            uid, "Class1", 11, MyEnum.FIRST)), cls=PropertyJSONEncoder, separators=(',', ':'), sort_keys=True)
        t = Template(
            '{"content":{"name":"Class1","position":"FIRST","uid":"${uid}","val":11},"name":"Container1","val":1}')
        expected = t.substitute(uid=str(uid))
        self.assertEqual(expected, actual)

    def testSerializeArray(self):
        self.maxDiff = None
        uid1 = uuid.uuid4()
        uid2 = uuid.uuid4()
        actual = json.dumps([MyClassContainer("Container2", 2, MyClass(uid1, "Class2", 12, MyEnum.SECOND)),
                             MyClassContainer("Container3", 3, MyClass(uid2, "Class3", 13, MyEnum.FIRST))], cls=PropertyJSONEncoder, sort_keys=True)
        t = Template('[{"content": {"name": "Class2", "position": "SECOND", "uid": "${uid1}", "val": 12}, "name": "Container2", "val": 2}, {"content": {"name": "Class3", "position": "FIRST", "uid": "${uid2}", "val": 13}, "name": "Container3", "val": 3}]')
        expected = t.substitute(uid1=str(uid1), uid2=str(uid2))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
