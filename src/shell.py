import processor
from argparse import ArgumentParser

class RequestExit(Exception):
    pass

def shell_loop():
    while True:
        command = input("StoryScript > ")
        if command.endswith("/*"):
            while True:
                if input("... > ").endswith("*/"):
                    break
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

if __name__ == "__main__":
    parser = ArgumentParser(description="Process StoryScript statements")
    parser.add_argument("-i", "--input", help="The file you wanted to process")
    parser.add_argument(
        "--simulate-input-from-text-file",
        "-textsiminput",
        help="Simulate input using the specified file.",
    )
    parser.add_argument(
        "--release-mode", action="store_false", help="Enable release mode"
    )
    parser.add_argument("--mad-error", action="store_true", help="Enable mad error mode")
    args = parser.parse_args()

    if args.mad_error:
        errcollection = [
            # Starting paranthesis needed errors
            "InvalidSyntax: YOU NEED A PARANTHESIS AFTER A FUNCTION NAME TO CALL IT, AND YOU CAN'T PRINT FUNCTION IN StorySript",
            "InvalidSyntax: HEY YOU YOU NEED A PARENTHESIS AFTER A FUNCTION NAME DON'T BE STUPID MOST OF THE TIME OTHER PROGRAMMING LANGUAGES USE THIS RULE TOO",
            # Closing parenthesis needed errors
            "InvalidSyntax: HEY YOU NEED A PARENTHESIS AFTER AN ARGUMENT LIST DON'T BE STUPID EVERYTHING THAT HAS ITS OPENING MUST HAVE A CLOSING",
            "InvalidSyntax: INSERT ) AT THE END OF ARGUMENTS LIST YOU STUPID"
        ]
        import lexer
        from random import randint
        lexer.paren_needed: str = errcollection[randint(0, 1)]
        lexer.close_paren_needed: str = errcollection[randint(2, 3)]

    processor.STORYSCRIPT_INTERPRETER_DEBUG_MODE = args.release_mode
    if args.input:
        processor.FileProcessor().parse_file(args.input, args.simulate_input_from_text_file)
    else:
        print("// StoryScript Shell //")
        print('Use "exit ()" (Without double quotes) or Press CTRL+C to exit')

        printNone = False

        try:
            shell_loop()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt recieved. Exiting...")
        except RequestExit:
            print("Exiting requested. Exiting...")
        except Exception:  # skipcq: PYL-W0703
            from traceback import print_exc

            print_exc()
