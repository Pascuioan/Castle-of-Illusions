#Pascu Ioan grupa 144

class CFGLoader:

    __variables = set()
    __terminals = set()
    __start = None
    __rules = {}

    def __init__(self, filename):
        f = open(filename)
        #we iterate through each rule
        for row in f:
            #split the rule into the variable and the value
            (left, right) = row.split('::=')
            (left, right) = (left.strip(), right.strip())

            #check if there is a variable on the left
            if '<' not in left or '>' not in left:
                raise ValueError('Only variables are allowed on the left!')
            
            #add the variable to the set
            variable = left.strip('<>')
            self.__variables.add(variable)

            #set the first variable as the start
            if self.__start == None:
                self.__start = variable

            #iterate through each possible value of the rule
            values = right.split('|')
            for value in values:
                value = value.strip()
                
                #extract the terminals and the rule itself
                term, rule = self.__processString(value)

                #add the terminals to the terminals set
                for t in term:
                    self.__terminals.add(t)
                
                #create or append the rule for the variable
                if variable not in self.__rules.keys():
                    self.__rules[variable] = [rule]
                else:
                    self.__rules[variable].append(rule)
        
        self.__validate()

        f.close()

    #function that recives an unparsed rule and returns the terminals present in that rule as well as the parsed rule(without "" and <>)
    def __processString(self, expression):
        terminals = []
        rule = []
        while expression != '':
            if expression[0] == '<':
                index = expression.find('>')
                rule.append(expression[1:index])
                expression = expression[index + 1:].strip()
            else:
                index = expression[1:].find('\"')
                index += 1
                terminals.append(expression[1:index])
                rule.append(expression[1:index])
                expression = expression[index + 1:].strip()
        return terminals, rule
    

    #check if all the elements in the rules are either terminals or well defined variables
    def __validate(self):
        rule = self.__rules
        ter = self.__terminals
        var = self.__variables
        for v in rule.keys():
            for option in rule[v]:
                for component in option:
                    if component not in ter:
                        if component not in var:
                            raise ValueError('Variable <' + component + '> is not defined!')
                        
    #getters
    def getVariables(self):
        return self.__variables
    
    def getTerminals(self):
        return self.__terminals
    
    def getRules(self):
        return self.__rules
    
    def getStart(self):
        return self.__start