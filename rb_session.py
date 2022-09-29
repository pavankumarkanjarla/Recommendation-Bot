from rb_actions import input_processor, intentIdentifier, check_required_params, check_actions
from rb_context import FirstGreeting
from rb_intents import IntentComplete
import pandas as pd


class Session:
    '''Initialise a default session'''
    def __init__(self, attributes=None, active_contexts=[FirstGreeting(), IntentComplete() ]):

        # Active contexts not used yet, can use it to have multiple contexts
        self.active_contexts = active_contexts

        # Contexts are flags which control dialogue flow
        self.context = FirstGreeting()

        # Intent tracks the current state of dialogue
        #self.current_intent = First_Greeting()
        self.current_intent = None

        # attributes hold the information collected over the conversation
        self.attributes = {}

    '''Not used yet, but is intended to maintain active contexts'''
    def update_contexts(self):

        for context in self.active_contexts:
            if context.active:
                context.decrease_lifespan()

    '''Generate response to user input'''
    def reply(self, user_input):

        self.attributes, clean_input = input_processor(user_input, self.context, self.attributes, self.current_intent)

        self.current_intent = intentIdentifier(clean_input, self.context, self.current_intent)

        prompt, self.context = check_required_params(self.current_intent, self.attributes, self.context)

        # prompt is None means all parameters satisfied, perform the intent action
        if prompt is None:
            if self.context.name != 'IntentComplete':
                prompt, self.context = check_actions(self.current_intent, self.attributes, self.context)
                print("reply - prompt ", prompt, " context ", self.context)
                #print(self.attributes)
                
                '''TODO : YOUR CODE HERE TO GET RECOMMENDATION BASED ON THE ENTITY VALUES'''
                if prompt == "cabsearch" :
                    cab=pd.read_excel("cab_recomm.xlsx")
                    x=cab.loc(axis=0)[(cab['pickup']==self.attributes['pickup'])&(cab['destination']==self.attributes['destination'])&(cab['no_of_passengers']==(self.attributes['no_of_passengers']))&(cab['type_of_cab']==self.attributes['type_of_cab'])].index
                    #print(x)
                    x1=cab['cab'][x]
                    print("your recommended cab is",x1)
        
                    #test_data=cab_data.drop("cab",axis=1)
                    #train_data=cab_data.cab
                    #from sklearn.neighbors import KNeighborsClassifier
                    #neigh = KNeighborsClassifier(n_neighbors=5)
                    #training
                    #neigh.fit("test_data","train_data" )
                    # Predicted class
                    #y_predicted=neigh.predict(test) 
                    #print("y_predicted")
                    
                    
                if prompt == "cropsearch" :
                    crop=pd.read_excel("df_crop.xlsx")
                    y=crop.loc(axis=0)[(crop['type_of_soil']==self.attributes['type_of_soil'])&(crop['type_of_crop']==self.attributes['type_of_crop'])&(crop['season']==self.attributes['season'])&(crop['availability_of_water']==self.attributes['availability_of_water'])].index
                   #print(y)
                    y1=crop['crop'][y]
                   #print(y1)
                    print("your recommended crop is",y1)
                    #test_data=crop_data.drop("crop",axis=1)
                    #train_data=crop_data.crop
                    #from sklearn.neighbors import KNeighborsClassifier
                    #neigh = KNeighborsClassifier(n_neighbors=5)
                    #training
                    #neigh.fit("test_data","train_data" )
                    # Predicted class
                    #y_predicted=neigh.predict(test)
                    #print("y_predicted")
                prompt = "BOT: Hi! How may I assist you?"

        # Resets the state after the Intent is complete
        if self.context.name == 'IntentComplete':
            self.attributes = {}
            self.context = FirstGreeting()
            self.current_intent = None

        return prompt

