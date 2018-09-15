---
title: "Bacon Solver With Breadth-First Search"
date: "2018-09-15 14:14:34"
excerpt: A simple application of graph search algorithms
header:
  teaser: assets/img/stock-photos/bigs-HOLLYWOOD-sign-with-flowers-in-foreground-Los-Angeles-CA-e1-Large.png
  overlay_image: assets/img/stock-photos/bigs-HOLLYWOOD-sign-with-flowers-in-foreground-Los-Angeles-CA-e1-Large.png
  overlay_filter: 0.5
classes: wide
categories:
- software
tags:
- python
- data structures
- algorithms
---


## Introduction

In this project, I implement and apply the breadth first search algorithm to a classic problem of finding an actor's Bacon umber. If you are not familiar with this game, then I forgive you and will now explain the game. The idea for it may have come from an interview with *Premiere* magazine when Kevin Bacon stated that "he had worked with everybody in Hollywood or someone who’s worked with them." Hence the game is to find the shortest connection between Kevin Bacon and a given actor. Kevin Bacon is the only person with a Bacon number of 0, and every person that has been in the same film as Kevin Bacon has a Bacon number of 1. An actor that has never been in a film with Kevin Bacon, but has worked with someone with a Bacon number of 1 will have Bacon number of 2. So finding an actor's Bacon number is as simple as finding the length of the shortest connecting path between Kevin Bacon and that actor.

![Kevin Bacon](https://upload.wikimedia.org/wikipedia/commons/d/d2/Kevin_Bacon.jpg)

## Implementation Details
The Internert Movie Database (IMDb) is the source of data used to make the graph. There are two options for how to create the graph. Both have advantages and drawbacks which I will briefly explain. In the end I chose option 2.
#### Option 1: Only actors are vertices
This is the first implementation that comes to mind. We could initialize all of the actors as nodes. Then to create the edges, we find all of the actors that participated in a given movie and create all of the edges to make that set of actors fully connected. This has the advantage of being intuitive. And finding the Bacon number is just a breadth first search and nothing more. However, making a fully connected graph for all of the actors in a given film is an inefficient use of memory. The number of vertices is already quite large, and the number of edges grows approximately as $$O(kn^2)$$ where $$k$$ is the number of films and $$n$$ is the average number of actors in a film. Furthermore, we would have to consider what happens when actors are connected through multiple films.

![Graph of actors](https://www.cs.dartmouth.edu/~cbk/classes/10/16fall/hws/PS-4/test-graph.png)

#### Option 2: Actors and films are vertices
To reduce the spatial complexity we can instead create connections between actors and the films they were in. In this method, actors are never directly connected to other actors, but only indrectly through movies. This cuts down the spatial complexity to about $$O(kn)$$. But we now have extra steps for calculating the Kevin Bacon number. After finding the shortest path length, we must then remove the films between them. Additionally, the longer path means we have increased the computation time for each Bacon number calculation. But neither of these drawbacks is a significant difficulty. Since a movie will appear on every other vertice in the path, it is trivial to calculate a Bacon number based on the path length. And since we expect this to be a strongly connected graph anyway, the longer path lengths are not a huge concern. Therefore this is the preferred method since it saves on memory without significant drawbacks.

![Graph of actors and films](https://www.cs.oberlin.edu/~asharp/cs151/labs/lab10/imdb.png)

##### Side Note
The implementation here is far from optimal. The best option is to calculate and save the Bacon number for all of the actors, possibly using Djikstra's algorithm. But that sort of detracts from the goal of this project, which is focusing on the breadth-first search algorithm.

## The Product
I am working on making this interactive. But for now, here are some quick results.


```python
from IPython.display import Markdown,display
from bfs_kbacon import BaconSolver
mysolver = BaconSolver()
```


```python
names = ["Bacon, Kevin", "Pitt, Brad", "Ford, Harrison", "Radcliffe, Daniel",
         "Hooda, Randeep", "Dujardin, Jean", "Medina, Sam", "Johnson, Corey",
         "Bronfman, Hannah", "Alexander, Nick"]

for name in names:
    display(Markdown("### {}".format(name)))
    print("Bacon Number: {}".format(mysolver.bacon_number(name)))
    print("Path {}".format(mysolver.path_to_bacon(name)))

```


### Bacon, Kevin


    Bacon Number: 0
    Path ['Bacon, Kevin']



### Pitt, Brad


    Bacon Number: 2
    Path ['Pitt, Brad', '12 Years a Slave', 'Fassbender, Michael', 'X-Men: First Class', 'Bacon, Kevin']



### Ford, Harrison


    Bacon Number: 2
    Path ['Ford, Harrison', 'Cowboys & Aliens', 'Huss, Toby', 'R.I.P.D.', 'Bacon, Kevin']



### Radcliffe, Daniel


    Bacon Number: 2
    Path ['Radcliffe, Daniel', 'Harry Potter and the Deathly Hallows: Part 2', 'Hurt, John', "Jayne Mansfield's Car", 'Bacon, Kevin']



### Hooda, Randeep


    Bacon Number: 6
    Path ['Hooda, Randeep', 'Jannat 2', 'Hashmi, Emraan', 'Raaz 3: The Third Dimension', 'Basu, Bipasha', 'Dum Maaro Dum', 'Sam', 'Beneath the Darkness', 'Banfield, Cameron', 'The Lucky One', 'Montgomery, Ritchie', "Jayne Mansfield's Car", 'Bacon, Kevin']



### Dujardin, Jean


    Bacon Number: 3
    Path ['Dujardin, Jean', 'The Artist', 'Tobin, John H.', 'The Master', 'Skomo, Matthew', 'X-Men: First Class', 'Bacon, Kevin']



### Medina, Sam


    Bacon Number: 2
    Path ['Medina, Sam', 'Puncture', 'Slemp, Morgane', 'R.I.P.D.', 'Bacon, Kevin']



### Johnson, Corey


    Bacon Number: 1
    Path ['Johnson, Corey', 'X-Men: First Class', 'Bacon, Kevin']



### Bronfman, Hannah


    Bacon Number: 4
    Path ['Bronfman, Hannah', 'American Milkshake', 'Fitzpatrick, Leo', 'Cold Comes the Night', 'Cranston, Bryan', 'Total Recall', 'Slemp, Morgane', 'R.I.P.D.', 'Bacon, Kevin']



### Alexander, Nick


    Bacon Number: 5
    Path ['Alexander, Nick', 'Extinction: The G.M.O. Chronicles', 'Bähr, Luise', 'What a Man', 'Aleardi, Pasquale', 'Resident Evil: Retribution', 'Li, Bingbing', 'Snow Flower and the Secret Fan', 'Jackman, Hugh', 'X-Men: First Class', 'Bacon, Kevin']


## Results
It works!
