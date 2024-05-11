allowedCharacters = ['(', ')', '*', '+', '.']
specialCharacters = []
for i in range(33, 127):
    if (i < 47) or (i < 96 and i > 90) or (i > 57 and i < 65) or (i > 122):
        specialCharacters.append(chr(i))


class RegularExpression:

    def __init__(self, userIn):
        global allowedCharacters
        self.expression = ''.join(str(i) for i in userIn)
        self.report = ''
        self.clean = ''

        if len(self.expression) == 0:
            # print('string allowed.')
            return  

        for i in self.expression:
            if (i in specialCharacters) and (i not in allowedCharacters):
                raise ValueError('Input is not a regular expression.')
            
        parenthesis = []
        for i in self.expression:
            if i == '(':
                parenthesis.append(1)
            if i == ')':
                try:
                    parenthesis.pop()
                except:
                    raise ValueError('Input includes invalid use of parenthesis')
        if len(parenthesis) != 0:
            raise ValueError('Input includes invalid use of parenthesis')
        
        for i in self.expression:
            if i == '+':
                if len(self.expression[self.expression.index(i):]) == 0 or len(self.expression[0:self.expression.index(i)]) == 0:
                    raise ValueError('Input includes invalid use of + operator')

            if i == '.':
                if len(self.expression[self.expression.index(i):]) == 0 or len(self.expression[0:self.expression.index(i)]) == 0:
                    raise ValueError('Input includes invalid use of . operator')

            if i == '*':
                if len(self.expression[0:self.expression.index(i)]) == 0:
                    raise ValueError('Input includes invalid use of * operator')
                j = self.expression.index(i) + 1
                if self.expression[j] == '*':
                    raise ValueError('Input includes invalid use of * operator')
        
        self.alphabet = []
        for i in self.expression:
            if (i not in (allowedCharacters + [' '])) and (i not in self.alphabet):
                self.alphabet.append(i)
        self.exp_degree = None

    def cleanInput(self):
        self.expression = self.expression.replace(' ', '')
        self.expression = '(' + self.expression + ')'
        # pdb.set_trace()
        temp = len(self.expression)
        for i in range(temp-1, -1, -1):
            if (self.expression[i] in (self.alphabet + ['('])) and (self.expression[i-1] not in ['+', '(', '.']):
                self.expression = self.expression[:i] + '.' + self.expression[i:]

        self.expression = self.expression[1:]
        self.clean = self.expression

    def minor_degree(self):
        self.list_format = [i for i in self.expression]
        for i in self.list_format:
            if i in self.alphabet:
                self.list_format[self.list_format.index(i)] = 0
        for i in range(len(self.list_format)):
            if self.list_format[i] == '*':
                try: 
                    self.list_format[i-1] += 1 # if the star was after a parenthesis
                    self.list_format[i] = '$'
                except: 
                    pass
        
        self.list_format = [i for i in self.list_format if i != '$']
        self.report += (''.join(str(i) for i in self.list_format) + '\n')

    def median_degree(self):
        for j in range(self.list_format.count('.') + self.list_format.count('+')): 
            for i in range(len(self.list_format)):
                if self.list_format[i] in ['+', '.']:
                    if self.list_format[i+1] not in allowedCharacters:
                        if self.list_format[i-1] not in allowedCharacters:
                            try:
                                temp = max(self.list_format[i-1], self.list_format[i+1])
                                self.list_format[i] = temp
                                self.list_format[i-1] = '$'
                                self.list_format[i+1] = '$'
                            except:
                                pass
            
            self.list_format = [i for i in self.list_format if i != '$']
        self.report += (''.join(str(i) for i in self.list_format) + '\n')

    def major_degree(self):
        for j in range(self.list_format.count('*')):
            for i in range(len(self.list_format)):
                if self.list_format[i] == '*':
                    self.list_format[i-3] = '$'
                    self.list_format[i-2] += 1
                    self.list_format[i-1] = '$'
                    self.list_format[i] = '$'
                    break
            self.list_format = [i for i in self.list_format if i != '$']
        self.report += (''.join(str(i) for i in self.list_format) + '\n')

    def degree(self):
        self.minor_degree()
        self.median_degree()
        self.major_degree()
        self.list_format = [i for i in self.list_format if i not in ['(', ')']]
        self.report += ''.join(str(i) for i in self.list_format)
        self.median_degree()
        self.exp_degree = ''.join(str(i) for i in self.list_format)
        self.exp_degree = int(''.join(str(i) for i in self.list_format))
        # print(self.report)
        # print(self.exp_degree)

