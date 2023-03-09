import re
from mctools import RCONClient

rcon_session = []
rcon_data = []
blocked_commands = []

def connect(session):
	global rcon_session
	rcon_session = session

def settings(setting, answer):
	if setting == "blocked_commads":
		global blocked_commands
		blocked_commands = [command.lower() for command in answer]
	if setting == "rcon_data":
		global rcon_data
		rcon_data = answer

def reconnect():
	ip = rcon_data[0]
	port = rcon_data[1]
	password = rcon_data[2]
	try:
		client = RCONClient(ip, port = port)
		if client.login(password):
			connect(client)
			return True
		else:
			return "Ошибка аутентификации, не верный пароль RCON"
	except Exception as error:
		return error


def send_command(command):
	try:
		command = command.split()
		if command[0].lower() in blocked_commands:
			return "Команда запрещена!"
		command = " ".join(command)
		if command == "rcon-reconnect":
			session = reconnect()
			if session == True:
				return "Успешное переподключение к RCON"
			return f"Переподключение не удался\nОшибка: {session}"
		answer = rcon_session.command(command)
		answer = re.sub(re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]"), "", answer)
		if not answer:
			answer = "Ваша команда выполнена!" #На случай если сервер ничего не вернет
		return answer
	except Exception as error:
		return f"Произошла ошибка при выполнении команды!\nОшибка: {error}\nВведите команду \"rcon-reconnect\" для переподключения к RCON"
