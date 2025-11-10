import aiml
import glob

bot = aiml.Kernel()
aiml_files = glob.glob('data/*.aiml')

for aiml_file in aiml_files:
    bot.learn(aiml_file)

while True:
    message = input("Human: ")
    if message.lower() == "quit":
        break
    else:
        response = bot.respond(message)
        print("Bot:", response)
