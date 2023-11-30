

class AppPluginMetaclass(type):
  
  def __init__(cls, name, bases, attrs):
    super(AppPluginMetaclass, cls).__init__(name, bases, attrs)

    if name != 'AppPlugin':
      cls.__ctx__ = attrs['context_name'] \
        if 'context_name' in attrs and attrs['context_name'] else name