""" How to get Telegram APP ID & API HASH
May 27, 2020
The Easy way
1. Go to @usetgsbot
2. Send /start
3. Send your Telegram phone number in format +91984175xxxx
4. You received a code on @telegram copy it and paste it on @usetgsbot
5. Bot sends your API I'd & HASH

The Legacy way
1. Go to my.telegram.org , if not accessible than use any VPN
2. Enter Telegram phone number in format +918457345497
3. Enter the received code on @telegram
4. Click on Create Application
5. Enter any name and nickname.
6. Select other and leave discription empty and proceed.
7. You will get your APP ID & HASH
Credits
© Adnan Ahmad  """

""" Ottenere le chiavi API di Bitly.
1. Vai sul sito di Bitly: Visita il sito ufficiale di Bitly all'indirizzo https://bitly.com/ e 
fai clic sul pulsante "Sign Up" o "Registrati" per creare un nuovo account.
2. Completa la registrazione: Compila il modulo di registrazione fornendo le informazioni richieste, 
come nome, indirizzo email e password. Assicurati di utilizzare un indirizzo email valido, poiché potrebbe 
essere necessario confermare l'account tramite email.
3. Accedi all'account: Dopo aver completato la registrazione, accedi al tuo account Bitly utilizzando 
l'indirizzo email e la password.
4. Accesso alle impostazioni API: Una volta effettuato l'accesso, cerca nel pannello di controllo 
dell'account Bitly l'opzione "Settings" o "Impostazioni". Potresti trovarla facendo clic sulla tua 
immagine del profilo o sul tuo nome utente.
5. Genera le chiavi API: Nelle impostazioni dell'account, cerca l'opzione relativa alle API. 
Potrebbe essere chiamata "API Keys", "Chiavi API" o qualcosa di simile. Da lì, dovresti poter generare 
le tue chiavi API personali.
6. Leggi e accetta le condizioni: Durante il processo di generazione delle chiavi API, potrebbe essere richiesto
di accettare i termini e le condizioni di utilizzo delle API di Bitly.
7. Copia le chiavi API: Una volta generate le chiavi API, dovrebbero essere visualizzate o scaricate dal sito. 
Assicurati di copiarle accuratamente e di tenerle al sicuro, poiché sono un'autorizzazione per utilizzare
le funzionalità dell'API di Bitly.
© ChatGPT
"""



from telethon import TelegramClient, events, utils
from telethon.errors import SessionPasswordNeededError
import re
import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import json

# dati API Telegram
api_id = XXXXXXX
api_hash = 'xxxxx'
client = TelegramClient('NOME UTENTE', api_id, api_hash)

real_id, peer_type = utils.resolve_id(-XXXXXXXXXX)

affiliate_tag = 'XXXXXXXXX'

def find_amazon_urls(text):
    # Definisci l'espressione regolare
    pattern = r"(www\.amazon|amzn\.to)"

    # Cerca la presenza dell'espressione regolare nella stringa di testo
    match = re.search(pattern, text)

    if match:
        return match.group()
    else:
        return None


@client.on(events.NewMessage(chats=real_id))  # canale da monitorare
async def my_event_handler(event):
    user_name = event.sender.username # gestire utenti con username "None" perche' non lo hanno inserito su Telegram
    txt_msg = event.raw_text  # estrazione del testo del messaggio
    if find_amazon_urls(txt_msg) is not None and user_name != 'xxxxxxx': # specificare il nick dell'amministratore per cui non si applica il filtro
        print('*********************************************')
        print(txt_msg)
        try:
            url_compress = re.search(r"(?P<url>https?://[^\s]+)", event.raw_text).group("url") # trovo la url nel testo del messaggio tramite una regular expression
            session = requests.Session()  # inizializzo una sessione
            url_espansa = session.head(url_compress, allow_redirects=True) # dalla url compressa ottengo la url normale
            url_utile = re.search(r"(?P<url>https?://[^\s]+)?[?]", url_espansa.url).group("url") # elimino dalla url normale tutto quello che viene dopo il ? cioe' i parametri
            mia_url = amazonify(url_utile, affiliate_tag) # passo la url per aggiungere il tag e comprimerla
        except AttributeError:
            mia_url = ""
            url_compress = ""
        righemessaggio = ""

        for riga in txt_msg.splitlines():
            if not riga: continue  # Filter out blank lines
            if riga.find("http") != -1:
                rigapulita = riga.replace(url_compress, mia_url)  # qui elimino la vecchia url dal messaggio aggiungo infine la mia url taggata e compressa
                righemessaggio = righemessaggio + '\n' + rigapulita  # accodo le righe del messaggio aggiungendo un crlf
            else:
                righemessaggio = righemessaggio + '\n' + riga  # accodo le righe del messaggio aggiungendo un crlf
                user_name = event.sender.username
        righemessaggio = '@' + user_name + ' ha inviato il seguente messaggio:' + righemessaggio
        await event.delete()
        destination_group_invite_link = 'https://t.me/+xxxxxxxx' # link del canale
        entity = await client.get_entity(destination_group_invite_link)
        await client.send_message(entity=entity, message=righemessaggio +'\n')


def amazonify(url, affiliatetag):
    new_url = urlparse(url)
    if not new_url.netloc:
        return None
    query_dict = parse_qs(new_url[4])
    query_dict['tag'] = affiliatetag
    new_url = new_url[:4] + (urlencode(query_dict, True), ) + new_url[5:]
    tagged = urlunparse(new_url)
    headers = {
        'Authorization': 'immetti qui API Bitly',
        'Content-Type': 'application/json',
    }
    data = '{ "long_url": "' + tagged + '", ' \
                                     '"domain": "bit.ly", ' \
                                     '"group_guid": "group_id" }' # accedi a Bitly,vai in Settings, Groups e vedi l'ultima parte delle URL ".../groups/group_id" 
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    shorten_dict = json.loads(response.text)
    good_one = shorten_dict['link']
    return good_one


def group_control():
    client.start()
    print("Client Created")
    # Ensure you're authorized
    if not client.is_user_authorized():
        # dati utente da impersonificare
        phone = "+39XXXXXXXXX"
        username = "xxxxxxxxxxx"
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))
    client.run_until_disconnected()


group_control()
