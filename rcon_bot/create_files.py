with open("../start.bat", "w") as file:
	file.write("@echo off\n")
	file.write("cd rcon_bot\n")
	file.write("call venv\\Scripts\\activate\n")
	file.write("python loader.py\n")
	file.write("pause")