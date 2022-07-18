import os
import discord
import requests
import json
import random
from random import randint
import youtube_dl
import io
import aiohttp
import asyncio
import urllib.parse
import urllib.request
import re
from discord_components import Button, ButtonStyle, ActionRow
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import tasks
from flask import Flask
from threading import Thread
from datetime import datetime
import keep_alive

from discord.ext import commands

HoloInfo = [ 
    ['Tokino Sora','ときのそら','May 15','160 cm','Ordan','hololive Generation 0','September 7th 2017','Sora-tomo','🐻💿','https://static.wikia.nocookie.net/virtualyoutuber/images/5/52/Tokino_Sora_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132939','https://twitter.com/tokino_sora','Sora-tomo no Minna~! Genki~?Konsomē! Tokino Sora desu! Sora-tomos~! How are you doing~? Konsomē! I\'m Tokino Sora!','Tokino+Sora','Sora','Goddess'],
    ['Roboco-san','ロボ子','May 23','154 cm','Kuromaru9','hololive Generation 0','March 4th 2018','Robosa','🤖','https://static.wikia.nocookie.net/virtualyoutuber/images/7/70/Roboco_San_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132755','https://twitter.com/robocosan','Hellobo! Roboco dayo!','Roboco+hololive','Roboco'],
    ['Hoshimachi Suisei','星街すいせい','March 22','160 cm','Teshina Nari & herself','hololive Generation 0','March 22 2018','Hoshiyomi','☄','https://static.wikia.nocookie.net/virtualyoutuber/images/4/43/Hoshimachi_Suisei_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207131140','https://twitter.com/suisei_hoshimati','It\'s your shooting star, your diamond in the rough! Idol VTuber Hoshimachi Suisei! Sui-chan is~ also cute today~!!','Hoshimachi+Suisei','Suisei','Suichan','Sui-chan','Psychopath','Suicopath'],
    ['Sakura Miko','さくらみこ','March 5','152 cm','Tanaka Yuuichi','hololive Generation 0','August 1st 2018','35P','🌸','https://static.wikia.nocookie.net/virtualyoutuber/images/e/e3/Sakura_Miko_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132810','https://twitter.com/sakuramiko35','Nya-hello~! Sakura Miko dayo!','Sakura+Miko','Miko','Mikochi','Baby'],
    ['AZKi','AZKi','July 1','168 cm','kasokuSato','hololive Generation 0 (formerly INoNaKa Music)','November 15th 2018','Kaitakusha','⚒️','https://static.wikia.nocookie.net/virtualyoutuber/images/9/9f/AZKi_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20210901132054','https://twitter.com/AZKi_VDiVA','KonAZKi AZKi desu!','Azki'],
    ['Yozora Mel','夜空メル','October 31','154 cm','Ayamy','hololive 1st Generation','May 13th 2018','Kapu-min','🌟','https://static.wikia.nocookie.net/virtualyoutuber/images/7/7e/Yozora_Mel_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901133121','https://twitter.com/yozoramel','Konkappu! It\'s Yozora Mel, the Underworld\'s vampire prodigy!','Yozora+Mel','Mel'],
    ['Shirakami Fubuki','白上フブキ','October 5','160 cm','Nagishiro Mito','hololive 1st Generation & hololive Gamers','June 1st 2018','Sukonbu','🌽','https://static.wikia.nocookie.net/virtualyoutuber/images/5/5f/Shirakami_Fubuki_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901132823','https://twitter.com/shirakamifubuki','Konbankitsune! I\'m Shirakami Fubuki!','Shirakami+fubuki','Fubuki'],
    ['Natsuiro Matsuri','夏色まつり','July 22','152 cm','Minamura Haruki','hololive 1st Generation','June 1st 2018','Matsurisu','https://static.wikia.nocookie.net/virtualyoutuber/images/9/90/Natsuiro_Matsuri_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901132606','https://twitter.com/natsuiromatsuri','Wasshoi! hololive\'s symbol of purity and everyone\'s idol, Natsuiro Matsuri here!','natsuiro+matsuri','Matsuri'],
    ['Aki Rosenthal','アキ・ローゼンタール','February 17','162 cm','Azumi Akitake','hololive 1st Generation','June 1st 2018','Rose-tai','🍎','https://static.wikia.nocookie.net/virtualyoutuber/images/7/70/Aki_Rosenthal_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901131926','https://twitter.com/akirosenthal','Alona, everyone! This is Aki Rosenthal a.k.a. AkiRose!','Aki+rosenthal','Aki','Akirose','Akiroze'],
    ['Akai Haato','赤井はあと','August 10','154 cm','Haruyuki','hololive 1st Generation','June 2nd 2018','Haaton','❣','https://static.wikia.nocookie.net/virtualyoutuber/images/b/b7/Akai_Haato_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901131912','https://twitter.com/akaihaato','Haachama-chama~!','Akai+haato','Haato','Haachama'],
    ['Minato Aqua','湊あくあ','December 1','148 cm','gaou','hololive 2nd Generation','August 8th 2018','Aqua Crew','⚓️','https://static.wikia.nocookie.net/virtualyoutuber/images/f/f8/Minato_Aqua_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211231140528','https://twitter.com/minatoaqua','Konaqua!A-quality day to one and all! I\'m Minato Aqua!','minato+aqua','Aqua','Aqutan','45kg','Ateshi','Onion'],
    ['Murasaki Shion','紫咲シオン','December 8','145 cm','Tam-u','hololive 2nd Generation','August 17th 2018','Shio-idren','🌙','https://static.wikia.nocookie.net/virtualyoutuber/images/1/12/Murasaki_Shion_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132516','https://twitter.com/murasakishionch','Konshio~! Murasaki Shion here!','murasaki+shion','Shion','Kusogaki','Garlic'],
    ['Yuzuki Choco','癒月ちょこ','February 14','165 cm','Masuishi Kinoto','hololive 2nd Generation','September 4th 2018','Chocomates','💋','https://static.wikia.nocookie.net/virtualyoutuber/images/2/20/Yuzuki_Choco_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133147','https://twitter.com/yuzukichococh','Good evening, my cute students! Choc-on!','yuzuki+choco','Choco','Nurse','Succubus'],
    ['Oozora Subaru','大空スバル','July 2','154 cm','Shigure Ui','hololive 2nd Generation','September 16th 2018','Subafriends','🚑','https://static.wikia.nocookie.net/virtualyoutuber/images/4/46/Oozora_Subaru_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132728','https://twitter.com/oozorasubaru','Chiwassu! I\'m Oozora Subaru from hololive 2nd Generation!','oozora+subaru','Subaru','Shuba'],
    ['Nakiri Ayame','百鬼あやめ','December 13','152 cm','Nana Kagura','hololive 2nd Generation','September 3rd 2018','Nakiri Gang','😈','https://static.wikia.nocookie.net/virtualyoutuber/images/d/d1/Nakiri_Ayame_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132530','https://twitter.com/nakiriayame','Konnakiri! Greetings, Humans! Yo Dayo!','nakiri+ayame','Ayame','Ojou','Ojou-sama','Oni','Yodayo','Yodazo'],
    ['Nekomata Okayu','猫又おかゆ','Febraury 22','152 cm','Kamioka Chiroru','hololive Gamers','April 6th 2019','Onigiris','🍙','https://static.wikia.nocookie.net/virtualyoutuber/images/5/5e/Nekomata_Okayu_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132624','https://twitter.com/nekomataokayu','Ikuyo~ Mogu mogu~ Okayu!','nekomata+okayu','Okayu','Okazu','Mogu'],
    ['Inugami Korone','戌神ころね','October 1','156 cm','Fukahire','hololive Gamers','April 13th 2019','Koronesuki','🥐','https://static.wikia.nocookie.net/virtualyoutuber/images/3/3c/Inugami_Korone_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132256','https://twitter.com/inugamikorone','\'Ello! Yubi! Give me your Yubis!','inugami+korone','Korone','Koro-chan',],
    ['Ookami Mio','大神ミオ','August 20','165 cm','Izumi Sai','hololive Gamers','December 7th 2018','Mio-fam','🌲','https://static.wikia.nocookie.net/virtualyoutuber/images/2/25/Ookami_Mio_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132711','https://twitter.com/ookamimio','Konbanmio, Ookami Mio dayo!','ookami+mio','Mio','Mio-sha','Miosha','Mion'],
    ['Usada Pekora','兎田ぺこら','January 12','153 cm','Yuuki Hagure','hololive 3rd Generation HoloFantasy','July 17th 2019','Nousagi','👯','https://static.wikia.nocookie.net/virtualyoutuber/images/3/3f/Usada_Pekora_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133050','https://twitter.com/usadapekora','Konpeko Konpeko Konpeko! It\'s Hololive 3rd Generation\'s Usada Pekora peko!','usada+pekora','Pekora','Peko-chan','Kuso Usagi','War Criminal','Peko'],
    ['Shiranui Flare','不知火フレア','April 2','158 cm','lack','hololive 3rd Generation HoloFantasy','August 7th 2019','Elfriend','🔥','https://static.wikia.nocookie.net/virtualyoutuber/images/4/47/Shiranui_Flare_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132842','https://twitter.com/shiranuiflare','Konnui! This is hololive 3rd Gen\'s Shiranui Flare!','shiranui+flare','Flare'],
    ['Houshou Marine','宝鐘マリン','July 30','150 cm','Akasa Ai','hololive 3rd Generation HoloFantasy','August 11th 2019','Houshou no Ichimi(Houshou\'s Pirate Crew','🏴‍☠️','https://static.wikia.nocookie.net/virtualyoutuber/images/f/f7/Houshou_Marine_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207131442','https://twitter.com/houshoumarine','Ahoy! Hololive 3rd Generation, Captain of the Houshou Pirates, Houshou Marine here!','houshou+marine','Marine','Senchou','Pervert','Hentai','Baba'],
    ['Shirogane Noel','白銀ノエル','November 24','158 cm',' Watao','hololive 3rd Generation HoloFantasy','August 8th 2019','Shirogane Kishidan(Knight\'s Order of Shirogane','⚔️','https://static.wikia.nocookie.net/virtualyoutuber/images/3/3b/Shirogane_Noel_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132858','https://twitter.com/shiroganenoel','Konbanmassuru! Shirogane Noel desu!','shirogane+noel','Noel','K-cup',''],
    ['Uruha Rushia','潤羽るしあ','January 22','143 cm','Yasuyuki','hololive 3rd Generation HoloFantasy','July 18th 2019, Retired: February 24th 2022','Fandead','🦋','https://static.wikia.nocookie.net/virtualyoutuber/images/1/14/Uruha_Rushia_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133032','https://twitter.com/uruharushia','Konrushi! Nice to meet you! I\'m Hololive 3rd Generation\'s Uruha Rushia desu!\n***(Terminated)***','uruha+rushia','Rushia','Ru-tan','Board','Pettan','Pettanko','Necromancer','Ru-chan'],
    ['Tokoyami Towa','常闇トワ','August 8','150 cm','rurudo','hololive 4th Generation','January 3rd 2020','Tokoyami Kenzoku','👾','https://static.wikia.nocookie.net/virtualyoutuber/images/a/a1/Tokoyami_Towa_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132952','https://twitter.com/tokoyamitowa','Konyappi! Tokoyami Towa desu!','Towa','Towachin','TMT','Devil','Towasama','Towa-sama'],
    ['Amane Kanata','天音かなた','April 22','149 cm','Oshioshio','hololive 4th Generation','DEcember 27th 2019','Hey-min','💫','https://static.wikia.nocookie.net/virtualyoutuber/images/0/05/Amane_Kanata_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901131938','https://twitter.com/amanekanatach','','Hey! It\'s hololive 4th Generation\'s Angel, Amane Kanata desu!','amane+kanata','Kanata','Kanatan','Gorilla','52kg','Kanataso','PP Tenshi'],
    ['Tsunomaki Watame','角巻わため','June 6','151 cm','fuumi','hololive 4th Generation','December 29th 2019','Watamates','🐏','https://static.wikia.nocookie.net/virtualyoutuber/images/c/c8/Tsunomaki_Watame_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133018','https://twitter.com/tsunomakiwatame','Konbandododooo! Tsunomaki Watame desu!','tsunomaki+watame','Watame','Sheep'],
    ['Himemori Luna','姫森ルーナ','October 10','150 cm','Kanzaki Hiro','hololive 4th Generation','January 4th 2020','Lu-knights','🍬','https://static.wikia.nocookie.net/virtualyoutuber/images/e/ec/Himemori_Luna_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132153','https://twitter.com/himemoriluna','Minna~Oru? Hololive\'s 4th generation, Himemori Luna nanora~','himemori+luna','Luna','Hime','Princess','Nanora'],
    ['Kiryu Coco','桐生ココ','June 17','180 cm','yaman**','hololive 4th Generation','December 28th 2019, Retired: July 1st 2021','Tatsunoko','🐉','https://static.wikia.nocookie.net/virtualyoutuber/images/6/6a/Kiryu_Coco_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132331','https://twitter.com/kiryucoco','Good Morning Motherfuckers\n***(Graduated)***','kiryu+coco','Coco','Asacoco','Dragon','Friend C'],
    ['Shishiro Botan','獅白ぼたん','September 6','166 cm','tomari','hololive 5th Generation NePoLaBo','August 14th 2020','SSRB','♌','https://static.wikia.nocookie.net/virtualyoutuber/images/1/1f/Shishiro_Botan_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132912','https://twitter.com/shishirobotan','La Lion~ La Lion~ Shishiro Botan desu!','shishiro+botan','Botan','Lion'],
    ['Yukihana Lamy','雪花ラミイ','November 15','158 cm','Rin☆Yuu','hololive 5th Generation NePoLaBo','August 12th 2020','Yukimin','☃️','https://static.wikia.nocookie.net/virtualyoutuber/images/7/78/Yukihana_Lamy_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133134','https://twitter.com/yukihanalamy','Yahoo! hololive 5th Generation\'s Yukihana Lamy desu!','yukihana+lamy','Lamy','Wamy'],
    ['Omaru Polka','尾丸ポルカ','January 30','153 cm','Kou Mashiro','hololive 5th Generation NePoLaBo','August 16th 2020','Omaru Troupe','🎪','https://static.wikia.nocookie.net/virtualyoutuber/images/6/6e/Omaru_Polka_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132655','https://twitter.com/omarupolka','Poruka oru ka? Oru yo!','omaru+polka','Polka','Omarun'],
    ['Momosuzu Nene','桃鈴ねね','March 2','159 cm','Nishizawa 5mm','hololive 5th Generation NePoLaBo','August 13th 2020','Nekko','🥟','https://static.wikia.nocookie.net/virtualyoutuber/images/e/ec/Momosuzu_Nene_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132429','https://twitter.com/momosuzunene','Konnene! Everyone are you ready? It\'s hololive 5th Generation\'s Orange Representitive Momosuzu Nene desu!','momosuzu+nene','Nene','Nenechi','Super Nenechi'],
    ['Kazama Iroha','風真いろは','June 18','156 cm','うみぼうず','hololive 6th Generation holoX','November 30th 2021','かざま隊','🍃','https://static.wikia.nocookie.net/virtualyoutuber/images/d/d7/Kazama_Iroha_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132819','https://twitter.com/kazamairohach','hololive 6th Generation Secret Society HoloX\'s Samurai Bodyguard Kamaza Iroha desu!','kazama+iroha','Iroha','De Gozaru','Bodyguard','Nin Nin','Samurai'],
    ['Laplus Darknesss','ラプラス・ダークネス','May 25','139 cm','三嶋くろね','hololive 6th Generation holoX','November 26th 2021','Yamada','🛸💜','https://static.wikia.nocookie.net/virtualyoutuber/images/7/7c/La%2B_Darknesss_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132611','https://twitter.com/laplusdarknesss','Katsumoku seyo! It\'s HoloX founder La+ Darknesss!','laplus+darkness','Laplus','La+','Darknesss','Darkness','Yes My Dark','YMD'],
    ['Sakamata Chloe','沙花叉クロヱ','May 18','148 cm','パセリ','hololive 6th Generation holoX','November 29th 2021','飼育員(Shiikuin),Zookeepers','🎣','https://static.wikia.nocookie.net/virtualyoutuber/images/d/d7/Sakamata_Chloe_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132752','https://twitter.com/sakamatachloe','Bakkubakkubakku~n! HoloX\'s Cleaner and Fixer Sakamata Chloe desu!','sakamata+chloe','Chloe','Kuroe','Orca','Bath'],
    ['Takane Lui','鷹嶺ルイ','June 11','161 cm','かかげ','hololive 6th Generation holoX','November 27th 2021','Lui-tomo','🥀','https://static.wikia.nocookie.net/virtualyoutuber/images/8/81/Takane_Lui_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132636','https://twitter.com/takanelui','Konlui! Executive Officer of HoloX Takane Lui at your service!','takane+lui','Lui','Lui-nee'],
    ['Hakui Koyori','博衣こより','March 15','153 cm','ももこ','hololive 6th Generation holoX','November 28th 2021','こよりの助手くん,Koyori\'s Helpers','🧪','https://static.wikia.nocookie.net/virtualyoutuber/images/d/d2/Hakui_Koyori_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132720','https://twitter.com/hakuikoyori','Konkoyo! HoloX\'s Brilliant Scientist Hakui Koyori desu!','hakui+koyori','Koyori','Scientist','Coyote'],
    ['Gawr Gura','がうる・ぐら','June 20','141 cm','Amashiro Natsuki','holoEN 1st Generation Myth','September 13th 2020','Chumbuds','🔱','https://static.wikia.nocookie.net/virtualyoutuber/images/a/a8/Gawr_Gura_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132122','https://twitter.com/gawrgura','A....... Dōmo, same desu!','gawr+gura','Gura','Guwa','Shark','A'],
    ['Mori Calliope','森カリオペ','April 4','167 cm','Yukisame','holoEN 1st Generation Myth','September 12th 2020','Deadbeats','💀','https://static.wikia.nocookie.net/virtualyoutuber/images/c/cd/Mori_Calliope_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132459','https://twitter.com/moricalliope','mori+calliope','Calli','Calliope','Dad','Reaper'],
    ['Ninomae Ina\'nis','にのまえいなにす','May 20','157 cm','Kurobashi Kouhaku','holoEN 1st Generation Myth','September 13th 2020','Takodachi','🐙','https://static.wikia.nocookie.net/virtualyoutuber/images/e/ec/Ninomae_Ina%27nis_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132639','https://twitter.com/ninomaeinanis','Wah! Good Day! It\'s Ninomae Ina\'nis!','ninomae+inanis','Ina','Wah','Inanis','Ina\'nis','Tako'],
    ['Watson Amelia','ワトソン・アメリア','January 6','150 cm','Nabi','holoEN 1st Generation Myth','September 13th 2020','Teamates','🔎','https://static.wikia.nocookie.net/virtualyoutuber/images/7/7d/Watson_Amelia_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133105','https://twitter.com/watsonameliaEN','Ameliaaaaaa WAAAAAATsoooooon','amelia+watson','Ame','Amelia'],
    ['Takanashi Kiara','小鳥遊キアラ','July 6','165 cm','huke','holoEN 1st Generation Myth','September 12th 2020','KFP','🐔','https://static.wikia.nocookie.net/virtualyoutuber/images/9/9a/Takanashi_Kiara_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132926','https://twitter.com/takanashikiara','Kikkeriki! Holomyth\'s Fiery Pheonix Takanashi Kiara!','takanashi+kiara','Kiara','Pheonix','Chicken'],
    ['Ouro Kronii','オーロ・クロニー','March 14','168 cm','WADARCO🍎','holoEN 2nd Generation Council','August 23rd 2021','Kronies','⌛','https://static.wikia.nocookie.net/virtualyoutuber/images/d/d4/Ouro_Kronii_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133511','https://twitter.com/ourokronii','Kroniichiwa! It\'s HoloCouncil\'s Warden of Time Ouro Kronii','ouro+kronii','Kronii'],
    ['Nanashi Mumei','七詩ムメイ','August 4','156 cm','azure','holoEN 2nd Generation Council','August 23rd','Hoomans','🦉','https://static.wikia.nocookie.net/virtualyoutuber/images/b/b9/Nanashi_Mumei_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132548','https://twitter.com/nanashimumei_en','Hello! It\'s HoloCouncil\'s Guardian of Civilization Nanashi Mumei','nanashi+mumei','Mumei'],
    ['Hakos Baelz','ハコス・ベールズ','February 29','149 cm','Mika Pikazo','holoEN 2nd Generation Council','August 23rd 2020','Brats','🎲','https://static.wikia.nocookie.net/virtualyoutuber/images/0/0a/Hakos_Baelz_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132137','https://twitter.com/hakosbaelz','¡zʅǝɐꓭ soʞɐH soɐɥϽ ⅎo ʇuǝɯᴉpoqɯƎ s╻ʅᴉɔunoϽoʅoH s╻ʇI ¡soʞɐɥO','hakos+baelz','Bae','Baelz','Hakos','Chaos'],
    ['Ceres Fauna','セレス・ファウナ','March 21','164 cm','Tohsaka Asagi','holoEN 2nd Generation Council','August 23rd 2020','Saplings','🌿','https://static.wikia.nocookie.net/virtualyoutuber/images/0/02/Ceres_Fauna_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132109','https://twitter.com/ceresfauna','Konfauna! It\'s HoloCouncil\'s Keeper of Nature Ceres Fauna!','ceres+fauna','Fauna','Ceres'],
    ['Tsukumo Sana','九十九佐命','June 10','169 cm','pako','holoEN 2nd Generation Council','August 23rd 2020','Sanallite','🪐','https://static.wikia.nocookie.net/virtualyoutuber/images/0/0f/Tsukumo_Sana_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133004','https://twitter.com/tsukumosana','Yo! It\'s HoloCouncil\'s Speaker of Space Tsukumo Sana\n***(Retiring July 31st)***','tsukumo+sana','Sana','Galaxy Girl'],
    ['IRyS','アイリス','March 7','166 cm','redjuice','holoEN Project:HOPE','July 11th 2021','Irystocrats','💎','https://static.wikia.nocookie.net/virtualyoutuber/images/f/ff/IRyS_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132316','https://twitter.com/irys_en','HIRyS, It\'s IRyS!','irys','Irys'],
    ['Ayunda Risu','アユンダ・リス','January 15','153 cm','Yatomi','HoloID','April 10th 2020','Risuners','🐿️','https://static.wikia.nocookie.net/virtualyoutuber/images/c/c5/Ayunda_Risu_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207132840','https://twitter.com/ayunda_risu','Konrisu! Puru puru ganbaririsu! It\'s Ayunda Risu','ayunda+risu','Risu'],
    ['Moona Hoshinova','ムーナ・ホシノヴァ','February 15','165 cm','により','HoloID','April 11th 2020','Moonafic','🔮','https://static.wikia.nocookie.net/virtualyoutuber/images/4/41/Moona_Hoshinova_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207132903','https://twitter.com/moonahoshinova','Moon Moon~ Moona Hoshinova Dayo!','moona+hoshinova','Moona','Moon'],
    ['Airani Iofifteen','アイラニ・イオフィフティーン','July 15','150 cm','Yano Mituki','HoloID','April 12th 2020','Ioforia','🎨','https://static.wikia.nocookie.net/virtualyoutuber/images/6/6e/Airani_Iofifteen_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207132936','https://twitter.com/airaniiofifteen','IOFORIA~! OBISA! Pagi semua! I’m your beloved smart alien Airani Iofifteen from hololive Indonesia, nice to meet you!','airani+iofifteen','Iofifteen','Iofi'],
    ['Kureiji Ollie','クレイジー・オリー','October 13','162 cm','LAM','HoloID 2nd Generation','December 4th 2020','#ZOMRADE','🧟‍♀️','https://static.wikia.nocookie.net/virtualyoutuber/images/3/3d/Kureiji_Ollie_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207133008','https://twitter.com/kureijiollie','ZOMBANWA!! SUPER KAWAII ZOMBIE IDOL, KU KU KU KUREIJI OLLIE DESU~!!','kureiji+ollie','Ollie','Olivia','Zombie'],
    ['Anya Melfissa','アーニャ・メルフィッサ','March 12','147 cm','上倉エク','HoloID 2nd Generation','December 5th 2020','Melfriends','🍂','https://static.wikia.nocookie.net/virtualyoutuber/images/3/37/Anya_Melfissa_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207133039','https://twitter.com/anyamelfissa','Good day! This is Anya Melfissa from hololive ID 2nd Generation.','anya+melfissa','Anya'],
    ['Pavolia Reine','パヴォリア・レイネ','September 9','172 cm','飯田ぽち','HoloID 2nd Generation','December 6th 2020','MERAKyats','🦚','https://static.wikia.nocookie.net/virtualyoutuber/images/3/34/Pavolia_Reine_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207133110','https://twitter.com/pavoliareine','Attention Please, The Peafowl Princess that was blown away by the wind, I am Pavolia Reine From Hololive ID','pavolia+reine','Reine'],

    ]


userid = [328551968098353154, 429550829595263001]
userwaifu = ['Amelia Watson', 'Hoshimachi Suisei']

client = commands.Bot(command_prefix="!")

query1 = ('sushi+hololive+clips', 'hololive+clips',
          'hololive+vtube+tengoku+clips', 'hololive+original+songs')


def positionValue(lst,ctx):
    return [ctx in a for a in lst].index(True)

def Extract(lst):
    return [item[0] for item in lst]

def savewrite(filterList, filename):
    f = open(filename, "a")
    f.write(filterList.lower().title() + "\n")
    f.close()


def loadwrite(filename):
    f = open(filename, "r")
    filterList = f.readlines()

    for i in range(0, len(filterList)):
        filterList[i] = filterList[i][:len(filterList[i]) - 1]

    f.close()
    return filterList


def saveid(filterList, filename):
    f = open(filename, 'a')
    for year in filterList:
        f.write("{}\n".format(year))


@tasks.loop(minutes=60)
async def holoClip():
    """A background task that gets invoked every 10 minutes."""
    c = client.get_channel(930497363758424094)
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?search_query=' + query1[randint(0, 3)])
    search_results = re.findall(
        r"watch\?v=(\S{11})", htm_content.read().decode())
    await c.send(
        'Here\'s your hourly hololive clip\n''https://www.youtube.com/watch?v=' + search_results[randint(0, 20)])


@holoClip.before_loop
async def my_background_task_before_loop():
    await client.wait_until_ready()


holoClip.start()


async def func():
    await client.wait_until_ready()
    c = client.get_channel(716497365137227836)
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?search_query=hololive+clips')
    search_results = re.findall(
        r"watch\?v=(\S{11})", htm_content.read().decode())
    await c.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 30)])


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('!commands to show list of commands, listening to !'))
    print("We are ready peko")

    # initializing scheduler
    scheduler = AsyncIOScheduler()

    # sends "Your Message" at 12PM and 18PM (Local Time)
    scheduler.add_job(func, CronTrigger(
        hour="12, 18, 23", minute="17", second="00"))

    # starting the scheduler
    scheduler.start()


@client.event
async def message(message):
    if message.author == client.user:
        return


notgay = ('im not gay okay', 'smh i like guys is that a problem', 'give me a mean wet kiss baby boy', 'why are you gay',
          'im not gay you are gay', 'suck on stun seed upside down')


@client.command()
async def gaybot(ctx):
    await ctx.send(notgay[randint(0, len(notgay) - 1)])


@client.command()
async def sleep(ctx):
    await ctx.send('It\'s {} and i need to sleep ZZZZ'.format(datetime.now()))


@client.command()
async def profile(ctx):
    if ctx.message.author.id in userid:
        profile = discord.Embed(title='{}\'s Profile'.format(ctx.message.author.display_name),
                                color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        profile.set_author(name=ctx.message.author.display_name, url="https://twitter.com/tokoyamitowa",
                           icon_url=ctx.message.author.avatar_url)
        profile.set_thumbnail(url=ctx.author.avatar_url)
        profile.add_field(
            name='Name', value=ctx.message.author.display_name, inline=False)
        profile.add_field(name='Waifu', value=userwaifu[userid.index(
            ctx.message.author.id)], inline=False)
        await ctx.send(embed=profile)
    else:
        profile = discord.Embed(title='{}\'s Profile'.format(ctx.message.author.display_name),
                                color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        profile.set_author(name=ctx.message.author.display_name, url="https://twitter.com/tokoyamitowa",
                           icon_url=ctx.message.author.avatar_url)
        profile.set_thumbnail(url=ctx.author.avatar_url)
        profile.add_field(
            name='Name', value=ctx.message.author.display_name, inline=False)
        profile.add_field(name='Waifu', value='None', inline=False)
        await ctx.send(embed=profile)


@client.command(aliases=['ly'])
async def loveyou(ctx):
    await ctx.send('😘<3 goodnight bb {} ily <3😘'.format(userwaifu[userid.index(ctx.message.author.id)]))


@client.command(aliases=['ll'])
async def lovelevel(ctx):
    v = loadwrite('userid.txt')
    x = loadwrite('userwaifu.txt')
    authorid = str(ctx.message.author.id)
    if str(authorid) in v:
        love = randint(0, 100)
        await ctx.send('You are {}% in love with {}'.format(love, x[v.index(authorid)]))
    else:
        await ctx.send('You are not in love')


@client.command()
async def waifu(ctx):
    author = ctx.message.author
    v = loadwrite('userid.txt')
    x = loadwrite('userwaifu.txt')
    authorid = str(author.id)

    if str(authorid) in v:
        await ctx.send(
            'Your waifu is {}, would you like to change it?\nOr if you\'d like to remove it type \'r\''.format(
                x[v.index(authorid)]))

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        user = await client.wait_for('message', check=check, timeout=None)

        if user.content.lower() == 'yes':
            await ctx.send('Who is new your waifu')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            usernew = await client.wait_for('message', check=check, timeout=None)

            if usernew.content.lower().title() == x[v.index(authorid)]:
                await ctx.send('Ay stop being so weird man that\'s already your waifu')

            else:

                x = loadwrite('userwaifu.txt')
                v = loadwrite('userid.txt')
                u1 = x[v.index(authorid)]

                with open('userwaifu.txt', 'r') as file:
                    filedata = file.read()

                filedata = filedata.replace(
                    u1, usernew.content.lower().title())

                with open('userwaifu.txt', 'w') as file:
                    file.write(filedata)
                reread = loadwrite('userwaifu.txt')
                await ctx.send('Your new waifu is {}'.format(reread[v.index(authorid)]))

        elif user.content.lower() == 'r':
            x = loadwrite('userwaifu.txt')
            v = loadwrite('userid.txt')
            u1 = x[v.index(authorid)]

            with open('userwaifu.txt', 'r') as file:
                filedata = file.read()

            filedata = filedata.replace(u1, 'None')

            with open('userwaifu.txt', 'w') as file:
                file.write(filedata)
            reread = loadwrite('userwaifu.txt')
            await ctx.send('Your waifu has been removed')

        else:
            await ctx.send('I guess {} is still the best for you ;)'.format(x[v.index(authorid)]))

    else:
        await ctx.send('Who is your waifu')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        user = await client.wait_for('message', check=check, timeout=None)
        savewrite(str(authorid), 'userid.txt')
        savewrite(str(user.content.lower().title()), 'userwaifu.txt')
        x = loadwrite('userwaifu.txt')
        v = loadwrite('userid.txt')
        print(author.id)
        await ctx.send('Your waifu is {}'.format(x[v.index(authorid)]))


@client.command(aliases=['g'])
async def gamble(ctx):
    check1 = Extract(HoloInfo)
    gambleHolomem = check1[randint(0, 53)]
    author = ctx.message.author
    await ctx.send("Do you think your number will be bigger or smaller than {}\'s?".format(gambleHolomem))

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await client.wait_for('message', check=check, timeout=None)
    botnum = randint(0, 100)
    usernum = randint(0, 100)

    userdif = botnum - usernum
    botdif = usernum - botnum

    if botnum < usernum and msg.content.lower() == 'bigger':
        await ctx.send(
            'Nice! Your number was {} bigger, {}\'s number was {} and your number was {}'.format(botdif, gambleHolomem,
                                                                                                 botnum, usernum))
    elif usernum < botnum and msg.content.lower() == 'smaller':
        await ctx.send('Nice! Your number was {} smaller, {}\'s number was {} and your number was {}'.format(userdif,
                                                                                                             gambleHolomem,
                                                                                                             botnum,
                                                                                                             usernum))
    elif usernum < botnum and msg.content.lower() == 'bigger':
        await ctx.send(
            'Nice try! Your number was {} smaller, {}\'s number was {} and your number was {}'.format(userdif,
                                                                                                      gambleHolomem,
                                                                                                      botnum, usernum))
    elif botnum < usernum and msg.content.lower() == 'smaller':
        await ctx.send('Nice try! Your number was {} bigger, {}\'s number was {} and your number was {}'.format(botdif,
                                                                                                                gambleHolomem,
                                                                                                                botnum,
                                                                                                                usernum))


@client.command()
async def pp(ctx):
    ppsize = "="
    x = int(randint(0, 10))
    y = int(9)
    if ctx.author.display_name.lower() in smallPP:
        ppmachine1 = discord.Embed(description='PP not found',
                                   color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        ppmachine1.add_field(name='X{}D'.format(0 * ppsize),
                             value='Yo where\'s your pp brooo even its laughing at you xD!!!!')
        await ctx.send(embed=ppmachine1)

    elif x < y:
        ppmachine2 = discord.Embed(description='PP Machine',
                                   color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        ppmachine2.add_field(name='X{}D'.format(
            randint(3, 10) * ppsize), value='nice cock bro')
        await ctx.send(embed=ppmachine2)
    else:
        ppmachine = discord.Embed(description='PP Machine',
                                  color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        ppmachine.add_field(name='X{}D'.format(55 * ppsize),
                            value='fucking monster cock')
        await ctx.send(embed=ppmachine)


@client.command()
async def pekofy(ctx, *, args):
    await ctx.send(args + " peko")


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong peko! {round(client.latency * 1000)}ms')


@client.command(aliases=['hmem'])
async def holomem(ctx):
    d0 = datetime(2008, 8, 18)
    d1 = datetime.now()
    delta = d1 - d0

    random.seed(delta.days)
    x = random.randint(0, 53)
    check = Extract(HoloInfo)

    position = int(positionValue(HoloInfo,check[x]))


    await ctx.send("Today\'s lucky holomember today is : " + HoloInfo[x][0])

    holoui = discord.Embed(title=HoloInfo[position][0], url=HoloInfo[position][10], description=HoloInfo[position][11], color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    holoui.set_author(name=ctx.author.display_name, url="https://twitter.com/tokoyamitowa", icon_url=ctx.author.avatar_url)
    holoui.set_thumbnail(url=HoloInfo[position][9])

    holoui.add_field(name='Name', value=HoloInfo[position][0], inline=True)
    holoui.add_field(name='Japanese Name', value=HoloInfo[position][1], inline=True)
    holoui.add_field(name='Birthday', value=HoloInfo[position][2], inline=True)
    holoui.add_field(name='Height', value=HoloInfo[position][3], inline=True)
    holoui.add_field(name='Illustrator', value=HoloInfo[position][4], inline=True)
    holoui.add_field(name='Generation', value=HoloInfo[position][5], inline=True)
    holoui.add_field(name='Debut Date', value=HoloInfo[position][6], inline=True)
    holoui.add_field(name='Fan Name', value=HoloInfo[position][7], inline=True)
    holoui.add_field(name='Oshi Mark', value=HoloInfo[position][8], inline=True)
    holoui.set_footer(text='Maxsimum #9474 is self maintaining this bot with very long break intervals')
        
    await ctx.send(embed=holoui)
    c = ctx.channel
    htm_content = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(HoloInfo[position][12]) + '+original')
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await c.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 5)])


@client.command()
async def holopro(ctx):
    await ctx.send("https://hololive.hololivepro.com/en")


@client.command()
async def commands(ctx):
    commands = discord.Embed(title='All Commands', description='List of all the commands in the bot with a summary',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    commands.add_field(name="!commands", value='Sends this Menu', inline=False)
    commands.add_field(
        name="!YAGOO", value='Sends a picture of sad YAGOO', inline=False)
    commands.add_field(name="!gamble !g",
                       value='Gamble against a hololive member', inline=False)
    commands.add_field(
        name="!clip", value='Sends a random hololive clip', inline=False)
    commands.add_field(name="!generation !gen", value='See Hololive members and their respective Generations',
                       inline=False)
    commands.add_field(
        name="!hololive", value='See info of specific Hololive members', inline=False)
    commands.add_field(name="!holomem !hmem",
                       value='Sends your Hololive member of the day', inline=False)
    commands.add_field(
        name="!holopro", value='Sends the Holopro Website', inline=False)
    commands.add_field(
        name="!pekofy", value='Adds peko to the end of your sentence peko', inline=False)
    commands.add_field(name="!ping", value='Shows bot latency', inline=False)
    commands.add_field(
        name="!sheesh", value='sheeeeeeeeeeeeeeeeeeeeeesh', inline=False)
    commands.add_field(
        name="!join", value='Bot joins the channel which you are in', inline=False)
    commands.add_field(name="!dc !disconnect",
                       value='Bot leaves the channel which you are in', inline=False)
    commands.add_field(name="!pp", value='See Yo PP Size', inline=False)
    commands.add_field(
        name="!waifu", value='Set or Change your waifu', inline=False)

    await ctx.send(embed=commands)


@client.command()
async def YAGOO(ctx):
    yagoo1 = discord.Embed()
    yagoo1.set_image(
        url='https://cdn.discordapp.com/attachments/716497365137227836/930501205988376606/yagoo.png')
    await ctx.send(embed=yagoo1)

@client.command()
async def hololive(ctx):

    

    holomem1 = discord.Embed(title='Hololive Members', url='',description='Who\'s info would you like to know more of?', color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    holomem1.add_field(name='hololive Generation 0',                value='Tokino Sora \nRoboco \nHoshimachi Suisei \nSakura Miko \nAZKi',inline=True)
    holomem1.add_field(name='hololive 1st Generation',              value='Yozora Mel \nShirakami Fubuki \nNatsuiro Matsuri \nAki Rosenthal \nAkai Haato',inline=True)
    holomem1.add_field(name='hololive 2nd Generation',              value='Minato Aqua \nMurasaki Shion \nYuzuki Choco \nOozora Subaru \nNakiri Ayame', inline=True)
    holomem1.add_field(name='hololive Gamers',                      value='Nekomata Okayu \nInugami Korone \nOokami Mio \nShirakami Fubuki', inline=True)
    holomem1.add_field(name='hololive 3rd Generation HoloFantasy',  value='Usada Pekora \nShiranui Flare \nHoushou Marine \nShirogane Noel \n**Uruha Rushia**',inline=True)
    holomem1.add_field(name='hololive 4th Generation',              value='Tokoyami Towa \nAmane Kanata \nTsunomaki Watame \nHimemori Luna \n**Kiryuu Coco**', inline=True)
    holomem1.add_field(name='hololive 5th Generation NePoLaBo',     value='Shishiro Botan \nYukihana Lamy \nOmaru Polka \nMomosuzu Nene', inline=True)
    holomem1.add_field(name='hololive 6th Generation HoloX',        value='Kazama Iroha \nLaplus Darkness \nSakamata Chloe \nTakane Lui \nHakui Koyori', inline=True)
    holomem1.add_field(name='holoEN 1st Generation Myth',           value='Gawr Gura \nMori Calliope \nNinomae Ina\'nis \nWatson Amelia \nTakanashi Kiara',inline=True)
    holomem1.add_field(name='holoEN 2nd Generation Council',        value='Ouro Kronii \nNanashi Mumei \nHakos Baelz \nCeres Fauna \n**Tsukumo Sana**', inline=True)
    holomem1.add_field(name='holoEN Project:HOPE',                  value='IRyS', inline=True)
    holomem1.add_field(name='hololive Indonesia',                   value='Ayunda Risu \nMoona Hoshinova \nAirani Iofifteen \nKureiji Ollie \nAnya Melfissa \nPavolia Reine',inline=True)

    await ctx.send(embed=holomem1)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await client.wait_for('message', check=check, timeout=None)

    if any(msg.content.lower().title() in sl for sl in HoloInfo):
        position = int(positionValue(HoloInfo,msg.content.lower().title()))

        holoui = discord.Embed(title=HoloInfo[position][0], url=HoloInfo[position][10], description=HoloInfo[position][11], color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        holoui.set_author(name=ctx.author.display_name, url="https://twitter.com/tokoyamitowa", icon_url=ctx.author.avatar_url)
        holoui.set_thumbnail(url=HoloInfo[position][9])

        holoui.add_field(name='Name', value=HoloInfo[position][0], inline=True)
        holoui.add_field(name='Japanese Name', value=HoloInfo[position][1], inline=True)
        holoui.add_field(name='Birthday', value=HoloInfo[position][2], inline=True)
        holoui.add_field(name='Height', value=HoloInfo[position][3], inline=True)
        holoui.add_field(name='Illustrator', value=HoloInfo[position][4], inline=True)
        holoui.add_field(name='Generation', value=HoloInfo[position][5], inline=True)
        holoui.add_field(name='Debut Date', value=HoloInfo[position][6], inline=True)
        holoui.add_field(name='Fan Name', value=HoloInfo[position][7], inline=True)
        holoui.add_field(name='Oshi Mark', value=HoloInfo[position][8], inline=True)
        holoui.set_footer(text='Maxsimum #9474 is self maintaining this bot with very long break intervals')
        
        await ctx.send(embed=holoui)
        c = ctx.channel
        htm_content = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(HoloInfo[position][12]) + '+original')
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
        await c.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 5)])

    else:
        await ctx.send(msg.content + ' is not a hololive member, please try again.')




@client.command()
async def sheesh(ctx):
    await ctx.send('https://c.tenor.com/IiWXIpQo1RkAAAAC/sheesh-sheeesh.gif')


@client.command()
async def join(ctx):
    user = ctx.message.author
    vc = user.voice.channel

    voice = discord.utils.get(client.voice_clients,
                              guild=ctx.guild)  # This allows for more functionality with voice channels

    # None being the default value if the bot isnt in a channel (which is why the is_connected() is returning errors)
    if voice == None:
        await vc.connect()
        await ctx.send(f"Joined **{vc}**")
    else:
        await ctx.send("I'm already connected!")


@client.command()
async def dc(ctx):
    user = ctx.message.author
    vc = user.voice.channel

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.voice_client.disconnect(force=True)
    await ctx.send(f'Disconnected from **{vc}**')


@client.command()
async def play(ctx, ):
    def check(m): return m.author == ctx.author and m.channel == ctx.channel

    msg = await client.wait_for('message', check=check, timeout=None)

    c = ctx.channel
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?search_query=' + msg.content)
    search_results = re.findall(
        r"watch\?v=(\S{11})", htm_content.read().decode())
    musicvid = 'https://www.youtube.com/watch?v=' + search_results[0]

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 =reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}

    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(musicvid, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)


@client.command()
async def clip(ctx):
    c = ctx.channel
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?search_query=' + query1[randint(0, 2)])
    search_results = re.findall(
        r"watch\?v=(\S{11})", htm_content.read().decode())
    await c.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 15)])


@client.command()
async def youtube(ctx, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string + "song")
    search_results = re.findall(
        r"watch\?v=(\S{11})", htm_content.read().decode())
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 15)])


keep_alive.keep_alive()

client.run("XXX")
