import vk_api
import rcon
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = []
allowed_users = []
enable_group = False
command_symbol = "/"

def connect(session):
	global vk_session
	vk_session = session

def settings(setting, answer):
	if setting == "allowed_users":
		global allowed_users
		allowed_users = answer
	if setting == "group_enable":
		global enable_group
		enable_group = answer
	if setting == "command_symbol":
		global command_symbol
		command_symbol = answer

def execute(command):
	cmd = rcon.send_command(command)
	if not cmd:
		cmd = "Ваша команда выполнена!" #На случай если RCON ничего не вернет
	return cmd

def handle_message(event):
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
		if not(event.user_id in allowed_users):
			return
		vk = vk_session.get_api()
		response = vk.messages.getConversationsById(peer_ids = event.peer_id)
		msg = event.text
		type = response["items"][0]["peer"]["type"]
		if type == "user":
			cmd = execute(msg)
			vk.messages.send(
				user_id = event.user_id,
				message = cmd,
				random_id = 0
			)
			return
		else:
			if not(enable_group):
				return
			if msg[0] != command_symbol:
				return
			cmd = execute(msg[1:])
			vk.messages.send(
				peer_id = event.peer_id,
				message = cmd,
				random_id = 0
			)

def run():
	longpoll = VkLongPoll(vk_session)
	print("ИНФО | [VK] Успешное подключение")
	for event in longpoll.listen():
		handle_message(event)