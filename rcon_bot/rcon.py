import re

rcon_session = []
blocked_commands = []

def connect(session):
	global rcon_session
	rcon_session = session

def settings(setting, answer):
	if setting == "blocked_commads":
		global blocked_commands
		blocked_commands = [command.lower() for command in answer]

def send_command(command):
	try:
		command = command.split()
		if command[0].lower() in blocked_commands:
			return "Команда запрещена!"
		command = " ".join(command)
		answer = rcon_session.command(command)
		answer = re.sub(re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]"), "", answer)
		if not answer:
			answer = "Ваша команда выполнена!" #На случай если сервер ничего не вернет
		return answer
	except Exception as error:
		print(f"ОШИБКА | [RCON] {error}")
		exit()
