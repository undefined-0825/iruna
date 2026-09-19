import re
from irunadblib import get_connection

def main():
    make_equip_property()

def make_equip_property():
    with get_connection() as conn:

        cur = conn.cursor()
        # equipの取得
        cur.execute("SELECT id, type, name, ds, t_ds FROM equip")
        equips = cur.fetchall()

        # propの取得
        cur.execute("SELECT id, name FROM prop")
        props = cur.fetchall()

        for eq in equips:
            eqid = eq[0]
            name = eq[2]
            t_ds = str(eq[4])

            # propを走査
            for prop in props:
                propid = prop[0]
                propname = prop[1]
                val, unit = find_value(t_ds, propname)
                if val:
                    s = re.sub('[\d\+\-\%\=\.]', '', val).strip()
                    if len(s) > 0:
                        if s != 's':
                            print(f'--- {name} --------------')
                            print(f"{propname} : {s}")
                            continue
                    #
                    cur.execute(f"INSERT INTO eq_prop(eqid, propid, value, unit) VALUES({eqid}, {propid}, {val}, '{unit}')")

        # iruna onlineの補正
        # ガンデーヴァのオートスキルは物理威力
        buturi = find_propid(props, '物理威力')
        autoskill = find_propid(props, 'オートスキル発動')
        if buturi:
            gandava_equips = find_equips(equips, 'ガンデーヴァ')
            for eq in gandava_equips:
                cur.execute(f"UPDATE eq_prop SET propid = {buturi} WHERE eqid = {eq[0]} AND propid = {autoskill}")

def find_equips(equips, name):
    # 指定された名称のpropidを返却
    return [equip for equip in equips if name in equip[2]]

def find_propid(props, name):
    # 指定された名称のpropidを返却
    for prop in props:
        if prop[1] == name:
            return prop[0]
    return None

def find_value(t_ds, propname):
    # 指定された単語を検索
    hit = t_ds.find(propname + ' ')
    if hit < 0:
        return '', ''

    # 固有のプロパティは真偽値として扱う
    # if propname == 'オートスキル発動' or propname == '攻撃間隔半減':
    if propname == '攻撃間隔半減':
        return '1', ''

    digitReg = re.compile(r'^[0-9\-\.]+$')

    # 見つかった位置から文字を走査し、登録用のvalueとunitに分割する
    value = ''
    unit = ''
    start = hit + len(propname)
    for i in range(len(t_ds) - start):
        c = t_ds[start + i]
        if c == ' ':
            # 空白が見つかったら終了する
            if len(value + unit) > 0:
                break
        elif c == '+':
            # +は無視
            continue
        elif digitReg.match(c):
            value += c
        else:
            unit += c

    if len(value + unit) == 0:
        print(f"  {propname}：なし")

    # print(f"{value} {unit}")

    return value, unit

if __name__ == '__main__':
    main()
