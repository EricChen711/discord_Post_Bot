import os
import datetime
import discord
import json,random
import requests
import re
import tweepy
import random
import codecs
import urllib.request
import ehapi  
import asyncio,validators,aiohttp,aiofiles,io
from discord.ext import commands
from discord import User
from core.classes import Cog_Extension
from plurk_oauth import PlurkAPI
from pathlib import Path
from bs4 import BeautifulSoup
from lxml import html
from xml.sax import saxutils as su

ICON_PIXIV = "https://cdn.discordapp.com/attachments/881168385507999798/883280819085520916/pixiv.png"
ICON_TWITTER = "https://cdn.discordapp.com/attachments/881168385507999798/883411224426070086/pngegg.png"
ICON_PLURK = "https://cdn.discordapp.com/attachments/881168385507999798/883280952510525500/plurk.jpg"
ICON_YANDE = "https://cdn.discordapp.com/attachments/881168385507999798/883285343107960842/yande.jpg"
ICON_SANKAKU = "https://cdn.discordapp.com/attachments/881168385507999798/883280516676202556/sankaku.png"
ICON_MELONBOOKS = "https://cdn.discordapp.com/attachments/881168385507999798/883264713159499796/melonbooks.png"
ICON_DISCORD = "https://cdn.discordapp.com/attachments/881168385507999798/884792515511857202/discord.png"

class Event(Cog_Extension):
   def __init__(self,bot:commands.Bot)->None:
      self.bot=bot


   #以下pixiv
   p1=re.compile('www\.pixiv\.net\/member_illust\.php')
   p2=re.compile('www\.pixiv\.net\/artworks')
   p3=re.compile('www\.pixiv\.net\/en\/artworks')
   #以下twitter
   p4=re.compile('twitter\.com\/(\w{0,60})\/status')
   p5=re.compile('t\.co\/')
   #以下plurk
   p6=re.compile('www\.plurk\.com\/p')
   #以下eh
   p7=re.compile('e-hentai\.org\/g\/')
   p8=re.compile('exhentai\.org\/g\/')
   #以下yande
   p9=re.compile('yande\.re\/post\/show\/')
   p10=re.compile('https:\/\/files\.yande\.re\/sample\/.*\.jpg","sample_width')
   #以下sankaku
   p11=re.compile('chan\.sankakucomplex\.com(\/ja)?\/post\/show\/\d+')
   p12=re.compile('\/\/(s|v)\.sankakucomplex\.com\/data\/sample\/.*\" property=og:image')
   #以下ptt
   p13=re.compile('www\.ptt\.cc\/bbs\/.*\.html')
   p14=re.compile('ptthito\.com\/.*')
   #以下melonbooks
   p15=re.compile('www\.melonbooks\.co\.jp\/detail\/detail\.php\?product_id=\d+')
   DISCORD_MEDIA=re.compile('(media|cdn)\.discordapp\.(net|com)\/attachments\/\d+\/\d+\/.*\.(jpg|jpeg|png|bmp|tif|TIFF|svg|gif)')
   #以下webm
   p16=re.compile("https://\S{3,50}.webm")
   
   with open('setting.json','r',encoding='utf8') as jfile:
      jdata=json.load(jfile)
   
   # Random User Agent List
   USER_AGENT_LIST = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
   ]

   USER_AGENT = random.choice(USER_AGENT_LIST)
   headers = {
     'user-agent': USER_AGENT
   }

   list_message_id=[]
   list_emojiname=[]
   list_roleassign=[]
   list_badGuy=[]
   roleAssign=True
   badGuyAssign=True

   @commands.Cog.listener()
   async def on_raw_reaction_add(self,payload):
      if not self.badGuyAssign:
         pass
      else:
         with open('setting.json','r',encoding='utf8') as jfile:
            jdata=json.load(jfile)
         self.list_badGuy=[]
         for i in range(len(jdata['badGuy'])):
            self.list_badGuy.append(jdata['badGuy'][i]['member_id'])
         self.badGuyAssign=False

      if not self.roleAssign:
         pass
      else:
         with open('setting.json','r',encoding='utf8') as jfile:
            jdata=json.load(jfile)
         self.list_message_id=[]
         self.list_emojiname=[]
         self.list_roleassign=[]
         for i in range(len(jdata['emoji_role'])):
            self.list_message_id.append(jdata['emoji_role'][i]['message_id'])
            self.list_emojiname.append(jdata['emoji_role'][i]['emojiname'])
            self.list_roleassign.append(jdata['emoji_role'][i]['roleassign'])
         self.roleAssign=False

      for i in range(len(self.list_message_id)):
         if payload.message_id==self.list_message_id[i] and payload.emoji.name==self.list_emojiname[i]:
            role = discord.utils.get(payload.member.guild.roles, name=self.list_roleassign[i])
            if payload.member.id not in self.list_badGuy:
               await payload.member.add_roles(role)
               print(payload.member,self.list_roleassign[i])
            else:
               print(payload.member,"在黑名單")
               break

      channel = await self.bot.fetch_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      url=""
      # Reload the url
      if message.author.id==self.bot.user.id and payload.emoji.name=="idk":
         print(message.embeds)
         if message.embeds!=[]:
            url=message.embeds[0].image.url
            p1=re.compile('\#')
            a=p1.search(url)
            if a==None:
               url+="#1"
            else:
               num=int(url[a.start()+1:])+1
               url=url[:a.start()]+"#"+str(num)
            embed=message.embeds[0]
            embed.set_image(url=url)
            await message.edit(embed=embed)
         else:
            url=message.content
            p1=re.compile('\#')
            a=p1.search(url)
            if a==None:
               url+="#1"
            else:
               num=int(url[a.start()+1:])+1
               url=url[:a.start()]+"#"+str(num)
            await message.edit(content=url)
      # Delete the bot message
      if message.author.id==self.bot.user.id and payload.emoji.name=="pepe4":
         for reaction in message.reactions:
            if reaction.emoji.name=='pepe4':
               if reaction.count>=1:
                  await message.delete()

   @commands.Cog.listener()
   async def on_message(self,msg):
      k=False
      chr={}
      strf=''
      askNum=1
      twitterMedia=None
      
      isExplicit=False
      # check message is explicit ?
      if msg.content.count("||") >= 2:
        isExplicit=True
        msg.content.replace("||","")
        
      print(msg.author,msg.content)

      #綜合篩選身分組
      if (msg.channel.id ==self.jdata['sfwchannel']):

         roleList1=msg.author.roles
         roleList2=[]
         for roles in roleList1:
            roleList2.append(roles.name)
         if ("想貼圖的島民" not in roleList2):
            return

      #以下pixiv
      a=self.p1.search(msg.content)
      if a==None:
         a=self.p2.search(msg.content)
         if a==None:
            a=self.p3.search(msg.content)
      if a!=None:
         k=True
         strf = re.search('\d{3,9}', msg.content[a.start():]).group()

      for i in range(len(msg.embeds)):
         chr=msg.embeds[i].to_dict()

      if k and msg.author!=self.bot.user:
         colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
         uId,uName,illustTitle,illustComment,pageCount,image_url,imageProfile_url,description,timestamp = self.pixivMetadata(strf)
         embed=discord.Embed(title=illustTitle,url="https://www.pixiv.net/artworks/"+strf, color=colonn, timestamp=timestamp)
         embed.set_author(name=uName, url="https://www.pixiv.net/users/"+uId, icon_url=ICON_PIXIV)
         embed.add_field(name="Author", value="["+uName+"]("+"https://www.pixiv.net/users/"+uId+")", inline=True)
         embed.add_field(name="Illust ID", value="["+strf+"]("+"https://www.pixiv.net/artworks/"+strf+")", inline=True)
         embed.description = description
         embed.set_footer(text="Pixiv | By "+str(msg.author.display_name)+" ")
         if "ugoira" in image_url:
            image_url, edit_imageProfile_url = self.pixivDLGIF2URL(uId,image_url,imageProfile_url)
            # pre-cache for server
            requests.get(image_url,headers = self.headers)
            requests.get(image_url,headers = self.headers)
            if isExplicit:
                embed.set_thumbnail(url=edit_imageProfile_url)
                await msg.channel.send(embed=embed)
                await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                embed.set_image(url=image_url)
                embed.set_thumbnail(url=edit_imageProfile_url)
                await msg.channel.send(embed=embed)
         elif pageCount>1:
            askpage = re.search('P\d{1,2}', msg.content[a.start():].upper())
            allpage = re.search('ALL', msg.content[a.start():].upper())
            if askpage:
               if int(askpage.group()[1:])>0 and int(askpage.group()[1:])<pageCount+1:
                  askNum=int(askpage.group()[1:])
                  pageNum="_p"+str(askNum-1)
                  edit_image_url, edit_imageProfile_url = self.pixivDL2URL(uId,image_url.replace('_p0',pageNum),imageProfile_url)
                  if isExplicit:
                      embed.set_thumbnail(url=edit_imageProfile_url)
                      await msg.channel.send(embed=embed)
                      await msg.channel.send(self.msgSendProcess(edit_image_url, isExplicit))
                  else:
                      embed.set_image(url=edit_image_url)
                      embed.set_thumbnail(url=edit_imageProfile_url)
                      await msg.channel.send(embed=embed)
                      
            if not askpage:
                edit_image_url, edit_imageProfile_url = self.pixivDL2URL(uId,image_url,imageProfile_url)
                if isExplicit:
                      embed.set_thumbnail(url=edit_imageProfile_url)
                      await msg.channel.send(embed=embed)
                      await msg.channel.send(self.msgSendProcess(edit_image_url, isExplicit))
                else:
                      embed.set_image(url=edit_image_url)
                      embed.set_thumbnail(url=edit_imageProfile_url)
                      await msg.channel.send(embed=embed)
                  
            if allpage:
               for page in range(2,pageCount+1):
                    pageNum="_p"+str(page-1)
                    edit_image_url, edit_imageProfile_url = self.pixivDL2URL(uId,image_url.replace('img-master','img-original').replace('_p0',pageNum),imageProfile_url)
                    await msg.channel.send(self.msgSendProcess(edit_image_url, isExplicit))
         else:
            edit_image_url, edit_imageProfile_url = self.pixivDL2URL(uId,image_url,imageProfile_url)
            if isExplicit:
                embed.set_thumbnail(url=edit_imageProfile_url)
                await msg.channel.send(embed=embed)
                await msg.channel.send(self.msgSendProcess(edit_image_url, isExplicit))
            else:
                embed.set_image(url=edit_image_url)
                embed.set_thumbnail(url=edit_imageProfile_url)
                await msg.channel.send(embed=embed)
         try:
            await asyncio.sleep(1.5)
            await msg.edit(suppress=True)
         except:
            print('沒有關閉embed的權限')
            
      #以下twitter
      a=self.p4.search(msg.content)
      if a!=None:
         #twitter oauth
         auth = tweepy.OAuthHandler(self.jdata['consumer_key'], self.jdata['consumer_secret'])
         auth.set_access_token(self.jdata['access_token'], self.jdata['access_token_secret'])
         api = tweepy.API(auth)
      
         strf = re.search('\d{15,20}', msg.content[a.start():]).group()
         status = api.get_status(strf, tweet_mode="extended")

         colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
         uId=status.user.screen_name
         uName=status.user.name
         timestamp=status.created_at
         retweet_count=status.retweet_count
         favorite_count=status.favorite_count
         imageProfile_url = status.user.profile_image_url_https.replace('_normal','_400x400')
         try:
             tweet_link=status.extended_entities['media'][0]['url']
             description=status.full_text.replace(tweet_link,'')
         except:
             description=status.full_text

         embed=discord.Embed(title='',url="https://twitter.com/"+uId+"/status/"+strf, color=colonn, timestamp=timestamp)
         embed.set_author(name=uName+"(@"+uId+")", url="https://twitter.com/"+uId, icon_url=ICON_TWITTER)
         embed.add_field(name="Retweets", value=retweet_count, inline=True)
         embed.add_field(name="Likes", value=favorite_count, inline=True)
         embed.description = self.html_decode(description)
         embed.set_thumbnail(url=imageProfile_url)
         embed.set_footer(text="Twitter | By "+str(msg.author.display_name)+" ")
         try:
            twitterMedia=status.extended_entities['media']
            k=True
         except AttributeError:  #twitter沒圖片
            await msg.channel.send(embed=embed)
         if k and msg.author!=self.bot.user:

            try:
                twitterMedia=status.extended_entities['media'][0]['video_info']
                bitrate = 0
                maxIndex = 0
                for index in range(len(twitterMedia['variants'])):
                    if twitterMedia['variants'][index]['content_type'] == "video/mp4" and twitterMedia['variants'][index]['bitrate'] > bitrate:
                        bitrate = twitterMedia['variants'][index]['bitrate']
                        maxIndex = index
                await msg.channel.send(embed=embed)
                await msg.channel.send(self.msgSendProcess(twitterMedia['variants'][maxIndex]['url'], isExplicit))
            except KeyError:  #twitter沒影片
               image_url=twitterMedia[0]['media_url_https']+":orig"
               if isExplicit:
                   await msg.channel.send(embed=embed)
                   await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
               else:
                   embed.set_image(url=image_url)
                   await msg.channel.send(embed=embed)
               for i in range(1,len(status.extended_entities['media'])):
                  await msg.channel.send(self.msgSendProcess(twitterMedia[i]['media_url_https']+":orig", isExplicit))
         try:
            await asyncio.sleep(1.5)
            await msg.edit(suppress=True)
         except:
            print('沒有關閉embed的權限')
                  
      #以下plurk
      a=self.p6.search(msg.content)
      if a!=None:
         # plurk info
         url = re.search("(?P<url>https?://www.plurk.com/p/[^\s]{6})", msg.content).group("url")
         plurk_id = int((url.rsplit('/', 1)[-1]), 36)
         plurk_image_format = re.compile("(?P<url>https?://images.plurk.com/[^\s]+.(?:png|jpg|gif))")
         
         # plurk oauth
         plurk = PlurkAPI(self.jdata['plurk_consumer_key'], self.jdata['plurk_consumer_secret'])
         plurk.authorize(self.jdata['plurk_access_token'], self.jdata['plurk_access_token_secret'])
         json_object_string = plurk.callAPI('/APP/Timeline/getPlurk', options={'plurk_id': plurk_id})        

         owner_id = json_object_string['plurk']['owner_id']
         nick_name = json_object_string['plurk_users'][str(owner_id)]['nick_name']
         avatar = json_object_string['plurk_users'][str(owner_id)]['avatar']
         display_name = json_object_string['plurk_users'][str(owner_id)]['display_name']
         content_raw = json_object_string['plurk']['content_raw'].replace("\n\n","\n")
         description = re.sub("(?P<url>https?://images.plurk.com/[^\s]+\.(?:png|jpg|gif))", '', content_raw)
         favorite_count = json_object_string['plurk']['favorite_count']
         response_count = json_object_string['plurk']['response_count']
         replurkers_count = json_object_string['plurk']['replurkers_count']
         posted = json_object_string['plurk']['posted']
         timestamp = datetime.datetime.strptime(posted, '%a, %d %b %Y %H:%M:%S %Z')
         
         colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
         embed=discord.Embed(title='', color=colonn, timestamp=timestamp)
         embed.set_author(name=display_name+"(@"+nick_name+")", url="https://www.plurk.com/"+nick_name, icon_url=ICON_PLURK)
         embed.set_thumbnail(url="https://avatars.plurk.com/"+str(owner_id)+"-big"+str(avatar)+".jpg")
         embed.set_footer(text="Plurk | By "+str(msg.author.display_name)+" ")
         embed.add_field(name="喜歡", value=favorite_count, inline=True)
         embed.add_field(name="轉噗", value=replurkers_count, inline=True)
         embed.add_field(name="回應", value=response_count, inline=True)
         embed.description = description
         if json_object_string:
             try:
                 image_url = re.search(plurk_image_format, content_raw).group("url")
                 if image_url:
                     if isExplicit:
                         await msg.channel.send(embed=embed)
                         await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
                     else:
                         embed.set_image(url=image_url)
                         await msg.channel.send(embed=embed)
                 allpage = re.search('ALL', msg.content[a.start():].upper())
                 if allpage:
                    image_urls = re.findall("(?P<url>https?://images.plurk.com/(?!mx_)[^\s]+.(?:png|jpg|gif))", content_raw, re.DOTALL)
                    image_urls_dedupe = []
                    for index in range(len(image_urls)):
                        if image_urls[index] not in image_urls_dedupe:
                            image_urls_dedupe.append(image_urls[index])
                    list_len = len(image_urls_dedupe)
                    for index in range(1,list_len):
                            await msg.channel.send(self.msgSendProcess(image_urls_dedupe[index], isExplicit))
             except AttributeError:  #plurk沒圖片
                 await msg.channel.send(embed=embed)
                 
             try:
                  await asyncio.sleep(1.5)
                  await msg.edit(suppress=True)
             except:
                  print('沒有關閉embed的權限')
         else:
             print("plurk not found")
             
      #以下eh
      a=self.p7.search(msg.content)
      ispage = 0
      if a==None:
         a=self.p8.search(msg.content)
         if a==None:
            a=ehapi.page_token.search(msg.content)
            if a!=None:
                ispage = 1
      if a!=None:
            if msg.channel.id ==self.jdata['sfwchannel']:
                isExplicit=True
            galleries = ehapi.get_galleries(msg.content)
            if galleries:
                if len(galleries) > 5:  # don't spam chat too much if user spams links
                    await msg.channel.send(embed=ehapi.embed_titles(galleries))
                else:
                    for gallery in galleries:
                        await msg.channel.send(embed=ehapi.embed_full(gallery, isExplicit))
                        if isExplicit:
                            await msg.channel.send(self.msgSendProcess(gallery['thumb'], isExplicit))
            '''
            if ispage:
                url = re.search('(?P<url>https?:\/\/e[\-x]hentai\.org\/s\/([\da-f]{10})\/(\d+)\-(\d+))', msg.content).group("url")
                page_token = url.rsplit('/', -1)[-2]
                gid = url.rsplit('/', 1)[-1].split('_', 1)[0].split('-', 1)[0]
                page = url.rsplit('/', 1)[-1].split('_', 1)[0].split('-', 1)[1]
                r =  requests.get(url,headers = {'ipb_member_id': self.jdata['eh_ipb_member_id'], 'ipb_pass_hash': self.jdata['eh_ipb_pass_hash']})
                key = re.compile(';key=\w+\"').search(r.text).group(0)[:-1][5:]
                download_url = "https://e-hentai.org/fullimg.php?gid="+gid+"&page="+page+"&key="+key
                img_name = page_token + ".jpg"
                print(download_url)
                IMG_DIR = self.jdata['IMG_DIR']
                DOMAIN = self.jdata['DOMAIN']
                PROJECT_DIR = "/home32/ch010060/downloads/github/kentaiBot2/"
                command = "aria2c --load-cookies='" + PROJECT_DIR +"cookies.txt' '"+ download_url + "' && mv $(ls *.{png,jpg} 2>/dev/null) " + IMG_DIR + img_name
                print(command)
                os.system(command)
                domain_url = DOMAIN + img_name
                await msg.channel.send(domain_url)
            '''
            try:
                if not isExplicit:
                    await asyncio.sleep(1.5)
                    await msg.edit(suppress=True)
            except:
               print('沒有關閉embed的權限')
               
      #以下yande
      a=self.p9.search(msg.content)
      if a!=None:
        url = re.search('(?P<url>https?:\/\/yande\.re\/post\/show\/(\d+))', msg.content).group("url")
        r =  requests.get(url,headers = self.headers)
        if r.text.find("Rating: Explicit") != -1:
            image_url = self.p10.search(r.text).group(0)[:-15]
            colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
            if isExplicit:
                await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                embed=discord.Embed(title='yande.re',url=image_url, color=colonn)
                embed.set_image(url=image_url)
                embed.set_thumbnail(url=ICON_YANDE)
                embed.set_footer(text="yande.re | By "+str(msg.author.display_name)+" ")
                await msg.channel.send(embed=embed)
            try:
                await asyncio.sleep(1.5)
                await msg.edit(suppress=True)
            except:
                print('沒有關閉embed的權限')
                
      #以下sankaku
      a=self.p11.search(msg.content)
      if a!=None:
        try:
            url = re.search('(?P<url>https?:\/\/chan\.sankakucomplex\.com(\/ja)?\/post\/show\/(\d+))', msg.content).group("url")
            r =  requests.get(url,headers={'user-agent': self.USER_AGENT, 'login': self.jdata['SANKAKU_ID'], 'pass_hash': self.jdata['SANKAKU_PASS_HASH'], 'PHPSESSID': self.jdata['SANKAKU_PHPSESSID']})
            image_url = "https:" + self.p12.search(r.text).group(0)[:-19]
            colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
            if isExplicit:
                await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                embed=discord.Embed(title='chan.sankakucomplex.com',url=image_url, color=colonn)
                embed.set_image(url=image_url)
                embed.set_thumbnail(url=ICON_SANKAKU)
                embed.set_footer(text="SankakuComplex | By "+str(msg.author.display_name)+" ")
                await msg.channel.send(embed=embed)
            try:
                if not isExplicit:
                    await asyncio.sleep(1.5)
                    await msg.edit(suppress=True)
            except:
                print('沒有關閉embed的權限')
        except:
                print('fetch fail')
                
      #以下ptt
      a=self.p13.search(msg.content)
      if a==None:
         a=self.p14.search(msg.content)
      if a!=None:
        # rewrite to moptt url
        try:
            url = re.search('(?P<url>https?:\/\/www\.ptt\.cc\/bbs\/.*\/.*\.html)', msg.content).group("url")
            if url:
                url = url.replace("www.ptt.cc","www.pttweb.cc").replace(".html","")
            #url = url.rsplit('/', 1)[0].replace("www.ptt.cc/bbs","moptt.tw/p") + "." + url.rsplit('/', 1)[1].replace(".html","")
        except:
            url = re.search('(?P<url>https?:\/\/ptthito\.com\/.*\/.*\/)', msg.content).group("url")
            if url[-1:] == "/":
                url = url[:-1]
            url = url.replace("ptthito.com","www.pttweb.cc").replace(".html","")
        await msg.channel.send(self.msgSendProcess(url, isExplicit))
        try:
            await asyncio.sleep(1.5)
            await msg.edit(suppress=True)
        except:
            print('沒有關閉embed的權限')
            
      #以下melonbooks
      a=self.p15.search(msg.content)
      if a!=None:
            url = re.search('(?P<url>https?:\/\/www\.melonbooks\.co\.jp\/detail\/detail.php\?product_id=\d+)', msg.content).group("url")
            image_url,title,circle,author,release_date,type,page,description,age = self.melonbooksMetadata(url)
            colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
            embed=discord.Embed(title=title,url=url, color=colonn)
            embed.set_author(name=author+" ("+circle+")", url="https://www.melonbooks.co.jp/search/search.php?name="+author+"&text_type=author")
            embed.set_footer(text="Melonbooks | "+page + " pages | By "+str(msg.author.display_name)+" ")
            embed.add_field(name="発行日", value=release_date, inline=True)
            embed.add_field(name="ジャンル", value=type, inline=True)
            embed.add_field(name="作品種別", value=age, inline=True)
            embed.set_thumbnail(url=ICON_MELONBOOKS)
            embed.description = description
            if isExplicit:
                await msg.channel.send(embed=embed)
                await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                embed.set_image(url=image_url)
                await msg.channel.send(embed=embed)
            try:
                await asyncio.sleep(1.5)
                await msg.edit(suppress=True)
            except:
                print('沒有關閉embed的權限')
                
      #以下discord media
      try:
         a=self.DISCORD_MEDIA.search(msg.attachments[0].url)
         media_channel_list = self.jdata['mediachannel']
         msg_channel_id=str(msg.channel.id)
         if hasattr(msg.channel,"parent_id"):
            msg_channel_id=str(msg.channel.parent_id)
         
         if a!=None and (msg_channel_id in media_channel_list or str(msg.channel.id) == "881168385507999798") and not msg.content.startswith('🍆'):
            colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
            for i in range(len(msg.attachments)):
                image_url = self.msgMedia2URL(msg.attachments[i].url, msg.author.id)
                if i == 0:
                    embed=discord.Embed(color=colonn, timestamp=msg.created_at)
                    #embed.set_author(name=msg.author, icon_url=ICON_DISCORD)
                    embed.set_author(name=msg.author, icon_url=msg.author.avatar.url)
                    embed.set_image(url=image_url)
                    embed.set_footer(text="Discord | By "+str(msg.author.display_name)+" ")
                    #embed.set_thumbnail(url=msg.author.avatar_url)
                    embed.description = msg.content
                    await msg.delete()
                    await msg.channel.send(embed=embed)
                else:
                    await msg.channel.send(image_url)
      except:
        pass # 無media
                
      #以下webm
      
      a=self.p16.search(msg.content)
      if a!=None:
         URL=a.group()
         if validators.url(URL):
            async with aiohttp.ClientSession(headers=self.headers) as session:
               async with session.get(URL) as resp:
                  if resp.status == 200 and resp.headers['Content-Type'] =="video/webm":
                     f = await aiofiles.open("temp.webm", mode='wb')
                     await f.write(await resp.read())
                     await f.close()
                     while True:
                        if os.path.exists("temp.mp4"):
                           await asyncio.sleep(0.5)
                        else:
                           break
                     os.system("ffmpeg -i temp.webm -preset veryfast -loglevel quiet temp.mp4")

                     data = io.BytesIO(await resp.read())
                     tempChannel = await self.bot.fetch_channel(self.jdata["temppicchannel"])
                     tempMessage=await tempChannel.send(file=discord.File("temp.mp4"))
                     picURL=tempMessage.attachments[0].url
                     await msg.channel.send(content=msg.author.display_name+"轉貼了一組webm網址：",reference=msg.reference)
                     await msg.channel.send(picURL)
                     os.remove("temp.mp4")
                     try:
                        await asyncio.sleep(1.5)
                        await msg.edit(suppress=True)
                     except:
                        print('沒有關閉embed的權限')

   # post process msg content
   def msgSendProcess(self,str,isExplicit):
        if not isExplicit:
            return str
        else:
            return "|| " + str + " ||"
   
   # get melonbooks metadata
   def melonbooksMetadata(self,url):
        R_COOKIE = {'AUTH_ADULT': '1'}
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        r = s.get(url, allow_redirects=False, cookies=R_COOKIE, headers=self.headers)
        if r.status_code != 200:
            print("Connect failed")
        else:
            tree = html.fromstring(r.content)
            image_url = tree.xpath('//meta[@property="og:image"]/@content')[0].split('&',1)[0]
            title = tree.xpath('//meta[@property="og:title"]/@content')[0].rsplit("（",1)[0]
            circle = tree.xpath('//meta[@property="og:title"]/@content')[0].rsplit("（",1)[1].rsplit("）",1)[0]
            description = ''.join(tree.xpath('//*[@style="padding:5px;border:1px dotted #ccc;"]/text()')).replace(" ", "")
            age = tree.xpath('//*[@class="stripe"]/tr/th[contains(text(), "作品種別")]/../td/text()')[0]
            # Some works without following attribute
            try:
                type = tree.xpath('//*[@class="stripe"]/tr/th[contains(text(), "ジャンル")]/../td/a/text()')[0]
            except:
                type = "N/A"
            try:
                release_date = tree.xpath('//*[@class="stripe"]/tr/th[contains(text(), "発行日")]/../td/text()')[0]
            except:
                release_date = "N/A"
            try:
                author = tree.xpath('//*[@class="stripe"]/tr/th[contains(text(), "作家名")]/../td/a/text()')[0]
            except:
                author = ""
            try:
                page = tree.xpath('//*[@class="stripe"]/tr/th[contains(text(), "総ページ数・CG数・曲数")]/../td/text()')[0]
            except:
                page = "N/A"
            
            return image_url,title,circle,author,release_date,type,page,description,age

   # get pixiv metadata
   def pixivMetadata(self,id):
        r =  requests.get("https://www.pixiv.net/artworks/"+id,headers = self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        meta=soup.select("meta#meta-preload-data")
        content=meta[0].get('content')
        content=content.replace('false','\"false\"').replace('true','\"true\"').replace('null','\"null\"')

        jdata=json.loads(content)
        
        uId = jdata['illust'][id]['userId']
        uName = jdata['illust'][id]['userName']
        illustTitle = jdata['illust'][id]['illustTitle']
        illustComment = jdata['illust'][id]['illustComment']
        pageCount = jdata['illust'][id]['userIllusts'][id]['pageCount']
        image_url = jdata['illust'][id]['urls']['original']
        imageProfile_url = jdata['user'][uId]['imageBig']
        description = self.cleanhtml(jdata['illust'][id]['description'].replace("<br />","\n"))
        timestamp = datetime.datetime.strptime(jdata['illust'][id]['createDate'], '%Y-%m-%dT%H:%M:%S%z')
        
        return uId,uName,illustTitle,illustComment,pageCount,image_url,imageProfile_url,description,timestamp
        
   # download pixiv image and return image url on server
   def pixivDL2URL(self,uId,img_url,imageProfile_url):
        IMG_DIR = self.jdata['IMG_DIR']
        DOMAIN = self.jdata['DOMAIN']
    
        # Get image id and extension
        img_id = img_url.rsplit('/', 1)[-1].split('_', 1)[0]
        img_page = img_url.rsplit('/', 1)[-1].split('_', 1)[1].split('.',1)[0].split('_',1)[0]
        img_path = os.path.join(IMG_DIR, img_id + "_" + img_page +".jpg")
        imgProfile_path = os.path.join(IMG_DIR, uId + "_profile.jpg")

        # Create opener with pixiv referer
        opener = urllib.request.build_opener()
        opener.addheaders = [('user-agent', self.USER_AGENT)]
        opener.addheaders = [('referer','https://www.pixiv.net/')]
        urllib.request.install_opener(opener)

        # Check profile image does exist ?
        if not os.path.isfile(imgProfile_path):
            # Download profile image
            urllib.request.urlretrieve(imageProfile_url, imgProfile_path)
        
        # Check image does exist ?
        if not os.path.isfile(img_path):
            # Download image
            urllib.request.urlretrieve(img_url, img_path)
            
            # Compress image with imagemagic
            command = "convert " + img_path + " " + img_path
            os.system(command)
        
        domain_url = DOMAIN + img_id + "_" + img_page +".jpg"
        print(domain_url)
        domain_imageProfile_url = DOMAIN + uId + "_profile.jpg"
        print(domain_imageProfile_url)
        return domain_url, domain_imageProfile_url
        
   # download pixiv animate image by pixivutil and return image url on server
   def pixivDLGIF2URL(self,uId,img_url,imageProfile_url):
        IMG_DIR = self.jdata['IMG_DIR']
        DOMAIN = self.jdata['DOMAIN']
    
        # Get image id
        img_id = img_url.rsplit('/', 1)[-1].split('_', 1)[0]
        img_path = os.path.join(IMG_DIR, img_id + ".gif")
        imgzip_path = os.path.join(IMG_DIR, img_id + ".zip")
        imgProfile_path = os.path.join(IMG_DIR, uId + "_profile.jpg")
        
        # Create opener with pixiv referer
        opener = urllib.request.build_opener()
        opener.addheaders = [('user-agent', self.USER_AGENT)]
        opener.addheaders = [('referer','https://www.pixiv.net/')]
        urllib.request.install_opener(opener)
        
        # Check profile image does exist ?
        if not os.path.isfile(imgProfile_path):
            # Download profile image
            urllib.request.urlretrieve(imageProfile_url, imgProfile_path)
            
        # Check image does exist ?
        if not os.path.isfile(img_path): 
            # Download image
            imgzip_url = img_url.replace("/img-original/", "/img-zip-ugoira/").replace('_ugoira0.jpg','_ugoira600x600.zip')
            urllib.request.urlretrieve(imgzip_url, imgzip_path)
            
            # Convert zip to gif with ffmpeg
            command = "cd "+IMG_DIR+" && 7z x -o"+img_id+" "+img_id+".zip && rm "+img_id+".zip && gifgen -o "+img_id+".gif "+img_id+"/%06d.jpg && rm -rf "+img_id
            os.system(command)
        
        domain_url = DOMAIN + img_id + ".gif"
        print(domain_url)
        domain_imageProfile_url = DOMAIN + uId + "_profile.jpg"
        print(domain_imageProfile_url)
        return domain_url, domain_imageProfile_url
        
   # get discord media
   def msgMedia2URL(self,img_url,author_id):
        MEDIA_PATH = "media"
        IMG_DIR = self.jdata['IMG_DIR']
        DOMAIN = self.jdata['DOMAIN']
        
        # Get timestamp, msg author, channel id, image id, image extension
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        channel_id = img_url.rsplit('/', -1)[-3]
        image_id = img_url.rsplit('/', -1)[-2]
        image_ext = img_url.rsplit('/', 1)[-1].rsplit('.',-1)[-1]
        if image_ext != "gif":
            img_filename = timestamp + "_" + channel_id + "_" + str(author_id) + ".jpg"
        else:
            img_filename = timestamp + "_" + channel_id + "_" + str(author_id) + ".gif"
        img_path = os.path.join(IMG_DIR, MEDIA_PATH, img_filename)
        
        # Download image
        opener = urllib.request.build_opener()
        opener.addheaders = [('user-agent', self.USER_AGENT)]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(img_url, img_path)
        
        # Compress image with imagemagic
        if image_ext != "gif":
            command = "convert " + img_path + " " + img_path
            os.system(command)
        
        domain_url = DOMAIN + MEDIA_PATH + "/" + img_filename
        print(domain_url)
        return domain_url
   
   def cleanhtml(self,raw_html):
      cleanr = re.compile('<.*?>')
      cleantext = re.sub(cleanr, '', raw_html)
      return self.html_decode(cleantext)
      
   def html_decode(self,s):
        """
        Returns the ASCII decoded version of the given HTML string. This does
        NOT remove normal HTML tags like <p>.
        """
        htmlCodes = (
                (",", '&#44;'),
                ("'", '&#39;'),
                ('"', '&quot;'),
                ('＞', '&gt;'),
                ('＜', '&lt;'),
                ('&', '&amp;')
            )
        for code in htmlCodes:
            s = s.replace(code[1], code[0])
        return s
   
async def setup(bot:commands.Bot)->None:
   await bot.add_cog(Event(bot))
