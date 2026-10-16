
class CandyStash:

    MAX_CAPACITY = 50

    @staticmethod
    def validate_amount(value: int) -> None:
        if not isinstance(value , int) :
            raise ValueError("Має бути ціле число.")
        if value < 0 :
            raise ValueError("Недозволяється взяти більше ніж є. ") 
    
    
    def __init__ (self, count ):
         self.validate_amount(count)
         self._count = min(count, self.MAX_CAPACITY)

    @classmethod 
    def full_stash(cls):
        return cls(cls.MAX_CAPACITY)
    
    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self , value: int) -> CandyStash:
        self.validate_amount(value)
        self._count = min(value , self.MAX_CAPACITY)

    def __str__(self)    -> str:
        return f"CandyStash({self._count} / {self.MAX_CAPACITY})"

    @classmethod
    def __repr__(self)   -> str:
        return self.__str__()

    def __add__(self , ammout : int) -> CandyStash:
        self.validate_amount(ammout)
        return CandyStash(min(self._count + ammout , self.MAX_CAPACITY))

    def __sub__(self , ammout : int) ->CandyStash:
        self.validate_amount(ammout)
        return CandyStash(max(self._count - ammout , 0))

    def __eq__(self , other : object):
        if isinstance (other , CandyStash):
            return self._count == other._count
        if isinstance(other , int):
            return self._count == other





