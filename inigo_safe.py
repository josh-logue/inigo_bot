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

	## The !day1 and !day2 commands are legacy and have been merged into the !day command
	
	##	This command is used by guild members to sign up to the first event of the week
	# if message.content.startswith('!day1'):
	# 	file = open('day1.txt', 'r')
	# 	response = message.content.split('!day1')[1]
	# 	found = False
	# 	author = message.author
	# 	for line in file: # will only let the user respond once			
	# 		if format(author) == format(line.split(None, 1)[0]):
	# 			found = True
	# 		if found:
	# 			break
	# 	file.close()
	# 	if not found:
	# 		file = open('day1.txt', 'a')
	# 		if response != '':
	# 			file.write(format(message.author) + ' ' + response.upper() + '\n')
	# 		else:
	# 			await client.send_message(message.author, "Empty role, respond again with '!day1 [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'")
	# 		file.close()
	# 	else:
	# 		await client.send_message(message.author, "Role already sent.")
		

	# ##  This command is used by guild members to sign up to the second event of the week
	# elif message.content.startswith('!day2'):
	# 	file = open('day2.txt', 'r')
	# 	response = message.content.split('!day2')[1]
	# 	found = False
	# 	author = message.author
	# 	for line in file: # will only let the user respond once
	# 		if format(author) == format(line.split(None, 1)[0]):
	# 			found = True
	# 		if found:
	# 			break
	# 	file.close()	
	# 	if not found:
	# 		file = open('day2.txt', 'a')	
	# 		if response != '':
	# 			file.write(format(message.author) + ' ' + response.upper() + '\n')
	# 		else:
	# 			await client.send_message(message.author, "Empty role, respond again with '!day2 [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'")
	# 		file.close()
	# 	else:
	# 		await client.send_message(message.author, "Role already sent.")

	if message.content.startswith('!day'):
		day = format(message.content.split(None, 1)[0])
		fName = day.replace('!', '') + '.txt'
		
		if fName == 'day1.txt' or fName == 'day2.txt':
			file = open(fName, 'r')
			response = message.content.split(day)[1]
			found = False
			author = message.author
			for line in file: # will only let the user respond once			
				if format(author) == format(line.split(None, 1)[0]):
					found = True
				if found:
					break
			file.close() 
			if not found:
				file = open(fName, 'a')
				if response != '':
					file.write(format(message.author) + ' ' + response.upper() + '\n')
					await client.send_message(message.author, "Signed up successfully!")
				else:
					await client.send_message(message.author, "Empty role, respond again with '![day1/day2] [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'")
			else:
				await client.send_message(message.author, "Role already sent.")
			file.close()

	if message.content.startswith('!week'):
		response = message.content.split('!week ')[1]
		found = False
		author = message.author
		file = open('day1.txt', 'r')
		for line in file: # will only let the user respond once			
				if format(author) == format(line.split(None, 1)[0]):
					found = True
				if found:
					break
		if not found:
				if response != '':
					file = open('day1.txt', 'a')
					file.write(format(author) + ' ' + response.upper() + '\n')
					file.close()
					file = open('day2.txt', 'a')
					file.write(format(author) + ' ' + response.upper() + '\n')
					file.close()
					await client.send_message(author, "Signed up successfully!")
				else:
					await client.send_message(author, "Empty role, respond again with '!week [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'")
		else:
			await client.send_message(message.author, "Role already sent.")
		file.close()
		
	## Used by an admin or officer to reset the two files holding the event roster; syntax is !setFile [date1] [date2]
	## Restricted from most users message.content.startswith('!setFile') and "@officer" in [x.name.lower() for x in message.author.roles]:
	elif message.content.startswith('!setFile') and "@officer" in [x.name.lower() for x in message.author.roles]:	
		event1 = open('day1.txt', 'w')
		date1 = message.content.split(' ')[1]
		event1.write('Raiders signed up for ' + format(date1) + ': \n')
		event1.close()
		event2 = open('day2.txt', 'w')
		date2 = message.content.split(' ')[2]
		event2.write('Raiders signed up for ' + format(date2) + ': \n')
		event2.close()



	## Used to private message the current event roster to sender
	elif message.content.startswith('!printlist'): #and "officer" in [x.name.lower() for x in message.author.roles]:
		if message.content.split('!printlist')[1] == ' day2':
			fName = 'day2.txt'
		else:
			fName = 'day1.txt'
			
		file = open(fName, 'r')
		line = file.readline()
		await client.send_message(message.author, line)
		for line in file:
			if line.split()[-1] == 'TANK':
				await client.send_message(message.author, line)
		file.seek(0)
		
		for line in file:
			if line.split()[-1] == 'HEAL':
				await client.send_message(message.author, line)
		file.seek(0)
		
		for line in file:
			if line.split()[-1] == 'DPS':
				await client.send_message(message.author, line)
		file.seek(0)
		
		for line in file:
			if line.split()[-1] != 'HEAL' and line.split()[-1] != 'DPS' and line.split()[-1] != 'TANK' and line.split()[0] != 'Raiders':
				await client.send_message(message.author, line)
		file.close()

		

	elif message.content.startswith('!delete'): # and "officer" in [x.name.lower() for x in message.author.roles]:
		rName = format(message.author)

		if message.content.split(' ')[1] == 'week':
			file = open('day1.txt', 'r+')
			lines = file.readlines()
			file.seek(0)
			for i in lines:
				if format(i.split(None, 1)[0]) != rName:
					file.write(i)
			file.truncate()
			file.close()
			file = open('day2.txt', 'r+')
			lines = file.readlines()
			file.seek(0)
			for i in lines:
				if format(i.split(None, 1)[0]) != rName:
					file.write(i)
			file.truncate()
			file.close()

		else:
			fName = format(message.content.split(' ')[1]) + '.txt' 
		
			
		
			print(rName)
			file = open(fName, 'r+')
			lines = file.readlines()
			file.seek(0)
			for i in lines:
				if format(i.split(None, 1)[0]) != rName:
					file.write(i)
			file.truncate()
			file.close()

	## Used by an admin or officer to send invites to users in the given list; syntax is !invite [date of first day in raid week]
	## Restricted from most users
	elif message.content.startswith('!invite') and "@officer" in [x.name.lower() for x in message.author.roles]:
		file = open('raiders.txt', 'r')
		date = message.content.split(' ')[1]
		for line in file:
			fName = line.replace('\n', '')
			if get_user(fName) == None:
				await client.send_message(message.author, "Error, couldn't send invite to " + format(fName))
			else:
				target = await get_user(fName)
				await client.send_message(target, "You've been invited to the event(s) in the week of " + format(date) + ""
					"\nTo sign up for both days, respond with !week [Character Name] [DPS/HEAL/TANK/UNAVAILABLE]" +
					"\nOtherwise, to sign up for individual days, respond with '!day1 [Character Name] [DPS/HEAL/TANK/UNAVAILABLE] for Tuesday\n" +
					"and repeat this in a seperate message but substitute '!day1' with '!day2' for Thursday")
		file.close()

	elif message.content.startswith('!surveyout') and "@officer" in [x.name.lower() for x in message.author.roles]:

		raiders = open('raiders.txt', 'r')
		content = message.content.split('!surveyout ')[1]
		for line in raiders:
			fName = line.replace('\n', '')
			if get_user(fName) == None:
				await client.send_message(message.author, "Error, couldn't send invite to " + format(fName))
			else:
				target = await get_user(fName)
				await client.send_message(target, content)
	
		raiders.close()
	
	elif message.content.startswith('!survey'):
		out = open('survey.txt', 'r')
		response = message.content.split('!survey ')[1]
		author = message.author
		found = False
		for line in out: # will only let the user respond once			
			if format(author) == format(line.split(None, 1)[0]):
				found = True
			if found:
				break
		out.close()

		if not found:
			out = open('survey.txt', 'a')
			if response != '':
				out.write(format(author) + ' ' + response + '\n')
				await client.send_message(author, "Response registered.")
			else:
				await client.send_message(author, "Empty response, reply again with a response.")
			out.close()
		else:
			await client.send_message(message.author, "Response already sent")

	elif message.content.startswith('!sPrint'):
		file = open('survey.txt', 'r')
		for line in file:
				await client.send_message(message.author, line)
		file.close()
			




client.run('TOKEN')