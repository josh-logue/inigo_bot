import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	def get_user(name):
		members = client.get_all_members()
		for member in members:
			if member.name.lower() == name.lower().replace(" ", ""):
				return client.get_user_info(member.id)

		return None

	##	This command is used by guild members to sign up to the first event of the week
	if message.content.startswith('!day1'):
		file = open('day1.txt', 'r')
		response = message.content.split('!day1')[1]
		found = False
		author = message.author
		for line in file: # will only let the user respond once			
			if format(author) == format(line.split(None, 1)[0]):
				found = True
			if found:
				break
		file.close()
		if not found:
			file = open('day1.txt', 'a')
			if response != '':
				file.write(format(message.author) + ' ' + response.upper() + '\n')
			else:
				await client.send_message(message.author, "Empty role, respond again with '!day1 [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'")
			file.close()
		else:
			await client.send_message(message.author, "Role already sent.")
		

	##  This command is used by guild members to sign up to the second event of the week
	elif message.content.startswith('!day2'):
		file = open('day2.txt', 'r')
		response = message.content.split('!day2')[1]
		found = False
		author = message.author
		for line in file: # will only let the user respond once
			if format(author) == format(line.split(None, 1)[0]):
				found = True
			if found:
				break
		file.close()	
		if not found:
			file = open('day2.txt', 'a')	
			if response != '':
				file.write(format(message.author) + ' ' + response.upper() + '\n')
			else:
				await client.send_message(message.author, "Empty role, respond again with '!day2 [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'")
			file.close()
		else:
			await client.send_message(message.author, "Role already sent.")
		
	## Used by an admin or officer to reset the two files holding the event roster; syntax is !setFile [date1] [date2]
	## Restricted from most users
	elif message.content.startswith('!setFile') and "officer" in [x.name.lower() for x in message.author.roles]:
		event1 = open('day1.txt', 'w')
		date1 = message.content.split(' ')[1]
		event1.write('Raiders signed up for ' + format(date1) + ': \n')
		event1.close()
		event2 = open('day2.txt', 'w')
		date2 = message.content.split(' ')[2]
		event2.write('Raiders signed up for ' + format(date2) + ': \n')
		event2.close()

	## Used by an admin or officer to send invites to users in the given list; syntax is !invite [date of first day in raid week]
	## Restricted from most users
	elif message.content.startswith('!invite') and "officer" in [x.name.lower() for x in message.author.roles]:
		file = open('raiders.txt', 'r')
		date = message.content.split(' ')[1]
		for line in file:
			fName = line.replace('\n', '')
			if get_user(fName) == None:
				await client.send_message(target, "Error, couldn't send invite to " + format(fName))
			else:
				target = await get_user(fName)
				await client.send_message(target, "You've been invited to the event(s) in the week of " + format(date) + ""
					"\nTo sign up for Tuesday's event respond with '!day1 [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'\n" +
					"To sign up for Thursday's event, repeat this in a seperate message but substitute '!day1' with '!day2'")
		file.close()

	## Used to private message the current event roster to sender
	elif message.content.startswith('!printlist'): #and "officer" in [x.name.lower() for x in message.author.roles]:
		if message.content.split('!printlist')[1] == ' day2':
			fName = 'day2.txt'
		else:
			fName = 'day1.txt'
			
		file = open(fName, 'r')
		for line in file:
			if line.split()[-1] == 'TANK':
				await client.send_message(message.author, line)
		file.close()

		file = open(fName, 'r')
		for line in file:
			if line.split()[-1] == 'HEAL':
				await client.send_message(message.author, line)
		file.close()

		file = open(fName, 'r')
		for line in file:
			if line.split()[-1] == 'DPS':
				await client.send_message(message.author, line)
		file.close()

	elif message.content.startswith('!delete') and "officer" in [x.name.lower() for x in message.author.roles]:
		
		fName = format(message.content.split(' ')[1]) + '.txt' 
		
		rName = message.content.split(' ')[2]
		
		file = open(fName, 'r+')
		lines = file.readlines()
		file.seek(0)
		for i in lines:
			if format(i.split(None, 1)[0]) != rName:
				file.write(i)
		file.truncate()
		file.close()


client.run('TOKEN')