class Particle:
    def evaluate(self, model):
        raise NotImplementedError
    
    def __repr__(self):
        raise NotImplementedError
    
class BinaryParticle(Particle):
    pass

class TrueSymbol(Particle):
    def evaluate(self, model):
        return True
    
    def __repr__(self):
        return "T"
    
class FalseSymbol(Particle):
    def evaluate(self, model):
        return False
    
    def __repr__(self):
        return "F"

class Symbol(Particle):
    def __init__(self, name):
        self.name = name

    def evaluate(self, model: dict):
        return model.get(self.name, False)
    
    def __repr__(self):
        return self.name
    
class Negation(Particle):
    def __init__(self, operand):
        self.operand = operand
    
    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def __repr__(self):
        return f"¬({self.operand})"


class Conjunction(BinaryParticle):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, model):
        return self.left.evaluate(model) and self.right.evaluate(model)

    def __repr__(self):
        return f"({self.left} ∧ {self.right})"


class Disjunction(BinaryParticle):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, model):
        return self.left.evaluate(model) or self.right.evaluate(model)

    def __repr__(self):
        return f"({self.left} ∨ {self.right})"


class Implication(BinaryParticle):
    def __init__(self, premise, conclusion):
        self.premise = premise
        self.conclusion = conclusion

    def evaluate(self, model):
        return not self.premise.evaluate(model) or self.conclusion.evaluate(model)

    def __repr__(self):
        return f"({self.premise} → {self.conclusion})"
    
class Bidirection(BinaryParticle):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self, model):
        return Conjunction(Implication(self.left, self.right),
                           Implication(self.right, self.left)).evaluate(model)
    
    def __repr__(self):
        return f"({self.left} ↔ {self.right})"
