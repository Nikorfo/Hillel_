from typing import Protocol

class Drawable(Protocol) :
   def draw() -> str:
       ...
   ...


def render ( shape: Drawable ) -> None:
   print(shape.draw())


class Circle:
    def draw(self) -> str:
        return "( )"


class Square:
 def draw(self) -> str:
         return "( )"   


render(Circle())
render(Square())