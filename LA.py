#Pascu Ioan grupa 144

class LA:
    
    __EPS = 'epsilon'
    __states = set()
    __sigma = set()
    __delta = {}
    __start = None
    __acceptStates = set()
    __sigmaS = set()
    __currentState = None
    __s = set()

    #the only class constructor which will read the LA from a config file
    def __init__(self, filename):
        f = open(filename)
        lines = f.readlines()

        #remove comments and blank lines
        lines = [x.strip() for x in lines if x[0] != '#' and x.strip() != ''] 

        #split the lines into sections
        sections = self.__sectionLines(lines)
        
        #for each section call the respective function to create the set
        for section in sections:
            if section[0] == 'States:':
                self.__initStates(section)
            if section[0] == 'Sigma:':
                self.__initSigma(section)
            if section[0] == 'Delta:':
                self.__initDelta(section)
            if section[0] == 'SigmaS:':
                self.__initSigmaS(section)

        self.__validate()

        #initiate the start state
        self.__currentState = self.__start

        f.close()


    def __sectionLines(self,lines):
        #get the limiting indexes for diffrent areas of the config file
        endIndexes = []
        for i in range(len(lines)):
            if lines[i] == 'End':
                endIndexes.append(i)
        
        sections = [lines[0:endIndexes[0]]]
        for i in range(len(endIndexes) - 1):
            sections.append(lines[endIndexes[i] + 1:endIndexes[i+1]])

        return sections
    
    #function that constructs the states set
    def __initStates(self, section):
        for state in section[1:]:

            #parse the line into an array contaning the state name and potentially the letters F or S
            state = [x.strip() for x in state.split(',')]

            #check if the state is an accepted state
            if 'F' in state:
                self.__acceptStates.add(state[0])

            #check if the state is the start state and if the start state has already been set
            if 'S' in state:
                if self.__start == None:
                    self.__start = state[0]
                else:
                    raise ValueError('You cannot have more than one start state!')
            
            self.__states.add(state[0])

    
    #function that constructs the sigma set
    def __initSigma(self, section):
        for symbol in section[1:]:
            self.__sigma.add(symbol)


    #function that constructs the delta dictionary
    def __initDelta(self, section):
        for definition in section[1:]:

            #parse the arguments and the results of the delta function into 2 different lists
            arguments, results = definition.split(':=')
            arguments = [x.strip() for x in arguments.split(',')]
            results = [x.strip() for x in results.split(',')]

            #create tuples based on the lists and add them to the delta dictionary
            self.__delta[(arguments[0],arguments[1],arguments[2])] = (results[0],results[1],results[2])

    #function that constructs the sigmaS set
    def __initSigmaS(self, section):
        for symbol in section[1:]:
            self.__sigmaS.add(symbol)

    #function that prints the definition of the automaton
    def displayInfo(self):
        print('States:', end= ' ' )
        print(*self.__states, sep=' , ')
        print('Sigma:', end = ' ')
        print( *self.__sigma, sep = ' , ')
        print('Delta:')
        for key in self.__delta:
            res = self.__delta[key]
            print('(', key[0], ',', key[1], ',', key[2], ')', '=', '(', res[0], ',', res[1], ',', res[2], ')')
        print('Start state:', self.__start)
        print('Accept states:', *self.__acceptStates)
        print('SigmaS:', end = ' ')
        print(*self.__sigmaS, sep = ' , ')

    #function that displays current state of the automaton
    def display(self):
        print('Current state:', self.__currentState)
        print('Set:', *self.__s)


    #function that validates the automaton
    def __validate(self):
        #verify that the automaton has at least one state
        if len(self.__states) == 0:
            raise ValueError('Must have at least one state!')
        
        #verify that there is a start state
        if self.__start == None:
            raise ValueError('Must have a start state!')
        
        #verify that delta function arguments and results are well defined
        for key in self.__delta:
            if key[0] not in self.__states:
                raise ValueError('State ' + key[0] + ' as a delta function argument is not valid!')
            if key[1] not in self.__sigma:
                raise ValueError('Symbol ' + key[1] + ' of delta function argument is not a part of the alphabet!')
            if key[2] not in self.__sigmaS and key[2] != self.__EPS:
                raise ValueError('Symbol ' + key[2] + ' of delta function argument is not a part of the set alphabet!')
            
            res = self.__delta[key]
            if res[0] not in self.__states:
                raise ValueError('State ' + res[0] + ' as a delta function result is not valid!')
            if res[1] not in self.__sigmaS and res[1] != self.__EPS:
                raise ValueError('Symbol ' + res[1] + ' of delta function result is not a part of the set alphabet!')
            if res[2] not in self.__sigmaS and res[2] != self.__EPS:
                raise ValueError('Symbol ' + res[2] + ' of delta function result is not a part of the set alphabet!')
            
            if self.__hasMatchingKey(key) != None:
                raise ValueError('Cannot have 2 branches going out from state ' + key[0] + 'with the symbol ' + key[1] + '!')
 
    #funtion that verifies if the first 2 elements of argument key matches any other key in the delta dictionary
    #returns the key if it exits, otherwise None
    def __hasMatchingKey(self,keyMatch):
        for key in self.__delta.keys():
            if key[0] == keyMatch[0] and key[1] == keyMatch[1] and key[2] != keyMatch[2]:
                return key
        return None

    #function that gets a symbol and treats it as a symbol from input
    #returns True if it has anywhere to go, otherwise False
    def step(self, symbol):
        key = self.__hasMatchingKey((self.__currentState, symbol, ''))
        if key != None:
            if key[2] in self.__s or key[2] == self.__EPS:
                res = self.__delta[key]
                if res[1] != self.__EPS:
                    self.__s.discard(res[1])
                if res[2] != self.__EPS:
                    self.__s.add(res[2])
                self.__currentState = res[0]
                return True
    
        return False
    
    #returns true if the current state is an accepted state
    def isAccepted(self):
        return self.__currentState in self.__acceptStates
    
    #simulates the automaton for a given string as input
    def run(self, string):
        for symbol in string:
            if not self.step(symbol):
                return False
        if not self.isAccepted():
            return False
        return True
    
    #getters
    def getCurrentState(self):
        return self.__currentState
    
    def getSet(self):
        return self.__s