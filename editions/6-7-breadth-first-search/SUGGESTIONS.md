> Welcome to week 6 of Programming Feedback for Advanced Beginners. In this series I review a program [sent to me by one of my readers][feedback]. I highlight the things that I like and discuss the things that I think could be better. Most of all, I suggest small and big changes that the author could make in order to bring their program up to the next level.
>
> (To receive all future PFABs as soon as they’re published, [subscribe by email][subscribe] or [follow me on Twitter][twitter]. For the chance to have your code analyzed and featured in future a PFAB, [go here][feedback]) 

This week we're going to peruse a program sent to me by Gianni Perez, a security analyst from the US of A. He says that he frequently throws together quick scripts to automate some part of attacking or defending a network, but rarely has to build and maintain large, scalable projects.

Gianni's program is an implementation of the *breadth-first search* algorithm for finding the shortest path from A to B. Breadth-first search is a staple of computer science undergraduate courses, although it's relatively rare that a real person has to implement it this outside of a university lab or an ill-conceived whiteboard interview. Nonetheless, as we'll see, doing so can still be a satisfying and educational exercise.

Don't worry if the words "computer science" or "algorithm" make you anxious. As we will see, we'll be able to make intelligent observations about Gianni's code without having to know *anything* about the internals of breadth-first search. That said, let's still spend an optional paragraph or two setting the scene.

## Breadth-first search

A more formal statement of the breadth-first search algorithm might be "find the shortest path through a *graph* from a source *vertex* to a destination *vertex*." For our purposes, a graph is a network of *vertices*, some of which are connected to each other by *edges*.

[IMG]

A variation of breadth-first search (called [*Djikstra's Algorithm*][]) is used by car and train journey-planning products that find the shortest route from A to B and show you advertisements as they do so.

To perform breadth-first search you start at the source vertex. Then you take a step to each of your source vertex's neighbors, storing a different path in your program for each different step.

In the next *iteration* through the algorithm you extend each path by one step to each new neighbor, creating and keeping track of further new paths where necessary. You repeat this process in each subsequent iteration too, stepping from the vertex at the end of each of your paths to each new neighbor that hasn't yet been touched by another path. You iterate until one of your paths steps onto your destination vertex. At this point you know for certain that you have found the shortest path between your source and destination vertices. It's possible and indeed likely that there are many other paths available between these two vertices. However, since you are tracing out every possible path simultaneously and only extending them by one hop at a time, those other paths are guaranteed to be longer.

If this doesn't quite make sense then you can either Google "breadth first search", or continue reading this post without worrying too much. We're not going to analyze whether Gianni has implemented the algorithm cleanly or even correctly (although as far as I can tell he has). Instead, we're going to analyze how his code looks from the outside, to a potential user. We'll do so by pretending that we're considering using his code as a library to perform breadth-first search in our own journey-planning project.

Let's start by discussing what it means to evaluate code from this perspective.

## How to write a useable libary

As users of Gianni's library, we only care whether the code is correct, reasonably efficient, and easy to use. We don't care at all whether the code inside it is neat or messy or well-commented or opaque, because we're never going to see any of its guts ourselves. All we're going to see are the names of the methods that the library exposes to us, and the forms of input and output that they expect.

To illustrate the difference between a useable and a useless library, here's a simple example. Which of these functionally-equivalent chart-drawing libraries would you rather work with?

Number 1:

```python
import ch

ch.do(data, None, None, None, 'x=Date|y=Sales Volume', 'YES', 5)
```

Or number 2:

```python
import charter

charter.draw_line_chart(
    data,
    x_axis_label="Date",
    y_axis_label="Sales Volume",
    show_gridlines=True,
    font_size=5)
```

Both libraries produce the same charts. Both libraries may even contain almost exactly the same code. But whereas library number 1 looks like an obfuscated nightmare to use, the second looks like a simple pleasure. The difference is in their *interfaces* - the form of their inputs and outputs.

When analyzing Gianni's code through this lens, I noted a few subtle ways in which its methods' interfaces could be made more user-friendly.

## Return values

One Gianni's most important functions is called `shortest_path`. This function takes in 3 arguments: a graph, a source vertex, and a destination vertex. As you might expect, it finds and returns the shortest path through the graph from source to destination. This is exactly the kind of function that is well-suited to being performed by a library. When writing our journey-planner product, we want to handle all of the parts of the code that are specific to our business - rendering the output maps, gathering the location data, and so on. But there's no reason for us to re-implement a core, generic computer science algorithm; this type of work is much better to outsource to a battle-tested algorithmic library.

However, from a user's perspective `shortest_path` has a substantial problem with the format in which it returns its results. Its output is a single string of the names of the vertices on the shortest path, joined together with ASCII arrows. For example, `'10->5->2-15'`. Suppose that we wanted to use this output to draw a route on a map and display it in a webpage to our user (along with lots and lots of advertisements). We'd have to split the path-string back into a list of its component vertices; a perfectly doable task, but also an annoying and unnecessary one.

I would much prefer it if `shortest_path` returned a list of the vertices on the shortest path (eg. `['10','5','2','15']`), allowing us to decide how we want to present it. The function's job is to calculate data; it shouldn't make any assumptions about how its user wants to display it.

As a rule of thumb, separate out data calculation from data formatting. Have your calculation components return their results as raw lists, dictionaries and objects, and avoid doing anything that smells like "display logic". Pass this output into a second component that knows nothing about how to calculate anything, but knows everything about to make data look good.

This applies even for code that you never intend to be used by anyone else. Separating out responsibilities for calculation and formatting allows you to completely change how your data is displayed without having to change anything about how this data produced (and vice versa).

```
+---------+
|Calculate|
+----+----+
     |
     v
+----+----+
| Format  |
+----+----+
     |
     v
+----+----+
| Output  |
+---------+
```

I've sketched out how I would change `shortest_path` and the way in which it is used [on GitHub][].

## A second example

I also spotted an almost identical problem in a function called `bfs_traversal`. This function's job is to find and return the shortest path from a source vertex to *every* other vertex in the graph. The original version of this function returned its output in a fancy display format called a `PrettyTable`. I don't know anything about `PrettyTable` - from some quick Googling it looks like it's a library that can be used to print cleanly structured tables to the terminal. But as a user of Gianni's breadth-first search library I don't want to have to learn anything about `PrettyTable`. I just want to receive the data that I asked for in a raw, usable structure, and then I'll take care of formatting and outputting it as I see fit.

Looking at the code for `bfs_traversal`, I noticed that it already stores all of its interim data in exactly the kind of raw, dictionary structure that I'd like to get back from it. The only problem is that it then tries to be too helpful and do my formatting for me. Fixing this simply requires the removal of the `PrettyTable` code.

This code:

```
def bfs_traversal(graph, source_vertex):
    distances = {}
    # <do a load of calculations>
    return convert_to_pretty_table(distances)
```

should become this code:

```
def bfs_traversal(graph, source_vertex):
    distances = {}
    # <do a load of calculations>
    return distances
```

## Conclusion

We've seen how we can analyze the exterior of a piece code from a user's perspective, without having to know anything about what goes on inside. Similarly, we can critique the user interfaces of complex gadgets without needing to know how they work. We might not care to learn how to build a smartphone, but we can still give useful feedback on how one feels to use.
