import telebot    #finale
import sqlite3
from telebot import custom_filters
from telebot import types

TOKEN='2038398666:AAEpYxwoeS_0T0JZ5nV_pFeJgMkcx5PO9hQ'
bot = telebot.TeleBot(TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        #self.age = None
        #self.sex = None

class GestorePiano:
    def crea(message):
     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

     item1 = types.KeyboardButton("Sistemi Operativi")
     item2 = types.KeyboardButton("Linguaggi formali e compilatori")
     item3 = types.KeyboardButton("Programmazione 2")
     item4 = types.KeyboardButton("Analisi 2")
     item5 = types.KeyboardButton("Diritto")
     item6 = types.KeyboardButton("Fisica")
     item7 = types.KeyboardButton("Vai")
     markup.add(item1, item2, item3, item4, item5, item6, item7)

     bot.send_message(message.chat.id, "Inserisci le lezioni nel tuo piano di studi",parse_mode='html', reply_markup=markup)

    def inizio(message):
     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

     item1 = types.KeyboardButton("Crea il tuo piano")
     item2 = types.KeyboardButton("Help")
     item3 = types.KeyboardButton("Exit")

     markup.add(item1, item2, item3)
     bot.send_message(message.chat.id, "Benvenuto!\n\n Scegli un'opzione",parse_mode='html', reply_markup=markup)

    def myplan(message):
     data=sqlite3.connect("my_database.sqlite")
     c=data.cursor()
     d=c.execute("SELECT DISTINCT * FROM prenotazioni")
     bot.send_message(message.chat.id,"PRENOTAZIONI EFFETTUATE:")
     for r in d:
         bot.send_message(message.chat.id,r)
     data.close()


    def action(message):
     if  message.text=='Vai':
           bot.send_message(message.chat.id,"IL TUO PIANO")
           stampa(message)
     else:
           data=sqlite3.connect("my_database.sqlite")
           c=data.cursor()
           a=c.execute("SELECT * FROM lezioni WHERE descrizione =?", (message.text,))
           for x in a:
               c.execute("INSERT INTO piano_studi(id ,descrizione ,data_ora ,aula,posti) VALUES(?,?,?,?,?);",(x[0],x[1],x[2],x[3],x[4]))
               c.execute("INSERT INTO piano(id ,descrizione ,data_ora ,aula,posti) VALUES(?,?,?,?,?);",(x[0],x[1],x[2],x[3],x[4]))
               data.commit()
     data.close()

    def aiuto(message):
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      item1 = types.KeyboardButton("CLOSE")
      markup.add(item1)
      bot.send_message(message.chat.id, "COMPONI IL TUO PIANO DI STUDI INSERENDO LE LEZIONI CHE DESIDERI SEGUIRE;DOPO AVERLO FATTO POTRAI EFFETTUARE LA PRENOTAZIONE PER UN POSTO IN AULA(SE ANCORA DISPONIBILE) PER LE LEZIONI INSERITE NEL TUO PIANO.QUANDO HAI FINITO,PREMI FINE PER VEDERE LE LEZIONI PRENOTATE FINO AD ORA E USCIRE,EFFETTUANDO IL LOGOUT", reply_markup=markup)

class GestorePrenotazione:
    global control
    def prenota_menu(message):
     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

     item1 = types.KeyboardButton("PRENOTA")
     item2 = types.KeyboardButton("CANCELLA PRENOTAZIONE")
     item3 = types.KeyboardButton("LE TUE PRENOTAZIONI")
     item5 = types.KeyboardButton("MODIFICA PIANO")
     item4 = types.KeyboardButton("FINE")

     markup.add(item1, item2, item3, item4, item5)

     bot.send_message(message.chat.id, 'AGGIUNGI ALTRE LEZIONI AL PIANO O EFFETTUA LA PRENOTAZIONE', reply_markup=markup)

    def stampa(message):
     data=sqlite3.connect("my_database.sqlite")
     c=data.cursor()
     bot.send_message(message.chat.id,"IL TUO PIANO")
     result=c.execute('SELECT DISTINCT * FROM piano_studi')
     for x in result:
         user=[]
         for y in range (5):
             user.append(x[y])
         mess="  id:  "+str(user[0])+"  descrizione:  "+user[1]+"  data e ora:  "+str(user[2])+"  aula:  "+str(user[3])+"  posti:  "+str(user[4])
         bot.send_message(message.chat.id,mess)
         data.commit()
     data.close()



    def sel(message):
     data=sqlite3.connect("my_database.sqlite")
     c=data.cursor()
     bot.send_message(message.chat.id,"Posti disponibili:")
     if message.text=='+Sistemi Operativi':
        control="Sistemi Operativi"
        data=sqlite3.connect("my_database.sqlite")
        c=data.cursor()
        b=c.execute("SELECT posti FROM posto WHERE descrizione=?",(control,))
        for riga in b:
            if riga[0]==0:
               bot.send_message(message.chat.id,"errore.....posti non disponibili")
               GestorePrenotazione.prenota_menu(message)
            else:
               a=c.execute('SELECT posti FROM lezioni WHERE descrizione="Sistemi Operativi"')
               for row in a:
                    row=row
               data=sqlite3.connect("my_database.sqlite")
               c=data.cursor()
               c.execute('UPDATE posto SET posti=posti-1 WHERE descrizione="Sistemi Operativi"')
               data.commit()
               b=c.execute('SELECT posti FROM posto WHERE descrizione="Sistemi Operativi"')
               for riga in b:
                   bot.send_message(message.chat.id,str(riga) +'/'+ str(row))
                   break;
               data.commit()
               bot.send_message(message.chat.id,'PRENOTAZIONE EFFETTUATA CON SUCCESSO PER IL CORSO SISTEMI OPERATIVI')
               c.execute("INSERT INTO prenotazioni(description) VALUES('Sistemi Operativi');")
               c.execute('DELETE FROM piano_studi WHERE descrizione="Sistemi Operativi"')
               data.commit()
               GestorePrenotazione.prenota_menu(message)
     if message.text=='+Linguaggi formali e compilatori':
        control="Linguaggi formali e compilatori"
        data=sqlite3.connect("my_database.sqlite")
        c=data.cursor()
        b=c.execute("SELECT posti FROM posto WHERE descrizione=?",(control,))
        for riga in b:
            if riga[0]==0:
               bot.send_message(message.chat.id,"errore.....posti non disponibili")
               GestorePrenotazione.prenota_menu(message)
            else:
               a=c.execute('SELECT posti FROM lezioni WHERE descrizione="Linguaggi formali e compilatori"')
               for row in a:
                   row=row
               data=sqlite3.connect("my_database.sqlite")
               c=data.cursor()
               c.execute('UPDATE posto SET posti=posti-1 WHERE descrizione="Linguaggi formali e compilatori"')
               data.commit()
               b=c.execute('SELECT posti FROM posto WHERE descrizione="Linguaggi formali e compilatori"')
               for riga in b:
                   bot.send_message(message.chat.id,str(riga) +'/'+ str(row))
                   break;
               data.commit()
               bot.send_message(message.chat.id,'PRENOTAZIONE EFFETTUATA CON SUCCESSO PER IL CORSO LINGUAGGI FORMALI E COMPILATORI')
               c.execute("INSERT INTO prenotazioni(description) VALUES('Linguaggi formali e compilatori');")
               c.execute('DELETE FROM piano_studi WHERE descrizione="Linguaggi formali e compilatori"')
               data.commit()
               GestorePrenotazione.prenota_menu(message)
     if message.text=='+Programmazione 2':
        control="Programmazione 2"
        data=sqlite3.connect("my_database.sqlite")
        c=data.cursor()
        b=c.execute("SELECT posti FROM posto WHERE descrizione=?",(control,))
        for riga in b:
            if riga[0]==0:
               bot.send_message(message.chat.id,"errore.....posti non disponibili")
               GestorePrenotazione.prenota_menu(message)
            else:
               a=c.execute('SELECT posti FROM lezioni WHERE descrizione="Programmazione 2"')
               for row in a:
                   row=row
               data=sqlite3.connect("my_database.sqlite")
               c=data.cursor()
               c.execute('UPDATE posto SET posti=posti-1 WHERE descrizione="Programmazione 2"')
               data.commit()
               b=c.execute('SELECT posti FROM posto WHERE descrizione="Programmazione 2"')
               for riga in b:
                   bot.send_message(message.chat.id,str(riga) +'/'+ str(row))
                   break;
               data.commit()
               bot.send_message(message.chat.id,'PRENOTAZIONE EFFETTUATA CON SUCCESSO PER IL CORSO PROGRAMMAZIONE 2')
               c.execute("INSERT INTO prenotazioni(description) VALUES('Programmazione 2');")
               c.execute('DELETE FROM piano_studi WHERE descrizione="Programmazione 2"')
               data.commit()
               GestorePrenotazione.prenota_menu(message)
     if message.text=='+Analisi 2':
        control="Analisi 2"
        data=sqlite3.connect("my_database.sqlite")
        c=data.cursor()
        b=c.execute("SELECT posti FROM posto WHERE descrizione=?",(control,))
        for riga in b:
            if riga[0]==0:
               bot.send_message(message.chat.id,"errore.....posti non disponibili")
               GestorePrenotazione.prenota_menu(message)
            else:
               a=c.execute('SELECT posti FROM lezioni WHERE descrizione="Analisi 2"')
               for row in a:
                   row=row
               data=sqlite3.connect("my_database.sqlite")
               c=data.cursor()
               c.execute('UPDATE posto SET posti=posti-1 WHERE descrizione="Analisi 2"')
               data.commit()
               b=c.execute('SELECT posti FROM posto WHERE descrizione="Analisi 2"')
               for riga in b:
                   bot.send_message(message.chat.id,str(riga) +'/'+ str(row))
                   break;
               data.commit()
               bot.send_message(message.chat.id,'PRENOTAZIONE EFFETTUATA CON SUCCESSO PER IL CORSO ANALISI 2')
               c.execute("INSERT INTO prenotazioni(description) VALUES('Analisi 2');")
               c.execute('DELETE FROM piano_studi WHERE descrizione="Analisi 2"')
               data.commit()
               GestorePrenotazione.prenota_menu(message)
     if message.text=='+Diritto':
        control="Diritto"
        data=sqlite3.connect("my_database.sqlite")
        c=data.cursor()
        b=c.execute("SELECT posti FROM posto WHERE descrizione=?",(control,))
        for riga in b:
            if riga[0]==0:
               bot.send_message(message.chat.id,"errore.....posti non disponibili")
               GestorePrenotazione.prenota_menu(message)
            else:
               a=c.execute('SELECT posti FROM lezioni WHERE descrizione="Diritto"')
               for row in a:
                   row=row
               GestorePrenotazione.check1(message,control)
               data=sqlite3.connect("my_database.sqlite")
               c=data.cursor()
               c.execute('UPDATE posto SET posti=posti-1 WHERE descrizione="Diritto"')
               data.commit()
               b=c.execute('SELECT posti FROM posto WHERE descrizione="Diritto"')
               for riga in b:
                   bot.send_message(message.chat.id,str(riga) +'/'+ str(row))
                   break;
               data.commit()
               bot.send_message(message.chat.id,'PRENOTAZIONE EFFETTUATA CON SUCCESSO PER IL CORSO DIRITTO')
               c.execute("INSERT INTO prenotazioni(description) VALUES('Diritto');")
               c.execute('DELETE FROM piano_studi WHERE descrizione="Diritto"')
               data.commit()
               GestorePrenotazione.prenota_menu(message)
     if message.text=='+Fisica':
        control="Fisica"
        data=sqlite3.connect("my_database.sqlite")
        c=data.cursor()
        b=c.execute("SELECT posti FROM posto WHERE descrizione=?",(control,))
        for riga in b:
            if riga[0]==0:
               bot.send_message(message.chat.id,"errore.....posti non disponibili")
               GestorePrenotazione.prenota_menu(message)
            else:
               a=c.execute('SELECT posti FROM lezioni WHERE descrizione="Fisica"')
               for row in a:
                   row=row
               data=sqlite3.connect("my_database.sqlite")
               c=data.cursor()
               c.execute('UPDATE posto SET posti=posti-1 WHERE descrizione="Fisica"')
               data.commit()
               b=c.execute('SELECT posti FROM posto WHERE descrizione="Fisica"')
               for riga in b:
                   bot.send_message(message.chat.id,str(riga) +'/'+ str(row))
                   break;
               data.commit()
               bot.send_message(message.chat.id,'PRENOTAZIONE EFFETTUATA CON SUCCESSO PER IL CORSO FISICA')
               c.execute("INSERT INTO prenotazioni(description) VALUES('Fisica');")
               c.execute('DELETE FROM piano_studi WHERE descrizione="Fisica"')
               data.commit()
               GestorePrenotazione.prenota_menu(message)
               data.close()

    def canc(message):
     if message.text=='-Sistemi Operativi':
           data=sqlite3.connect("my_database.sqlite")
           c=data.cursor()
           bot.send_message(message.chat.id,'STAI CANCELLANDO LA PRENOTAZIONE PER SISTEMI OPERATIVI...')
           c.execute('DELETE FROM prenotazioni WHERE description="Sistemi Operativi"')
           data.commit()
           a=c.execute('SELECT * FROM lezioni WHERE descrizione="Sistemi Operativi"')
           for x in a:
               c.execute("INSERT INTO piano_studi(id ,descrizione ,data_ora ,aula,posti) VALUES(?,?,?,?,?);",(x[0],x[1],x[2],x[3],x[4]))
               data.commit()
           c.execute('UPDATE posto SET posti=posti+1 WHERE descrizione="Sistemi Operativi"')
           data.commit()
           GestorePrenotazione.prenota_menu(message)

     if message.text=='-Linguaggi formali e compilatori':
           data=sqlite3.connect("my_database.sqlite")
           c=data.cursor()
           bot.send_message(message.chat.id,'STAI CANCELLANDO LA PRENOTAZIONE PER LINGUAGGI FORMALI E COMPILATORI...')
           c.execute('DELETE FROM prenotazioni WHERE description="Linguaggi formali e compilatori"')
           data.commit()
           a=c.execute('SELECT * FROM lezioni WHERE descrizione="Linguaggi formali e compilatori"')
           for x in a:
               c.execute("INSERT INTO piano_studi(id ,descrizione ,data_ora ,aula,posti) VALUES(?,?,?,?,?);",(x[0],x[1],x[2],x[3],x[4]))
               data.commit()
           c.execute('UPDATE posto SET posti=posti+1 WHERE descrizione="Linguaggi formali e compilatori"')
           data.commit()
           GestorePrenotazione.prenota_menu(message)
     if message.text=='-Programmazione 2':
           data=sqlite3.connect("my_database.sqlite")
           c=data.cursor()
           bot.send_message(message.chat.id,'STAI CANCELLANDO LA PRENOTAZIONE PER PROGRAMMAZIONE 2...')
           c.execute('DELETE FROM prenotazioni WHERE description="Programmazione 2"')
           data.commit()
           a=c.execute('SELECT * FROM lezioni WHERE descrizione="Programmazione 2"')
           for x in a:
               c.execute("INSERT INTO piano_studi(id ,descrizione ,data_ora ,aula,posti) VALUES(?,?,?,?,?);",(x[0],x[1],x[2],x[3],x[4]))
               data.commit()
               c.execute('UPDATE posto SET posti=posti+1 WHERE descrizione="Programmazione 2"')
               data.commit()
           GestorePrenotazione.prenota_menu(message)
     if message.text=='-Analisi 2':
           data=sqlite3.connect("my_database.sqlite")
           c=data.cursor()
           bot.send_message(message.chat.id,'STAI CANCELLANDO LA PRENOTAZIONE PER ANALISI 2...')
           c.execute('DELETE FROM prenotazioni WHERE description="Analisi 2"')
           data.commit()
           a=c.execute('SELECT * FROM lezioni WHERE descrizione="Analisi 2"')
           for x in a:
               c.execute("INSERT INTO piano_studi(id ,descrizione ,data_ora ,aula,posti) VALUES(?,?,?,?,?);",(x[0],x[1],x[2],x[3],x[4]))
               data.commit()
               c.execute('UPDATE posto SET posti=posti+1 WHERE descrizione="Analisi 2"')
               data.commit()
           GestorePrenotazione.prenota(message)
     if message.text=='-Diritto':
           data=sqlite3.connect("my_database.sqlite")
           c=data.cursor()
           bot.send_message(message.chat.id,'STAI CANCELLANDO LA PRENOTAZIONE PER DIRITTO...')
           c.execute('DELETE FROM prenotazioni WHERE description="Diritto"')
           data.commit()
           a=c.execute('SELECT * FROM lezioni WHERE descrizione="Diritto"')
           for x in a:
               c.execute("INSERT INTO piano_studi(id ,descrizione ,data_ora ,aula,posti) VALUES(?,?,?,?,?);",(x[0],x[1],x[2],x[3],x[4]))
               data.commit()
               c.execute('UPDATE posto SET posti=posti+1 WHERE descrizione="Diritto"')
               data.commit()
           GestorePrenotazione.prenota_menu(message)
     if message.text=='-Fisica':
           data=sqlite3.connect("my_database.sqlite")
           c=data.cursor()
           bot.send_message(message.chat.id,'STAI CANCELLANDO LA PRENOTAZIONE PER FISICA...')
           c.execute('DELETE FROM prenotazioni WHERE description="Fisica"')
           data.commit()
           a=c.execute('SELECT * FROM lezioni WHERE descrizione="Fisica"')
           for x in a:
               c.execute("INSERT INTO piano_studi(id ,descrizione ,data_ora ,aula,posti) VALUES(?,?,?,?,?);",(x[0],x[1],x[2],x[3],x[4]))
               data.commit()
               c.execute('UPDATE posto SET posti=posti+1 WHERE descrizione="Fisica"')
               data.commit()
           GestorePrenotazione.prenota_menu(message)




    def riassunto(message):
     data=sqlite3.connect("my_database.sqlite")
     c=data.cursor()
     result=c.execute("SELECT DISTINCT * FROM prenotazioni")
     bot.send_message(message.chat.id,"TABELLA RIASSUNTIVA PRENOTAZIONI EFFETTUATE:")
     for j in result:
            x=c.execute("SELECT DISTINCT id ,descrizione ,data_ora ,aula FROM lezioni,prenotazioni WHERE lezioni.descrizione=prenotazioni.description ")
            for pi in x:
                user=[]
                for y in range(4):
                       user.append(pi[y])
                mess="  id:  "+str(user[0])+"  descrizione:  "+user[1]+"  data e ora:  "+str(user[2])+"  aula:  "+str(user[3])
                bot.send_message(message.chat.id,mess)
                data.commit()
     data.close()
     GestoreAccesso.login(message)

    #def register(message):
     #bot.send_message(message.chat.id, "\nSCEGLI UN USERNAME :\n")
     #reg(message)




    def Checking_add(message):
     check=message.text#check ha l'user inserito
     if check !='+Sistemi Operativi' and check !='+Linguaggi formali e compilatori' and check !='+Programmazione 2' and check !='+Analisi 2' and check!='+Diritto' and check!='+Fisica' :
        bot.send_message(message.chat.id,"errore.......lezione non presente nel piano\n\nPuoi effettuare prenotazioni solo per lezioni nel tuo piano di studi!!!")
        GestorePrenotazione.prenota(message)
     else:
          if check=='+Sistemi Operativi':
              data=sqlite3.connect("my_database.sqlite")
              c=data.cursor()
              counting=0;
              a=c.execute("SELECT DISTINCT description FROM prenotazioni WHERE description='Sistemi Operativi'")
              for row1 in a:
                  counting=counting+1
              if counting!=0:
                  bot.send_message(message.chat.id,"Lezione gia' prenotata...")
                  GestorePrenotazione.prenota(message)
              else:
                  GestorePrenotazione.sel(message)
          if check=='+Linguaggi formali e compilatori':
               data=sqlite3.connect("my_database.sqlite")
               c=data.cursor()
               counting=0;
               a=c.execute("SELECT DISTINCT description FROM prenotazioni WHERE description='Linguaggi formali e compilatori'")
               for row1 in a:
                   counting=counting+1
               if counting!=0:
                   bot.send_message(message.chat.id,"Lezione gia' prenotata...")
                   GestorePrenotazione.prenota(message)
               else:
                   GestorePrenotazione.sel(message)
          if check=='+Programmazione 2':
                data=sqlite3.connect("my_database.sqlite")
                c=data.cursor()
                counting=0;
                a=c.execute("SELECT DISTINCT description FROM prenotazioni WHERE description='Programmazione 2'")
                for row1 in a:
                    counting=counting+1
                if counting!=0:
                    bot.send_message(message.chat.id,"Lezione gia' prenotata...")
                    GestorePrenotazione.prenota(message)
                else:
                    GestorePrenotazione.sel(message)
          if check=='+Analisi 2':
                 data=sqlite3.connect("my_database.sqlite")
                 c=data.cursor()
                 counting=0;
                 a=c.execute("SELECT DISTINCT description FROM prenotazioni WHERE description='Analisi 2'")
                 for row1 in a:
                     counting=counting+1
                 if counting!=0:
                     bot.send_message(message.chat.id,"Lezione gia' prenotata...")
                     GestorePrenotazione.prenota(message)
                 else:
                     GestorePrenotazione.sel(message)
          if check=='+Diritto':
                data=sqlite3.connect("my_database.sqlite")
                c=data.cursor()
                counting=0;
                a=c.execute("SELECT DISTINCT description FROM prenotazioni WHERE description='Diritto'")
                for row1 in a:
                    counting=counting+1
                if counting!=0:
                    bot.send_message(message.chat.id,"Lezione gia' prenotata...")
                    GestorePrenotazione.prenota(message)
                else:
                    GestorePrenotazione.sel(message)
          if check=='+Fisica':
                 data=sqlite3.connect("my_database.sqlite")
                 c=data.cursor()
                 counting=0;
                 a=c.execute("SELECT DISTINCT description FROM prenotazioni WHERE description='Fisica'")
                 for row1 in a:
                     counting=counting+1
                 if counting!=0:
                     bot.send_message(message.chat.id,"Lezione gia' prenotata...")
                     GestorePrenotazione.prenota(message)
                 else:
                     GestorePrenotazione.sel(message)


    def prenota(message):
     msg2=""
     data=sqlite3.connect("my_database.sqlite")
     c=data.cursor()
     a=c.execute("SELECT DISTINCT descrizione FROM piano_studi")
     bot.send_message(message.chat.id,"SCEGLI TRA LE LEZIONI CHE HAI INSERITO NEL PIANO; SCRIVI '+nome del corso per accedere':")
     for row in a:
         msg2=bot.send_message(message.chat.id,row)
     bot.register_next_step_handler(msg2,GestorePrenotazione.Checking_add)



    def resume(message):
     data=sqlite3.connect("my_database.sqlite")
     c=data.cursor()
     a=c.execute("SELECT DISTINCT description FROM prenotazioni")
     bot.send_message(message.chat.id,"SCEGLI TRA LE LEZIONI CHE HAI prenotato; SCRIVI '-nome del corso per eliminare':")
     for row in a:
          bot.send_message(message.chat.id,row)
     c.close()
     data.close()

class GestoreAccesso:
    messaggino=""
    def login(message):
     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

     item1 = types.KeyboardButton("ACCEDI")
     item2 = types.KeyboardButton("REGISTRATI")

     markup.add(item1, item2)
     bot.send_message(message.chat.id, "ACCEDI O REGISTRATI",parse_mode='html', reply_markup=markup)
     #inizio(message)

    def enter(message):
     msg1=bot.send_message(message.chat.id,"INSERISCI UN USERNAME")
     bot.register_next_step_handler(msg1,GestoreAccesso.process1_name_step)


    def process1_passw_step(message):
     chat_id = message.chat.id
     age = message.text
     user = user_dict[chat_id]
     pin=message.text#pin ha la password
     #print(pin)
     #print(messaggino)
     data=sqlite3.connect("my_database.sqlite")
     c=data.cursor()
     a=c.execute("SELECT password FROM utenti WHERE username=?",(messaggino,))
     for row in a:#print(row) e' password
         user=[]
         for y in range(1):
              user.append(row[y])
              mess=str(user[0])#in mess ho la password
              if mess==pin:
                   bot.send_message(message.chat.id, "AUTENTICAZIONE EFFETTUATA CON SUCCESSO")
                   GestorePiano.inizio(message)
              else:
                    bot.send_message(message.chat.id, "PASSWORD ERRATA")
                    GestoreAccesso.process1_name_step(message)


    def process1_name_step(message):
     chat_id = message.chat.id
     name = message.text
     user = User(name)
        #print(name)
     user_dict[chat_id] = user
     global messaggino
     messaggino=message.text#come name stesso valore,cioe l'username inserito
     data=sqlite3.connect("my_database.sqlite")
     c=data.cursor()
     a=c.execute("SELECT username FROM utenti WHERE username=?",(messaggino,))
     i=0
     for row in a:
         i=i+1
     if i==0:
         bot.send_message(message.chat.id, "USERNAME INSESISTENTE...")
         GestoreAccesso.login(message)
     else:
         msg=bot.send_message(message.chat.id, "INSERISCI UNA PASSWORD")
         bot.register_next_step_handler(msg,GestoreAccesso.process1_passw_step)




class GestoreRegistrazione:
    messaggino=""

    def reg(message):
        msg=bot.send_message(message.chat.id,"INSERISCI UN USERNAME")
        bot.register_next_step_handler(msg,GestoreRegistrazione.process_name_step)

    def acc(message):
         msg=bot.send_message(message.chat.id, "INSERISCI UNA PASSWORD")
         bot.register_next_step_handler(msg, GestoreRegistrazione.process_passw_step)


    def process_name_step(message):
        #chat_id = message.chat.id
        name = message.text
        user = User(name)
        #print(name)
        #user_dict[chat_id] = user
        global messaggino
        messaggino=message.text#come name stesso valore,cioe l'username inserito
        if len(messaggino)>8:
         bot.send_message(message.chat.id, "L'USERNAME SCELTO VIOLA I VINCOLI DEL SISTEMA(max 8 caratteri)")
         GestoreRegistrazione.reg(message)
        else:
         if len(messaggino)<3:
          bot.send_message(message.chat.id, "L'USERNAME SCELTO VIOLA I VINCOLI DEL SISTEMA(min 3 caratteri)")
          GestoreRegistrazione.reg(message)
         else:
           data=sqlite3.connect("my_database.sqlite")
           c=data.cursor()
           a=c.execute("SELECT nome FROM sol WHERE nome=?",(messaggino,))
           i=0
           for row in a:
             i=i+1
           if i==0:
            bot.send_message(message.chat.id,"username non associato a alcun profilo studente nel SOL")
            GestoreRegistrazione.reg(message)
           else:
            a=c.execute("SELECT username FROM utenti WHERE username=?",(messaggino,))
            i=0
            for row in a:
                i=i+1
            if i==0:
                c.execute("INSERT INTO utenti(username ,password) VALUES(?,?);",(message.text,0))
                data.commit()
                GestoreRegistrazione.acc(message)
                #msg=bot.send_message(message.chat.id, "INSERISCI UNA PASSWORD")
                #bot.register_next_step_handler(msg, GestoreRegistrazione.process_passw_step)
                data.close()
            else:
                bot.send_message(message.chat.id,"username gia' in uso")
                GestoreRegistrazione.reg(message)




    def process_passw_step(message):
        #chat_id = message.chat.id
        #age = message.text
        #user = user_dict[chat_id]
        pin=message.text#pin ha la password
        if len(pin)>10:
         bot.send_message(message.chat.id, "LA PASSWORD SCELTA VIOLA I VINCOLI DEL SISTEMA(max 10 caratteri)")
         GestoreRegistrazione.acc(message)
        else:
         if len(pin)<5:
          bot.send_message(message.chat.id, "LA PASSWORD SCELTA VIOLA I VINCOLI DEL SISTEMA(min 5 caratteri)")
          GestoreRegistrazione.acc(message)
         else:
        #print(pin)
        #print(messaggino)
          data=sqlite3.connect("my_database.sqlite")
          c=data.cursor()
          c.execute('UPDATE utenti SET password=? WHERE username=?',(pin,messaggino))
          data.commit()
          data.close()
          bot.send_message(message.chat.id,"registrazione effettuata,effettua l'accesso...")
          GestoreAccesso.login(message)
        #enter()









class init:
    @bot.message_handler(func=lambda m: True)
    def init(message):
     if message.text=='/start':
        GestoreAccesso.login(message)
     if message.text=='Crea il tuo piano':
        GestorePiano.crea(message)
     if message.text=='Help':
        GestorePiano.aiuto(message)
     if message.text=='Sistemi Operativi' or message.text=='Linguaggi formali e compilatori' or message.text=='Programmazione 2' or message.text=='Analisi 2' or message.text=='Diritto' or message.text=='Fisica' :
        GestorePiano.action(message)
     if message.text=='Vai':
        GestorePrenotazione.stampa(message)
        GestorePrenotazione.prenota_menu(message)
     if message.text=='PRENOTA':
        GestorePrenotazione.prenota(message)
     #if message.text=='+Sistemi Operativi' or message.text=='+Linguaggi formali e compilatori' or message.text=='+Programmazione 2' or message.text=='+Analisi 2' or message.text=='+Diritto' or message.text=='+Fisica' :
        #GestorePrenotazione.sel(message)
     if message.text=='ACCEDI':
        GestoreAccesso.enter(message)
     if message.text=='REGISTRATI':
        GestoreRegistrazione.reg(message)
     if message.text=='CANCELLA PRENOTAZIONE':
        GestorePrenotazione.resume(message)
     if message.text=='LE TUE PRENOTAZIONI':
        GestorePiano.myplan(message)
     if message.text=='-Sistemi Operativi' or message.text=='-Linguaggi formali e compilatori' or message.text=='-Programmazione 2' or message.text=='-Analisi 2' or message.text=='-Diritto' or message.text=='-Fisica' :
        GestorePrenotazione.canc(message)
     if message.text=='FINE':
        GestorePrenotazione.riassunto(message)
     if message.text=='CLOSE':
        GestorePiano.inizio(message)
     if message.text=='Exit' or message.text=='Termina':
        GestoreAccesso.login(message)
     if message.text=='MODIFICA PIANO':
        GestorePiano.crea(message)







     #RUN
bot.polling(none_stop=True)
