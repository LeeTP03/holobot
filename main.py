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
import urllib.parse, urllib.request, re
from discord_components import Button, ButtonStyle, ActionRow
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import tasks
from flask import Flask
from threading import Thread
from datetime import datetime
import keep_alive

from discord.ext import commands

HGen0 = ('hololive gen 0', 'gen 0', '0', 'sora', 'robo', 'suisei', 'miko', 'tokino sora', 'roboco', 'hoshimachi suisei',
         'sakura miko', 'suichan')
HGen1 = ('hololive gen 1', 'gen 1', '1', 'mel', 'fubuki', 'matsuri', 'aki', 'haato', 'yozora mel', 'shirakami fubuki',
         'natsuiro matsuri', 'aki rosenthal', 'akai haato', 'akirose', 'hentai', 'haachama', 'fbk')
HGen2 = ('hololive gen 2', 'gen 2', '2', 'aqua', 'shion', 'choco', 'subaru', 'ayame', 'minato aqua', 'murasaki shion',
         'yuzuki choco', 'oozora subaru', 'shuba', '44.5')
HGenGamers = (
'hololive gamers', 'gamers', 'okayu', 'korone', 'mio', 'inugami korone', 'nekomata okayu', 'ookami mio', 'miosha')
HGen3 = ('hololive gen 3', 'gen 3', '3', 'fantasy', 'pekora', 'flare', 'marine', 'noel', 'rushia', 'usada pekora',
         'shiranui flare', 'houshou marine', 'shirogane noel', 'uruha rushia', 'senchou', 'futan', 'pettanko')
HGen4 = ('hololive gen 4', 'gen 4', '4', 'towa', 'kanata', 'watame', 'luna', 'coco', 'tokoyami towa', 'amane kanata',
         'tsunomaki watame', 'himemori luna', 'kiryu coco', 'towasama')
HGen5 = (
'hololive gen 5', 'gen 5', '5', 'holofive', 'botan', 'lamy', 'polka', 'nene', 'shishiro botan', 'yukihana lamy',
'omaru polka', 'momosuzu nene', 'nenechi')
HGen6 = (
'hololive gen 6', 'gen 6', '6', 'holox', 'iroha', 'laplus', 'chloe', 'lui', 'koyori', 'kazama iroha', 'laplus darkness',
'sakamata chloe', 'takane lui', 'hakui koyori', 'yamada')
HGenEn1 = (
'holoen gen 1', 'en gen 1', 'myth', 'en 1', 'gura', 'calli', 'ina', 'ame', 'kiara', 'gawr gura', 'mori calliope',
'ninomae ina\'nis', 'watson amelia', 'takanashi kiara', 'amelia')
HGenEn2 = ('holoen gen 2', 'en gen 2', 'council', 'en 2', 'kronii', 'mumei', 'bae', 'fauna', 'sana', 'ouro kronii',
           'nanashi mumei', 'hakos baelz', 'ceres fauna', 'tsukumo sana')
HGenID = (
'holoid', 'id', 'ayunda risu', 'moona hoshinova', 'airani iofifteen', 'kureiji ollie', 'anya melfissa', 'pavolia reine',
'risu', 'moona', 'iofi', 'ollie', 'anya', 'reine')
HGenSolo = ('hololive vsinger', 'vsinger', 'irys', 'azki', 'hope', 'innk', 'innk music', 'inonaka')

HGenOverall = (HGen0, HGen1, HGen2)

smallPP = ('max',)

alias1 = ('sora', 'robo', 'suisei', 'miko',
          'mel', 'fubuki', 'matsuri', 'aki', 'haato',
          'aqua', 'shion', 'choco', 'subaru', 'ayame',
          'okayu', 'korone', 'mio',
          'pekora', 'flare', 'marine', 'noel', 'rushia',
          'towa', 'kanata', 'watame', 'luna', 'coco',
          'botan', 'lamy', 'polka', 'nene',
          'iroha', 'laplus', 'chloe', 'lui', 'koyori',
          'azki',
          'gura', 'calli', 'ina', 'ame', 'kiara',
          'kronii', 'mumei', 'bae', 'fauna', 'sana',
          'irys',
          'risu', 'moona', 'iofi',
          'ollie', 'anya', 'reine')

holomember = ('Tokino Sora', 'Roboco', 'Hoshimachi Suisei', 'Sakura Miko', 'Yozora Mel', 'Shirakami Fubuki',
              'Natsuiro Matsuri', 'Aki Rosenthal', 'Akai Haato', 'Minato Aqua', 'Murasaki Shion',
              'Yuzuki Choco', 'Oozora Subaru', 'Nakiri Ayame', 'Inugami Korone', 'Nekomata Okayu', 'Ookami Mio',
              'Usada Pekora', 'Shiranui Flare', 'Houshou Marine', 'Shirogane Noel', 'Uruha Rushia', 'Tokoyami Towa',
              'Amane Kanata', 'Tsunomaki Watame', 'Himemori Luna', 'Kiryu Coco', 'Shishiro Botan', 'Yukihana Lamy',
              'Omaru Polka',
              'Momosuzu Nene', 'Kazama Iroha', 'Laplus Darkness', 'Sakamata Chloe', 'Takane Lui', 'Hakui Koyori',
              'Azki', 'Gawr Gura', 'Mori Calliope', 'Ninomae Ina\'nis', 'Watson Amelia', 'Takanashi Kiara',
              'Ouro Kronii', 'Nanashi Mumei', 'Hakos Baelz', 'Ceres Fauna', 'Tsukumo Sana', 'Irys', 'Ayunda Risu',
              'Moona Hoshinova', 'Airani Iofifteen', 'Kureiji Ollie', 'Anya Melfissa', 'Pavolia Reine')

holomembervid = ('Tokino+Sora', 'Roboco', 'Hoshimachi+Suisei', 'Sakura+Miko', 'Yozora+Mel', 'Shirakami+Fubuki',
                 'Natsuiro+Matsuri', 'Aki+Rosenthal', 'Akai+Haato', 'Minato+Aqua', 'Murasaki+Shion',
                 'Yuzuki+Choco', 'Oozora+Subaru', 'Nakiri+Ayame', 'Inugami+Korone', 'Nekomata+Okayu', 'Ookami+Mio',
                 'Usada+Pekora', 'Shiranui+Flare', 'Houshou+Marine', 'Shirogane+Noel', 'Uruha+Rushia', 'Tokoyami+Towa',
                 'Amane+Kanata', 'Tsunomaki+Watame', 'Himemori+Luna', 'Kiryu+Coco', 'Shishiro+Botan', 'Yukihana+Lamy',
                 'Omaru+Polka',
                 'Momosuzu+Nene', 'Kazama+Iroha', 'Laplus+Darkness', 'Sakamata+Chloe', 'Takane+Lui', 'Hakui+Koyori',
                 'Azki', 'Gawr+Gura', 'Mori+Calliope', 'Ninomae+Ina\'nis', 'Watson+Amelia', 'Takanashi+Kiara',
                 'Ouro+Kronii', 'Nanashi+Mumei', 'Hakos+Baelz', 'Ceres+Fauna', 'Tsukumo+Sana', 'Hololive+Irys',
                 'Ayunda+Risu',
                 'Moona+Hoshinova', 'Airani+Iofifteen', 'Kureiji+Ollie', 'Anya+Melfissa', 'Pavolia+Reine')

HoloPic = (
'https://static.wikia.nocookie.net/virtualyoutuber/images/5/52/Tokino_Sora_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132939',
'https://static.wikia.nocookie.net/virtualyoutuber/images/7/70/Roboco_San_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132755',
'https://static.wikia.nocookie.net/virtualyoutuber/images/4/43/Hoshimachi_Suisei_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207131140',
'https://static.wikia.nocookie.net/virtualyoutuber/images/e/e3/Sakura_Miko_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132810',
'https://static.wikia.nocookie.net/virtualyoutuber/images/7/7e/Yozora_Mel_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901133121',
'https://static.wikia.nocookie.net/virtualyoutuber/images/5/5f/Shirakami_Fubuki_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901132823',
'https://static.wikia.nocookie.net/virtualyoutuber/images/9/90/Natsuiro_Matsuri_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901132606',
'https://static.wikia.nocookie.net/virtualyoutuber/images/7/70/Aki_Rosenthal_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901131926',
'https://static.wikia.nocookie.net/virtualyoutuber/images/b/b7/Akai_Haato_-_Icon.png/revision/latest/scale-to-width-down/80?cb=20210901131912',
'https://static.wikia.nocookie.net/virtualyoutuber/images/f/f8/Minato_Aqua_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211231140528',
'https://static.wikia.nocookie.net/virtualyoutuber/images/1/12/Murasaki_Shion_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132516',
'https://static.wikia.nocookie.net/virtualyoutuber/images/2/20/Yuzuki_Choco_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133147',
'https://static.wikia.nocookie.net/virtualyoutuber/images/4/46/Oozora_Subaru_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132728',
'https://static.wikia.nocookie.net/virtualyoutuber/images/d/d1/Nakiri_Ayame_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132530',
'https://static.wikia.nocookie.net/virtualyoutuber/images/3/3c/Inugami_Korone_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132256',
'https://static.wikia.nocookie.net/virtualyoutuber/images/5/5e/Nekomata_Okayu_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132624',
'https://static.wikia.nocookie.net/virtualyoutuber/images/2/25/Ookami_Mio_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132711',
'https://static.wikia.nocookie.net/virtualyoutuber/images/3/3f/Usada_Pekora_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133050',
'https://static.wikia.nocookie.net/virtualyoutuber/images/4/47/Shiranui_Flare_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132842',
'https://static.wikia.nocookie.net/virtualyoutuber/images/f/f7/Houshou_Marine_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207131442',
'https://static.wikia.nocookie.net/virtualyoutuber/images/3/3b/Shirogane_Noel_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132858',
'https://static.wikia.nocookie.net/virtualyoutuber/images/1/14/Uruha_Rushia_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133032',
'https://static.wikia.nocookie.net/virtualyoutuber/images/a/a1/Tokoyami_Towa_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132952',
'https://static.wikia.nocookie.net/virtualyoutuber/images/0/05/Amane_Kanata_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901131938',
'https://static.wikia.nocookie.net/virtualyoutuber/images/c/c8/Tsunomaki_Watame_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133018',
'https://static.wikia.nocookie.net/virtualyoutuber/images/e/ec/Himemori_Luna_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132153',
'https://static.wikia.nocookie.net/virtualyoutuber/images/6/6a/Kiryu_Coco_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132331',
'https://static.wikia.nocookie.net/virtualyoutuber/images/1/1f/Shishiro_Botan_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132912',
'https://static.wikia.nocookie.net/virtualyoutuber/images/7/78/Yukihana_Lamy_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133134',
'https://static.wikia.nocookie.net/virtualyoutuber/images/6/6e/Omaru_Polka_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132655',
'https://static.wikia.nocookie.net/virtualyoutuber/images/e/ec/Momosuzu_Nene_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132429',
'https://static.wikia.nocookie.net/virtualyoutuber/images/d/d7/Kazama_Iroha_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132819',
'https://static.wikia.nocookie.net/virtualyoutuber/images/7/7c/La%2B_Darknesss_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132611',
'https://static.wikia.nocookie.net/virtualyoutuber/images/d/d7/Sakamata_Chloe_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132752',
'https://static.wikia.nocookie.net/virtualyoutuber/images/8/81/Takane_Lui_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132636',
'https://static.wikia.nocookie.net/virtualyoutuber/images/d/d2/Hakui_Koyori_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20211207132720',
'https://static.wikia.nocookie.net/virtualyoutuber/images/9/9f/AZKi_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20210901132054',
'https://static.wikia.nocookie.net/virtualyoutuber/images/a/a8/Gawr_Gura_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132122',
'https://static.wikia.nocookie.net/virtualyoutuber/images/c/cd/Mori_Calliope_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132459',
'https://static.wikia.nocookie.net/virtualyoutuber/images/e/ec/Ninomae_Ina%27nis_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132639',
'https://static.wikia.nocookie.net/virtualyoutuber/images/7/7d/Watson_Amelia_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133105',
'https://static.wikia.nocookie.net/virtualyoutuber/images/9/9a/Takanashi_Kiara_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132926',
'https://static.wikia.nocookie.net/virtualyoutuber/images/d/d4/Ouro_Kronii_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133511',
'https://static.wikia.nocookie.net/virtualyoutuber/images/b/b9/Nanashi_Mumei_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132548',
'https://static.wikia.nocookie.net/virtualyoutuber/images/0/0a/Hakos_Baelz_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132137',
'https://static.wikia.nocookie.net/virtualyoutuber/images/0/02/Ceres_Fauna_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132109',
'https://static.wikia.nocookie.net/virtualyoutuber/images/0/0f/Tsukumo_Sana_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901133004',
'https://static.wikia.nocookie.net/virtualyoutuber/images/f/ff/IRyS_-_Icon.png/revision/latest/scale-to-width-down/100?cb=20210901132316',
'https://static.wikia.nocookie.net/virtualyoutuber/images/c/c5/Ayunda_Risu_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207132840',
'https://static.wikia.nocookie.net/virtualyoutuber/images/4/41/Moona_Hoshinova_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207132903',
'https://static.wikia.nocookie.net/virtualyoutuber/images/6/6e/Airani_Iofifteen_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207132936',
'https://static.wikia.nocookie.net/virtualyoutuber/images/3/3d/Kureiji_Ollie_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207133008',
'https://static.wikia.nocookie.net/virtualyoutuber/images/3/37/Anya_Melfissa_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207133039',
'https://static.wikia.nocookie.net/virtualyoutuber/images/3/34/Pavolia_Reine_-_Icon.png/revision/latest/scale-to-width-down/130?cb=20211207133110')

HoloLink = ('https://twitter.com/tokino_sora', 'https://twitter.com/robocosan', 'https://twitter.com/suisei_hoshimati',
            'https://twitter.com/sakuramiko35',
            'https://twitter.com/yozoramel', 'https://twitter.com/shirakamifubuki',
            'https://twitter.com/natsuiromatsuri', 'https://twitter.com/akirosenthal', 'https://twitter.com/akaihaato',
            'https://twitter.com/minatoaqua', 'https://twitter.com/murasakishionch',
            'https://twitter.com/yuzukichococh', 'https://twitter.com/oozorasubaru', 'https://twitter.com/nakiriayame',
            'https://twitter.com/inugamikorone', 'https://twitter.com/nekomataokayu', 'https://twitter.com/ookamimio',
            'https://twitter.com/usadapekora', 'https://twitter.com/shiranuiflare', 'https://twitter.com/houshoumarine',
            'https://twitter.com/shiroganenoel', 'https://twitter.com/uruharushia',
            'https://twitter.com/tokoyamitowa', 'https://twitter.com/amanekanatach',
            'https://twitter.com/tsunomakiwatame', 'https://twitter.com/himemoriluna', 'https://twitter.com/kiryucoco',
            'https://twitter.com/shishirobotan', 'https://twitter.com/yukihanalamy', 'https://twitter.com/omarupolka',
            'https://twitter.com/momosuzunene',
            'https://twitter.com/kazamairohach', 'https://twitter.com/laplusdarknesss',
            'https://twitter.com/sakamatachloe', 'https://twitter.com/takanelui', 'https://twitter.com/hakuikoyori',
            'https://twitter.com/AZKi_VDiVA',
            'https://twitter.com/gawrgura', 'https://twitter.com/moricalliope', 'https://twitter.com/ninomaeinanis',
            'https://twitter.com/takanashikiara', 'https://twitter.com/watsonameliaEN',
            'https://twitter.com/ourokronii', 'https://twitter.com/nanashimumei_en', 'https://twitter.com/hakosbaelz',
            'https://twitter.com/ceresfauna', 'https://twitter.com/tsukumosana',
            'https://twitter.com/irys_en',
            'https://twitter.com/ayunda_risu', 'https://twitter.com/moonahoshinova',
            'https://twitter.com/airaniiofifteen',
            'https://twitter.com/kureijiollie', 'https://twitter.com/anyamelfissa', 'https://twitter.com/pavoliareine')

HoloGreeting = (
'Sora-tomo no Minna~! Genki~?Konsomē! Tokino Sora desu! Sora-tomos~! How are you doing~? Konsomē! I\'m Tokino Sora!',
'Hellobo! Roboco dayo!',
'It\'s your shooting star, your diamond in the rough! Idol VTuber Hoshimachi Suisei! Sui-chan is~ also cute today~!!',
'Nya-hello~! Sakura Miko dayo!',
"Konkappu! It's Yozora Mel, the Underworld's vampire prodigy!", "Konbankitsune! I'm Shirakami Fubuki!",
"Wasshoi! hololive's symbol of purity and everyone's idol, Natsuiro Matsuri here!",
"Alona, everyone! This is Aki Rosenthal a.k.a. AkiRose!", 'Haachama-chama~!',
'Konaqua!A-quality day to one and all! I\'m Minato Aqua!', 'Konshio~! Murasaki Shion here!',
"Good evening, my cute students! Choc-on!", 'Chiwassu! I\'m Oozora Subaru from hololive 2nd Generation!',
'Konnakiri! Greetings, Humans! Yo Dayo!',
'\'Ello! Yubi! Give me your Yubis!', 'Ikuyo~ Mogu mogu~ Okayu!', 'Konbanmio, Ookami Mio dayo!',
'Konpeko Konpeko Konpeko! It\'s Hololive 3rd Generation\'s Usada Pekora peko!',
"Konnui! This is hololive 3rd Gen's Shiranui Flare!",
'Ahoy! Hololive 3rd Generation, Captain of the Houshou Pirates, Houshou Marine here!',
'Konbanmassuru! Shirogane Noel desu!', 'Konrushi! Nice to meet you! I\'m Hololive 3rd Generation\'s Uruha Rushia desu!',
'Konyappi! Tokoyami Towa desu!', 'Hey! It\'s hololive 4th Generation\'s Angel, Amane Kanata desu!',
'Konbandododooo! Tsunomaki Watame desu!', "Minna~Oru? Hololive's 4th generation, Himemori Luna nanora~",
'Good Morning Motherfuckers',
'La Lion~ Shishiro Botan desu!', 'Yahoo! hololive 5th Generation\'s Yukihana Lamy desu!', 'Poruka oru ka? Oru yo!',
'Konnene! Everyone are you ready? It\'s hololive 5th Generation\'s Orange Representitive Momosuzu Nene desu!',
'hololive 6th Generation Secret Society HoloX\'s Samurai Bodyguard Kamaza Iroha desu!',
'Katsumoku seyo! It\'s HoloX founder La+ Darknesss!',
'Bakkubakkubakku~n! HoloX\'s Cleaner and Fixer Sakamata Chloe desu!',
'Konlui! Executive Officer of HoloX Takane Lui at your service!',
'Konkoyo! HoloX\'s Brilliant Scientist Hakui Koyori desu!',
'KonAZKi AZKi desu!',
'Dōmo, same desu!', 'It\'s HoloMyth\'s Grim Reaper Mori Calliope!',
'Wah! Good Morning/Afternoon/Evening! It\'s Ninomae Ina\'nis!', 'Ameliaaaaaa WAAAAAATsoooooon',
'Kikkeriki! Holomyth\'s Fiery Pheonix Takanashi Kiara!',
'Kroniichiwa! It\'s HoloCouncil\'s Warden of Time Ouro Kronii',
'Hello! It\'s HoloCouncil\'s Guardian of Civilization Nanashi Mumei',
'¡zʅǝɐꓭ soʞɐH soɐɥϽ ⅎo ʇuǝɯᴉpoqɯƎ s╻\ʅᴉɔunoϽoʅoH s╻\ʇI ¡soʞɐɥO',
'Konfauna! It\'s HoloCouncil\'s Keeper of Nature Ceres Fauna!',
'Yo!  It\'s HoloCouncil\'s Speaker of Space Tsukumo Sana',
'HIRyS, It\'s IRyS!',
'Konrisu! Puru puru ganbaririsu! It\'s Ayunda Risu', "Moon Moon~ Moona Hoshinova Dayo!",
'IOFORIA~! OBISA! Pagi semua! I’m your beloved smart alien Airani Iofifteen from hololive Indonesia, nice to meet you!',
'ZOMBANWA!! SUPER KAWAII ZOMBIE IDOL, KU KU KU KUREIJI OLLIE DESU~!!',
"Good day! This is Anya Melfissa from hololive ID 2nd Generation.",
'Attention Please, The Peafowl Princess that was blown away by the wind, I am Pavolia Reine From Hololive ID')

HoloMark = ('🐻💿', '🤖', '☄', '🌸',
            '🌟', '🌽', '🏮', '🍎', '❣',
            '⚓️', '🌙', '💋', '🚑', '😈',
            '🥐', '🍙', '🌲',
            '👯', '🔥', '🏴‍☠️', '⚔️', '🦋',
            ' 👾', '💫', '🐏', '🍬', '🐉',
            '♌', '☃️', '🎪', '🥟',
            '🍃', '🛸💜', '🎣', '🥀', '🧪',
            '⚒️',
            '🔱', '💀', '🐙', '🔎', '🐔',
            '⌛', '⌛', '🎲', '🌿', '🪐',
            '💎',
            '🐿️', '🔮', '🎨', '🧟‍♀️', '🍂', '🦚')

HoloJpName = ('ときのそら', 'ロボ子さん', '星街すいせい', 'さくらみこ',
              '夜空メル', '白上フブキ', '夏色まつり', 'アキ・ローゼンタール', '赤井はあと',
              '湊あくあ', '紫咲シオン', '癒月ちょこ', '大空スバル', '百鬼あやめ',
              '戌神ころね', '猫又おかゆ', '大神ミオ',
              '兎田ぺこら', '不知火フレア', '宝鐘マリン', '白銀ノエル', '潤羽るしあ',
              '常闇トワ', '天音かなた', '角巻わため', '姫森ルーナ', '桐生ココ',
              '獅白ぼたん', '雪花ラミィ', '尾丸ポルカ', '桃鈴ねね',
              '風真いろは', 'ラプラス・ダークネス', '沙花叉クロヱ', '鷹嶺ルイ', '博衣こより',
              '-',
              'がうる・ぐら', '森カリオペ', 'にのまえいなにす', 'ワトソン・アメリア', '小鳥遊キアラ',
              'オーロ・クロニー', '七詩ムメイ', 'ハコス・ベールズ', 'セレス・ファウナ', '九十九佐命',
              'アイリス',
              'アユンダ・リス', 'ムーナ・ホシノヴァ', 'アイラニ・イオフィフティーン',
              'クレイジー・オリー', 'アーニャ・メルフィッサ', 'パヴォリア・レイネ')

HoloEnName = ('Tokino Sora', 'Roboco-san', 'Hoshimachi Suisei', 'Sakura Miko',
              'Yozora Mel', 'Shirakami Fubuki', 'Natsuiro Matsuri', 'Aki Rosenthal', 'Akai Haato',
              'Minato Aqua', 'Murasaki Shion', 'Yuzuki Choco', 'Oozora Subaru', 'Nakiri Ayame',
              'Inugami Korone', 'Nekomata Okayu', 'Ookami Mio',
              'Usada Pekora', 'Shiranui Flare', 'Houshou Marine', 'Shirogane Noel', 'Uruha Rushia',
              'Tokoyami Towa', 'Amane Kanata', 'Tsunomaki Watame', 'Himemori Luna', 'Kiryu Coco',
              'Shishiro Botan', 'Yukihana Lamy', 'Omaru Polka', 'Momosuzu Nene',
              'Kazama Iroha', 'La+ Darkness', 'Sakamata Chloe', 'Takane Lui', 'Hakui Koyori',
              'AZKi',
              'Gawr Gura', 'Mori Calliope', 'Ninomae Ina\'nis', 'Watson Amelia', 'Takanashi Kiara',
              'Ouro Kronii', 'Nanashi Mumei', 'Hakos Baelz', 'Ceres Fauna', 'Tsukumo Sana',
              'IRyS',
              'Ayunda Risu', 'Moona Hoshinova', 'Airani Iofifteen',
              'Kureiji Ollie', 'Anya Melfissa', 'Pavolia Reine')

HoloBday = ('May 15', 'May 23', 'March 22', 'March 5',
            'October 31', 'October 5', 'July 22', 'February 17', 'August 10',
            'December 1', 'December 8', 'February 14', 'July 2', 'December 13',
            'October 1', 'February 22', 'August 20',
            'January 12', 'April 2', 'July 30', 'November 24', 'January 22',
            'August 8', 'April 22', 'June 6', 'October 10', 'June 17',
            'September 8', 'November 15', 'January 30', 'March 2',
            'June 18', 'May 25', 'May 18', 'June 11', 'March 15',
            'July 1',
            'June 20', 'April 4', 'May 20', 'January 6', 'July 6',
            'March 14', 'August 4', 'February 29', 'March 21', 'June 10',
            'March 7',
            'January 15', 'February 15', 'July 15',
            'October 13', 'March 12', 'September 9')

HoloHeight = ('160', '154', '160', '152',
              '154', '160', '152', '162', '154',
              '148', '145', '165', '154', '152',
              '156', '152', '165',
              '153', '158', '150', '158', '143',
              '150', '149', '151', '150', '180',
              '166', '158', '153', '159',
              '156', '139', '148', '161', '153',
              '168',
              '141', '167', '157', '150', '165',
              '168', '156', '149', '164', '169',
              '166',
              '153', '165', '150',
              '162', '147', '172')

Holoillust = ('Ordan', 'Kuromaru9', 'Teshina Nari', 'Tanaka Yuuichi',
              'Ayamy', 'Nagishiro Mito', 'Minamura Haruki', 'Azumi Akitake', 'Haruyuki',
              'gaou', 'Tam-U', 'Masuishi Kinoto', 'Shigure Ui', 'Nana Kagura',
              'Fukahire', 'Kamioka Chiroru', 'Izumi Sai',
              'Yuuki Hagure', 'lack', 'Akasa Ai', 'Watao', 'Yasuyuki',
              'rurudo', 'Oshioshio', 'fuumi', 'Kanzaki Hiro', 'yaman**',
              'tomari', 'Rin☆Yuu', 'Kou Mashiro', 'Nishizawa 5mm',
              'うみぼうず', '三嶋くろね', 'パセリ', 'かかげ', 'ももこ',
              'kasokuSato',
              'Amashiro Natsuki', 'Yukisame', 'Kuroboshi Kouhaku', 'Nabi', 'huke',
              'WADARCO🍎', 'azure', 'Mika Pikazo', 'Tohsaka Asagi', 'pako',
              'redjuice',
              'Yatomi', 'により', 'Yano Mituki',
              'LAM', '上倉エク', '飯田ぽち。')

HoloFan = ("Sora-tomo", 'Robosa', 'Hoshiyomi', '35P/Mikopi',
           'Kapu-min', 'Sukonbu', 'Matsurisu', 'Rose-tai', 'Haaton',
           'Aqua Crew', 'Shio-Idren', 'Chocomates', 'Subafriends', 'Nakiri Gang',
           'Koronesuki', 'Onigiris', 'Mio-fam',
           'The Rabbit Alliance', 'Elfriend', 'Houshou no Ichimi (Houshou\'s Pirate Crew)',
           'Shirogane Kishidan (Knight’s Order of Shirogane', 'Fandead',
           'Tokoyami Kenzoku', 'Hey-min', 'Watamates', 'Lu-knights', 'Tatsunoko',
           'SSRB', 'Yukimin', 'Omaru Troupe', 'Husbands',
           'かざま隊', '山田', '飼育員', '-', 'こよりの助手くん',
           'Kaitakusha',
           'Chumbuds', 'Deadbeats', 'Tentacult', 'Teamates', 'KFP',
           'Kronies', 'Hoomans', 'Brats', 'Saplings', 'Sanallite',
           'Irystocrats',
           'Risuners', 'Moonafic', 'Ioforia',
           '#ZOMRADE', 'MelFriends', 'MERAKyats')

HoloGen = ('hololive Generation 0', 'hololive Generation 0', 'hololive Generation 0', 'hololive Generation 0',
           'hololive 1st Generation', 'hololive 1st Generation', 'hololive 1st Generation', 'hololive 1st Generation',
           'hololive 1st Generation',
           'hololive 2nd Generation', 'hololive 2nd Generation and hololive Gamers', 'hololive 2nd Generation',
           'hololive 2nd Generation', 'hololive 2nd Generation',
           'hololive Gamers', 'hololive Gamers', 'hololive Gamers',
           'hololive 3rd Generation HoloFantasy', 'hololive 3rd Generation HoloFantasy',
           'hololive 3rd Generation HoloFantasy', 'hololive 3rd Generation HoloFantasy',
           'hololive 3rd Generation HoloFantasy',
           'hololive 4th Generation', 'hololive 4th Generation', 'hololive 4th Generation', 'hololive 4th Generation',
           'hololive 4th Generation',
           'hololive 5th Generation HoloFive', 'hololive 5th Generation HoloFive', 'hololive 5th Generation HoloFive',
           'hololive 5th Generation HoloFive',
           'hololive 6th Generation HoloX', 'hololive 6th Generation HoloX', 'hololive 6th Generation HoloX',
           'hololive 6th Generation HoloX', 'hololive 6th Generation HoloX',
           'INoNaKa Music',
           'holoEN 1st Generation Myth', 'holoEN 1st Generation Myth', 'holoEN 1st Generation Myth',
           'holoEN 1st Generation Myth', 'holoEN 1st Generation Myth',
           'holoEN 2nd Generation Council', 'holoEN 2nd Generation Council', 'holoEN 2nd Generation Council',
           'holoEN 2nd Generation Council', 'holoEN 2nd Generation Council',
           'holoEN Project:HOPE',
           'Hololive Indonesia', 'Hololive Indonesia', 'Hololive Indonesia', 'Hololive Indonesia', 'Hololive Indonesia',
           'Hololive Indonesia',)

HoloDebut = ('September 7th 2017', 'March 4th 2018', 'March 22nd 2018', 'August 1st 2018',
             'May 13th 2018', 'June 1st 2018', 'June 1st 2018', 'June 1st 2018', 'June 2nd 2018',
             'August 8th 2018', 'August 17th 2018', 'September 4th 2018', 'September 16th 2018', 'September 3rd 2018',
             'April 13th 2019', 'April 6th 2019', 'December 7th 2018',
             'July 17th 2019', 'August 7th 2019', 'August 11th 2019', 'August 8th 2019', 'July 18th 2019',
             'January 3rd 2020', 'December 27th 2019', 'December 29th 2019', 'January 4th 2020', 'December 28th 2019',
             'August 14th 2020', 'August 12th 2020', 'August 16th 2020', 'August 13th 2020',
             'November 30th 2021', 'November 26th 2021', 'November 29th 2021', 'November 27th 2021',
             'November 28, 2021',
             '-',
             'September 13th 2020', 'September 12th 2020', 'September 13th 2020', 'September 13th 2020',
             'September 12th 2020',
             'August 23rd 2021', 'August 23rd 2021', 'August 23rd 2020', 'August 23rd 2020', 'August 23rd 2020',
             'July 11th 2021',
             'April 10th 2020', 'April 11th 2020', 'April 12th 2020',
             'December 4th 2020', 'December 5 2020', 'December 6th 2020')
holoinfo = ['1st member', 'first 3d', 'comet']
hmem = len(holomember)

userid = [328551968098353154, 429550829595263001]
userwaifu = ['Amelia Watson', 'Hoshimachi Suisei']

client = commands.Bot(command_prefix="!")

query1 = ('sushi+hololive+clips', 'hololive+clips', 'hololive+vtube+tengoku+clips', 'hololive+original+songs')


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
    htm_content = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + query1[randint(0, 3)])
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await c.send(
        'Here\'s your hourly hololive clip\n''https://www.youtube.com/watch?v=' + search_results[randint(0, 20)])


@holoClip.before_loop
async def my_background_task_before_loop():
    await client.wait_until_ready()


holoClip.start()


async def func():
    await client.wait_until_ready()
    c = client.get_channel(716497365137227836)
    htm_content = urllib.request.urlopen('https://www.youtube.com/results?search_query=hololive+clips')
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await c.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 30)])


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('!commands to show list of commands, listening to !'))
    print("We are ready peko")

    # initializing scheduler
    scheduler = AsyncIOScheduler()

    # sends "Your Message" at 12PM and 18PM (Local Time)
    scheduler.add_job(func, CronTrigger(hour="12, 18, 23", minute="17", second="00"))

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
    now = datetime.now()
    time = now.strftime("%H:%M")

    await ctx.send('It\'s {} and i need to sleep ZZZZ'.format(time))


@client.command()
async def profile(ctx):
    if ctx.message.author.id in userid:
        profile = discord.Embed(title='{}\'s Profile'.format(ctx.message.author.display_name),
                                color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        profile.set_author(name=ctx.message.author.display_name, url="https://twitter.com/tokoyamitowa",
                           icon_url=ctx.message.author.avatar_url)
        profile.set_thumbnail(url=ctx.author.avatar_url)
        profile.add_field(name='Name', value=ctx.message.author.display_name, inline=False)
        profile.add_field(name='Waifu', value=userwaifu[userid.index(ctx.message.author.id)], inline=False)
        await ctx.send(embed=profile)
    else:
        profile = discord.Embed(title='{}\'s Profile'.format(ctx.message.author.display_name),
                                color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        profile.set_author(name=ctx.message.author.display_name, url="https://twitter.com/tokoyamitowa",
                           icon_url=ctx.message.author.avatar_url)
        profile.set_thumbnail(url=ctx.author.avatar_url)
        profile.add_field(name='Name', value=ctx.message.author.display_name, inline=False)
        profile.add_field(name='Waifu', value='None', inline=False)
        await ctx.send(embed=profile)


@client.command(aliases=['ly'])
async def loveyou(ctx):
    author = ctx.message.author
    v = loadwrite('userid.txt')
    x = loadwrite('userwaifu.txt')
    authorid = str(author.id)

    if x[v.index(authorid)] == 'None':
        await ctx.send('😘 <3 goodnight bb holobot ily <3 😘\n\np.s. set a !waifu')

    elif str(authorid) in v:
        await ctx.send('😘 <3 goodnight bb {} ily <3 😘'.format(x[v.index(authorid)]))

    else:
        await ctx.send('😘 <3 goodnight bb holobot ily <3 😘\n\np.s. set a !waifu')


@client.command()
async def waifu(ctx):
    author = ctx.message.author
    v = loadwrite('userid.txt')
    x = loadwrite('userwaifu.txt')
    authorid = str(author.id)

    if x[v.index(authorid)] == 'None':
        await ctx.send('You don\'t have a waifu yet, who is your waifu?')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        usernew = await client.wait_for('message', check=check, timeout=None)
        x = loadwrite('userwaifu.txt')
        v = loadwrite('userid.txt')
        u1 = x[v.index(authorid)]

        with open('userwaifu.txt', 'r') as file:
            filedata = file.read()

        filedata = filedata.replace(u1, usernew.content.lower().title())

        with open('userwaifu.txt', 'w') as file:
            file.write(filedata)
        reread = loadwrite('userwaifu.txt')
        await ctx.send('Your new waifu is {}'.format(reread[v.index(authorid)]))

    elif str(authorid) in v:
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

                filedata = filedata.replace(u1, usernew.content.lower().title())

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
    gambleHolomem = holomember[randint(0, 53)]
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
    else:
        await ctx.send('You\'re a loser, don\'t call me if you\'re not gonna gamble smh my head :rolling_eyes:')


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
        ppmachine2.add_field(name='X{}D'.format(randint(3, 10) * ppsize), value='nice cock bro')
        await ctx.send(embed=ppmachine2)
    else:
        ppmachine = discord.Embed(description='PP Machine',
                                  color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        ppmachine.add_field(name='X{}D'.format(55 * ppsize), value='fucking monster cock')
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

    m = holomember[x]
    u = holomember.index(m)
    await ctx.send("Today\'s' lucky holomember today is : {}".format(m))

    holoui = discord.Embed(title=holomember[u], url=HoloLink[u], description=HoloGreeting[u],
                           color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    holoui.set_author(name=ctx.author.display_name, url="https://twitter.com/tokoyamitowa",
                      icon_url=ctx.author.avatar_url)
    holoui.set_thumbnail(url=HoloPic[u])
    holoui.add_field(name='Name', value=HoloEnName[u], inline=True)
    holoui.add_field(name='Japanese Name', value=HoloJpName[u], inline=True)

    holoui.add_field(name='Birthday', value=HoloBday[u], inline=True)
    holoui.add_field(name='Height', value=HoloHeight[u] + 'cm', inline=True)

    holoui.add_field(name='Illustrator', value=Holoillust[u], inline=True)
    holoui.add_field(name='Generation', value=HoloGen[u], inline=True)

    holoui.add_field(name='Debut Date', value=HoloDebut[u], inline=True)
    holoui.add_field(name='Fan Name', value=HoloFan[u], inline=True)
    holoui.add_field(name='Oshi Mark', value=HoloMark[u], inline=True)
    holoui.set_footer(text='Hoshimachi Suisei is the best')

    await ctx.send(embed=holoui)
    c = ctx.channel
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?search_query=' + str(holomembervid[u]) + 'clips')
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await c.send('Here\'s one of her clips!\nhttps://www.youtube.com/watch?v=' + search_results[randint(0, 5)])


@client.command()
async def holopro(ctx):
    await ctx.send("https://hololive.hololivepro.com/en")


@client.command()
async def commands(ctx):
    commands = discord.Embed(title='All Commands', description='List of all the commands in the bot with a summary',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    commands.add_field(name="!commands", value='Sends this Menu', inline=False)
    commands.add_field(name="!YAGOO", value='Sends a picture of sad YAGOO', inline=False)
    commands.add_field(name="!gamble !g", value='Gamble against a hololive member', inline=False)
    commands.add_field(name="!clip", value='Sends a random hololive clip', inline=False)
    commands.add_field(name="!generation !gen", value='See Hololive members and their respective Generations',
                       inline=False)
    commands.add_field(name="!hololive", value='See info of specific Hololive members', inline=False)
    commands.add_field(name="!holomem !hmem", value='Sends your Hololive member of the day', inline=False)
    commands.add_field(name="!holopro", value='Sends the Holopro Website', inline=False)
    commands.add_field(name="!pekofy", value='Adds peko to the end of your sentence peko', inline=False)
    commands.add_field(name="!ping", value='Shows bot latency', inline=False)
    commands.add_field(name="!sheesh", value='sheeeeeeeeeeeeeeeeeeeeeesh', inline=False)
    commands.add_field(name="!join", value='Bot joins the channel which you are in', inline=False)
    commands.add_field(name="!dc !disconnect", value='Bot leaves the channel which you are in', inline=False)
    commands.add_field(name="!pp", value='See Yo PP Size', inline=False)
    commands.add_field(name="!waifu", value='Set or Change your waifu', inline=False)

    await ctx.send(embed=commands)


@client.command()
async def YAGOO(ctx):
    yagoo1 = discord.Embed()
    yagoo1.set_image(url='https://cdn.discordapp.com/attachments/716497365137227836/930501205988376606/yagoo.png')
    await ctx.send(embed=yagoo1)


@client.command()
async def info(ctx):
    keepgoing = True
    while keepgoing:
        await ctx.send(">>> Who\'s info would you like to know?" +
                       '\nTokino Sora, Roboco, Hoshimachi Suisei, Sakura Miko, \nYozora Mel, Shirakami Fubuki,' +
                       ' Natsuiro Matsuri, Aki Rosenthal, Akai Haato(Hachaama),\nMinato Aqua, Murasaki Shion,' +
                       ' Yuzuki Choco, Oozora Subaru, Nakiri Ayame,\nInugami Korone, Nekomata Okayu, Ookami Mio,' +
                       '\nUsada Pekora, Shiranui Flare, Houshou Marine, Shirogane Noel, Uruha Rushia,\nTokoyami Towa,' +
                       ' Amane Kanata, Tsunomaki Watame, Himemori Luna,\nShishiro Botan, Yukihana Lamy, Omaru Polka,' +
                       ' Momosuzu Nene,\nKazama Iroha, Laplus Darkness, Sakamata Chloe, Takane Lui, Hakui Koyori,' +
                       ' AZKi,\nGawr Gura, Mori Calliope, Ninomae Ina\'nis, Watson Amelia, Takanashi Kiara,' +
                       '\nOuro Kronii, Nanashi Mumei, Hakos Baelz, Ceres Fauna, Tsukumo Sana,\nIRyS, \nAyunda Risu,' +
                       ' Moona Hoshinova, Airani Iofifteen,\nKureiji Ollie, Anya Melfissa, Pavolia Reine\n\n\nType \'quit\' to exit.\n\n')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await client.wait_for('message', check=check, timeout=None)
        u = holomember.index(msg.content.lower().title())
        if msg.content.lower().title() in holomember:

            await ctx.channel.send(f'________________________' +
                                   '\nEnglish Name: ' + HoloEnName[u] +
                                   "\nJapanese Name: " + HoloJpName[u] +

                                   "\nBirthday: " + HoloBday[u] +
                                   "\nHeight: " + HoloHeight[u] + "cm" +
                                   "\nIllustrator: " + Holoillust[u] +
                                   "\nFan Name: " + HoloFan[u] +
                                   "\nGeneration: " + HoloGen[u] +
                                   "\nDebut Date: " + HoloDebut[u] + '\n________________________')
            await asyncio.sleep(3)


        else:
            await ctx.channel.send('not in database')

    if msg.content == 'quit':
        keepgoing = False


suisei = ('hoshimachi suisei', 'ほしまちすいせい', 'March 22', '160', 'Teshina Nari', '')


@client.command()
async def hololive(ctx):
    holomem1 = discord.Embed(title='Hololive Members', url='',
                             description='Who\'s info would you like to know more of?',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    holomem1.add_field(name='hololive Generation 0', value='Tokino Sora \nRoboco \nHoshimachi Suisei \nSakura Miko',
                       inline=True)
    holomem1.add_field(name='hololive 1st Generation',
                       value='Yozora Mel \nShirakami Fubuki \nNatsuiro Matsuri \nAki Rosenthal \nAkai Haato',
                       inline=True)
    holomem1.add_field(name='hololive 2nd Generation',
                       value='Minato Aqua \nMurasaki Shion \nYuzuki Choco \nOozora Subaru \nNakiri Ayame', inline=True)
    holomem1.add_field(name='hololive Gamers', value='Nekomata Okayu \nInugami Korone \nOokami Mio', inline=True)
    holomem1.add_field(name='hololive 3rd Generation HoloFantasy',
                       value='Usada Pekora \nShiranui Flare \nHoushou Marine \nShirogane Noel \nUruha Rushia',
                       inline=True)
    holomem1.add_field(name='hololive 4th Generation',
                       value='Tokoyami Towa \nAmane Kanata \nTsunomaki Watame \nHimemori Luna \nKiryu Coco',
                       inline=True)
    holomem1.add_field(name='hololive 5th Generation HoloFive',
                       value='Shishiro Botan \nYukihana Lamy \nOmaru Polka \nMomosuzu Nene', inline=True)
    holomem1.add_field(name='hololive 6th Generation HoloX',
                       value='Kazama Iroha \nLaplus Darkness \nSakamata Chloe \nTakane Lui \nHakui Koyori', inline=True)
    holomem1.add_field(name='INoNaKa Music', value='AZKi', inline=True)
    holomem1.add_field(name='holoEN 1st Generation Myth',
                       value='Gawr Gura \nMori Calliope \nNinomae Ina\'nis \nWatson Amelia \nTakanashi Kiara',
                       inline=True)
    holomem1.add_field(name='holoEN 2nd Generation Council',
                       value='Ouro Kronii \nNanashi Mumei \nHakos Baelz \nCeres Fauna \nTsukumo Sana', inline=True)
    holomem1.add_field(name='holoEN Project:HOPE', value='IRyS', inline=True)
    holomem1.add_field(name='hololive Indonesia',
                       value='Ayunda Risu \nMoona Hoshinova \nAirani Iofifteen \nKureiji Ollie \nAnya Melfissa \nPavolia Reine',
                       inline=False)

    await ctx.send(embed=holomem1)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await client.wait_for('message', check=check, timeout=None)

    if msg.content.lower().title() in holomember:
        u = holomember.index(msg.content.lower().title())
        holoui = discord.Embed(title=holomember[u], url=HoloLink[u], description=HoloGreeting[u],
                               color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        holoui.set_author(name=ctx.author.display_name, url="https://twitter.com/tokoyamitowa",
                          icon_url=ctx.author.avatar_url)
        holoui.set_thumbnail(url=HoloPic[u])
        holoui.add_field(name='Name', value=HoloEnName[u], inline=True)
        holoui.add_field(name='Japanese Name', value=HoloJpName[u], inline=True)

        holoui.add_field(name='Birthday', value=HoloBday[u], inline=True)
        holoui.add_field(name='Height', value=HoloHeight[u] + 'cm', inline=True)

        holoui.add_field(name='Illustrator', value=Holoillust[u], inline=True)
        holoui.add_field(name='Generation', value=HoloGen[u], inline=True)

        holoui.add_field(name='Debut Date', value=HoloDebut[u], inline=True)
        holoui.add_field(name='Fan Name', value=HoloFan[u], inline=True)
        holoui.add_field(name='Oshi Mark', value=HoloMark[u], inline=True)
        holoui.set_footer(text='Hoshimachi Suisei is the best')
        u = holomember.index(msg.content.lower().title())
        await ctx.send(embed=holoui)
        c = ctx.channel
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?search_query=' + str(holomembervid[u]) + '+original')
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
        await c.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 15)])

    elif msg.content.lower() in alias1:
        u = alias1.index(msg.content.lower())

        holoui = discord.Embed(title=holomember[u], url=HoloLink[u], description=HoloGreeting[u],
                               color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        holoui.set_author(name=ctx.author.display_name, url="https://twitter.com/tokoyamitowa",
                          icon_url=ctx.author.avatar_url)
        holoui.set_thumbnail(url=HoloPic[u])
        holoui.add_field(name='Name', value=HoloEnName[u], inline=True)
        holoui.add_field(name='Japanese Name', value=HoloJpName[u], inline=True)

        holoui.add_field(name='Birthday', value=HoloBday[u], inline=True)
        holoui.add_field(name='Height', value=HoloHeight[u] + 'cm', inline=True)

        holoui.add_field(name='Illustrator', value=Holoillust[u], inline=True)
        holoui.add_field(name='Generation', value=HoloGen[u], inline=True)

        holoui.add_field(name='Debut Date', value=HoloDebut[u], inline=True)
        holoui.add_field(name='Fan Name', value=HoloFan[u], inline=True)
        holoui.add_field(name='Oshi Mark', value=HoloMark[u], inline=True)
        holoui.set_footer(text='Hoshimachi Suisei is the best')

        await ctx.send(embed=holoui)
        c = ctx.channel
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?search_query=' + str(holomembervid[u]) + '+original')
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
        await c.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 15)])



    elif msg.content.lower().title() not in holomember:
        await ctx.send(msg.content + ' is not a hololive member, please try again.')


@client.command(name='generation', aliases=['gen'])
async def generation(ctx):
    genembed = discord.Embed(title='Hololive Generations',
                             description='All Hololive Generations\n p.s You can search generations by members names',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
    genembed.add_field(name='Hololive JP Generations',
                       value='hololive gen 0 \nhololive gen 1\nhololive gen 2\nhololive gamers\nhololive gen 3\nhololive gen 4\nhololive gen 5\n hololive gen 6',
                       inline=False)
    genembed.add_field(name='Hololive EN Generations', value='holoen gen 1\nholoen gen 2', inline=False)
    genembed.add_field(name='Hololive ID Generations', value='holoid gen 1\nhololid gen2', inline=False)

    await ctx.send(embed=genembed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await client.wait_for('message', check=check, timeout=None)

    if msg.content.lower() in HGen0:

        gen0 = discord.Embed(title='Hololive Gen 0', description='gen 0',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        gen0.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        gen0.add_field(name=holomember[0],
                       value=HoloGreeting[0] + '\nhttps://hololive.hololivepro.com/en/talents/tokino-sora/',
                       inline=False)
        gen0.add_field(name=holomember[1],
                       value=HoloGreeting[1] + '\nhttps://hololive.hololivepro.com/en/talents/roboco/', inline=False)
        gen0.add_field(name=holomember[2],
                       value=HoloGreeting[2] + '\nhttps://hololive.hololivepro.com/en/talents/hoshimachi-suisei/',
                       inline=False)
        gen0.add_field(name=holomember[3],
                       value=HoloGreeting[3] + '\nhttps://hololive.hololivepro.com/en/talents/sakura-miko/',
                       inline=False)
        await ctx.send(embed=gen0)

    elif msg.content.lower() in HGen1:
        gen1 = discord.Embed(title='Hololive Gen 1', description='gen 1',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        gen1.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        gen1.add_field(name=holomember[4],
                       value=HoloGreeting[4] + '\nhttps://hololive.hololivepro.com/en/talents/yozora-mel/',
                       inline=False)
        gen1.add_field(name=holomember[5],
                       value=HoloGreeting[5] + '\nhttps://hololive.hololivepro.com/en/talents/shirakami-fubuki/',
                       inline=False)
        gen1.add_field(name=holomember[6],
                       value=HoloGreeting[6] + '\nhttps://hololive.hololivepro.com/en/talents/natsuiro-matsuri/',
                       inline=False)
        gen1.add_field(name=holomember[7],
                       value=HoloGreeting[7] + '\nhttps://hololive.hololivepro.com/en/talents/aki-rosenthal/',
                       inline=False)
        gen1.add_field(name=holomember[8],
                       value=HoloGreeting[8] + '\nhttps://hololive.hololivepro.com/en/talents/akai-haato/',
                       inline=False)

        await ctx.send(embed=gen1)

    elif msg.content.lower() in HGen2:
        gen2 = discord.Embed(title='Hololive Gen 2', description='gen 2',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        gen2.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        gen2.add_field(name=holomember[9],
                       value=HoloGreeting[9] + '\nhttps://hololive.hololivepro.com/en/talents/yozora-mel/',
                       inline=False)
        gen2.add_field(name=holomember[10],
                       value=HoloGreeting[10] + '\nhttps://hololive.hololivepro.com/en/talents/shirakami-fubuki/',
                       inline=False)
        gen2.add_field(name=holomember[11],
                       value=HoloGreeting[11] + '\nhttps://hololive.hololivepro.com/en/talents/natsuiro-matsuri/',
                       inline=False)
        gen2.add_field(name=holomember[12],
                       value=HoloGreeting[12] + '\nhttps://hololive.hololivepro.com/en/talents/aki-rosenthal/',
                       inline=False)
        gen2.add_field(name=holomember[13],
                       value=HoloGreeting[13] + '\nhttps://hololive.hololivepro.com/en/talents/akai-haato/',
                       inline=False)

        await ctx.send(embed=gen2)

    elif msg.content.lower() in HGenGamers:
        geng = discord.Embed(title='Hololive Gamers', description='Gamers',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        geng.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        geng.add_field(name=holomember[14],
                       value=HoloGreeting[14] + '\nhttps://hololive.hololivepro.com/en/talents/inugami-korone/',
                       inline=False)
        geng.add_field(name=holomember[15],
                       value=HoloGreeting[15] + '\nhttps://hololive.hololivepro.com/en/talents/nekomata-okayu/',
                       inline=False)
        geng.add_field(name=holomember[16],
                       value=HoloGreeting[16] + '\nhttps://hololive.hololivepro.com/en/talents/ookami-mio/',
                       inline=False)

        await ctx.send(embed=geng)

    elif msg.content.lower() in HGen3:
        gen3 = discord.Embed(title='Hololive Gen 3', description='gen 3',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        gen3.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        gen3.add_field(name=holomember[17],
                       value=HoloGreeting[17] + '\nhttps://hololive.hololivepro.com/en/talents/usada-pekora/',
                       inline=False)
        gen3.add_field(name=holomember[18],
                       value=HoloGreeting[18] + '\nhttps://hololive.hololivepro.com/en/talents/shiranui-flare/',
                       inline=False)
        gen3.add_field(name=holomember[19],
                       value=HoloGreeting[19] + '\nhttps://hololive.hololivepro.com/en/talents/houshou-marine/',
                       inline=False)
        gen3.add_field(name=holomember[20],
                       value=HoloGreeting[20] + '\nhttps://hololive.hololivepro.com/en/talents/shirogane-noel/',
                       inline=False)
        gen3.add_field(name=holomember[21],
                       value=HoloGreeting[21] + '\nhttps://hololive.hololivepro.com/en/talents/uruha-rushia/',
                       inline=False)

        await ctx.send(embed=gen3)

    elif msg.content.lower() in HGen4:
        gen4 = discord.Embed(title='Hololive Gen 4', description='gen 4',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        gen4.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        gen4.add_field(name=holomember[22],
                       value=HoloGreeting[22] + '\nhttps://hololive.hololivepro.com/en/talents/tokoyami-towa/',
                       inline=False)
        gen4.add_field(name=holomember[23],
                       value=HoloGreeting[23] + '\nhttps://hololive.hololivepro.com/en/talents/amane-kanata/',
                       inline=False)
        gen4.add_field(name=holomember[24],
                       value=HoloGreeting[24] + '\nhttps://hololive.hololivepro.com/en/talents/tsunomaki-watame/',
                       inline=False)
        gen4.add_field(name=holomember[25],
                       value=HoloGreeting[25] + '\nhttps://hololive.hololivepro.com/en/talents/himemori-luna/',
                       inline=False)
        gen4.add_field(name=holomember[26],
                       value=HoloGreeting[26] + '\nhttps://hololive.hololivepro.com/en/talents/kiryu-coco/',
                       inline=False)

        await ctx.send(embed=gen4)

    elif msg.content.lower() in HGen5:
        gen5 = discord.Embed(title='Hololive Gen 5', description='gen 5',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        gen5.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        gen5.add_field(name=holomember[27],
                       value=HoloGreeting[27] + '\nhttps://hololive.hololivepro.com/en/talents/shishiro-botan/',
                       inline=False)
        gen5.add_field(name=holomember[28],
                       value=HoloGreeting[28] + '\nhttps://hololive.hololivepro.com/en/talents/yukihana-lamy/',
                       inline=False)
        gen5.add_field(name=holomember[29],
                       value=HoloGreeting[29] + '\nhttps://hololive.hololivepro.com/en/talents/omaru-polka/',
                       inline=False)
        gen5.add_field(name=holomember[30],
                       value=HoloGreeting[30] + '\nhttps://hololive.hololivepro.com/en/talents/momosuzu-nene/',
                       inline=False)

        await ctx.send(embed=gen5)

    elif msg.content.lower() in HGen6:
        gen6 = discord.Embed(title='Hololive Gen 6', description='gen 6',
                             color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        gen6.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        gen6.add_field(name=holomember[31],
                       value=HoloGreeting[31] + '\nhttps://hololive.hololivepro.com/en/talents/kazama-iroha/',
                       inline=False)
        gen6.add_field(name=holomember[32],
                       value=HoloGreeting[32] + '\nhttps://hololive.hololivepro.com/en/talents/la-darknesss/',
                       inline=False)
        gen6.add_field(name=holomember[33],
                       value=HoloGreeting[33] + '\nhttps://hololive.hololivepro.com/en/talents/sakamata-chloe/',
                       inline=False)
        gen6.add_field(name=holomember[34],
                       value=HoloGreeting[34] + '\nhttps://hololive.hololivepro.com/en/talents/takane-lui/',
                       inline=False)
        gen6.add_field(name=holomember[35],
                       value=HoloGreeting[35] + '\nhttps://hololive.hololivepro.com/en/talents/hakui-koyori/',
                       inline=False)

        await ctx.send(embed=gen6)

    elif msg.content.lower() in HGenEn1:
        genEN1 = discord.Embed(title='HoloEN Gen 1', description='EN gen 1',
                               color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        genEN1.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        genEN1.add_field(name=holomember[37],
                         value=HoloGreeting[37] + '\nhttps://hololive.hololivepro.com/en/talents/gawr-gura/',
                         inline=False)
        genEN1.add_field(name=holomember[38],
                         value=HoloGreeting[38] + '\nhttps://hololive.hololivepro.com/en/talents/mori-calliope/',
                         inline=False)
        genEN1.add_field(name=holomember[39],
                         value=HoloGreeting[39] + '\nhttps://hololive.hololivepro.com/en/talents/ninomae-inanis/',
                         inline=False)
        genEN1.add_field(name=holomember[40],
                         value=HoloGreeting[40] + '\nhttps://hololive.hololivepro.com/en/talents/watson-amelia/',
                         inline=False)
        genEN1.add_field(name=holomember[41],
                         value=HoloGreeting[41] + '\nhttps://hololive.hololivepro.com/en/talents/takanashi-kiara/',
                         inline=False)

        await ctx.send(embed=genEN1)

    elif msg.content.lower() in HGenEn2:
        genEN2 = discord.Embed(title='HoloEN Gen 2', description='EN gen 2',
                               color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        genEN2.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        genEN2.add_field(name=holomember[42],
                         value=HoloGreeting[42] + '\nhttps://hololive.hololivepro.com/en/talents/ouro-kronii/',
                         inline=False)
        genEN2.add_field(name=holomember[43],
                         value=HoloGreeting[43] + '\nhttps://hololive.hololivepro.com/en/talents/nanashi-mumei/',
                         inline=False)
        genEN2.add_field(name=holomember[44],
                         value=HoloGreeting[44] + '\nhttps://hololive.hololivepro.com/en/talents/hakos-baelz/',
                         inline=False)
        genEN2.add_field(name=holomember[45],
                         value=HoloGreeting[45] + '\nhttps://hololive.hololivepro.com/en/talents/ceres-fauna/',
                         inline=False)
        genEN2.add_field(name=holomember[46],
                         value=HoloGreeting[46] + '\nhttps://hololive.hololivepro.com/en/talents/tsukumo-sana/',
                         inline=False)

        await ctx.send(embed=genEN2)

    elif msg.content.lower() in HGenID:
        genID = discord.Embed(title='HoloID', description='Indonesia',
                              color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        genID.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        genID.add_field(name=holomember[48],
                        value=HoloGreeting[48] + '\nhttps://hololive.hololivepro.com/en/talents/ayunda-risu/',
                        inline=False)
        genID.add_field(name=holomember[49],
                        value=HoloGreeting[49] + '\nhttps://hololive.hololivepro.com/en/talents/moona-hoshinova/',
                        inline=False)
        genID.add_field(name=holomember[50],
                        value=HoloGreeting[50] + '\nhttps://hololive.hololivepro.com/en/talents/airani-iofifteen/',
                        inline=False)
        genID.add_field(name=holomember[51],
                        value=HoloGreeting[51] + '\nhttps://hololive.hololivepro.com/en/talents/kureiji-ollie/',
                        inline=False)
        genID.add_field(name=holomember[52],
                        value=HoloGreeting[52] + '\nhttps://hololive.hololivepro.com/en/talents/anya-melfissa/',
                        inline=False)
        genID.add_field(name=holomember[53],
                        value=HoloGreeting[53] + '\nhttps://hololive.hololivepro.com/en/talents/pavolia-reine/',
                        inline=False)

        await ctx.send(embed=genID)

    elif msg.content.lower() in HGenSolo:
        genSolo = discord.Embed(title='Hololive VSingers', description='Project:HOPE and INoNaka Music',
                                color=discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        genSolo.set_thumbnail(url='https://c.tenor.com/rVeVTm7Qq0UAAAAd/suisei-hololive.gif')
        genSolo.add_field(name=holomember[36],
                          value=HoloGreeting[36] + '\nhttps://hololive.hololivepro.com/en/talents/azki/', inline=False)
        genSolo.add_field(name=holomember[47],
                          value=HoloGreeting[47] + '\nhttps://hololive.hololivepro.com/en/talents/irys/', inline=False)

        await ctx.send(embed=genSolo)

    else:
        await ctx.send('Your search returned no results')


@client.command()
async def sheesh(ctx):
    await ctx.send('https://c.tenor.com/IiWXIpQo1RkAAAAC/sheesh-sheeesh.gif')


@client.command()
async def join(ctx):
    user = ctx.message.author
    vc = user.voice.channel

    voice = discord.utils.get(client.voice_clients,
                              guild=ctx.guild)  # This allows for more functionality with voice channels

    if voice == None:  # None being the default value if the bot isnt in a channel (which is why the is_connected() is returning errors)
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
    htm_content = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + msg.content)
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    musicvid = 'https://www.youtube.com/watch?v=' + search_results[0]

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 =reconnect_delay_max 5', 'options': '-vn'}
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
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await c.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 15)])


@client.command()
async def youtube(ctx, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen('https://www.youtube.com/results?' + query_string + "song")
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[randint(0, 15)])


keep_alive.keep_alive()

client.run("xxx")



