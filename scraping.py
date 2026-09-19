import os
import requests
from bs4 import BeautifulSoup
from ds_split import split_t_ds
from irunadblib import make_db
from regist_equip import regist_equip
from analyst import make_equip_property
from math_prop import split_math
from lib import write_text

def main():
    # スクレイピングからDB登録までの一連の処理
    DB_FILE='./iruna.db'
    if os.path.exists(DB_FILE):
        print(f'{DB_FILE}を削除')
        os.remove(DB_FILE)

    # DB再構築
    make_db()

    # スクレイピング
    scraping()
    # 装備をDBに登録
    regist_equip()
    # 装備プロパティを構築
    make_equip_property()
    #t_dsを分割して正規化
    split_t_ds()
    # mathを分割して正規化
    split_math()
    print('done!')

def scraping():
    # iruna.onlineから装備情報をスクレイピングしてファイルに出力する
    equips = [
        'Swords', 'Bows', 'Canes', 'Claws', 'Throwing',
        'Armor', 'Additional', 'Special', 'Crystas',
        'AlCrystas', 'RelicCrystas'
    ]

    for equip in equips:
        save_html(equip)

    print('done!')

def save_html(equip):
    outputfile = f'./html/{equip}.html'
    if os.path.exists(outputfile):
        return

    BASE_URL = 'https://jp.iruna-online.info/iruna'
    target_url = f'{BASE_URL}/items/{equip}'
    print(target_url)
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, "html.parser")

    write_text(outputfile, soup.prettify())


if __name__ == '__main__':
    print('start')
    main()
