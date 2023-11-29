

class ComponentMetaclass(type):
  """
  Metaclass for all components.
  """
  
  def __init__(cls, name, bases, attrs):
    super(ComponentMetaclass, cls).__init__(name, bases, attrs)
    
    # get component name from class attrs['component_name']
    if name != 'Component':
      cls.__component_name__ = attrs['component_name'] \
        if 'component_name' in attrs and attrs['component_name'] else name

  def __new__(cls, name, bases, attrs):
    return super(ComponentMetaclass, cls).__new__(cls, name, bases, attrs)