# Week 4 - Representing and Reasoning with Knowledge I

<details><summary><h2>Reading for this week</h2></summary>

## Required Reading

### Lesson 1

Chapter 7, Section 7.2 of Artificial Intelligence: A Modern Approach

Chapter 7, Section 7.3 of Artificial Intelligence: A Modern Approach

Chapter 7, Section 7.4 of Artificial Intelligence: A Modern Approach

### Lesson 2

Chapter 7, Section 7.5.2 of Artificial Intelligence: A Modern Approach

Chapter 7, Section 7.5.3 of Artificial Intelligence: A Modern Approach

Chapter 7, Section 7.5.4 of Artificial Intelligence: A Modern Approach

## Optional Reading

Chapter 8 of Artificial Intelligence: A Modern Approach

This is a whole chapter so only have a look through it. It should be useful in applying first-order logic to different domains. Good for when propositional logic (introduced here) is too large to fit in a computer.

</details>

## Contents

1. [Principles of Logic and Propositional Logic](#principles-of-logic-and-propositional-logic)
    1. [Logical Agent Design (KB Agents)](#logical-agent-design-kb-agents)
    2. [The Wumpus World](#the-wumpus-world)

## Principles of Logic and Propositional Logic

Logic is something we touched on in [week 1](../Week%201%20-%20Introduction%20to%20Artificial%20Intelligence%20-%20uniformed%20search%20strategies/README.md#logic-solvers). The basic concepts that we need to remember from that time are:

- Knowledge bases
  - All the information about a given logical problem is stored in sentences
- Sentences
  - Sentences are written in a knowledge representation language. These are the components of knowledge bases
- Knowledge Reperesentation Language
  - The language that sentences are written in
- Logical Inference
  - The algorithm that is used to infer new information from the knowledge base

Logic takes problem solving agents to the next level. Problem solvers have their deduction logic hard-coded into their transition model functions (I denote this as `neighbours` usually)

### Logical Agent Design (KB Agents)

A knowledge based agent's main component is the **knowledge base (KB)**, comprised of **sentences**, written in a **knowledge representation language**. If a sentence is taken as a given without prior deduction, it is an **axiom**.

In order to add or query a KB, we use the terms `TELL` and `ASK`, both of which may involve **inference**

```pseudo
function KB-AGENT(percept) returns an action
    persistent: KB, a knowledge base
                t, a counter, initially 0, indicating time
    
    TELL(KB, MAKE-PERCEPT-SENTENCE(percept, t))
    action ← ASK(KB, MAKE-ACTION-QUERY(t))
    TELL(KB, MAKE-ACTION-SENTENCE(action, t))
    t ← t + 1
    return action
```

Above is the pseudocode for a simple KB agent. Step by step:

1. The agent is told new information, the percept
2. The KB is queried to find out what action should be performed
    1. This may require extensive reasoning
3. The KB is told which action was taken and the action is returned

Details of the representation language are abstracted within the `MAKE` operations, while the inference mechanisms are found in the `TELL` and `ASK` operations.

A KB agent can be built entirely by `TELL`ing it what it needs to know. It can then build up its own knowledge base until it knows how to operate within the given environment. This is known as **declarative** system building. On the other hand, a **procedural** approach aims to hard-code desired behaviours into the KB as program code. It's helpful to remember that declarative can be used to get the agent to operate in its environment. This can then be translated into a procedural approach since it can be made more efficient.

We can also provide mechanisms that allow for self-learning, covered in chapter 18 (machine learning)

### The Wumpus World

![Wumpus World](wumpus_world.png)

Wumpus (just like the one in Discord) is a monster found in the eponymous **Wumpus World**. This is a small environment that has a wumpus, pits, an agent and a pile of gold in it. You'll find a breeze in tiles adjacent to a pit, and a stench for those adjacent to the wumpus. There is only one wumpus in the world at any one time.

Let's write this out in PEAS structure:

#### Performance Measures

+1000 for climbing out of the cave with the gold, –1000 for falling into a pit or being eaten by the wumpus, –1 for each action taken and –10 for using up the arrow. The game ends either when the agent dies or when the agent climbs out of the cave.

#### Environment

A 4×4 grid of rooms. The agent always starts in the square labeled [1,1], facing to the right. The locations of the gold and the wumpus are chosen randomly, with a uniform distribution, from the squares other than the start square. In addition, each square other than the start can be a pit, with probability 0.2.

#### Actuators

The agent can move Forward, TurnLeft by 90◦, or TurnRight by 90◦. The agent dies a miserable death if it enters a square containing a pit or a live wumpus. (It is safe, albeit smelly, to enter a square with a dead wumpus.) If an agent tries to move forward and bumps into a wall, then the agent does not move. The action Grab can be used to pick up the gold if it is in the same square as the agent. The action Shoot can be used to fire an arrow in a straight line in the direction the agent is facing. The arrow continues until it either hits (and hence kills) the wumpus or hits a wall. The agent has only one arrow, so only the first Shoot action has any effect. Finally, the action Climb can be used to climb out of the cave, but only from square [1,1].

#### Sensors

The agent has five sensors, each of which gives a single bit of information:

- In the square containing the wumpus and in the directly (not diagonally) adjacent squares, the agent will perceive a Stench.
- In the squares directly adjacent to a pit, the agent will perceive a Breeze.
- In the square where the gold is, the agent will perceive a Glitter.
- When an agent walks into a wall, it will perceive a Bump.
- When the wumpus is killed, it emits a Scream that can be perceived anywhere in the cave.

Have a look at the image at the top of this section. You can see what we're getting at here. We can represent this using more concise notation such that:

- A = Agent
- B = Breeze
- G = Glitter
- OK = Safe Square
- P = Pit
- S = Stench
- V = Visited
- W = Wumpus

with modifiers for things we're not certain of (?), and those we become certain of (!).

![Wumpus Notated](wumpus_notation.png)

The thing about some of the logic involved with this is that we must infer information from a *lack* of information (things like "no stench" or "no breeze" meaning the absence of an adjacent wumpus or pit). This is something difficult because our agent currently only responds to precepts, rather than overall states of the environment.

> An important thing to recognise in all of this is that the agent's view of the wumpus world is *incomplete* until enough information is gathered. As such, what we saw in the first image is a **possible world** - one that is not concrete, but is a state that is allowed by the rules of the game.

### Logic

### Section 4

## Lesson 2

### Section 5
