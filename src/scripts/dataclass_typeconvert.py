from functools import wraps
from typing import Any, Callable, Dict, TypeVar

T = TypeVar("T")
def convert_types(caller_annotations: Dict[str, Any], final_dict: Dict[str, T]) -> Dict[str, T]:
    for f_name, f_type in caller_annotations.items():
        if type(final_dict[f_name]) is not f_type: # the required and the given types are not the same
            required_params = final_dict[f_name]
            is_union = False
            if required_params is None: continue # typing.Optional

            if hasattr(f_type, "__origin__"): # typing.Tuple or anything like that
                f_type = getattr(f_type, "__origin__")

            if hasattr(caller_annotations[f_name], "__args__"):
                # fun fact: caller_annotations is Union and has __args__ but f_type which is also Union, does not have __args__ :)
                if len(caller_annotations[f_name].__args__) > 1: # typing.Union
                    is_union = True

            #! FIXME: redundancy
            if isinstance(required_params, dict):
                if is_union:
                    for probable_type in caller_annotations[f_name].__args__:
                        try:
                            required_object = probable_type(**required_params)
                        except: pass
                        else: break
                else:
                    required_object = f_type(**required_params)
            else:
                if is_union:
                    for probable_type in caller_annotations[f_name].__args__:
                        try:
                            required_object = probable_type(required_params)
                        except: pass
                        else: break
                else:
                    required_object = f_type(required_params) # single values, like float, int, etc

            final_dict[f_name] = required_object # welp

    return final_dict 

def type_check(function: Callable[..., T]) -> Callable[..., T]:
    "Type check and cast for dataclasses"
    # With this I can easily create dataclass with complex data (for instance with multiple other
    # dataclasses as well) that is automaticly converted to the right annotated type.
    # For example when i read from json files and give that data for a complex model, it wont 
    # be autocasted by default.
    @wraps(function)
    def inner(final_object: object):
        caller_class = final_object.__class__
        caller_mro = caller_class.__mro__

        if len(caller_mro) > 2:
            # inheritance related checking and conversions
            for mro_level in caller_mro[1:-1]:
                needed_subclass_fields: Dict[str, Any] = {}
                for needed_field in mro_level.__annotations__:
                    final_objects_needed_field = final_object.__dict__.get(needed_field, None)

                    if final_objects_needed_field is None: # fix dataclasses.field(default = )
                        needed_subclass_fields[needed_field] = getattr(mro_level, needed_field)
                    else:
                        needed_subclass_fields[needed_field] = final_objects_needed_field

                result = convert_types(mro_level.__annotations__, needed_subclass_fields)
                final_object.__dict__.update(result)

        final_object.__dict__.update(convert_types(caller_class.__annotations__, final_object.__dict__))
        return function(final_object)
    return inner
