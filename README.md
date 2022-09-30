# properties-json-encoder

PropertyJSONEncoder overrides default JSONEncoder that serializes properties of given object.

## Using:

```python
from pje import PropertyJSONEncoder
import json

class MyClass():
    def __init__(self, name, val):
        self._n = name
        self._v = val

    @property
    def name(self):
        return self._n

    @property
    def value(self):
        return self._v

print(json.dumps(MyClass('MyName', 13), cls=PropertyJSONEncoder))
# {"name": "ClassName", "value": 13}
```