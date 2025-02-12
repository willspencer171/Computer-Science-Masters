from logic import *
from collections import deque, defaultdict

def normalise_KB_get_agenda(KB):
    agenda = deque()
    new_KB = []

    for clause in KB:
        if not isinstance(clause, Implication):
            new_KB.append(Implication(TrueSymbol(), clause))
        else:
            new_KB.append(clause)

        while True:
            if not isinstance(clause.premise, Symbol):
                clause = clause.premise
                continue
            elif not isinstance(clause.conclusion, Symbol):
                clause = clause.conclusion
                continue
            else:
                if clause not in agenda:
                    agenda.append(clause)
                break

        print(agenda)
        
        return new_KB, agenda

def forward_chaining(KB, query: Particle):
    """Implements forward chaining for definite clauses, supporting conjunctions."""
    KB, agenda = normalise_KB_get_agenda(KB)
    inferred = defaultdict(bool)  # Track inferred facts
    count = {}  # Track how many premises are yet to be satisfied for each rule
    premise_map = defaultdict(list)  # Maps literals to the implications they appear in

    # Initialize premise counts
    for clause in KB:
        count[clause] = 0
        if isinstance(clause.premise, BinaryParticle):
            # Count multiple literals in the premise
            count[clause] = 2
            premise_map[clause.premise.left].append(clause)
            premise_map[clause.premise.right].append(clause)
        elif not isinstance(clause.premise, TrueSymbol):
            count[clause] = 1
            premise_map[clause.premise].append(clause)

    # Process initial agenda
    while agenda:
        p = agenda.popleft()
        
        if p == query:
            return True  # If query is inferred, return True
        
        if not inferred[p]:  # Mark as inferred
            inferred[p] = True

            # Check all implications where p is in the premise
            for clause in premise_map[p]:
                count[clause] -= 1  # Reduce the number of premises left
                
                if count[clause] == 0:  # If all premises satisfied, infer conclusion
                    if not inferred[clause.conclusion]:
                        agenda.append(clause.conclusion)

    return False  # If we exhaust the agenda and don't infer query, return False


St11 = Symbol('Stench in [1, 1]')
St12 = Symbol('Stench in [1, 2]')
St13 = Symbol('Stench in [1, 3]')
St21 = Symbol('Stench in [2, 1]')
St22 = Symbol('Stench in [2, 2]')
St23 = Symbol('Stench in [2, 3]')
Sa11 = Symbol('Safe in [1, 1]')
Sa12 = Symbol('Safe in [1, 2]')
Sa13 = Symbol('Safe in [1, 3]')
Sa21 = Symbol('Safe in [2, 1]')
Sa22 = Symbol('Safe in [2, 2]')
Sa23 = Symbol('Safe in [2, 3]')
Wu11 = Symbol('Wumpus in [1, 1]')
Wu12 = Symbol('Wumpus in [1, 2]')
Wu13 = Symbol('Wumpus in [1, 3]')
Wu21 = Symbol('Wumpus in [2, 1]')
Wu22 = Symbol('Wumpus in [2, 2]')
Wu23 = Symbol('Wumpus in [2, 3]')

KB = [
    Implication(Conjunction(St11, Sa21), Wu12),
    Implication(Conjunction(St11, Sa12), Wu21),
    Implication(Conjunction(St22, Sa23), Wu12),
]

# Provide a series of facts in the agenda as a deque, then a query

print(forward_chaining(KB, Wu12))
