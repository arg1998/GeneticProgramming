# Introduction
This is a very simple library for Genetic Algorithm which uses Tree-Based Genetic programming to evolve some solutions to
find answers or improve them.
its writen in Python  with the help of [GraphViz](http://www.graphviz.org/) library for rendering the result as a graph(tree).

NOTE : this is just one of my personal projects and first expirence with python, so be cool if you found a bug ;-).

and also feel free to fork it and tweak it ...
      
***
# Features
#### - Independent Fitness Function (FF) :
one of the key features is that you can implement your own FitnessFunction (or FF) completely independent to GP system.
each Individual has a variable called ```fitness``` which you can overwrite it in your FF and let the GP system handles the rest of the job.

**NOTE**: in this library, the **Higher** fitness is **Better**. so be careful about fitness calculation in your FF





#### - HyperParameter(HP)  and Online Tuning :
with the use of HyperParameters you can control the decision flow of GP system. for an example
you can tune the range of selection both in cross-over and mutation while your GP is running

**NOTE**: although there's a few of these HPs, but in the future there will be more

***

# Dependencies

the only dependency is [GraphViz](http://www.graphviz.org/) library which you can go to their website and see the installation 
manual. BUT , for the sake of simplicity, here is how you can install it on **Linux**:

first install GraphViz compiler through apt : 
```sudo apt install graphviz```

and then through python pip : 
```pip install pydot graphviz```


now you're ready to go. -_*

***

# Examples
[Here](https://github.com/arg1998/GeneticProgramming/tree/master/Problems) you can find an example of how this works.
if you're familiar with genetic programming and boolean operations, the code is simple as a NOT gate for you :-)

in this example i tried to make a XOR gate , using Only 4 NAND gate...
so here is the 18'th Generation of GP : ![alt text center](https://github.com/arg1998/GeneticProgramming/blob/master/Problems/LogicalCircuits/output/Generation%2018/Individual%206.png)


There are some notations in graphs which are :
+ G : is the current Generation number
+ F : is the Fitness Value
+ D : Depth of the Tree
+ W : Width of the Tree
+ n : Number of Nodes(both functions and terminals) in tree



***

# What's Next???
well, the next step is to **Optimize** this and make it cleaner, also im thinking adding **concurrency** to make it work parallel.
I might also solve some other famous problems with this and compare the performance.

But the main goal is to implement my own ideas and thoughts and test them.
