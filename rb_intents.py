from rb_context import Context

class Intent(object):
    # intent name, parameters and actions
    def __init__(self, name, params, action):
        self.name = name
        self.action = action
        self.params = []
        for param in params:
            # print param['required']
            self.params += [Parameter(param)]

class IntentComplete(Context):

    def __init__(self):
        self.lifespan = 1
        self.name = 'IntentComplete'
        self.active = True

class Parameter():
    def __init__(self, info):
        self.name = info['name']
        self.placeholder = info['placeholder']
        self.prompts = info['prompts']
        self.required = info['required']
        self.context = info['context']