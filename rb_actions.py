import random
import json
import os
import re

from rb_generate_ngrams import ngrammatch
from rb_intents import Intent, IntentComplete


def check_actions(current_intent, attributes, context):
    '''This function performs the action for the intent
    as mentioned in the intent config file'''
    '''Performs actions pertaining to current intent
    for action in current_intent.actions:
        if action.contexts_satisfied(active_contexts):
            return perform_action()
    '''

    context = IntentComplete()
    # return 'action: ' + current_intent.action, context
    return current_intent.action, context

'''Collects attributes pertaining to the current intent'''
def check_required_params(current_intent, attributes, context):

    for para in current_intent.params:
        if para.required == 'True':
            if para.name not in attributes:
                # Example of where the context is born
                # if para.name=='RegNo':
                    # context = GetRegNo()
                # returning a random prompt from available choices.
                return random.choice(para.prompts), context

    return None, context

'''Spellcheck and entity extraction functions go here'''
def input_processor(user_input, context, attributes, intent):

    # uinput = TextBlob(user_input).correct().string

    # update the attributes, abstract over the entities in user input
    attributes, cleaned_input = getattributes(user_input, context, attributes)

    return attributes, cleaned_input

def loadIntent(path, intent):
    with open(path) as file_intent:
        dat = json.load(file_intent)
        intent = dat[intent]
        return Intent(intent['intentname'], intent['parameters'], intent['actions'])

'''This function is used to classify the intent'''
def intentIdentifier(clean_input, context, current_intent):
    clean_input = clean_input.lower()
    # print("intentIdentifier - clean_input ", clean_input)

    '''TODO : YOUR CODE HERE TO CLASSIFY THE INTENT'''
    # Scoring Algorithm, can be changed.
    scores = ngrammatch(clean_input)

    # choosing here the intent with the highest score
    scores = sorted_by_second = sorted(scores, key=lambda tup: tup[1])
    # print('intentIdentifier - scores ', scores)

    if current_intent is None:
        if clean_input == "search":
            current_intent = loadIntent('params/newparams.cfg', 'SearchStore')
        if clean_input == 'book':
            current_intent = loadIntent('params/newparams.cfg', 'OrderBook')
        else:
            '''TODO : YOUR CODE HERE TO EXTRACT INTENT OUT OF SCORES'''
            current_intent = loadIntent('params/newparams.cfg', scores[-1][0])
        print("intentIdentifier - current_intent ", current_intent.name)
        return current_intent
    else:
        # If current intent is not none, stick with the ongoing intent
        return current_intent

'''This function masks the entities in user input, and updates the attributes dictionary'''
def getattributes(uinput, context, attributes):

    # Can use context to context specific attribute fetching
    # print("getattributes context ", context)
    if context.name.startswith('IntentComplete'):
        return attributes, uinput
    else:
        # Code can be optimised here, loading the same files each time suboptimal
        files = os.listdir('./entities/')
        # Filtering dat files and extracting entity values inside the entities folder
        entities = {}
        for fil in files:
            if fil == ".ipynb_checkpoints":
                continue
            lines = open('./entities/'+fil).readlines()
            for i, line in enumerate(lines):
                lines[i] = line[:-1]
            entities[fil[:-4]] = '|'.join(lines)

        # Extract entity and update it in attributes dict
        for entity in entities:
            for i in entities[entity].split('|'):
                if i.lower() in uinput.lower():
                    attributes[entity] = i

        # Masking the entity values $ sign
        for entity in entities:
            uinput = re.sub(entities[entity], r'$'+entity, uinput, flags=re.IGNORECASE)


        return attributes, uinput
