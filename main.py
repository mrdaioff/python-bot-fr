import time
import json
import telebot

# TOKEN DETAILS
TOKEN = "FCFA"
BOT_TOKEN = "8177340321:AAGHE1YI41hpAj3mVQaX2YXb3eiizAROLVg"
PAYMENT_CHANNEL = "@parrainegagnetest"  # add payment channel here including the '@' sign
OWNER_ID = 411645290  # write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@parrainegagnetest"]  # add channels to be checked here
Daily_bonus = 500  # Put daily bonus amount here!
Mini_Withdraw = 30000  # Minimum withdrawal amount
Per_Refer = 2000  # add per referral bonus here

bot = telebot.TeleBot(BOT_TOKEN)

# Define a temporary storage for users setting up their withdrawal accounts
awaiting_withdrawal_setup = {}

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Mon Compte')
    keyboard.row('🙌🏻 Invités', '🎁 Bonus Quotidien', '💸 Retirer')
    keyboard.row('⚙️ Configurer le compte de Retrait', '📊 Statistiques')
    bot.send_message(id, "*🏡 Accueil*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('users.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = "0"
            if user not in data['balance']:
                data['balance'][user] = 0
            # Change here from "none" to "aucun"
            if user not in data['wallet']:
                data['wallet'][user] = "aucun"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Rejoint', callback_data='check'))
            msg_start = "*🍔 Pour utiliser ce bot, vous devez rejoindre ce canal - "
            for i in CHANNELS:
                msg_start += f"\n➡️ {i}\n"
            msg_start += "*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markup)
        else:
            data = json.load(open('users.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            # Change here from "none" to "aucun"
            if user not in data['wallet']:
                data['wallet'][user] = "aucun"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Rejoint', callback_data='check'))
            msg_start = "*🍔 Pour utiliser ce bot, vous devez rejoindre ce canal - \n➡️ @ Remplissez vos canaux à la ligne : 101 et 157*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markups)
    except Exception as e:
        bot.send_message(message.chat.id, "Cette commande a rencontré une erreur, veuillez attendre que l'administrateur résolve le problème.")
        bot.send_message(OWNER_ID, f"Votre bot a rencontré une erreur : {str(e)}\nCommande : {message.text}")
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(callback_query_id=call.id, text='✅ Vous avez rejoint. Vous pouvez maintenant gagner de l\'argent.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user not in data['refer']:
                    data['refer'][user] = True

                    if user not in data['referby']:
                        data['referby'][user] = user
                        json.dump(data, open('users.json', 'w'))
                    if int(data['referby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)
                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0
                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1  # Increment the referrer's count
                        bot.send_message(ref_id, f"*🏧 Nouvelle Référence au Niveau 1, Vous Avez : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))  # Save after updates
                        return menu(call.message.chat.id)
                    else:
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                else:
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='❌ Vous n\'avez pas rejoint.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Rejoint', callback_data='check'))
                msg_start = "*🍔 Pour utiliser ce bot, vous devez rejoindre ce canal - \n➡️ @ Remplissez vos canaux à la ligne : 101 et 157*"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Cette commande a rencontré une erreur, veuillez attendre que l'administrateur résolve le problème.")
        bot.send_message(OWNER_ID, f"Votre bot a rencontré une erreur : {str(e)}\nDonnées de rappel : {call.data}")
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 Mon Compte':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 Utilisateur : {}\n\n⚙️ Compte : *{}*\n\n💸 Solde : *{}* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            # Change here from "none" to "aucun"
            if user not in data['wallet']:
                data['wallet'][user] = "aucun"

            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name, wallet, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == '🙌🏻 Invités':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ Total Invités : {} Utilisateurs\n\n👥 Système de Référence\n\n1 Niveau:\n🥇 Niveau°1 - {} {}\n\n🔗 Lien de Référence ⬇️\n{}*"
            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['referred']:
                data['referred'][user] = 0
            json.dump(data, open('users.json', 'w'))

            total_ref = data['referred'][user]
            ref_link = f"https://t.me/{bot_name}?start={user_id}"
            msg = ref_msg.format(total_ref, total_ref, TOKEN, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == '🎁 Bonus Quotidien':
            user_id = message.chat.id
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            user = str(user_id)
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if data['checkin'][user] == 1:
                bot.send_message(user_id, "❌ Vous avez déjà pris votre bonus quotidien aujourd'hui.")
            else:
                data['balance'][user] += Daily_bonus
                data['checkin'][user] = 1
                bot.send_message(user_id, f"✅ Vous avez reçu votre bonus quotidien de {Daily_bonus} {TOKEN}.")
            json.dump(data, open('users.json', 'w'))

        elif message.text == '💸 Retirer':
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            user = str(user_id)
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "aucun"
            balance = data['balance'][user]
            wallet = data['wallet'][user]
            if balance < Mini_Withdraw:
                bot.send_message(user_id, f"❌ Votre solde est de *{balance}* {TOKEN}.\n\nLe montant minimum de retrait est de *{Mini_Withdraw}* {TOKEN}.", parse_mode="Markdown")
            else:
                bot.send_message(user_id, "🏦 Entrez le montant à retirer.")

        elif message.text == '📊 Statistiques':
            user_id = message.chat.id
            data = json.load(open('users.json', 'r'))

            # Get the number of referrals for the user
            if user_id not in data['referred']:
                data['referred'][user_id] = 0  # Ensure the user is initialized
            user_referrals = data['referred'][user_id]  # Get user's referrals

            # Total balance is the same as before
            total_balance = sum(data['balance'].values())

            # Construct the message to send
            msg = f"*📈 Statistiques :*\n\n*Nombre de Références : {user_referrals}*\n*Total de solde : {total_balance} {TOKEN}*"
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == '⚙️ Configurer le compte de Retrait':
            user_id = message.chat.id
            data = json.load(open('users.json', 'r'))
            if user_id not in data['wallet']:
                data['wallet'][user_id] = "aucun"
                
            # Notify user to enter their account details
            msg = "*💼 Quel est votre compte ?*\n\n*Exemple : Moov Money 229 98 76 54 32*"
            bot.send_message(user_id, msg, parse_mode="Markdown")
            
            # Set the state for awaiting input
            awaiting_withdrawal_setup[user_id] = True
            
            # New handler for capturing user input for withdrawal account setup
        elif message.chat.id in awaiting_withdrawal_setup:
            user_id = message.chat.id
            account_info = message.text.strip()
            
            # Save the account information to the user's wallet
            data = json.load(open('users.json', 'r'))
            data['wallet'][user_id] = account_info  # Save the account info

            # Inform the user that their account has been set
            bot.send_message(user_id, f"*✅ Votre compte de retrait a été configuré : {account_info}*", parse_mode="Markdown")
            
            # Clean up the temporary state
            del awaiting_withdrawal_setup[user_id]

            # Save updated data
            json.dump(data, open('users.json', 'w'))

    except Exception as e:
        bot.send_message(message.chat.id, "Cette commande a rencontré une erreur, veuillez attendre que l'administrateur résolve le problème.")
        bot.send_message(OWNER_ID, f"Votre bot a rencontré une erreur : {str(e)}\nDonnées du message : {message.text}")
        return

# Start the bot
bot.polling()
