import os
os.system("pip install --upgrade telethon")
os.system("clear")
from telethon.tl.functions.channels import *
from telethon.tl.functions.channels import CreateChannelRequest, UpdateUsernameRequest
from telethon.tl.types import *
from telethon import *
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.errors import *
import asyncio, telethon, time, string, threading, telebot, requests, sys, json, random, datetime, names, pytz
from telethon.tl.functions.messages import *
from telethon.tl.functions.account import *
from telethon.sessions import StringSession
from lsedb import *












def getSessions():
    global sessionsdb, sessions0, sessions, main_s,all_sessions_count, all_flood_sessions_count,all_user_points
    allsessions = sessionsdb.get()["msg"]
    sessions0 = []
    all_flood_sessions_count = 0
    all_user_points = 0
    for u in allsessions:
        if u["user"] == user0:
            sessions0.append(u)
            if "flood" in u:
                all_flood_sessions_count += 1
            if u["main"] and "points" in u:
                try:
                    all_user_points += int(u["points"])
                except:
                    pass
    all_sessions_count = len(sessions0)
    sessions = []
    sessions0 = sorted(sessions0, key=lambda x: x['phone'])
    dt = int(round(datetime.now().timestamp()))
    for s in range(len(sessions0)):
      if sessions0[s]["million_bot"]:
        if "flood" in sessions0[s]:
            if dt > int(sessions0[s]["flood"]):
                sessions.append(sessions0[s])
                sessions0[s].pop("flood")
                sessionsdb.edit(sessions0[s])
        else:
            sessions.append(sessions0[s])
      if sessions0[s]["main"] and sessions0[s]["phone"] == main_phone:
        if not "points" in sessions0[s]:
            sessions0[s]["points"] = 0
            sessionsdb.edit(sessions0[s])
        main_s = sessions0[s]
    sessions = sorted(sessions, key=lambda x: x['phone'])
    





main_s = None
sessionsdb = lsedb("lse","mahmoud123","billion","sessions")





sessions0 = []
sessions = []
client = None
all_sessions_count = 0
all_flood_sessions_count = 0
all_user_points = 0
bot = None
destroy_link = False
session = 0
points_link = None





async def login(session, add=False):
    print(f"\nConnected To : {session['phone']}")
    global client, sessionsdb
    if not client:
      client = TelegramClient(StringSession(), session['api_id'], session['api_hash'])
      await client.connect()
    await client.send_code_request(session['phone'], force_sms=False)
    while True:
     try:
      await client.sign_in(code=input("code: "))
      print("Login Completed 🎉\nStart Script Again \n Session : " +str(client.session.save()))
      break
     except SessionPasswordNeededError:
      while True:
        try:
          await client.sign_in(password=input("pass: "))
          print("Login Completed 🎉\nStart Script Again \n Session : " +str(client.session.save()))
          break
        except:
          print("Password Is Wrong")
      break
     except PhoneCodeInvalidError:
      pass
     except PhoneCodeExpiredError:
      pass
    s = str(client.session.save())
    if add:
        session["session"] = s
        print(f"Session : {session['session']}")
        sessionsdb.edit(session)
    await client.disconnect()
    client = None
    return s








async def main(session0):
  global client
  global my_id
  global channels
  global event_action, recv_id
  global points
  global last_time, destroy_link
  global event_e
  global sessions, million_fee
  global phone, my_user, bot_user,auto_start
  global session, bot, wait_s, end_index, start_index
  global sessions0, group_link, group_id
  global msg_id, last_channel,sessionsdb,user
  global points_link, main_s, max, m_bot, disconnect
  session = session0
  if session >= end_index+1:
    session = start_index
  if points_link:
    phone = main_s["phone"]
    api_id = main_s["api_id"]
    api_hash = main_s["api_hash"]
    a = main_s["session"]
    max = False
  else:
    phone = sessions[session]["phone"]
    api_id = sessions[session]["api_id"]
    api_hash = sessions[session]["api_hash"]
    sessions[session]["running"] = True
    sessionsdb.edit(sessions[session])
    if "session" in sessions[session]:
      a = sessions[session]["session"]
    else:
      a = ""
  client = TelegramClient(StringSession(a), api_id, api_hash)
  try:
      await client.connect()
      await asyncio.sleep(5)
  except AuthKeyDuplicatedError:
    if sessions[session]["phone"] == phone and not sessions[session]["main"]:
      bot.send_message(group_id,f"الرقم ده {phone} جاب خطأ فى كود الجلسة, وتم إزالته من السيرفر")
      sessionsdb.delete(sessions[session])
      getSessions()
      disconnect = True
  if await client.is_user_authorized():
    try:
      client.parse_mode = "markdown"
      os.system("clear")
      print(f"Connected To : {phone}")
      my_user = await client.get_me()
      my_id = my_user.id
      print("Script Started Successfully ... In " + str(my_id))
      while True:
        try:
          await client.get_input_entity(group_link)
          break
        except FloodWaitError as e:
          await editEventMsg("Disconnected For Some Time ...")
          sessions[session]["flood"] = int(round(datetime.now().timestamp())) + int(e.seconds)
          sessionsdb.edit(sessions[session])
          await client.disconnect()
          break
        except ValueError:
          await follow(client, group_link)
          await asyncio.sleep(wait_s)
      event_action = group_id
      await asyncio.sleep(3)
      try:
        m_bot = await client.get_input_entity(bot_user)
      except:
        m_bot = bot_user
      
      
      
      try:
        await editEventMsg("Checking Account Details ...")
        await asyncio.sleep(3)
        if not my_user.username:
            na = str(my_user.first_name).lower().strip()+get_rand(5)
            await client(telethon.tl.functions.account.UpdateUsernameRequest(na))
      except:
        pass
      

      
      if not "msg_id" in sessions[session]:
        if not msg_id:
            msg_id = bot.send_message(event_action,"Script Started ...").id
        sessions[session]["msg_id"] = msg_id
        sessionsdb.edit(sessions[session])
      else:
        if not msg_id:
            msg_id = sessions[session]["msg_id"]
    except FloodWaitError as e:
      sessions[session]["flood"] = int(round(datetime.now().timestamp())) + int(e.seconds)
      sessionsdb.edit(sessions[session])
      try:
        await editEventMsg("Disconnected For Some Time ...")
      except:
        pass
      await client.disconnect()
    last_time = int(round(datetime.now().timestamp()))

    @client.on(events.MessageEdited(chats=[m_bot]))
    @client.on(events.NewMessage(chats=[m_bot]))
    async def handler(event):
      try:
        global points, million_fee, my_user
        global last_time, bot_event,auto_start,bot_user
        global event_e, max_points, new_user
        global session,sessionsdb,user, destroy_link
        global channels, sessions, sessions0, session, last_channel, bot, wait_s
        global points_link, max, main_s, m_bot, phone, disconnect, recv_id
        event_e = event
        last_time = int(round(datetime.now().timestamp()))
        auto_start = 0
        reply = event.reply_markup
        if not sessions[session]["phone"] == phone and not phone == main_s["phone"]:
            disconnect = True
            reply = None
            event.text = None
            await client.disconnect()
        if reply and "اشترك فالقناة" in str(event.text) and "اشتركت" in str(event.buttons[0][0].text) and not disconnect and not max:
          last_channel = None
          link = str(event.text).replace("*","").replace("(","").replace(")","").replace("]","").replace("[","").replace("`","")
          i1 = link.find("\n", link.find("@"))
          if int(i1) == -1:
              i1 = link.find(" ", link.find("@"))
              if int(i1) == -1:
                  i1 = None
          if i1:
              link = link[link.find("@"):i1]
          else:
              link = link[link.find("@"):]
          link = "https://t.me/"+link[1:]
          await asyncio.sleep(wait_s)
          await editEventMsg(f"Subscribe To : {link}")
          channels.append(link)
          d = await follow(client, link)
          await asyncio.sleep(wait_s)
          if max:
            await event.click(1)
          elif d:
            print("Success")
            last_channel = link
            await asyncio.sleep(wait_s)
            await editEventMsg("Clicking Submit Button ...")
            await asyncio.sleep(wait_s)
            m = (await event.click(0,0)).message
            if "تم اضافة" in m:
                points += 5
                await editEventMsg(f"Done Add +5 Points ~> Points: {points}")
                if points >= max_points+million_fee and not new_user and main_s and not phone == main_s["phone"]:
                  max = True
                  await editEventMsg(f"Account Reached {points} Points, Start Transfer ...")
                  await asyncio.sleep(wait_s)
                  await client.send_message(m_bot, "/start")
                elif phone == main_s["phone"]:
                  max = False
                  await client.disconnect()
                elif len(channels) >= 50:
                  await asyncio.sleep(wait_s)
                  await editEventMsg("Subscribe To 50 Channel Completed, Disconnecting ...")
                  await client.disconnect()
                  disconnect = True
            elif "عليك الاشتراك بالقناة" in m:
                await editEventMsg("Some Errors, Run Again ...")
                await asyncio.sleep(wait_s)
                await editEventMsg("Clicking Skip Button ...")
                await asyncio.sleep(wait_s)
                await event.click(0,1)
          else:
            print("Faild")
            await asyncio.sleep(wait_s)
            await editEventMsg("Clicking Skip Button ...")
            await asyncio.sleep(wait_s)
            await event.click(0,1)

        elif reply and "مرحبا بك في بوت DomKom 👋" in str(event.text) or "DomKom" in str(event.text):
          points = int(str(event.text).split(":")[1].split("\n")[0].strip())
          if points >= max_points+million_fee and not new_user and main_s and not phone == main_s["phone"]:
              max = True
              await editEventMsg(f"Account Reached {points} Points, Start Transfer ...")
              await asyncio.sleep(wait_s)
          if max and not new_user:
            if phone == main_s["phone"]:
              max = False
              await client.disconnect()
            elif points > 99 and main_s:
              await editEventMsg("Start Transfer Points ...")
              await asyncio.sleep(wait_s)
              await event.click(2, 1)
            elif not main_s:
              new_user = True
              await asyncio.sleep(wait_s)
              await event.click(1,0)
            else:
              await editEventMsg("Not Enough Points, Disconnecting ...")
              max = False
              await client.disconnect()
          elif max and new_user:
            sessions[session]["million_bot"] = False
            sessions[session]["max"] = True
            sessionsdb.edit(sessions[session])
            await client.disconnect()
          else:
            await editEventMsg("Click Collect Points Button ...")
            await asyncio.sleep(wait_s)
            await event.click(1,0)
        
        
        elif reply and "✳️ تجميع نقاط" in str(event.text):
          if (last_time - int(sessions[session]["gift"])) >= 86500:
            await editEventMsg("Take Daily Gift ...")
            await asyncio.sleep(wait_s)
            m = (await event.click(2)).message
            if "لقد حصلت على" in str(m):
               await editEventMsg("You Take 50 Points From Daily Gift ^_^")
               points += 50
               sessions[session]["gift"] = int(round(datetime.now().timestamp()))
               sessionsdb.edit(sessions[session])
               await asyncio.sleep(wait_s)
               await client.send_message(m_bot, "/start")
    
            elif "طالب بالهدية بعد" in str(m):
               await editEventMsg("Gift Already Taken -_-")
               sessions[session]["gift"] = int(round(datetime.now().timestamp())) - 82800
               sessionsdb.edit(sessions[session])
               await asyncio.sleep(wait_s)
               await event.click(0)
               
          else:
            await editEventMsg("Click Join Channels Button ...")
            await asyncio.sleep(wait_s)
            await event.click(0)
        

        elif "عليك الاشتراك بقناة البوت" in str(event.text) or "دون الاشتراك في قناه البوت" in str(event.text) or "عليك متابعه حسابي" in str(event.text) or "عليك الأشتراك بقناة البوت أولاً لتتمكن من أستخدامه" in str(event.text) or "عليك الأشتراك بقناة البوت لتتمكن من أستخدام" in str(event.text) or "عذراً يجب عليك الاشتراك في القناه لتستطيع استخدام البوت" in str(event.text):
          link = str(event.text).replace("*","").replace("(","").replace(")","").replace("]","").replace("[","").replace("`","")
          if "https://t.me" in event.text:
              i1 = link.find("\n", link.find("https://"))
              if int(i1) == -1:
                  i1 = link.find(" ", link.find("https://"))
                  if int(i1) == -1:
                      i1 = None
              if i1:
                  link = link[link.find("https://"):i1]
              else:
                  link = link[link.find("https://"):]
          else:
              i1 = link.find("\n", link.find("@"))
              if int(i1) == -1:
                  i1 = link.find(" ", link.find("@"))
                  if int(i1) == -1:
                      i1 = None
              if i1:
                  link = link[link.find("@"):i1]
              else:
                  link = link[link.find("@"):]
              link = "https://t.me/"+link[1:]
          await editEventMsg(f"Subscribe To : {link}")
          d = await follow(client, link)
          await asyncio.sleep(wait_s)
          if not d and max:
              async for dialog in client.iter_dialogs():
                  await dialog.delete()
                  break
          await asyncio.sleep(wait_s)
          if phone == main_s["phone"] and points_link:
              await client.send_message(m_bot, "/start "+points_link.split("=")[1])
          else:
              await client.send_message(m_bot, "/start 5885003956")

        elif "لا يوجد قنوات حالياً 🤍" in str(event.text):
          if max:
              pass
          else:
              await editEventMsg("No Channels Available Now, Closing This Session ...")
              #sessions[session]["million_bot"] = False
              #sessions[session]["arab_bot"] = False
              #sessions[session]["blue_bot"] = False
              #sessions[session]["max"] = True
              #sessionsdb.edit(sessions[session])
              #bot.send_message(chat_id=group_id,text=f"هذا الرقم {phone} وصل إلى 500 قناة")
              await client.disconnect()

        elif "ارسل ايدي الشخص :" in str(event.text):
          await asyncio.sleep(wait_s)
          await editEventMsg(f"Sending {recv_id} ID ...")
          await client.send_message(m_bot, recv_id)

        elif "ارسل الكمية :" in str(event.text):
          await asyncio.sleep(wait_s)
          await editEventMsg(f"Sending Points Count ({points-million_fee}) ...")
          await client.send_message(m_bot, str(points - million_fee))
        
        elif "تم ارسال" in str(event.text):
          if "الى الشخص" in str(event.text):
            await editEventMsg("Done, Transfer Points Completed")
            points_link = None
            await asyncio.sleep(wait_s)
            await client.disconnect()

        elif "يجب ان يكون عدد التحويل 10 فأكثر" in str(event.text):
          await asyncio.sleep(wait_s)
          await editEventMsg("Faild To Create Points Link,Points Not Enough")
          await event.click(0)

        elif "تم حظرك لمده" in str(event.text):
          await editEventMsg("Blocked From The Bot -_-, Close This Session ...")
          await client.disconnect()
        
        elif "يجب ان نتحقق من انك لست روبوت" in str(event.text):
            await editEventMsg("Sending Contact To Verify Not Robot ...")
            await asyncio.sleep(5)
            if "verify_phone" in sessions[session]:
                r_phone = sessions[session]["verify_phone"]
            else:
                r_phone = "+144"+get_rand_int(8)
                sessions[session]["verify_phone"] = r_phone
                sessionsdb.edit(sessions[session])
            input_media_contact = InputMediaContact(phone_number=r_phone,first_name=my_user.first_name,last_name=my_user.last_name,vcard='')
            await client.send_file(m_bot, file=input_media_contact)
        
        elif "جهة الاتصال غير مطابقة مع حسابك" in str(event.text):
            await editEventMsg("Checking Robot Faild -_-")
            await asyncio.sleep(5)
            r_phone = my_user.phone
            if "verify_phone" in sessions[session]:
                if sessions[session]["verify_phone"] == r_phone:
                    sessions[session]["million_bot"] = False
                    sessionsdb.edit(sessions[session])
                    await client.send_message(m_bot, f"فشل فى تأكيد هذا الحساب {sessions[session]['phone']}")
                    await client.disconnect()
            sessions[session]["verify_phone"] = r_phone
            sessionsdb.edit(sessions[session])
            input_media_contact = InputMediaContact(phone_number=r_phone,first_name=my_user.first_name,last_name=my_user.last_name,vcard='')
            try:
                await client.send_file(m_bot, file=input_media_contact)
            except:
                pass
        
        elif "تم التحقق" in str(event.text):
            await editEventMsg("Checking Robot Completed ^_^")
            await asyncio.sleep(5)
            await client.send_message(m_bot, "/start 5885003956")
        
        elif "لان الرقم وهمي" in str(event.text):
            sessions[session]["million_bot"] = False
            sessionsdb.edit(sessions[session])
            bot.send_message(group_id,f"فشل فى تأكيد هذا الحساب, تم اعتبار الرقم وهمى، وتم إلغاء العمل فى سكربت لهذا الرقم {sessions[session]['phone']}")
            await editEventMsg("failed to verify contact")
            await client.disconnect()

      except FloodWaitError as e:
        await editEventMsg(f"FloodWaitError, Waiting {(int(e.seconds)+2800)/60} Minutes")
        sessions[session]["flood"] = int(round(datetime.now().timestamp())) + int(e.seconds)
        sessionsdb.edit(sessions[session])
        await asyncio.sleep(1)
        await editEventMsg("Disconnected For Some Time ...")
        await client.disconnect()
      except ChannelsTooMuchError:
       if sessions[session]["phone"] == phone and not max:
        max = True
        sessions[session]["million_bot"] = False
        sessions[session]["arab_bot"] = False
        sessions[session]["blue_bot"] = False
        sessions[session]["max"] = True
        sessionsdb.edit(sessions[session])
        bot.send_message(chat_id=group_id,text=f"هذا الرقم {phone} وصل إلى 500 قناة")
        await editEventMsg("This Account Reached 500 Channels ...")
        await client.send_message(m_bot, "/start 5885003956")
      except AuthKeyDuplicatedError:
       if sessions[session]["phone"] == phone and not sessions[session]["main"]:
        bot.send_message(group_id,f"الرقم ده {phone} جاب خطأ فى كود الجلسة, وتم إزالته من السيرفر")
        sessionsdb.delete(sessions[session])
        getSessions()
        disconnect = True
      except Exception:
        await client.send_message(m_bot, "/start 5885003956")


    await asyncio.sleep(wait_s)
    try:
      await editEventMsg("Sending /start Message ...")
      if points_link and phone == main_s["phone"]:
        await client.send_message(m_bot, "/start " + points_link.split("=")[1])
      else:
        await client.send_message(m_bot, "/start 5885003956")

    except telethon.errors.rpcerrorlist.FloodWaitError as e:
      await editEventMsg(f"FloodWaitError, Waiting {(int(e.seconds)+2800)/60} Minutes")
      sessions[session]["flood"] = int(round(datetime.now().timestamp())) + int(e.seconds)
      sessionsdb.edit(sessions[session])
      await asyncio.sleep(1)
      await editEventMsg("Disconnected For Some Time ...")
      await client.disconnect()

    except TypeError:
      await editEventMsg("Disconnected For Some Time ...")
      await client.disconnect()

    except YouBlockedUserError:
      await client(functions.contacts.UnblockRequest(id=m_bot))
      await asyncio.sleep(5)
    if disconnect:
      try:
        await client.disconnect()
      except:
        pass

    while client.is_connected() and not disconnect:
      try:
        await asyncio.sleep(15)
        dt = int(round(datetime.now().timestamp()))
        if (dt - last_time) > 55 and client.is_connected():
          await editEventMsg(f"Sending /start Message (Auto)... {auto_start}")
          auto_start += 1
          if phone == main_s["phone"] and points_link:
              await client.send_message(m_bot, "/start "+points_link.split("=")[1])
          else:
              await client.send_message(m_bot, "/start 5885003956")
        if auto_start > 10:
            disconnect = True
            await client.disconnect()
            auto_start = 0
            break
      except Exception:
        pass
    await asyncio.sleep(3)
    if max and points_link:
      pass
    elif not phone == main_s["phone"] and points_link:
      pass
      destroy_link = True
    else:
      session += 1
  else:
      try:
          await client.send_message("me", "test")
          bot.send_message(chat_id=group_id,text=f"هذا الرقم {phone} يعمل ولكن رفض تسجيل الدخول ")
      except UserDeactivatedBanError:
        if sessions[session]["phone"] == phone and not sessions[session]["main"]:
          sessionsdb.delete(sessions[session])
          bot.send_message(chat_id=group_id,text=f"تم حذف هذا الرقم {phone} نهائيا عن طريق طلب حذف الحساب وتم إزالته من السيرفر")
          getSessions()
          disconnect = True
      except AuthKeyUnregisteredError:
        if sessions[session]["phone"] == phone and not sessions[session]["main"]:
          sessionsdb.delete(sessions[session])
          bot.send_message(chat_id=group_id,text=f"تم إنهاء جلسة هذا الرقم {phone} نهائيا من نظام تليجرام, وتم إزالته من السيرفر, الرجاء تسجيل الدخول به مرة آخرى")
          getSessions()
          disconnect = True
      except Exception as e:
        if sessions[session]["phone"] == phone and not sessions[session]["main"]:
          sessionsdb.delete(sessions[session])
          getSessions()
          disconnect = True
          bot.send_message(chat_id=group_id,text=f"تم رفض عملية تسجيل الدخول لهذا الرقم {phone}, السبب : {str(e)}, تم حذف الرقم من السيرفر")
      session += 1
      disconnect = True


#        await client.run_until_disconnected()


def get_rand(count):
  return ''.join(random.choice("qwertyuiopasdfghjklzxcvbnm1234567890")for x in range(int(count)))


def get_rand_str(count):
  return ''.join(random.choice("qwertyuiopasdfghjklzxcvbnm") for x in range(int(count)))


def get_rand_int(count):
  return ''.join(random.choice("1234567890") for x in range(int(count)))


async def follow(client, channel):
  global max, m_bot, wait_s,phone
  try:
    channel = filterurl(channel, getlast=True)
    channel = await client.get_entity(channel)
    if isinstance(channel, telethon.tl.types.Channel):
      return await client(JoinChannelRequest(channel))
    else:
      return await client(ImportChatInviteRequest(hash=channel))
  except FloodWaitError as e:
   if not phone == main_s["phone"]:
    await editEventMsg(f"FloodWaitError, Waiting {(int(e.seconds)+2800)/60} Mintues")
    sessions[session]["flood"] = int(round(datetime.now().timestamp())) + int(e.seconds)
    sessionsdb.edit(sessions[session])
    await asyncio.sleep(1)
    await editEventMsg("Disconnected For Some Time ...")
    await client.disconnect()
    return None
  except ValueError:
    try:
      return await client(ImportChatInviteRequest(hash=channel))
    except UserAlreadyParticipantError:
      return True
    except Exception as e:
      await editEventMsg("Subscribe Error : " + str(e))
      if "a wait of" in str(e).lower() and not phone == main_s["phone"]:
        await editEventMsg("Disconnected For Some Time ...")
        await client.disconnect()
      elif "You have successfully requested to join" in str(e):
        await asyncio.sleep(10)
        return True
      else:
        return None
  except ChannelsTooMuchError:
   if sessions[session]["phone"] == phone and not max:
    max = True
    await editEventMsg("This Account Reached 500 Channels ...")
    sessions[session]["million_bot"] = False
    sessions[session]["arab_bot"] = False
    sessions[session]["blue_bot"] = False
    sessions[session]["max"] = True
    sessionsdb.edit(sessions[session])
    bot.send_message(chat_id=group_id,text=f"هذا الرقم {phone} وصل إلى 500 قناة")
   return None
  except UserAlreadyParticipantError:
    return True
  except Exception as e:
    await editEventMsg("Subscribe Error : " + str(e))
    if "a wait of" in str(e).lower() and not phone == main_s["phone"]:
      await editEventMsg("Disconnected For Some Time ...")
      await client.disconnect()
      return None
    elif "You have successfully requested to join" in str(e):
      await asyncio.sleep(wait_s)
      return None
    else:
      return None


def filterurl(url, end=" ", getlast=False):
  link = str(url)
  if int(link.find("http")) > -1:
    link = link[link.find("http"):]
  if int(link.find(end)) > -1:
    link = link[0:link.find(end)]
  link = link.replace(" ", "")
  if getlast:
    link = link.split("/")
    link = link[len(link) - 1]
  link = link.replace("+", "")
  link = link.replace("*", "")
  return link.strip()


async def editEventMsg(e):
  global event_action
  global points
  global client
  global my_id
  global phone, bot_user
  global channels, all_sessions_count, all_flood_sessions_count, all_user_points, main_s
  global sessions, my_user
  global session, bot
  global msg_id, user0
  msg = """
[Damkom Bot Script](https://t.me/{}?start=5885003956) {}
* User *: {}
* Name *: [{}](tg://user?id={})
* Phone *: {}
* UserId *: {}
* UserName *: `@{}`
* AccPoints *: {}
* SessionPoints *: {}
* UserPoints *: {}
* Channel *: {}/50
* Session *: {}/{}
* All Sessions *: {}
* Flood Sessions *: {}

~> *{}*

Made By [𝗠𝗮𝗛𝗠𝗼𝘂𝗗](tg://user?id=1502342753) 💝
"""
  try:
    usn = my_user.username
    if not usn:
        usn = ""
  except:
    pass
  try:
    msg = msg.format(bot_user, str(datetime.now(pytz.timezone("Egypt")).strftime("%Y/%m/%d %I:%M %p")), str(user0), str(my_user.first_name), str(my_user.id),str(phone), str(my_id),str(usn), str(points), str(main_s["points"]), str(all_user_points), str(len(channels)),str(int(session) + 1), str(len(sessions)), str(all_sessions_count), str(all_flood_sessions_count), str(e))
    bot.edit_message_text(chat_id=event_action, text=msg, message_id=msg_id, parse_mode="markdown", disable_web_page_preview=True)
  except Exception:
    pass
  #os.system("clear")
  m = """
[*] connected to {}
  [~] Points : {}
  [~] Channels : {}/50
  [~] Sessions : {}/{}
  [~] FloodS : {}
[~>] {}
  """
  m = m.format(phone, points, len(channels), str(int(session) + 1), str(len(sessions)), str(all_flood_sessions_count), str(e))
  print(e)





















def run(session):
  asyncio.new_event_loop().run_until_complete(main(session))



#for session in sessions:
#    if session["million_bot"]:
#        threading.Thread(target=run, args=[session["phone"], session["api_id"], session["api_hash"]]).start()
#        time.sleep(10)



while True:

    d = json.loads(os.environ['config'])

    #put Your User Here
    user0 = d["user"]
    #put Main Phone Here
    main_phone = d["main_phone"]
    #put Here Bot Message Id
    msg_id = d["msg_id"]
    #put Here Chat Link
    group_link = d["group_link"]
    #put Here Chat Id
    group_id = d["group_id"]
    #put Here Max Points To Transfer
    max_points = int(d["max_points"])
    #put Here Start Index
    start_index = int(d["start_index"])
    #put Here End Index
    end_index = int(d["end_index"])
    #tele_damkom recv_id
    recv_id = d["recv_id"]
    #put Wait Seconds Here
    wait_s = 4
    #put Billion Bot Transfer Fee Here
    million_fee = 0
    
    all_user_points = 0
    getSessions()
    if not bot:
        bot = telebot.TeleBot(d["token"])
    
    
    
    
    
    if end_index >= len(sessions):
        end_index = len(sessions)-1
        
    if start_index >= len(sessions):
        bot.send_message(chat_id=group_id,text=f"لا يوجد جلسات متاحه لهذا السكربت و جارى انتظار جلسات جديدة")
        print("No Sessions Available, Search For It ...")
        while True:
            time.sleep(600)
            getSessions()
            if start_index < len(sessions):
                break
    
    if not sessions:
        bot.send_message(chat_id=group_id,text="لا يوجد جلسات لهذا المستخدم {user0}, وجارى انتظار إضافة جلسات جديدة")
        print("This User Didn't Have Any Sessions, Waiting To Add It ...")
        while True:
            time.sleep(600)
            getSessions()
            if sessions:
                break
    
    for i in range(start_index, end_index+1):
        s = sessions[i]
        if not "running" in s:
            s["running"] = False
            sessionsdb.edit(s)
        elif s["running"]:
            s["running"] = False
            sessionsdb.edit(s)
    
    
    my_id = None
    checker = True
    channels = []
    event_action = None
    points = 0
    last_time = 0
    event_e = None
    phone = None
    max = False
    m_bot = None
    bot_user = "DamKombot"
    last_channel = None
    new_user = False
    bot_event = None
    my_user = None
    disconnect = False
    auto_start = 0
    
    
    if session > start_index:
      run(session)
    elif sessions:
      run(start_index)
    else:
      print("No Sessions Avalible")
   
  
 












