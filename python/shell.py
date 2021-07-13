import processor
from sys import argv

if __name__ == "__main__":
    is_in_named_arguments = False
    input_file = ""
    textfiletosimulate = None
    # Parse flags and named command line arguments
    for i in argv:
        if i in ("-i", "--input"):
            is_in_named_arguments = "-i"
            continue
        if i in ("--simulate-input-from-text-file", "-textsiminput"):
            is_in_named_arguments = "-textsiminput"
            continue
        if i == "--release-mode":
            processor.STORYSCRIPT_INTERPRETER_DEBUG_MODE = False
        elif i == "--debug-mode":
            processor.STORYSCRIPT_INTERPRETER_DEBUG_MODE = True
        if is_in_named_arguments:
            if is_in_named_arguments == "-i":
                input_file = i
            elif is_in_named_arguments == "-textsiminput":
                textfiletosimulate = i
            is_in_named_arguments = False
    if input_file:
        processor.parse_file(input_file, textfiletosimulate)
    else:

        class RequestExit(Exception):
            pass

        print("// StoryScript Shell //")
        print('Use "exit ()" (Without double quotes) or Press CTRL+C to exit')

        printNone = False

        try:
            while True:
                command = input("StoryScript > ")
                if command.startswith("exit ("):
                    raise RequestExit
                if command.startswith("#define"):
                    scommand = command.split()
                    try:
                        if (
                            scommand[1] == "shellSettings"
                            and scommand[2] == "printWhenReturnNone"
                        ):
                            if scommand[3] == "true":
                                printNone = True
                                continue
                            if scommand[3] == "false":
                                printNone = False
                                continue
                    except IndexError:
                        print(
                            "InvalidSyntax: The Option you wanted to settings is required."
                        )
                out = processor.execute(command)
                if not printNone:
                    if out is not None:
                        print(out)
                else:
                    print(out)
        except KeyboardInterrupt:
            print("\nKeyboard interrupt recieved. Exiting...")
        except RequestExit:
            print("Exiting requested. Exiting...")
        except Exception:  # skipcq: PYL-W0703
            from traceback import print_exc

            print_exc()
