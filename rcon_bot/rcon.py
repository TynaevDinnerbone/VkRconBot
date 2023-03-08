import re

rcon_session = []

def connect(session):
	global rcon_session
	rcon_session = session

def send_command(command):
	try:
		answer = rcon_session.command(command)
		answer = re.sub(re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]"), "", answer)
		return answer
	except Exception as error:
		print(f"ОШИБКА | [RCON] {error}")
		exit()
