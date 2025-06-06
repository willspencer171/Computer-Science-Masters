# Week 4: Choosing an Appropriate Analysis Technique

## Weekly Learning Outcomes

1. Apply multiple regression and support vector regression (MLO 3)
2. Apply Naïve Bayes and support vector classification (MLO 3)
3. Choose between techniques for a given analysis in a principled way (MLO 3)
4. Identify, address and document residual threats to validity for a given analysis (MLO 3)

## Reading for this Week

### Lesson 1

- Read Section 7.2 of Witten et al

### Lesson 2

- Section 4.2 of Witten et al

### Lesson 3

- Model Selection Management Systems: The Next Frontier of Advanced Analytics
- Read Sections 5.2 and 5.6 of Witten et al

## Table of Contents

1. [Alternative Techniques for Regression](#alternative-techniques-for-regression)
    1. [Multiple Linear Regression](#multiple-linear-regression)
    2. [Extending the Linear Model](#extending-the-linear-model)
    3. [Support Vector Machines](#support-vector-machines)
2. [Alternative Techniques for Classification](#alternative-techniques-for-classification)
    1. []()
    2. []()
    3. []()
3. [Choosing a Learning Technique](#choosing-a-learning-technique)
    1. []()
    2. []()
    3. []()

## Alternative Techniques for Regression

In order to decide which regression methods are best for our data, we need to be aware of other kinds of regression. Here, I'll talk about a few others like Multiple Linear Regression, Support Vector Regression (or Machine, SVM) and Kernel Ridge Regression.

### Multiple Linear Regression

Okay, so this isn't really extending linear regression much from what I described last week. However, it's the more general form of linear regression. Simple linear regression is characterised by the form

$$y=w_0+w_1x_1$$

or $y=mx+c$. Multiple linear regression is an extension of this into multiple dimensions:

$$y=w_0 + w_1x_1 + w_2x_2 + \dots + w_nx_n$$

The effects are additive! The goal is to minimise the squared error $\sum(y_i-\hat{y}_i)^2$ by estimating the weights $w_0, w_1, \dots, w_n$ that optimise this

The assumptions of linear regression are:

- Linear relationship between inputs and outputs
- Independent input variables
  - Low multicollinearity
- Homoscedasticity
  - Constant variance of errors
- Normally distributed residuals
  - Useful for making statistical inferences about those residuals

#### Multicollinearity

Multicollinearity is a property of attributes such that they are less independent of one another. For example, temperature and pressure are linearly correlated (by a factor of $n\times r\times v^{-1}$). If we measured the effects of temperature and pressure on another feature, they would be difficult to distinguish from one another as drivers of the changes in that feature.

This also leads to unstable coefficients for each of the collinear features and the model may generalise poorly if overfitting occurs because of this.

We can remove correlated features using a Variance Inflation Factor to identify multicollinearity (or if we know which features are likely to be correlated). We can also combine them. For example, instead of using volume and temperature as separate values, we can combine them to create pressure. Another way to manage multicollinearity is to use regularisation. Ridge kernel regression uses this technique to reduce the effects of mullticollinearity.

### Extending the Linear Model

So, while linear regression tools are useful, it's important to recognise that there are times where your real-world data won't be linear (many times, really). Before we get to support vector machines, let's try to extend the linear model that we had before so that we can effectively model nonlinear relationships.

Let's say we have two attributes, $a_1$ and $a_2$. In the multiple linear regression, this would look like:

$$x=w_0 + w_1a_1 + w_2a_2$$

But this doesn't fit the data well! What we can do, however, is transform our inputs by mapping them to a nonlinear space! Now, when we make a straight line in the nonlinear space, it won't look like a straight line in linear space! The decision boundary is no longer a hyperplane!

So, let's apply this idea to the above ordinary linear model. Let's say our original attributes are replaced by a set of attributes giving all products of $n$ factors that can be constructed from those original attributes. For two attributes (as above) with three factors, this would look like:

$$x=w_1a_1^3 + w_2a_1^2a_2 + w_3a_1a_2^2 + w_4a_2^3$$

Now, we can classify our training and test instances by transforming them using the structure above. There is nothing to stop us (in principle) from adding more attributes to this. The problem we come up against, however, is that the number of coefficients to compute explodes as we add more features (problem 1). If we were to add one more attribute (with three factors again) would increase the number of weights from 4 to 10. With 10 attributes with 5 factors, the learning algorithm has to compute over 2000 coefficients. Insane given that linear regression runs in cubic time anyway! Aside from this, the problem comes to be that the data is very likely to be overfit (problem 2).

Support Vector Machines (SVMs) address these two problems

### Support Vector Machines

Let's get into what's known as the *maximum margin hyperplane*.

This is the result of a special kind of linear model. A maximum margin hyperplane is a hyperplane that separates two classes linearly (of course), but it lies equidistant from the convex hulls of the classes' instances. A convex hull is essentially the perimeter of a set of instances. The maximum margin hyperplane is as far as possible from both hulls - it is the perpendicular bisector of the shortest line connecting the hulls.

![Maximum Margin Hyperplane](../Images/max_mar_hyp.png)

The instances that are closest to the MMH are called the support vectors. The set of support vectors define, uniquely, the maximum margin hyperplane for the problem.

The hyperplane can be written in the usual form, or it can be written with respect to the support vectors:

$$x=b+\sum_{i}\alpha_i y_i\text{a(i)}\cdot \text{a}$$

Where $y_i$ is the class value of training instance $\text{a(i)}$, while $b$ and $\alpha_i$ are hyperparameters. $\text{a}$ is a test instance and $\text{a(i)}$ is a support vector. The dot product just means $\sum_j a(i)_ja_j$, the sum of the vectors' products.

So, the problem of finding the support vectors, and the values for $b$ and $\alpha_i$ belongs to a class of optimisation problems called constrained quadratic optimisation problems. I'd like to find out how these work.

#### Support Vector Classification

So how does a support vector machine overcome the problems above?

Let's address problem 2 first. When we use the attribute transformation we had before, we tend to overfit because all training instances are used to inform the fit and thus the location of the decision boundary; it's unstable. However, we use the support vectors to train our maximum margin hyperplane, making the decision boundary much more robust (we are using significantly fewer points to make this decision). Overfitting is now less likely to occur!

The problem of computational complexity is still here. Every time a new instance is classified, its dot product has to be calculated with all support vectors, an O(n) action. In the high dimensional mapping, this is hugely expensive!

There is a workaround though. What if we computed the dot products before the nonlinear mapping? This way, we're computing our dot products in the original low-dimensional space, rather than the high dimensional space:

$$x=b+\sum\alpha_iy_i(\text{a(i)}\cdot\text{a})^n$$

where $n$ is the number of factors that we chose in the original high-dimensional mapping. This uses the form $(x\cdot y)^n$, which is called a polynomial kernel. This polynomial kernel can be used as a map to higher dimensionality in a whole bunch of different ways. For example, $(x\cdot y+1)^n$ allows us to include lower-order terms as well. To find a good value of $n$, increment it until the estimated error stops improving.

The type of kernel used opens the door to perceptrons. The radial basis function (RBF) and sigmoid kernels correspond to RBF networks (neural networks, yes!) and multilayer perceptrons with one hidden layer, respectively.

We do, however still need to compute the coefficients for the high dimensional space.

#### Support Vector Regression

Up to this point, we have been using the maximum margin hyperplane to apply to a classification problem. We can also use them for regression problems if we modify them a bit though!

Since the concept of an MMH doesn't exist in regression, we need to find out where to get our support vectors from! This is just like linear regression, really. Let's look at the linear form for simplicity.

The user defines a cutoff, $\epsilon$. The basic idea is to find a function that approximates training points by minimising error. The main difference is that all deviations up to $\epsilon$ are simply discarded. Overfitting risk is minimised by trying to maximise the flatness of the function. The error measure chosen for this is typically the absolute error instead of the squared error.

The $\epsilon$ defines the radius of a tube around the regression function. For linear regression, this tube is a cylinder. If all training points are encapsulated by the tube of width $2\epsilon$, the SVM returns the function in the middle of the tube. The choice for the value of $\epsilon$ is nontrivial. As this value increases, more and more instances are included in the tube and the perceived error reaches zero. In the extreme case, if $2\epsilon$ exceeds the range of class values, the regression line is horizontal and the mean class value is predicted.

When instances fall outside of the tube, they are called support vectors! These are then used to influence the flatness of the tube and almost act like sources of gravity, pulling the tube towards them. The aim of the SVM is to minimise prediction error, but also to maximise tube flatness. When support vectors are involved, the flatness decreases while error also decreases. An upper limit $C$ is placed to restrict the influence of each of the support vectors by limiting the value of $\alpha_i$ in the kernel equation:

$$x=b+\sum\alpha_iy_i(\text{a(i)}\cdot\text{a})^n$$

In contrast to the classification implementation, $\alpha_i$ may be negative.

#### Kernel Ridge Regression

## Alternative Techniques for Classification

## Choosing a Learning Technique
