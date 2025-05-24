from os import truncate
from irunadblib import get_connection, make_db
import re
import jaconv
from lib import unify_fluctuations, write_text

# [equip]
#  id INTEGER PRIMARY KEY AUTOINCREMENT
#  type INTEGER
#  name STRING
#  ds STRING
#  t_ds STRING
#  math STRING
#  note1 STRING
#  note2 STRING

# [prop]
#  id INTEGER PRIMARY KEY AUTOINCREMENT
#  name STRING

# [eq_prop]
#  eqid INTEGER
#  propid INTEGER
#  value REAL
#  unit STRING



def main():

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, type, name, ds, t_ds, math FROM equip")
    equips = cur.fetchall()

    # propの取得
    cur.execute("SELECT id, name FROM prop")
    props = cur.fetchall()
    prop_names = [kv[1] for kv in props]

    maths = []

    for eq in equips:
        math = eq[5].strip()
        if math != '':
            maths.append(math)

        ds = eq[3]
        ds = ds.replace('、 ', '、')
        ds = ds.replace(' 、', '、')
        ds = ds.replace(' が', 'が')
        ds = ds.replace(' しよう', 'しよう')
        ds = ds.replace(' だと', 'だと')
        ds = ds.replace(' して', 'して')
        ds = ds.replace(' で', 'で')
        ds = ds.replace(' の', 'の')
        ds = ds.replace(' ほど', 'ほど')
        ds = ds.replace(' を', 'を')
        ds = ds.replace(' を', 'を')
        ds = ds.replace(' ちょっと', 'ちょっと')
        ds = ds.replace(' の', 'の')
        ds = ds.replace(' ど増加', 'ほど増加')
        ds = ds.replace(' なら', 'なら')
        ds = ds.replace(' ほんの', 'ほんの')
        ds = ds.replace(' ・', '・')
        ds = ds.replace(' 中', '中')
        ds = ds.replace('・ ', '・')

        tokens = ds.split(' ')

        for token in tokens:
            token = jaconv.z2h(token, kana=False, digit=True, ascii=True)
            token = jaconv.h2z(token, kana=True, digit=False, ascii=False)
            s = re.sub('[\d\+\-\%\=\.]', '', token).strip()
            if s not in prop_names:
                prop_names.append(s)

    names = sorted(prop_names)

    with open(f'./propnames.txt', mode='w', encoding = 'utf-8') as fw:
        for nm in names:
            if '・' in nm:
                fw.write(nm + '\n')

    write_text('./maths.txt', '\n'.join(maths))


def split_math(math):
    # 表記ゆれを平坦化
    math = math.replace('[ ', '[').replace(' ]', ']')
    math = unify_fluctuations(math, 'if', 'If')
    math = unify_fluctuations(math, 'then', 'Then')
    math = unify_fluctuations(math, 'when', 'When')
    math = unify_fluctuations(math, 'equip', 'equip')








if __name__ == '__main__':
    main()
