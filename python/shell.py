import processor

print("// StoryScript Shell //")

try:
	while True:
		command = input("StoryScript > ")
		print(processor.execute(command))
except KeyboardInterrupt:
	print("Keyboard interrupt recieved. Exiting...")
except Exception:
	from traceback import print_exc
	print_exc()