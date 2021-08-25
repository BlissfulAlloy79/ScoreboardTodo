import time
import json
from mcdreforged.api.all import *

PLUGIN_METADATA = {
	'id': 'todo',
	'version': '1.0.0',
	'name': 'ScoreboardTodolist',  # RText component is allowed
	'description': 'use scoreboard as todo list',  # RText component is allowed
	'author': 'BlissfulAlloy79',
	'link': '',
	'dependencies': {
		'mcdreforged': '>=0.9.0',
	}
}

todo_list = []
loc = './config/todolist.json'
msg = '''
§b!!todo§r show this message
§b!!todo show§r show todo list
§b!!todo hide§r hide todo list
§b!!todo add§r add a task in todo list
§b!!todo remove§r remove a task in todo list
'''


def initialize(server):
	with open(loc, 'r') as f:
		items = json.load(f)
		for i in items:
			todo_list.append(i)


def reload(server):
	server.execute('scoreboard objectives remove todo')
	server.execute('scoreboard objectives add todo dummy {"text": "§6§l§o=====[TODO]=====§r"}')
	showList(server)
	for i in todo_list:
		server.execute('scoreboard players add ' + str(i) + ' todo ' + str(todo_list.index(i)))
	with open(loc, 'w') as w:
		json.dump(todo_list, w)


def showList(server):
	server.execute('scoreboard objectives setdisplay sidebar todo')


def hideList(server):
	server.execute('scoreboard objectives setdisplay sidebar')


def addList(server, item):
	if item not in todo_list:
		todo_list.append(item)
		server.say(todo_list)
		reload(server)
	else:
		server.say('§c§l[WARN]§ritem already in list!')


def removeList(server, item):
	if item in todo_list:
		todo_list.remove(item)
		server.say(todo_list)
		reload(server)
	else:
		server.say('§c§l[WARN]§ritem not in list!')


def on_load(server: ServerInterface, old):
	server.register_help_message('!!todo', '服务器任务列表')
	time.sleep(0.1)
	initialize(server)


def on_info(server, info):
	args = info.content.split(' ')
	if args[0] == '!!todo':
		if len(args) == 1:
			server.say(msg)
		if len(args) >= 2:
			if args[1] == 'show':
				showList(server)
				server.say('shows the todolist')
			if args[1] == 'hide':
				hideList(server)
				server.say('hidden the todolist')
			if args[1] == 'add':
				addList(server, args[2])
			if args[1] == 'remove':
				removeList(server, args[2])
