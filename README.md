# StoryScript

![StoryScript Logo](https://github.com/lines-of-codes/StoryScript/blob/be67a0b872783b78378dc3ac0969fb1111cb3e0f/StoryScript.png)

![Issues](https://img.shields.io/github/issues/lines-of-codes/StoryScript)
![Forks](https://img.shields.io/github/forks/lines-of-codes/StoryScript)
![Stars](https://img.shields.io/github/stars/lines-of-codes/StoryScript)
![License](https://img.shields.io/github/license/lines-of-codes/StoryScript)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=StoryScriptorg_StoryScript&metric=alert_status)](https://sonarcloud.io/dashboard?id=StoryScriptorg_StoryScript)
[![Join the chat at https://gitter.im/StoryScripting/community](https://badges.gitter.im/StoryScripting/community.svg)](https://gitter.im/StoryScripting/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![codecov](https://codecov.io/gh/StoryScriptorg/StoryScript/branch/main/graph/badge.svg?token=BWC521L4X5)](https://codecov.io/gh/StoryScriptorg/StoryScript)
[![Maintainability](https://api.codeclimate.com/v1/badges/808f1a45d594387472eb/maintainability)](https://codeclimate.com/github/StoryScriptorg/StoryScript/maintainability)
[![DeepSource](https://deepsource.io/gh/StoryScriptorg/StoryScript.svg/?label=active+issues&show_trend=true&token=5Ju5wGtlKSj6HZrmU7HnIA72)](https://deepsource.io/gh/StoryScriptorg/StoryScript/?ref=repository-badge)
[![Discord](https://img.shields.io/discord/879964500151914526)](https://discord.gg/2ymyB4n6Ad)

StoryScript is an interpreted programming language that is made to being easy to learn.

## How to install
You can install StoryScript from PyPi using `pip`

```
pip install storyscript # Install storyscript
pip install --upgrade storyscript # Update storyscript if you already have it
```

## Repository archival
I'm archiving this repository soon due to the fact I don't have the interest in developing this project further in Python. Maybe I'll comeback in the future with this project but written in another programming language? or maybe that day would never come?

If anyone wants to continue this project, I'd recommend that you don't fork this repository as the structure is hell.
but I won't stop you from doing so.

### Syntax I have planned so far
This will include the syntax I've planned, both implemented and not implemented.
so you could use this as a reference for StoryScript's syntax if you're gonna recreate StoryScript.

```
// Comments
/*
Multiline comments
*/

// Variables
Type a
Type a = null

// creating a new instance of a class
Type a = new type()
Type<int> a = new Type<int>()

// Imports
import Something from "./something.sts"
import FromPackage from "PackageName"

// An anonymous function
// When storing an anonymous function in a variable, the type of the variable should be Action<return type>
// For example:
Action<int> anonymousFunction = (int a, int b) => return a + b;
Action<void> anotherAnonymousFunction = () => {
    // multiline anonymous function
    print("weeeeeeee")
}

// Functions
void function(string name) {
    print("Hello, " + name)
}

// Classes
class A {
    int field;
    int property { get; private set; }
    
    void method();
}

// structs
struct Struct {
    int field;
}
```

### Code style in StoryScript
Classes and Structs should be in PascalCase

Variables and Functions should be in camelCase

Built-in types (including: int, float, dynamic, string) should also be in camelCase

## Download lastest code from main

You can just download or `git clone` the source code from Main branch. \(And wish there is no bug\)

Firstly, remember that **you need Python installed.**

I recommended at least Python 3.8 to make sure it is working.

Due to Pull request #27, You can now easily setup StoryScript by doing:
```bash
python setup.py install
```

Note: If you are looking for C Transpiler source, It has been moved [here](https://github.com/StoryScriptorg/StoryScript-CTranspiler/)

### Required Packages
Required packages:
- Numpy
- Colorama

These are required packages for StoryScript, You can setup them manually or install through the setup script.

Optional:
- PyInstrument (Used for benchmarking)

## Usage
You can either `python -m storyscript`, or `storyscript` (if the Python program installation is on your PATH), Then it will launch the shell, And you can use the language.
All the examples listed below should work with both methods.

And to execute a file, Use `storyscript -i [filename]` and replace `[filename]` with the real file name. For example:

```text
storyscript -i main.sts
```

## How to use the Language

Please visit the [Wiki](https://github.com/StoryScriptOrg/StoryScript/wiki) for more info about how to use StoryScript. 

Or if you would rather want a tutorial, you could try the free [StoryScript course](https://github.com/StoryScriptOrg/StoryScriptCourse).
