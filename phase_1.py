import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque


class DFA:
    states = {}
    input_symbols={}
    transitions={}
    initial_state= ''
    final_states={}

    def __init__(self,states,input_symbols,transitions,initial_state,final_states) -> None:
        # Initialize DFA
        self.states = states
        self.input_symbols = input_symbols
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        #object.__setattr__(self, '_count_cache', [])

    def IsAccept(self,Text):
        # Return True if DFA was at final state when we finish reading text
        current = self.initial_state
        for c in Text:
            current = self.transitions.get(current).get(c)
        if current in self.final_states :
            print('Accept')
        else:
            print('Not Accept')

    def IsNull(self):
        #Return True if there is a final state in reachable states from initial state
        Reachables = []
        States = []
        Reachables.append(self.initial_state)
        States.append(self.initial_state)
        CheckNull = True
        while(len(States)>0):
            state = States.pop(0)
            for next_state in self.transitions[state].values():
                if not(next_state in Reachables):
                    if next_state in self.final_states:
                        CheckNull=False
                    Reachables.append(next_state)
                    States.append(next_state)
        return CheckNull
    
    def ToGraph(self):
        #Convert DFA to NetworkX Graph
        return nx.DiGraph([
            (start_state, end_state)
            for start_state, transition in self.transitions.items()
            for end_state in transition.values()
        ])

    def IsFinite(self):
        # Return True if There is a longest path available in converted graph
        # Return True (Finite) if DFA is Null
        if self.IsNull():
            return True

        graph = self.ToGraph()
        # Calculate all reachable nodes from initial state
        Reachables = nx.descendants(graph, self.initial_state) 
        # Calculate all nodes that have a path to 1 or more final states 
        NeededNodes = self.final_states.union(*(
            nx.ancestors(graph, state)
            for state in self.final_states
        ))

        GoodNodes = Reachables.intersection(NeededNodes)
        #Create Good SubGraph
        subgraph = graph.subgraph(GoodNodes)
        try:
            #Finite Language
            Longest =  nx.dag_longest_path_length(subgraph)
            return True
        except nx.exception.NetworkXUnfeasible:
            #Infinite Language
            return False

    def RemoveUnreachables(self):
        Reachables = []
        States = []
        Reachables.append(self.initial_state)
        States.append(self.initial_state)
        while(len(States)>0):
            state = States.pop(0)
            for next_state in self.transitions[state].values():
                if not(next_state in Reachables):
                    Reachables.append(next_state)
                    States.append(next_state)
        UnReachables = []
        for State in self.states:
            if not(State in Reachables):
                UnReachables.append(State)
        #Remove Unreachable from States,FinalStates and Transitions
        for i in range (0,len(UnReachables)):
            self.transitions.pop(UnReachables[i])
            self.states.remove(UnReachables[i])
            if UnReachables[i] in self.final_states:
                self.final_states.remove(UnReachables[i])

    def MinimizeDFA(self):
        self.RemoveUnreachables()
        table = []
        #Initialize First Level Myhil
        NoneFinals = []
        Finals = []
        for State in self.states:
            if not(State in self.final_states):
                NoneFinals.append(State)
            else:
                Finals.append(State)
        table.append(NoneFinals)
        table.append(Finals)
        #print(table)
        flag = False
        Steps = 0
        breaking = False
        #Changed = False
        while True:
            breaking = False
            Changed=False
            for LargePack in table:
                if breaking==True:
                    break
                for X in LargePack:
                    if breaking == True:
                        break
                    #Check X with all other largepac items
                    for Y in LargePack:
                        if breaking == True:
                            break

                        if X!=Y:
                            #Check for All Alphabets
                            for Alphabet in self.input_symbols:
                                if breaking == True:
                                    break

                                XGoesTo = self.transitions.get(X).get(Alphabet)
                                YGoesTo = self.transitions.get(Y).get(Alphabet)
                                #print('X:' + X + 'GoesTo:' +XGoesTo+' and y:' + Y+ "Goes to:"+  YGoesTo)
                                #Check For Targets in 1 Hamarzi CLass
                                smallflag = False

                                for Pack in table:

                                    if breaking == True:
                                        break
                                    if XGoesTo in Pack and YGoesTo in Pack:
                                        smallflag=True
                                        #1class
                                if smallflag == False:

                                    #X should leave that pack or y?
                                    for Other in LargePack:

                                        if breaking == True:
                                            break
                                        if Other != X and Other != Y:
                                            #Compare X with Other if there was in 1 group, y Leave
                                            for alpha in self.input_symbols:

                                                if breaking == True:
                                                    break
                                                xGoesTo = self.transitions.get(X).get(alpha)
                                                OtherGoesTo = self.transitions.get(Y).get(alpha)
                                                smallestflag = False
                                                for Pack in table:
                                                    if xGoesTo in Pack and OtherGoesTo in Pack:
                                                        smallestflag=True
                                                        #Other and X are in 1 class so y should leave
                                                        #print(Y + 'Should Leave becuse of '+ Other)
                                                        table.append([Y])
                                                        LargePack.remove(Y)
                                                        Changed=True
                                                        # print(table)
                                                        breaking = True
                                                        break
                                    if breaking==True:
                                        break
                                    # print(X + 'Should Leave becuse of'+ Y)
                                    table.append([X])
                                    LargePack.remove(X)
                                    Changed=True
                                    #print(table)
                                    breaking = True
                                    break
            #print("Dore Baad")
            Steps = Steps + 1
            if Changed == False:
                break
        #table is our hamarzi class -> create new DFA
        newTransition = {}
        for Tab in table:
            newTransition[str(Tab)] = self.transitions.get(Tab[0])
        newdfa = DFA(
        states=self.states,
        input_symbols=self.input_symbols,
        transitions=newTransition,
        initial_state=self.initial_state,
        final_states=self.final_states
        )
        return newdfa

    def isEqual(self,OtherDFA):
        self2 = self.MinimizeDFA()
        selfgraph = self2.ToGraph()
        OtherDFAGraph = OtherDFA.ToGraph()
        return nx.is_isomorphic(selfgraph, OtherDFAGraph)


class Automaton:
    def __init__(self, graphData):
        self.data = graphData
        self.graph = nx.DiGraph()
        for node in graphData['nodes']:
            self.graph.add_node(node)
        for edge in graphData['edges']:
            self.graph.add_edge(edge[0], edge[1], label=edge[2])
        self.edge_labels = nx.get_edge_attributes(self.graph, 'label')
        self.pos = nx.circular_layout(self.graph)

    def draw(self):
        nx.draw_networkx_nodes(self.graph, self.pos, node_size=1600)
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[self.data['nodes'][0]], node_color='green', node_size=1600)
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[self.data['nodes'][-1]], node_color='red', node_size=2400)

        nx.draw_networkx_edges(self.graph, self.pos, width=6)

        nx.draw_networkx_labels(self.graph, self.pos, font_size=20, font_family='sans-serif')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=self.edge_labels)

        plt.axis('off')
        plt.show()

    def get_data(self):
        print(self.graph.nodes())
        print(self.graph.edges())



dfa = DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q2', '1': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)


dfa2 = dfa.MinimizeDFA()
print(dfa.isEqual(dfa2))