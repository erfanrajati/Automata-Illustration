from phase_1 import *
from phase_3 import *
import matplotlib.pyplot as plt
import ast
import prewirtten as pw
import random

def regex_analysis(userIn):
    try: 
        new_expression = RegularExpression(i for i in userIn)
        print('Evaluation Began!')
        new_expression.cleanInput()
        new_expression.degree()

        analysis = f'''
Initial Expression:
{userIn}

Alphabet Used:
{new_expression.alphabet}

Cleaned expression:
{new_expression.clean}

Evaluation Steps:
{new_expression.report}

Final Degree Evaluation:
{new_expression.exp_degree}
        '''
    
    except ValueError:
        analysis = 'Input string is not a Regular Expression'
    

    with open('Expression_Analysis.txt', 'w') as file:
        file.write(analysis)
        print('Evaluation Completed!')


def extract_automaton_by_input(nodes, edges):
    nodes = ast.literal_eval(nodes)
    edges = ast.literal_eval(edges)
    graphData = {
        'nodes': [node for node in nodes],
        'edges': [edge for edge in edges]
    }
    
    new_automaton = Automaton(graphData)
    new_automaton.draw()


def extract_automaton_by_sample():
    graphData = random.choice(pw.dfa_samples)
    new_automaton = Automaton(graphData)
    new_automaton.draw()
    # new_automaton.get_data()




# i want you to give me 5 sample DFAs so I can test my code on, you should give each in a python dictionary like: 
# dfa1 = {
# 'nodes': [ 'q1', 'q2', ...],
#  'edges': [('q1', 'q2', 'a'), ('q2', 'q3', 'b'), ...]
# }
# where the nodes are obvious what they are and the edges are triplets where first is the initial state of transition, second is the final state of trnasition and third is the letter that is being read by the machine.
# cosider to folow the wiritng format strictly. also, add at least 5 nodes for each DFA and have them all reachable.