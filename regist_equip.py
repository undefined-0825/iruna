import re
from irunadblib import get_connection
from constants import equips
from bs4 import BeautifulSoup
from lib import read_text, included_lines, find_first_index
import unicodedata

props = []

def main():
    print('start')
    regist_equip()

    # print('------------------------------------------')
    # for p in props:
    #     print(p)
    print('done')

def regist_equip():
    with get_connection() as conn:
        cur = conn.cursor()

        # アイテムを抽出してequipテーブルに登録
        for equip in equips:
            print(equip)
            eqtype = equip[0]   # 装備種別
            filepath = equip[1] # htmlファイルのパス
            clsname = equip[2]  # 装備クラス名称（日本語名）
            soup = BeautifulSoup(read_text(filepath), 'html.parser')
            # print(soup)
            items = soup.find_all("div", class_=clsname)
            # print(len(items))

            for item in items:
                # print(item)
                insert_equip(cur, item, eqtype, clsname)


def insert_equip(cur, item, eqtype, jp_name):
    # 名称
    text = item.find("a").text
    name = text.replace(f'【{jp_name}】', '').replace('📷', '')
    # print(name)

    # DEF, ATK, 備考を含む行を抽出
    words = ['DEF:', 'ATK:', '備考:']
    hits = included_lines(item.text, words)
    note1 = ''
    note2 = ''
    atk = ''
    def_ = ''
    if len(hits) > 0:
        note1 = hits[0]
        print(note1)
        atk_def = parse_atk_def(note1)
        atk = atk_def.get("atk")
        def_ = atk_def.get("def")
    if len(hits) > 1:
        note2 = hits[1]
        print(note2)

    # 詳細(ds)
    ds = item.find("div", class_="ds")
    if ds:
        ds = ds.text
    else:
        ds = ''

    t_ds = item.find("div", class_="t_ds")
    math = ''
    if t_ds:
        # 計算式を分離
        t_ds = str(t_ds.text).replace(' スに', ' ボスに').strip()
        math_index = find_first_index(t_ds, ['[', 'if', 'If', 'When', 'equip'])
        if math_index >= 0:
            math = t_ds[math_index: len(t_ds)]
            # print(f'  {math.strip()}')
            t_ds = t_ds[0: math_index]

        t_ds = t_ds
        # print(f'  {t_ds}')
        add_prop(t_ds)
    else:
        t_ds = ''

    t_ds_normalized = remove_spaces_before_signs(zen_to_han(t_ds)).replace(' ', '\r\n').strip()

    query = f"""INSERT INTO equip(type, [name], ds, t_ds, t_ds_normalized, math, atk, def, note1, note2) 
VALUES({eqtype}, 
"{cnv(name)}", 
"{cnv(ds)}", 
"{cnv(t_ds)}", 
"{t_ds_normalized}", 
"{cnv(math)}", 
"{atk}", 
"{def_}", 
"{cnv(note1)}", 
"{cnv(note2)}")"""
    # print(query)
    cur.execute(query)

def cnv(s):
    if s:
        return s.replace('\r', ' ').replace('\n', ' ').replace('\"', "'").replace('　', ' ').strip().encode('cp932', "ignore").decode('cp932')
    return ''

def parse_atk_def(text: str) -> dict:
    # 大文字小文字を無視してコロン前後の数値を抽出
    atk_match = re.search(r'ATK\s*:\s*(\d+)', text, re.IGNORECASE)
    def_match = re.search(r'DEF\s*:\s*(\d+)', text, re.IGNORECASE)
    
    return {
        "atk": int(atk_match.group(1)) if atk_match else None,
        "def": int(def_match.group(1)) if def_match else None
    }

def zen_to_han(text: str) -> str:
    # 全角英数・記号などを半角に正規化
    return unicodedata.normalize('NFKC', text)


def remove_spaces_before_signs(text: str) -> str:
    # 半角の「+」「-」の前にある1文字以上の半角スペースを削除
    return re.sub(r' +([+\-])', r'\1', text)

def add_prop(t_ds):
    # イルーナのプロパティを配列に追加
    global props
    tokens = t_ds.split(' ')

    for token in tokens:
        token = token.replace('更に', '')
        s = re.sub('[\d\+\-\%\=\.]', '', token).strip()
        if len(s) > 0:
            # 's'のみの場合は秒なので追加しない
            if s == 's':
                continue

            if s not in props:
                # if s == '防御時、確率でパリィ発動':
                #     print(t_ds)
                props.append(s)


if __name__ == '__main__':
    main()
