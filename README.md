# FIGURE
Compilers Project

### Requirements

- You need to install (In case you don't have it) [Python](https://www.python.org/), from version 3 onwards.
- Also you need the library Tkinter for graph. You can installed with the next command:
- `$ sudo apt-get install python3-tk `

### Compile

For compiling and executing you need to type the next command in terminal:

- `$ python3 main.py <your_file_name.fig> `

### Getting Started
You have three data types in FIGURE:
* int
* float
* string

To declare a function:
* `function <void/type> name(params,...) { }`

	Example:
	`function  int suma(int a , int b) { }`


In each program you should always have your **mainF** being this the main function.

```
program firstProgram;

mainF{
    <your code>
}
```
### Graph

FIGURE allows you to create diverse shapes like circles or squares. You could try something like this. !start creating!

```
program circles;

string colors[3] = ["Red","Blue","Yellow"];


mainF{
    int i = 1;
    int pos;
    pointer_size(3);
    speed("fast");

    for(i:3){
        pointer_color(colors[i]);
        circle(i*40);
        up;
        pos = -1 * i;
        pos = pos * 10;
        position(0,pos);
        down;
    }

    exit;
}
```