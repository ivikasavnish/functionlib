"""
Python Introspection Functions

Runtime object inspection, type analysis, and code introspection.
"""

import inspect
import sys
import types
from typing import Any, List, Dict, Callable, Optional, Type
import dis
import ast

__all__ = [
    # Object Inspection
    'get_object_type', 'get_object_size', 'get_object_id', 'get_object_repr',
    'is_instance_of', 'is_subclass_of', 'get_base_classes', 'get_subclasses',
    
    # Attribute Inspection
    'get_attributes', 'get_methods', 'get_properties', 'has_attribute',
    'get_attribute_value', 'set_attribute_value', 'get_class_attributes',
    
    # Function Inspection
    'get_function_signature', 'get_function_args', 'get_function_defaults',
    'get_function_annotations', 'get_function_source', 'get_function_module',
    
    # Module Inspection
    'get_module_functions', 'get_module_classes', 'get_module_variables',
    'get_module_path', 'is_module_loaded',
    
    # Code Inspection
    'get_source_code', 'get_bytecode', 'get_line_number', 'get_file_location',
    
    # Type Checking
    'is_callable', 'is_iterable', 'is_mapping', 'is_number', 'is_string',
    'get_type_name', 'get_mro'
]

# ============================================================================
# OBJECT INSPECTION
# ============================================================================

def get_object_type(obj: Any) -> Type:
    """
    Get the type of an object.
    
    Args:
        obj: Any object
        
    Returns:
        Type of the object
        
    Example:
        >>> get_object_type(42)
        <class 'int'>
        >>> get_object_type("hello")
        <class 'str'>
    """
    return type(obj)


def get_object_size(obj: Any) -> int:
    """
    Get the size of an object in bytes.
    
    Args:
        obj: Any object
        
    Returns:
        Size in bytes
        
    Example:
        >>> size = get_object_size([1, 2, 3])
        >>> size > 0
        True
    """
    return sys.getsizeof(obj)


def get_object_id(obj: Any) -> int:
    """
    Get the unique identifier of an object.
    
    Args:
        obj: Any object
        
    Returns:
        Object ID
        
    Example:
        >>> obj = [1, 2, 3]
        >>> id1 = get_object_id(obj)
        >>> id2 = get_object_id(obj)
        >>> id1 == id2
        True
    """
    return id(obj)


def get_object_repr(obj: Any) -> str:
    """
    Get the string representation of an object.
    
    Args:
        obj: Any object
        
    Returns:
        String representation
        
    Example:
        >>> get_object_repr([1, 2, 3])
        '[1, 2, 3]'
    """
    return repr(obj)


def is_instance_of(obj: Any, class_or_tuple: Any) -> bool:
    """
    Check if object is instance of a class.
    
    Args:
        obj: Object to check
        class_or_tuple: Class or tuple of classes
        
    Returns:
        True if instance
        
    Example:
        >>> is_instance_of(42, int)
        True
        >>> is_instance_of("hello", (int, str))
        True
    """
    return isinstance(obj, class_or_tuple)


def is_subclass_of(cls: Type, class_or_tuple: Any) -> bool:
    """
    Check if class is subclass of another class.
    
    Args:
        cls: Class to check
        class_or_tuple: Parent class or tuple of classes
        
    Returns:
        True if subclass
        
    Example:
        >>> is_subclass_of(bool, int)
        True
    """
    try:
        return issubclass(cls, class_or_tuple)
    except TypeError:
        return False


def get_base_classes(cls: Type) -> tuple:
    """
    Get base classes of a class.
    
    Args:
        cls: Class to inspect
        
    Returns:
        Tuple of base classes
        
    Example:
        >>> class MyClass(dict, list):
        ...     pass
        >>> bases = get_base_classes(MyClass)
        >>> dict in bases
        True
    """
    return cls.__bases__


def get_subclasses(cls: Type) -> List[Type]:
    """
    Get direct subclasses of a class.
    
    Args:
        cls: Class to inspect
        
    Returns:
        List of subclass types
        
    Example:
        >>> subs = get_subclasses(BaseException)
        >>> Exception in subs
        True
    """
    return cls.__subclasses__()


# ============================================================================
# ATTRIBUTE INSPECTION
# ============================================================================

def get_attributes(obj: Any, include_private: bool = False) -> List[str]:
    """
    Get all attributes of an object.
    
    Args:
        obj: Object to inspect
        include_private: Include private attributes (starting with _)
        
    Returns:
        List of attribute names
        
    Example:
        >>> attrs = get_attributes([1, 2, 3])
        >>> 'append' in attrs
        True
    """
    attrs = dir(obj)
    if not include_private:
        attrs = [a for a in attrs if not a.startswith('_')]
    return attrs


def get_methods(obj: Any, include_private: bool = False) -> List[str]:
    """
    Get all methods of an object.
    
    Args:
        obj: Object to inspect
        include_private: Include private methods
        
    Returns:
        List of method names
        
    Example:
        >>> methods = get_methods([1, 2, 3])
        >>> 'append' in methods
        True
    """
    methods = []
    for name in dir(obj):
        if include_private or not name.startswith('_'):
            try:
                attr = getattr(obj, name)
                if callable(attr):
                    methods.append(name)
            except:
                pass
    return methods


def get_properties(cls: Type) -> List[str]:
    """
    Get all properties of a class.
    
    Args:
        cls: Class to inspect
        
    Returns:
        List of property names
        
    Example:
        >>> class MyClass:
        ...     @property
        ...     def value(self):
        ...         return 42
        >>> props = get_properties(MyClass)
        >>> 'value' in props
        True
    """
    props = []
    for name in dir(cls):
        try:
            attr = getattr(cls, name)
            if isinstance(attr, property):
                props.append(name)
        except:
            pass
    return props


def has_attribute(obj: Any, name: str) -> bool:
    """
    Check if object has an attribute.
    
    Args:
        obj: Object to check
        name: Attribute name
        
    Returns:
        True if attribute exists
        
    Example:
        >>> has_attribute([1, 2, 3], 'append')
        True
        >>> has_attribute([1, 2, 3], 'nonexistent')
        False
    """
    return hasattr(obj, name)


def get_attribute_value(obj: Any, name: str, default: Any = None) -> Any:
    """
    Get attribute value with default.
    
    Args:
        obj: Object to inspect
        name: Attribute name
        default: Default value if not found
        
    Returns:
        Attribute value or default
        
    Example:
        >>> get_attribute_value([1, 2, 3], '__len__')
        <method-wrapper '__len__' of list object at ...>
    """
    return getattr(obj, name, default)


def set_attribute_value(obj: Any, name: str, value: Any) -> None:
    """
    Set attribute value on an object.
    
    Args:
        obj: Object to modify
        name: Attribute name
        value: New value
        
    Example:
        >>> class MyClass:
        ...     pass
        >>> obj = MyClass()
        >>> set_attribute_value(obj, 'value', 42)
        >>> obj.value
        42
    """
    setattr(obj, name, value)


def get_class_attributes(cls: Type) -> Dict[str, Any]:
    """
    Get class-level attributes (not instance attributes).
    
    Args:
        cls: Class to inspect
        
    Returns:
        Dictionary of class attributes
        
    Example:
        >>> class MyClass:
        ...     class_var = 42
        >>> attrs = get_class_attributes(MyClass)
        >>> 'class_var' in attrs
        True
    """
    return {name: value for name, value in cls.__dict__.items()
            if not name.startswith('_')}


# ============================================================================
# FUNCTION INSPECTION
# ============================================================================

def get_function_signature(func: Callable) -> inspect.Signature:
    """
    Get function signature.
    
    Args:
        func: Function to inspect
        
    Returns:
        Function signature
        
    Example:
        >>> def example(a: int, b: str = "default") -> str:
        ...     return f"{a}{b}"
        >>> sig = get_function_signature(example)
        >>> 'a' in str(sig)
        True
    """
    return inspect.signature(func)


def get_function_args(func: Callable) -> List[str]:
    """
    Get function argument names.
    
    Args:
        func: Function to inspect
        
    Returns:
        List of argument names
        
    Example:
        >>> def example(a, b, c=3):
        ...     pass
        >>> get_function_args(example)
        ['a', 'b', 'c']
    """
    sig = inspect.signature(func)
    return list(sig.parameters.keys())


def get_function_defaults(func: Callable) -> Dict[str, Any]:
    """
    Get function default argument values.
    
    Args:
        func: Function to inspect
        
    Returns:
        Dictionary of parameter names to default values
        
    Example:
        >>> def example(a, b=10, c="hello"):
        ...     pass
        >>> defaults = get_function_defaults(example)
        >>> defaults['b']
        10
    """
    sig = inspect.signature(func)
    defaults = {}
    for name, param in sig.parameters.items():
        if param.default is not inspect.Parameter.empty:
            defaults[name] = param.default
    return defaults


def get_function_annotations(func: Callable) -> Dict[str, Any]:
    """
    Get function type annotations.
    
    Args:
        func: Function to inspect
        
    Returns:
        Dictionary of annotations
        
    Example:
        >>> def example(a: int, b: str) -> bool:
        ...     return True
        >>> annot = get_function_annotations(example)
        >>> annot['a']
        <class 'int'>
    """
    return func.__annotations__ if hasattr(func, '__annotations__') else {}


def get_function_source(func: Callable) -> str:
    """
    Get source code of a function.
    
    Args:
        func: Function to inspect
        
    Returns:
        Source code as string
        
    Example:
        >>> def example():
        ...     return 42
        >>> source = get_function_source(example)
        >>> 'return 42' in source
        True
    """
    try:
        return inspect.getsource(func)
    except (OSError, TypeError):
        return ""


def get_function_module(func: Callable) -> Optional[str]:
    """
    Get module name where function is defined.
    
    Args:
        func: Function to inspect
        
    Returns:
        Module name or None
        
    Example:
        >>> def example():
        ...     pass
        >>> module = get_function_module(example)
        >>> module == '__main__'
        True
    """
    return func.__module__ if hasattr(func, '__module__') else None


# ============================================================================
# MODULE INSPECTION
# ============================================================================

def get_module_functions(module: types.ModuleType) -> Dict[str, Callable]:
    """
    Get all functions defined in a module.
    
    Args:
        module: Module to inspect
        
    Returns:
        Dictionary of function names to functions
        
    Example:
        >>> import math
        >>> funcs = get_module_functions(math)
        >>> 'sin' in funcs
        True
    """
    return {name: obj for name, obj in inspect.getmembers(module)
            if inspect.isfunction(obj) or inspect.isbuiltin(obj)}


def get_module_classes(module: types.ModuleType) -> Dict[str, Type]:
    """
    Get all classes defined in a module.
    
    Args:
        module: Module to inspect
        
    Returns:
        Dictionary of class names to classes
        
    Example:
        >>> import collections
        >>> classes = get_module_classes(collections)
        >>> 'Counter' in classes
        True
    """
    return {name: obj for name, obj in inspect.getmembers(module)
            if inspect.isclass(obj)}


def get_module_variables(module: types.ModuleType) -> Dict[str, Any]:
    """
    Get module-level variables.
    
    Args:
        module: Module to inspect
        
    Returns:
        Dictionary of variable names to values
        
    Example:
        >>> import math
        >>> vars = get_module_variables(math)
        >>> 'pi' in vars
        True
    """
    return {name: obj for name, obj in inspect.getmembers(module)
            if not (inspect.isfunction(obj) or inspect.isclass(obj) 
                   or inspect.ismodule(obj) or name.startswith('_'))}


def get_module_path(module: types.ModuleType) -> Optional[str]:
    """
    Get file path of a module.
    
    Args:
        module: Module to inspect
        
    Returns:
        Module file path or None
        
    Example:
        >>> import os
        >>> path = get_module_path(os)
        >>> path is not None
        True
    """
    return getattr(module, '__file__', None)


def is_module_loaded(module_name: str) -> bool:
    """
    Check if a module is already loaded.
    
    Args:
        module_name: Name of module
        
    Returns:
        True if loaded
        
    Example:
        >>> is_module_loaded('sys')
        True
        >>> is_module_loaded('nonexistent_module_xyz')
        False
    """
    return module_name in sys.modules


# ============================================================================
# CODE INSPECTION
# ============================================================================

def get_source_code(obj: Any) -> str:
    """
    Get source code of an object (function, class, method).
    
    Args:
        obj: Object to inspect
        
    Returns:
        Source code as string
        
    Example:
        >>> def example():
        ...     pass
        >>> code = get_source_code(example)
        >>> 'def example' in code
        True
    """
    try:
        return inspect.getsource(obj)
    except (OSError, TypeError):
        return ""


def get_bytecode(func: Callable) -> str:
    """
    Get bytecode disassembly of a function.
    
    Args:
        func: Function to disassemble
        
    Returns:
        Bytecode as string
        
    Example:
        >>> def example():
        ...     return 42
        >>> bytecode = get_bytecode(example)
        >>> 'LOAD_CONST' in bytecode or 'RETURN_VALUE' in bytecode
        True
    """
    import io
    output = io.StringIO()
    dis.dis(func, file=output)
    return output.getvalue()


def get_line_number(obj: Any) -> Optional[int]:
    """
    Get line number where object is defined.
    
    Args:
        obj: Object to inspect
        
    Returns:
        Line number or None
        
    Example:
        >>> def example():
        ...     pass
        >>> line = get_line_number(example)
        >>> line is not None
        True
    """
    try:
        return inspect.getsourcelines(obj)[1]
    except (OSError, TypeError):
        return None


def get_file_location(obj: Any) -> Optional[str]:
    """
    Get file location where object is defined.
    
    Args:
        obj: Object to inspect
        
    Returns:
        File path or None
        
    Example:
        >>> import os
        >>> location = get_file_location(os.path.join)
        >>> location is not None
        True
    """
    try:
        return inspect.getfile(obj)
    except TypeError:
        return None


# ============================================================================
# TYPE CHECKING
# ============================================================================

def is_callable(obj: Any) -> bool:
    """
    Check if object is callable.
    
    Args:
        obj: Object to check
        
    Returns:
        True if callable
        
    Example:
        >>> is_callable(lambda x: x)
        True
        >>> is_callable(42)
        False
    """
    return callable(obj)


def is_iterable(obj: Any) -> bool:
    """
    Check if object is iterable.
    
    Args:
        obj: Object to check
        
    Returns:
        True if iterable
        
    Example:
        >>> is_iterable([1, 2, 3])
        True
        >>> is_iterable(42)
        False
    """
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def is_mapping(obj: Any) -> bool:
    """
    Check if object is a mapping (dict-like).
    
    Args:
        obj: Object to check
        
    Returns:
        True if mapping
        
    Example:
        >>> is_mapping({'a': 1})
        True
        >>> is_mapping([1, 2, 3])
        False
    """
    from collections.abc import Mapping
    return isinstance(obj, Mapping)


def is_number(obj: Any) -> bool:
    """
    Check if object is a number.
    
    Args:
        obj: Object to check
        
    Returns:
        True if number
        
    Example:
        >>> is_number(42)
        True
        >>> is_number("42")
        False
    """
    return isinstance(obj, (int, float, complex))


def is_string(obj: Any) -> bool:
    """
    Check if object is a string.
    
    Args:
        obj: Object to check
        
    Returns:
        True if string
        
    Example:
        >>> is_string("hello")
        True
        >>> is_string(42)
        False
    """
    return isinstance(obj, str)


def get_type_name(obj: Any) -> str:
    """
    Get human-readable type name.
    
    Args:
        obj: Object to inspect
        
    Returns:
        Type name as string
        
    Example:
        >>> get_type_name([1, 2, 3])
        'list'
        >>> get_type_name(42)
        'int'
    """
    return type(obj).__name__


def get_mro(cls: Type) -> tuple:
    """
    Get Method Resolution Order for a class.
    
    Args:
        cls: Class to inspect
        
    Returns:
        Tuple of classes in MRO
        
    Example:
        >>> mro = get_mro(bool)
        >>> int in mro
        True
    """
    return cls.__mro__
