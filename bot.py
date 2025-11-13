import discord
import brain
import os
import dotenv
import json
import re

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.all())

dice_symbols = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
dice_emojis = [
	"<:face_1:1429054731384524871>",
	"<:face_2:1429054732730765353>",
	"<:face_3:1429054734421069936>",
	"<:face_4:1429054736388067459>",
	"<:face_5:1429054738242076702>",
	"<:face_6:1429054739546374256>"
]


@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	message_list = message.content.split()

	if message.content[0:2] == "%r":
		n_dice = int(message_list[1])
		final_result, dice_results = brain.roll_dice(n_dice)

		dice_string = ""
		for die in dice_results:
			dice_string = dice_string + dice_emojis[die-1]+ " "

		await message.channel.send(f"# {dice_string} \n# {final_result}")

	if message.content[0:2] == "%c":
		try:
			with open("clocks.json") as f:
				clocks = json.load(f)
		except json.decoder.JSONDecodeError:
			clocks = {}

		async def send_clock(clock):
			brain.circ_sectors(clocks[clock]["size"], clocks[clock]["filled"]).savefig("clock.png")
			await message.channel.send(f"## {message_list[2]}",file=discord.File('clock.png'))

		if message_list[1] in ["create", "c"]:
			if message_list[2] in clocks:
				await message.channel.send(f"Replacing clock: {message_list[2]} with {clocks[message_list[2]]["filled"]}/{clocks[message_list[2]]["size"]} segments filled")
			
			filled = int(message_list[4]) if len(message_list) >= 5 else 0
			clocks[message_list[2]] = {"size":int(message_list[3]), "filled":filled}

			await message.channel.send(f"**Created clock: {message_list[2]}**")
			await send_clock(message_list[2])

		elif message_list[1] in ["print", "p"]:
			if message_list[2] in clocks:
				await send_clock(message_list[2])
			else:
				await message.channel.send(f"clock {message_list[2]} doesn't exist.")
		
		elif message_list[1] in ["fill", "f"]: 
			if message_list[2] in clocks:
				segments_exceeded = 0
				new_fill = clocks[message_list[2]]["filled"] + int(message_list[3])
				if new_fill > clocks[message_list[2]]["size"]:
					segments_exceeded = new_fill - clocks[message_list[2]]["size"]
					new_fill = clocks[message_list[2]]["size"]
				if new_fill < 0:
					segments_exceeded = new_fill
					new_fill = 0
				clocks[message_list[2]]["filled"] = new_fill


				await send_clock(message_list[2])
				if segments_exceeded > 0:
					await message.channel.send(f"{segments_exceeded} segments exceeding full")
				if segments_exceeded < 0:
					await message.channel.send(f"{-segments_exceeded} segments bellow empty")
			else:
				await message.channel.send(f"clock {message_list[2]} doesn't exist.")	

		elif message_list[1] in ["set", "s"]: 
			if message_list[2] in clocks:
				segments_exceeded = 0
				new_fill = int(message_list[3])
				if new_fill > clocks[message_list[2]]["size"]:
					segments_exceeded = new_fill - clocks[message_list[2]]["size"]
					new_fill = clocks[message_list[2]]["size"]
				if new_fill < 0:
					segments_exceeded = new_fill
					new_fill = 0
				clocks[message_list[2]]["filled"] = new_fill

				brain.circ_sectors(clocks[message_list[2]]["size"], clocks[message_list[2]]["filled"]).savefig("clock.png")
				await message.channel.send(f"## {message_list[2]}",file=discord.File('clock.png'))
				if segments_exceeded > 0:
					await message.channel.send(f"{segments_exceeded} segments exceeding full")
				if segments_exceeded < 0:
					await message.channel.send(f"{-segments_exceeded} segments bellow empty")
			else:
				await message.channel.send(f"clock {message_list[2]} doesn't exist.")

		with open("clocks.json", "w") as f:
			json.dump(clocks, f, indent=4)
	
	if message.content[0:2] == "%g":
		try:
			with open("gambits.json") as f:
				gambits = json.load(f)
		except json.decoder.JSONDecodeError:
			gambits = {"default":3, "current":3}

		if len(message_list) == 1 or message_list[1] in ["print", "p"]:
			await message.channel.send(f"Remaining Gambits: {gambits["current"]}")

		elif message_list[1] in ["set", "s"]:
			gambits["current"] = int(message_list[2])
			await message.channel.send(f"Gambits set to {gambits["current"]}")
		
		elif message_list[1] in ["reset", "r"]:
			gambits["current"] = gambits["default"]
			await message.channel.send(f"Gambits reset to {gambits["current"]}")
		
		elif message_list[1] in ["default", "set_default", "d"]:
			gambits["default"] = int(message_list[2])
			await message.channel.send(f"Default starting gambits set to {gambits["current"]}")

		elif bool(re.match(r"[+-]?\d+$", message_list[1])):
			gambits["current"] += int(message_list[1])
			await message.channel.send(f"Remaining Gambits: {gambits["current"]}")

		with open("gambits.json", "w") as f:
			json.dump(gambits, f, indent=4)
		



client.run(TOKEN)