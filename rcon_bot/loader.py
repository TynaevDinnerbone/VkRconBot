from yaml import safe_load
from mctools import RCONClient
import vk_api
import vk_bot
import rcon

with open("../config.yml", "r") as file:
	config = safe_load(file)


vk_token = config["vk_token"]
ip = config["address"]
port = config["port"]
password = config["password"]
users = config["users"]
group_enable = config["group_enable"]
prefix = config["prefix"]
blocked_commads = config["blocked"]

try:
	client = RCONClient(ip, port = port)
	if client.login(password):
		rcon.connect(client)
		rcon.settings("blocked_commads", blocked_commads)
		rcon.settings("rcon_data", [ip, port, password])
		print("ИНФО | [RCON] Успешное подключение")
	else:
		print("ОШИБКА | [RCON] Не верный пароль")
		exit()

except Exception as error:
	print(f"ОШИБКА | [RCON] {error}")
	exit()

try:
	vk_session = vk_api.VkApi(token = vk_token)
	vk_bot.connect(vk_session)
	vk_bot.settings("group_enable", group_enable)
	vk_bot.settings("allowed_users", users)
	vk_bot.settings("command_prefix", prefix)
	vk_bot.run()

except vk_api.exceptions.ApiError as error:
	print(f"ОШИБКА | [VK] {error}")
	exit()
