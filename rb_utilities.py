from rb_context import Context


class GetRegNo(Context):

    def __init__(self):
        print('Hi')
        self.lifespan = 1
        self.name = 'GetRegNo'
        self.active = True

class SpellConformation(Context):

    def __init__(self,index,CorrectWord,user_input,context):
        self.lifespan = 1
        self.name = 'SpellConformation'
        self.active = True
        self.index = index
        self.correct = CorrectWord
        self.tobecorrected = user_input
        self.contexttobestored = context