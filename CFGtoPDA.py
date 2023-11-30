#Pascu Ioan grupa 144

from CFGLoader import CFGLoader
import copy

class CFGtoPDA:

    __EPS = 'epsilon'
    __stack = []
    __states = set(['start', 'loop', 'accept'])
    __sigma = None #alphabet for input and for stack are the same
    __start = 'start'
    __accepted = set(['accept'])
    __delta = {} # (state, symbol from input, symbol from stack) = [(state,(symbols to push on the stack in reverse order)) * ?]

    def __init__(self, filename):
        #read the cfg from a file
        cfg = CFGLoader(filename)

        self.__sigma = cfg.getTerminals().union(cfg.getVariables())

        #transition that puts a $ at the bottom of the stack
        self.__delta[('start', self.__EPS, self.__EPS)] = [('loop', (cfg.getStart(), '$'))]

        #transitions that pops the bottom of the stack
        self.__delta[('loop', self.__EPS, '$')] = [('accept', tuple([self.__EPS]))]

        #transitions that pop terminals from the top of the stack
        for terminal in cfg.getTerminals():
            self.__delta[('loop', terminal, terminal)] = [('loop', tuple([self.__EPS]))]

        #for each variable add a transition that that pops the variable from the stack and pushes the rule
        rules = cfg.getRules()
        for variable in rules.keys():
            #set the key with the variable to be poped
            key = ('loop', self.__EPS, variable)
            #list of all the possible replacements for the rule
            expressions = rules[variable]

            #add the first possible replacement
            self.__delta[key] = [('loop', tuple(expressions[0]))]
            #add the rest replacements
            for expression in expressions[1:]:
                self.__delta[key].append(('loop', tuple(expression)))


    def run(self, symbols, startState = None):
        #you can either start the run from the start state or a chosen state
        if startState == None:
            startState = self.__start
        
        currentState = startState

        if currentState in self.__accepted:
            return True

        if symbols == []:
            symbols = [None]

        #select all the possible keys that match the current state of the automaton    
        possibleKeys = []

        for key in self.__delta.keys():
            #check we are in the right state
            if key[0] == currentState:
                #check if there is the right input 
                if key[1] == symbols[0] or key[1] == self.__EPS:
                    #check if the top of the stack is right
                    if self.__stack != [] and key[2] == self.__stack[-1]:#top of the stack is the read symbol
                        possibleKeys.append(key)
                    elif key[2] == self.__EPS:#top of the stack is the empty string
                        possibleKeys.append(key)

        if len(possibleKeys) == 0:
            return False

        #go through each possible key for delta function
        for key in possibleKeys:
            options = self.__delta[key]
            #go through each substitution possibility
            for option in options:
                nextState = option[0]
                symbolsToBePushed = option[1]
                #create a copy of this automaton instance
                branch = copy.deepcopy(self)
                #pop the element for the current transition
                branch.__pop(key[2])
                #push the elements that replace the variable/ or nothing is it is a terminal
                branch.__pushOnStack(symbolsToBePushed)

                isValid = None

                if key[1] == self.__EPS:
                    isValid = branch.run(symbols, nextState)
                else:
                    isValid = branch.run(symbols[1:], nextState)
                if isValid:
                    return True
        return False



    #pushes elements in reversed order from the elements array/tuple
    def __pushOnStack(self, elements):
        elements = [x for x in list(elements) if x != self.__EPS]
        if len(elements) != 0:
            elements.reverse()
            self.__stack.extend(elements)

    #pops an element or does nothing if the element is epsilon
    def __pop(self, element):
        if element == self.__EPS:
            return
        else:
            self.__stack = self.__stack[:-1]