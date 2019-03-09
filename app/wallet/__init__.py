import os

from app.chatfunc import send_msg, send_img

from .wallet import *

mychat = os.environ['mychat']
ledgeracc = btc_xpub(xpub=os.environ['xpub'])
bitmexacc = bitmex_account(api_key=os.environ['bitmex_key'], api_secret=os.environ['bitmex_sec'])
krakenacc = kraken_account(api_key=os.environ['kraken_key'], api_secret=os.environ['kraken_sec'])
eosacc = eos_account(accname='shortestpath')
eos_oldacc = eos_account(accname='gqytaojvgmge')
ethacc = eth_address(pubkey=os.environ['eth_pub'])
bittrexacc = bittrex_account(api_key=os.environ['bittrex_key'], api_secret=os.environ['bittrex_sec'])
w = Wallet(ledgeracc, bitmexacc, ethacc, krakenacc, eosacc, bittrexacc, eos_oldacc)

def process_msg(chat_id, msg):
    if chat_id != float(mychat):
        send_msg(chat_id, 'Unknown user.')
        return

    if 'text' in msg:
        #txt = msg['text'].lower().split(' ')
        #if txt[0] in accounts:
        #    send_msg(chat_id, txt[0].upper() + ': ' + str(accounts[txt[0]]))
        txt = msg['text'].lower()
        if txt == 'btc':
            send_msg(chat_id, str(w.total_btc()))
        elif txt == 'eur':
            send_msg(chat_id, str(w.total_curr('EUR')))
