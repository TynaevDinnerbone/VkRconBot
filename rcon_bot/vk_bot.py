import vk_api
import rcon
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = []
allowed_users = []
enable_group = False
command_prefix = "/"

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
	if setting == "command_prefix":
		global command_prefix
		command_prefix = answer

def execute(command):
	cmd = rcon.send_command(command)
	return cmd

def handle_message(event):
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
		vk = vk_session.get_api()
		msg = event.text
		if msg[0] != command_prefix:
			return
		if msg[1:] == "id":
			vk.messages.send(
				peer_id = event.peer_id,
				message = "Ваш цифровой ID: " + str(event.user_id),
				random_id = 0
			)
			return
		if not(event.user_id in allowed_users):
			return
		response = vk.messages.getConversationsById(peer_ids = event.peer_id)
		type = response["items"][0]["peer"]["type"]
		if type == "chat":
			if not(enable_group):
				return
		cmd = execute(msg[1:])
		message_parts = [cmd[i:i+4000] for i in range(0, len(cmd), 4000)]
		for part in message_parts:
			vk.messages.send(
				peer_id = event.peer_id,
				message = part,
				random_id = 0
			)

def run():
	longpoll = VkLongPoll(vk_session)
	print("ИНФО | [VK] Успешное подключение")
	for event in longpoll.listen():
		handle_message(event)
