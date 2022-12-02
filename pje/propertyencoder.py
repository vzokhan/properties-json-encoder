from enum import Enum
from json import JSONEncoder
from typing import Any, Dict, Tuple, Type

class PropertyJSONEncoder(JSONEncoder):
    prop_cache : Dict[str, Tuple[Tuple[str, property]]] = {}
        
    def default(self, obj):
        if(isinstance(obj, Enum)):
            return obj.name
        elif isinstance(obj, object):
            return PropertyJSONEncoder.__obj_to_dict(obj)
        else:
            return super().default(obj)

    @staticmethod
    def __obj_to_dict(obj) -> Dict[str, Tuple[Tuple[str, property]]]:
        t = type(obj)
        props = PropertyJSONEncoder.prop_cache.get(t)
        if props is None:
            props = PropertyJSONEncoder.__collect_props(obj)
            PropertyJSONEncoder.prop_cache[t] = props
        dict = {}
        for prop in props:
            dict[prop[0]] = prop[1].fget(obj)

        return dict

    @staticmethod
    def __collect_props(type: Type) -> Tuple[Tuple[str, property]]:
        """Collects the type`s properties

        Args:
            type (Type): The type whose properties we need to collect

        Returns:
            Tuple[Tuple[str, property]]: The tuple of tuple(property name, property attribute)
        """
        return tuple((attr.fget.__name__, attr) for attr in 
            filter(lambda attr:isinstance(attr, property), 
            map(lambda name: getattr(type.__class__, name), 
            filter(lambda name:not name.startswith('_'), 
            tuple(method_name for method_name in dir(type))))))
        
