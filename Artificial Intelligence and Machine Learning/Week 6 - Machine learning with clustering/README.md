# Week 6 - Machine Learning with Clustering

<details><summary><h2>Reading for this Week</h2></summary>

## Required Reading

### Lesson 1

Artificial Intelligence: A Modern Approach, Chapter 19 Introduction and Section 19.1

### Lesson 2

[Data Mining: Practical Machine Learning Tools and Techniques, Witten, Frank, Hall, Pal (4th edition, Elsevier 2016)](https://ebookcentral.proquest.com/lib/york-ebooks/detail.action?docID=4708912&pq-origsite=primo) Section 4.8 the start of the section and the first sub-section, titled “Iterative Distance-Based Clustering”

### Lesson 3

Artificial Intelligence: A Modern Approach, Chapter 19, Section 19.2

## Optional Reading

Data Mining: Practical Machine Learning Tools and Techniques, Witten, Frank, Hall, Pal (4th edition, Elsevier 2016) - Section 4.7

</details>

## Contents

1. [Supervised, Unsupervised and Reinforcement Learning](#supervised-unsupervised-and-reinforcement-learning)
2. [Clustering with K-Means](#clustering-with-k-means)
3. [Principles and Pitfalls of Supervised Learning](#principles-and-pitfalls-of-supervised-learning)

I think, actually, there's every chance the reading material referenced above is not correct, since chapter 18 is the start of the machine learning section. I think I should have a look at chapter 18

## Supervised, Unsupervised and Reinforcement Learning

We've all heard about these. The main ways of implementing Machine learning in computers. To put it simply:

- **Supervised Learning** takes a set of examples with corresponding labels as inputs and learns how to best classify new data based on what it's learned
  - The aim of supervised learning is to learn a function that effectively maps between the inputs and outputs of the environment.
  - Outputs may well be given in the form of a teacher providing an action to the agent. However, the teacher doesn't need to be a person - the environment itself can become the teacher in many cases
- **Unsupervised Learning** also takes a set of examples, but without their corresponding labels. This class of algorithms' job is to find patterns in data that aren't previously identified
  - A common example of this is **clustering**, which we'll be looking at this week
- **Reinforcement Learning** doesn't provide examples of anything. An agent navigates an environment with actions and the results of those actions are fed back to the agent to Pavlov's Dog them - Behavioural Conditioning styles.
  - Zapping a computer agent isn't morally wrong at the end of the day, is it?

In this week (at least, anyway), we'll be looking at how any one of these methods takes information in the form of a **factored representation**. This is a simple vector of attribute (AKA feature) values that allow each value to be access individually. A table or database is a good example of this. Propositional logic models are a form of factored representation, too! We'll also see how this approach will output either a continuous numerical value or discrete value (which you'll know from regression types like linear and logistic). This is also known as **inductive learning**.

This isn't to say that we can't incorporate things like prior knowledge in the form of first-order logic or by using Bayesian Networks.

We also have the intermediate case of **semi-supervised learning**. This is a mixture of supervised and unsupervised learning that compensates the fact that supervised learning from a set of incorrect labels will lead the model to be incorrect too.

### Supervised Learning

We talked about it already, but here's a bit of dedicated information.

Formally speaking, supervised learning completes the following task:

> Given a training set of $N$ example input-output pairs $$\qquad(x_1,y_1),(x_2,y_2),\cdots (x_N,y_N)$$ where each $y_j$ was generated by an unknown function $y=f(x)$, discover a function $h$ that approximates the true function $f$

Essentially, the goal is to test a bunch of **hypothesis** functions to see which best approximates the true function $f$. This is, at its heart, a search problem through the space of possible hypotheses. We can test each hypothesis by giving it a test set of samples distinct from the training set.

We say that a hypothesis **generalises well** if it correctly predicts the value of $y$ for a test sample. In some cases, the function $f$ is stochastic, meaning it is not necessarily a function of $x$. In this case, what the agent has to learn is a **conditional probability distribution** $P(Y|x)$.

In our search through the **hypothesis space** $\mathcal{H}$, we will find all sorts of functions that fit the data particularly well. Some will have high degree polynomials, and some will be linear. **Ockham's Razor** is a principle that states we must choose the simplest hypothesis that is consistent with the data.

Classification analysis falls into this category, and a good example of this is decision tree classifiers

### Unsupervised Learning

As we did with supervised learning, let's have a bit more of a look at unsupervised learning.

The objective of unsupervised learning is to spot and highlight patterns in data that were previously not recognised or known. A typical example of this is using clustering algorithms to show which data points are closest to one another.

Instances in a group may be exclusive (can only be members of one group), overlapping (can be members of more than one group), probabilistic (instances belong to each group with a certain probability), or hierarchical (groups are divided into subgroups, refining eventually to each individual point).

## Clustering with K-Means

Take a look at [this portion](https://youtu.be/E4M_IQG0d9g?list=PLBw9d_OueVJS_084gYQexJ38LC2LEhpR4&t=6019) of the CS50 video on AI Learning. It goes over, very quickly and visually, how the k-means clustering algorithm works. You've seen this all before in the DMTA module, but you're seeing it again here with fresh, AI-oriented eyes.

**K-Means Clustering** is very simple. We create, at random, k points that we call **centroids**. These are what will become the centre of each of our clusters. For a simple example, data points are given a "location" that can be represented on a grid of sorts. Our centroids are also placed at random on this grid. All the data points are assigned to a centroid that they are closest to. Then, the centroid is moved to the point that is most average amongst these data points. Then, the cycle repeats and data points are assigned to a centroid. The centroid moves. Once a point is reached such that the centroid is not moving by a significant amount, we can say the algorithm has reached a point of equilibrium and our data points are assigned to our k clusters.

An alternative algorithm that identifies the most average instance of a cluster is the k-medoids clustering algorithm, where the median of each cluster is taken, instead of the mean.

The main goal of k-means clustering is to minimise the total squared distance of each cluster's data points to its center. Typically, the distance metric chosen is Euclidean distance since it is straightforward, but some problems may require different distance metrics.

There is also an improved version of k-means called **k-means++** that I won't go into too much detail on. However, in principle, it means to choose the **seeds** (the original centroids) based on the seeds that have been chosen before it. For the initial seed, a random location is chosen based on uniform probability distribution. The successors are then chosen with a probability distribution proportional to the square of the distance from the previous. This improves speed and accuracy over the original random-seed k-means.

If you want to find out a bit more about how to optimise the k-means algorithm, have a look at the next section titled Faster Distance Calculations in Section 4.8 of [Data Mining](https://ebookcentral.proquest.com/lib/york-ebooks/detail.action?docID=4708912&pq-origsite=primo) as well as a bit of background reading of kD- and ball trees in section 4.7

A little bit of talk there about hyperspheres which was fun. Also brush up on your definitions of hyperplanes. In many instances they are decision boundaries, but not in the case of kD-trees and ball trees, they're just splits in the data.

## Principles and Pitfalls of Supervised Learning

Okay so I kinda went ahead and did this in the last section (oopsies!) and also the further reading was to look into k-nearest neighbours which I looked at a bit in the section 4.7 part. Cool. Anyway, the title of this section is Principles and Pitfalls of Supervised Learning so let's have a look at the main pitfalls:

- Attempting to learn using an inappropriate hypothesis space;
- Using the entire data set for training and failing to test whether the hypothesis generalizes well;
- Learning a very complex hypothesis that is accurate on the training set but less accurate on the test set, and probably also less accurate when deployed in the real world.

Out of these three main pitfalls, the first two are common sense and standard practice - don't use a hypothesis space that's irrelevant to what you're trying to find out, and don't use your whole dataset as a training set unless you have separated it from some testing samples (think `sklearn`'s `train_test_split` method).

The last one is about model **overfitting** which is a big problem that pretty much all learning approaches suffer from. It makes sense - imagine you've been taught something your whole life and it turns out that when you get to adulthood, that behaviour you were taught is harmful. Specialise that to your data and that translates to "your model is perfect for the data you trained it on, but doesn't work well for new data". So be careful, yeah?
