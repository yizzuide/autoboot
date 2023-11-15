
from typing import Any


def has_property(obj: Any, prop: str, is_own: bool) -> bool:
  """
  Checks if a property is present in an object.

  Args:
    obj(Any): The object to check.
    prop(str): The property to check.
    is_own(bool): Whether to check the object's own properties or all properties.
    
  Returns:
    bool: True if the property is present, False otherwise.
  """
  if is_own:
    # 返回本地作用域中定义的属性和属性值构成的字典：返回object 对象的 __dict__ 属性
    return prop in vars(obj)
  else:
    #获取的属性来自对象所属的类或父类
    return hasattr(obj, prop)
