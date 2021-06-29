# StoryScript

![StoryScript Logo](https://github.com/lines-of-codes/StoryScript/blob/be67a0b872783b78378dc3ac0969fb1111cb3e0f/StoryScript.png)

![Issues](https://img.shields.io/github/issues/lines-of-codes/StoryScript) ![Forks](https://img.shields.io/github/forks/lines-of-codes/StoryScript) ![Stars](https://img.shields.io/github/stars/lines-of-codes/StoryScript) ![License](https://img.shields.io/github/license/lines-of-codes/StoryScript) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=StoryScriptorg_StoryScript&metric=alert_status)](https://sonarcloud.io/dashboard?id=StoryScriptorg_StoryScript) [![Join the chat at https://gitter.im/StoryScripting/community](https://badges.gitter.im/StoryScripting/community.svg)](https://gitter.im/StoryScripting/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

StoryScript is a \(mainly\) interpreted language

## How to install

First, Download the Source code. At the time of writing, I don't have any complete releases yet.

So, Just download the source code from Main branch. \(And wish there is no bug\)

**And also, You need Python installed**

Then you can just `python shell.py`, Then it will launch the shell, And you can use the language.

And to execute a file, Use `python processor.py [filename]` and replace `[filename]` with the real File name. For example:

```text
python processor.py main.sts
```

Note: If you are looking for C Transpiler source, It has been moved [here](https://github.com/StoryScriptorg/StoryScript/tree/CTranspiler)

### Required Packages

#### Interpreter \(REPL\)

There are no required Packages for the Interpreter \(REPL\) version.

#### C Transpiler

To use C transpiler properly, You'll need a package called `tqdm` installed. Just type this \(If you've installed Python properly\):

```text
pip install tqdm
```

In your command line then you have it! Or If it throws an Error saying that `pip` does not exist, Then try:

```text
python -m pip install tqdm
```

If it throws an Error saying that `python` does not exist, Then python executable is not in your Environment path.

## How to use the Language

Please visit the [Wiki](https://github.com/lines-of-codes/StoryScript/wiki) for more info about how to use StoryScript.

