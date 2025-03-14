from http.client import HTTPSConnection
import sys
from json import dumps
from time import sleep
from random import random

# Read config file
file = open("info.txt")
text = file.read().splitlines()

if len(sys.argv) > 1 and sys.argv[1] == "--setall" and input("Configure bot? (y/n)") == "y":
    file.close()
    file = open("info.txt", "w")
    text = []
    text.append(input("User agent: "))
    text.append(input("Discord token: "))
    text.append(input("Discord channel URL: "))
    text.append(input("Discord channel ID: "))

    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--setchannel" and input("Set channel? (y/n)") == "y":
    user_agent = text[0]
    token = text[1]
    text = text[0:2]
    file.close()
    file = open("info.txt", "w")
    text.append(input("Discord channel URL: "))
    text.append(input("Discord channel ID: "))
    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--setauth" and input("Set authentication? (y/n)") == "y":
    channelurl = text[2]
    channelid = text[3]
    text = text[2:4]
    file.close()
    file = open("info.txt", "w")
    text.insert(0, input("Discord token: "))
    text.insert(0, input("User agent: "))
    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--help":
    print("Showing help for discord-auto-message")
    print("Usage:")
    print("  'python3 bot.py'               :  Runs the autotyper. Fill in the messages and wait times.")
    print("  'python3 bot.py --setall'      :  Configure all settings.")
    print("  'python3 bot.py --setchannel'  :  Set channel to send message to. Includes Channel ID and Channel URL")
    print("  'python3 bot.py --setauth'     :  Set authentication. Includes User Token and User Agent")
    print("  'python3 bot.py --help'        :  Show help")
    exit()

if len(text) != 4:
    print("An error was found inside the user information file. Run the script with the 'Set All' flag ('python3 bot.py --setall') to reconfigure.")
    exit()

if len(sys.argv) > 1:
    exit()

header_data = {
    "content-type": "application/json",
    "user-agent": text[0],
    "authorization": text[1],
    "host": "discord.com",
    "referrer": text[2]
}

print("Messages will be sent to " + header_data["referrer"] + ".")

def get_connection():
    return HTTPSConnection("discord.com", 443)

def send_message(conn, channel_id, message_data):
    try:
        conn.request("POST", f"/api/v10/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()

        if 199 < resp.status < 300:
            print("Message sent!")
        else:
            sys.stderr.write(f"Received HTTP {resp.status}: {resp.reason}\n")

    except Exception as e:
        sys.stderr.write(f"Failed to send_message: {str(e)}\n")
        for key in header_data:
            print(key + ": " + header_data[key])

def main(messages):
    """
    Sends each message from the list sequentially.
    """
    for i, msg in enumerate(messages):
        message_data = {
            "content": msg.strip(),
            "tts": "false",
        }

        send_message(get_connection(), text[3], dumps(message_data))
        print(f"Message {i + 1}/{len(messages)} sent: {msg.strip()}")

        if i < len(messages) - 1:
            wait_time = main_wait + (random() * human_margin)
            print(f"Waiting {round(wait_time, 2)} seconds before next message...\n")
            sleep(wait_time)

if __name__ == '__main__':
    print("Enter your messages (one per line). When finished, press Ctrl+D (EOF):")
    messages = sys.stdin.read().splitlines()

    if not messages:
        print("No messages entered. Exiting.")
        exit()

    main_wait = int(input("Seconds between messages: "))
    human_margin = int(input("Human error margin: "))

    print(f"\nStarting message sequence: {len(messages)} messages will be sent.")
    main(messages)

    print("Session complete! All messages sent.")
