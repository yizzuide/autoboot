

class Property(type):
      def __get__(self, instance, owner):
            return self.value

      def __set__(self, instance, value):
            self.value = value