# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver


#### QUESTION ANSWERS ####

# General setup for answers to question 1 and question 2.
To quote from the lesson, "Constraint Propagation is all about using local constraints in a space (in the case of Sudoku, the constraints of each square) to
dramatically reduce the search space." In Sudoku, the constraints are that each row, each column, and each 'box' must each exhaust the digit space from 1 to 9.
The constraint global constraint space of the board is thus composed of local constraint spaces in each unit (a row, a column or a 'box'). Each unit likewise
consists of local constraint spaces of the given digits that remain as valid options for a given square.

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: Naked twins is a strategy for constraint propogation in sudoku. It consists of first searching a given "unit" for two squares that each have the same 2
   digits remaining as options. Since each box can only have 1 digit, we know that any valid final state will have those two digits in those two boxes.
   Thus, we can reduce the search space by removing those two digits as options from every other square int he unit.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: First, the 'diagonal' constraint must be added to the board. This simply consists of adding two units, one for each diagonal, that must each exhaust
   the digit space from one to nine. Then we use a strategy of alternating constraint propagation and depth-first search to find a solution. During
   the constraint propagation state, we use each of the Elimination, Only Choice, and Naked Twins constraint propagation strategy to reduce the state space.
   Then, when none of those strategies can further reduce the space, we find the *un-assigned* square with the fewest remaining options, assign the 'left-most'
   digit to that square, and return to constraint propagation. If during constraint propagation, any square becomes 'empty' of options, then we know that
   we can never arive at a valid solution. In such case, we return to the last square assigned via the depth first search and assign the next option.

#### END QUESTION ANSWERS ####


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.