from sqlite3 import connect
from telethon import TelegramClient, events, sync, functions
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import PeerChannel
from asyncio import run
import asyncio
from Bot_Future import isOrder, Order
from Phone_Notif import send_message
from dotenv import load_dotenv
import os
from pathlib import Path
from Bot_Scrapping_Functions import contentAnalyser, performAction

# #working part

load_dotenv()
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
userName = os.getenv('TELEGRAM_USERNAME')
phone = os.getenv('TELEGRAM_PHONE')


# client = TelegramClient(userName, api_id, api_hash)

# main_channel = -1001599269755
# test_channel = -1001740948544
# test2 = -1001201186029
# test3 = -1001301686284


# @client.on(events.NewMessage(chats=[main_channel, test_channel]))
# async def handler(event):

#     print(event.raw_text)
#     action = contentAnalyser.analysis(event.raw_text)
#     performAction.performAction(action)


# client.start()
# client.run_until_disconnected()

# end working part


client = TelegramClient(userName, api_id, api_hash)


def get_channels():
    channels_id = {}
    channels_id['Main_hassoul'] = -1001599269755
    channels_id['Chat_hassoul'] = -1001740948544
    #channels_id['MaiarExchange'] = -1001201186029
    #channels_id['Other'] = -1001301686284

    return channels_id


async def listen_message():

    channels = get_channels()
    channels_id = list(channels.values())

    @client.on(events.NewMessage(chats=channels_id))
    async def handler(event):
        print(event.date)
        print(event.raw_text)
        action = contentAnalyser.analysis(event.raw_text)
        performAction.performAction(action)
    return


def main():
    try:
        with client:
            client.loop.run_until_complete(listen_message())
            client.run_until_disconnected()

    except ConnectionError:  # catches the ConnectionError and starts the connections process again

        print('ConnectionError')
        # main()


if __name__ == '__main__':
    main()
