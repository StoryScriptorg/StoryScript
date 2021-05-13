import processor

class RequestExit(Exception):
	pass

print("// StoryScript Shell //")
print("Use \"exit()\" (Without double quotes) or Press CTRL+C to exit")

try:
	while True:
		command = input("StoryScript > ")
		if(command == "exit()"): raise RequestExit
		print(processor.execute(command))
except KeyboardInterrupt:
	print("\nKeyboard interrupt recieved. Exiting...")
except RequestExit:
	print("Exiting requested. Exiting...")
except Exception:
	from traceback import print_exc
	print_exc()