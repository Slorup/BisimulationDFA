#TODO: Find trace in case of reject
#TODO: Verify DFA syntax

class DFA:
    language_text = ""
    alphabet = []
    states = []
    initial_state = ""
    final_states = []
    transitions = {}

    def __init__(self, alphabet, states, initial_state, final_states, transitions, language_text):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions
        self.language_text = language_text

def get_to_state(state, action, transitions):
    for ((from_state, apply_action), to_state) in transitions.items():
        if from_state == state and action == apply_action:
            return to_state
    return None

bisim_relation = []

def dfs(state, solution_state, dfa, solution_dfa, trace):
    if (state, solution_state) in bisim_relation:
        return True

    if state in dfa.final_states and solution_state not in solution_dfa.final_states:
        print("\nCounterexample: " + str(trace) + " is not in the language, but in the given dfa!")
        return False
    if state not in dfa.final_states and solution_state in solution_dfa.final_states:
        print("\nCounterexample: " + str(trace) + " is in the language, but not in the given dfa!")
        return False

    bisim_relation.append((state, solution_state))

    for action in solution_dfa.alphabet:
        to_state = get_to_state(state, action, dfa.transitions)
        if to_state is None:
            print("Missing action " + action + " in state " + state)
            return False
        to_state_solution = get_to_state(solution_state, action, solution_dfa.transitions)
        if to_state_solution is None:
            print("Missing action " + action + " in state " + state + " in the solution!")
            return False
        trace.append(action)
        is_bisim = dfs(to_state, to_state_solution, dfa, solution_dfa, trace)
        trace.pop()
        if not is_bisim:
            return False

    return True

def read_input_dfa(alphabet):
    print('initial_state: ', end='')
    initial_state = input()

    waiting = {initial_state}
    done = []
    finals = []
    transitions = {}

    while len(waiting) > 0:
        q = waiting.pop()
        done.append(q)

        print(f'{q} is_final? ', end='')
        if input() == 'y':
            finals.append(q)

        for s in alphabet:
            print(f'{q}  ->_{s}  ', end='')
            r = input()
            transitions[(q, s)] = r
            if r not in done:
                waiting.add(r)

    dfa = DFA(alphabet, done, initial_state, finals, transitions, "")
    return dfa


def load_solution(name):
    match name:
        case "binary_divisible_3": #Can be solved with 3 states instead
            langauge_text = "L = {w \in {1,0}* | w is a binary number and divisible by 3 or w is the empty string}"
            alphabet = ['1', '0']
            states = ['a', 'd', 'b', 'c', 'e', 'f']
            initial_state = "a"
            final_states = ['a', 'd']
            transitions = {('a', '1'): 'b', ('a', '0'): 'd', ('d', '1'): 'e', ('d', '0'): 'a', ('b', '1'): 'a',
                           ('b', '0'): 'c', ('c', '1'): 'f', ('c', '0'): 'b', ('e', '1'): 'd', ('e', '0'): 'f',
                           ('f', '1'): 'c', ('f', '0'): 'e'}
            return DFA(alphabet, states, initial_state, final_states, transitions, langauge_text)
        case "contains_substring_01":
            language_text = "L = {w \in {1,0}* | w contains the substring '01'}"
            alphabet = ['1', '0']
            states = ['a', 'b', 'c']
            initial_state = "a"
            final_states = ['c']
            transitions = {('a', '1'): 'a', ('a', '0'): 'b', ('b', '1'): 'c', ('b', '0'): 'b', ('c', '1'): 'c', ('c', '0'): 'c'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "contains_exactly_two_1s":
            language_text = "L = {w \in {1,0}* | w contains exactly two 1's}"
            alphabet = ['1', '0']
            states = ['a', 'b', 'c', 'd']
            initial_state = "a"
            final_states = ['c']
            transitions = {('a', '1'): 'b', ('a', '0'): 'a', ('b', '1'): 'c', ('b', '0'): 'b', ('c', '1'): 'd', ('c', '0'): 'c',
                           ('d', '1'): 'd', ('d', '0'): 'd'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "binary_representation_of_even_natural_number":
            language_text = "L = {w \in {1,0}* | w is an even binary number or the empty string}"
            alphabet = ['1', '0']
            states = ['a', 'b']
            initial_state = "a"
            final_states = ['a']
            transitions = {('a', '0'): 'a', ('a', '1'): 'b', ('b', '0'): 'a', ('b', '1'): 'b'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "((a(b*)a)|(c(d*)c))*":
            language_text = "Regular Expression: ((a(b*)a)|(c(d*)c))*"
            alphabet = ['a', 'b', 'c', 'd']
            states = ['s0', 's3', 's2', 's1']
            initial_state = "s0"
            final_states = ['s0']
            transitions = {('s0', 'a'): 's2', ('s0', 'b'): 's3', ('s0', 'c'): 's1', ('s0', 'd'): 's3', ('s3', 'a'): 's3',
                           ('s3', 'b'): 's3', ('s3', 'c'): 's3', ('s3', 'd'): 's3', ('s2', 'a'): 's0', ('s2', 'b'): 's2',
                           ('s2', 'c'): 's3', ('s2', 'd'): 's3', ('s1', 'a'): 's3', ('s1', 'b'): 's3', ('s1', 'c'): 's0',
                           ('s1', 'd'): 's1'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "tricky_full":
            language_text = "L = {xy \in {a,b}* | The number of a's in x equals the number of b's in y}"
            alphabet = ['a', 'b']
            states = ['s0']
            initial_state = "s0"
            final_states = ['s0']
            transitions = {('s0', 'a'): 's0', ('s0', 'b'): 's0'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "0_equals_01":
            language_text = "L = {w \in {0,1}* | the number of times the substring '0' appears in w equals the number of times the substring '01' appears in w}"
            alphabet = ['0', '1']
            states = ['s0', 's1', 's2']
            initial_state = "s0"
            final_states = ['s0']
            transitions = {('s0', '0'): 's1', ('s0', '1'): 's0', ('s1', '0'): 's2', ('s1', '1'): 's0', ('s2', '0'): 's2',
                           ('s2', '1'): 's2'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "min_two_as":
            language_text = "L = {w \in {a,b}* | w contains at least 2 a's}"
            alphabet = ['a', 'b']
            states = ['s0', 's1', 's2']
            initial_state = "s0"
            final_states = ['s2']
            transitions = {('s0', 'a'): 's1', ('s0', 'b'): 's0', ('s1', 'a'): 's2', ('s1', 'b'): 's1',
                           ('s2', 'a'): 's2', ('s2', 'b'): 's2'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "even_as_and_bs":
            language_text = "L = {w \in {a,b}* | w contains an even number of a's and even number of b's}"
            alphabet = ['a', 'b']
            states = ['s0', 's1', 's3', 's2']
            initial_state = "s0"
            final_states = ['s0']
            transitions = {('s0', 'a'): 's1', ('s0', 'b'): 's3', ('s1', 'a'): 's0', ('s1', 'b'): 's2', ('s3', 'a'): 's2',
                           ('s3', 'b'): 's0', ('s2', 'a'): 's3', ('s2', 'b'): 's1'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "larger_than_5_binary":
            language_text = "L = {w \in {1,0}* | w is a binary number and is larger than 5}"
            alphabet = ['1', '0']
            states = ['a', 'b', 'c', 'd', 'f', 'e']
            initial_state = "a"
            final_states = ['f']
            transitions = {('a', '1'): 'b', ('a', '0'): 'a', ('b', '1'): 'c', ('b', '0'): 'd', ('c', '1'): 'f', ('c', '0'): 'f',
                           ('d', '1'): 'e', ('d', '0'): 'e', ('f', '1'): 'f', ('f', '0'): 'f', ('e', '1'): 'f', ('e', '0'): 'f'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "num_0s_divisible_by_3":
            language_text = "L = {w \in {1,0}* | the number of 0's in w is a multiple of 3}"
            alphabet = ['1', '0']
            states = ['s0', 's1', 's2']
            initial_state = "s0"
            final_states = ['s0']
            transitions = {('s0', '1'): 's0', ('s0', '0'): 's1', ('s1', '1'): 's1', ('s1', '0'): 's2', ('s2', '1'): 's2',
                           ('s2', '0'): 's0'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "a_followed_by_1_or_3_bs":
            language_text = "L = {w \in {a,b}* | each a is followed by exactly 1 or 3 b's}"
            alphabet = ['a', 'b']
            states = ['s0', 's1', 's2', 's5', 's3', 's4']
            initial_state = "s0"
            final_states = ['s0', 's2', 's4']
            transitions = {('s0', 'a'): 's1', ('s0', 'b'): 's0', ('s1', 'a'): 's5', ('s1', 'b'): 's2', ('s2', 'a'): 's1',
                           ('s2', 'b'): 's3', ('s5', 'a'): 's5', ('s5', 'b'): 's5', ('s3', 'a'): 's5', ('s3', 'b'): 's4',
                           ('s4', 'a'): 's1', ('s4', 'b'): 's5'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "even_end_aa_odd_end_aba":
            language_text = "L = {w \in {a,b}* | either |w| is even and ends with 'aa' or |w| is odd and ends with 'aba'}"
            alphabet = ['a', 'b']
            states = ['ol', 'ou', 'al', 'au', 'abl', 'aal', 'abau']
            initial_state = "ol"
            final_states = ['aal', 'abau']
            transitions = {('ol', 'a'): 'au', ('ol', 'b'): 'ou', ('ou', 'a'): 'al', ('ou', 'b'): 'ol', ('al', 'a'): 'au',
                           ('al', 'b'): 'ou', ('au', 'a'): 'aal', ('au', 'b'): 'abl', ('abl', 'a'): 'abau', ('abl', 'b'): 'ou',
                           ('aal', 'a'): 'au', ('aal', 'b'): 'ou', ('abau', 'a'): 'aal', ('abau', 'b'): 'abl'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "start_end_same_symbol_abc":
            language_text = "L = {w \in {a,b}* | the first symbol of w equals the last symbol of w or w is the empty string}"
            alphabet = ['a', 'b', 'c']
            states = ['s0', 'sb', 'sb0', 'sc', 'sc0', 'sa', 'sa0']
            initial_state = "s0"
            final_states = ['s0', 'sb', 'sc', 'sa']
            transitions = {('s0', 'a'): 'sa', ('s0', 'b'): 'sb', ('s0', 'c'): 'sc', ('sb', 'a'): 'sb0', ('sb', 'b'): 'sb',
                           ('sb', 'c'): 'sb0', ('sb0', 'a'): 'sb0', ('sb0', 'b'): 'sb', ('sb0', 'c'): 'sb0', ('sc', 'a'): 'sc0',
                           ('sc', 'b'): 'sc0', ('sc', 'c'): 'sc', ('sc0', 'a'): 'sc0', ('sc0', 'b'): 'sc0', ('sc0', 'c'): 'sc',
                           ('sa', 'a'): 'sa', ('sa', 'b'): 'sa0', ('sa', 'c'): 'sa0', ('sa0', 'a'): 'sa', ('sa0', 'b'): 'sa0',
                           ('sa0', 'c'): 'sa0'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "substring_len_3_has_exactly_two_as":
            language_text = "L = {w \in {a,b}* | \\forall_x,y,z . ((w = xyz and |y| = 3) => |y|_a = 2)}"
            #every subword with length 3 has exactly two a’s.
            alphabet = ['a', 'b']
            states = ['s0', 'sb', 'sa', 'sab', 'sg', 'sba', 'sbb', 'saa']
            initial_state = "s0"
            final_states = ['s0', 'sb', 'sa', 'sab', 'sba', 'sbb', 'saa']
            transitions = {('s0', 'a'): 'sa', ('s0', 'b'): 'sb', ('sb', 'a'): 'sba', ('sb', 'b'): 'sbb', ('sa', 'a'): 'saa',
                           ('sa', 'b'): 'sab', ('sab', 'a'): 'sba', ('sab', 'b'): 'sg', ('sg', 'a'): 'sg', ('sg', 'b'): 'sg',
                           ('sba', 'a'): 'saa', ('sba', 'b'): 'sg', ('sbb', 'a'): 'sg', ('sbb', 'b'): 'sg', ('saa', 'a'): 'sg',
                           ('saa', 'b'): 'sab'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "num_aba_plus_1_equals_num_b":
            language_text = "L = {w \in {a,b}* | |w|_aba + 1 = |w|_b}"
            #the number of occurrences of aba is one less than the number of occurrences of b.
            alphabet = ['a', 'b']
            states = ['s0', 's3', 's1', 's2', 's4', 's6', 's5']
            initial_state = "s0"
            final_states = ['s3', 's2', 's4']
            transitions = {('s0', 'a'): 's1', ('s0', 'b'): 's3', ('s3', 'a'): 's4', ('s3', 'b'): 's6', ('s1', 'a'): 's1',
                           ('s1', 'b'): 's2', ('s2', 'a'): 's1', ('s2', 'b'): 's6', ('s4', 'a'): 's4', ('s4', 'b'): 's5',
                           ('s6', 'a'): 's6', ('s6', 'b'): 's6', ('s5', 'a'): 's4', ('s5', 'b'): 's6'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)
        case "num_bs_right_of_a_is_even":
            language_text = "L = {w \in {a,b}* | \\forall_x,y . (w = xay => |y|_b is even)}"
            #the right of each occurrence of a there is an even number of b’s.
            alphabet = ['a', 'b']
            states = ['s0', 's1', 's2', 's3']
            initial_state = "s0"
            final_states = ['s0', 's1']
            transitions = {('s0', 'a'): 's1', ('s0', 'b'): 's0', ('s1', 'a'): 's1', ('s1', 'b'): 's2', ('s2', 'a'): 's3',
                           ('s2', 'b'): 's1', ('s3', 'a'): 's3', ('s3', 'b'): 's3'}
            return DFA(alphabet, states, initial_state, final_states, transitions, language_text)

    #TODO: valid regular expressions (or arithmetric)
    #TODO: L = {xyz \in {a,b}* | xyz contains 'ab' and xz does not contain 'ab' and |y| = 1}
    return None

def print_dfa_text(dfa):
    print("\nThe input as DFA:")
    print("alphabet = " + str(dfa.alphabet))
    print("states = " + str(dfa.states))
    print("initial_state = \"" + dfa.initial_state + "\"")
    print("final_states = " + str(dfa.final_states))
    print("transitions = " + str(dfa.transitions))


if __name__ == '__main__':
    solution_dfa = load_solution("even_end_aa_odd_end_aba")
    if solution_dfa is None:
        print("Invalid solution name")
        exit()
    dfa = read_input_dfa(solution_dfa.alphabet)
    print_dfa_text(dfa)
    is_bisim = dfs(dfa.initial_state, solution_dfa.initial_state, dfa, solution_dfa, [])
    print("Bisimulation: " + str(is_bisim))

    if is_bisim:
        print("Bisimulation relation: " + str(bisim_relation))
