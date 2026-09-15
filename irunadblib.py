import sqlite3

dbname = 'iruna.db'

def main():
    make_db()


def make_db():
    with get_connection() as conn:
        cur = conn.cursor()
        create_equip_table(cur)
        create_prop_table(cur)
        create_eq_prop_table(cur)
        insert_prop(cur)

# prop.nameを持つ装備
# select eq.type, eq.name, eqp.value from equip as eq, eq_prop as eqp, prop as pp where pp.name like '%火属性に物理%' and eqp.value > 0 and pp.id = eqp.propid and eqp.eqid = eq.id order by eq.type, eqp.value desc;

def create_equip_table(cur):
    if not exists_table(cur, 'equip'):
        cur.execute("""CREATE TABLE equip(
id INTEGER PRIMARY KEY AUTOINCREMENT,
type INTEGER,
name STRING,
ds STRING,
ds_normalized STRING,
t_ds STRING,
math STRING,
atk STRING,
def STRING,
note1 STRING,
note2 STRING
)""")

def create_prop_table(cur):
    if not exists_table(cur, 'prop'):
        cur.execute("""CREATE TABLE prop(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name STRING
)""")

def create_eq_prop_table(cur):
    if not exists_table(cur, 'eq_prop'):
        cur.execute("""CREATE TABLE eq_prop(
eqid INTEGER,
propid INTEGER,
value REAL,
unit STRING,
PRIMARY KEY(eqid, propid))""")

def delete_equip_table(cur):
    cur.execute('DELETE FROM equip')

def insert_prop(cur):
    cur.execute("INSERT INTO prop(name) VALUES('STR')")
    cur.execute("INSERT INTO prop(name) VALUES('AGI')")
    cur.execute("INSERT INTO prop(name) VALUES('VIT')")
    cur.execute("INSERT INTO prop(name) VALUES('INT')")
    cur.execute("INSERT INTO prop(name) VALUES('DEX')")
    cur.execute("INSERT INTO prop(name) VALUES('CRT')")
    cur.execute("INSERT INTO prop(name) VALUES('ATK')")
    cur.execute("INSERT INTO prop(name) VALUES('MATK')")
    cur.execute("INSERT INTO prop(name) VALUES('DEF')")
    cur.execute("INSERT INTO prop(name) VALUES('MDEF')")
    cur.execute("INSERT INTO prop(name) VALUES('ASPD')")
    cur.execute("INSERT INTO prop(name) VALUES('MaxHP')")
    cur.execute("INSERT INTO prop(name) VALUES('MaxMP')")
    cur.execute("INSERT INTO prop(name) VALUES('物理耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('魔法耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('異常耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('全属性耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('闇耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('光耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('水耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('風耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('無耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('地耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('火耐性')")
    cur.execute("INSERT INTO prop(name) VALUES('範囲軽減')")
    cur.execute("INSERT INTO prop(name) VALUES('スタン中ダメージ軽減')")
    cur.execute("INSERT INTO prop(name) VALUES('全ダメージ軽減')")
    cur.execute("INSERT INTO prop(name) VALUES('割合軽減')")
    cur.execute("INSERT INTO prop(name) VALUES('詠唱防御')")
    cur.execute("INSERT INTO prop(name) VALUES('ボスに物理')")
    cur.execute("INSERT INTO prop(name) VALUES('クリティカルダメージ')")
    cur.execute("INSERT INTO prop(name) VALUES('無属性に物理')")
    cur.execute("INSERT INTO prop(name) VALUES('水属性に物理')")
    cur.execute("INSERT INTO prop(name) VALUES('闇属性に物理')")
    cur.execute("INSERT INTO prop(name) VALUES('火属性に物理')")
    cur.execute("INSERT INTO prop(name) VALUES('光属性に物理')")
    cur.execute("INSERT INTO prop(name) VALUES('風属性に物理')")
    cur.execute("INSERT INTO prop(name) VALUES('地属性に物理')")
    cur.execute("INSERT INTO prop(name) VALUES('物理貫通')")
    cur.execute("INSERT INTO prop(name) VALUES('物理威力')")
    cur.execute("INSERT INTO prop(name) VALUES('クリティカル率')")
    cur.execute("INSERT INTO prop(name) VALUES('シェルブレイク率')")
    cur.execute("INSERT INTO prop(name) VALUES('命中')")
    cur.execute("INSERT INTO prop(name) VALUES('絶対命中')")
    cur.execute("INSERT INTO prop(name) VALUES('ボスに魔法')")
    cur.execute("INSERT INTO prop(name) VALUES('魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('闇魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('水魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('光魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('無魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('火魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('風魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('地魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('魔法貫通')")
    cur.execute("INSERT INTO prop(name) VALUES('魔法威力')")
    cur.execute("INSERT INTO prop(name) VALUES('スペルバースト率')")
    cur.execute("INSERT INTO prop(name) VALUES('絶対回避')")
    cur.execute("INSERT INTO prop(name) VALUES('魔法回避')")
    cur.execute("INSERT INTO prop(name) VALUES('回避')")
    cur.execute("INSERT INTO prop(name) VALUES('ヒール回復')")
    cur.execute("INSERT INTO prop(name) VALUES('アイテム回復')")
    cur.execute("INSERT INTO prop(name) VALUES('HP自然回復')")
    cur.execute("INSERT INTO prop(name) VALUES('MP自然回復')")
    cur.execute("INSERT INTO prop(name) VALUES('HP回復')")
    cur.execute("INSERT INTO prop(name) VALUES('MP回復')")
    cur.execute("INSERT INTO prop(name) VALUES('ヒール受け')")
    cur.execute("INSERT INTO prop(name) VALUES('ダメージ反射')")
    cur.execute("INSERT INTO prop(name) VALUES('オートスキル発動')")
    cur.execute("INSERT INTO prop(name) VALUES('反動ダメージ')")
    cur.execute("INSERT INTO prop(name) VALUES('防御時、確率でパリィ発動')")
    cur.execute("INSERT INTO prop(name) VALUES('回避時反撃率')")
    cur.execute("INSERT INTO prop(name) VALUES('攻撃間隔半減')")
    cur.execute("INSERT INTO prop(name) VALUES('スキルディレイ')")
    cur.execute("INSERT INTO prop(name) VALUES('アイテムディレイ')")
    cur.execute("INSERT INTO prop(name) VALUES('詠唱時間')")
    cur.execute("INSERT INTO prop(name) VALUES('MP消費')")
    cur.execute("INSERT INTO prop(name) VALUES('ヘイト増加')")
    cur.execute("INSERT INTO prop(name) VALUES('射程')")
    cur.execute("INSERT INTO prop(name) VALUES('移動速度')")
    cur.execute("INSERT INTO prop(name) VALUES('ドロップ')")
    cur.execute("INSERT INTO prop(name) VALUES('経験値')")
    cur.execute("INSERT INTO prop(name) VALUES('毒発生')")
    cur.execute("INSERT INTO prop(name) VALUES('出血発生')")
    cur.execute("INSERT INTO prop(name) VALUES('凍結発生')")
    cur.execute("INSERT INTO prop(name) VALUES('恐怖発生')")
    cur.execute("INSERT INTO prop(name) VALUES('発火発生')")
    cur.execute("INSERT INTO prop(name) VALUES('暗闇発生')")
    cur.execute("INSERT INTO prop(name) VALUES('気絶発生')")
    cur.execute("INSERT INTO prop(name) VALUES('麻痺発生')")
    cur.execute("INSERT INTO prop(name) VALUES('気絶時間')")
    cur.execute("INSERT INTO prop(name) VALUES('麻痺時間')")
    cur.execute("INSERT INTO prop(name) VALUES('脱力時間')")
    cur.execute("INSERT INTO prop(name) VALUES('眩暈時間')")
    cur.execute("INSERT INTO prop(name) VALUES('恐怖時間')")
    cur.execute("INSERT INTO prop(name) VALUES('発火時間')")
    cur.execute("INSERT INTO prop(name) VALUES('凍結持続')")
    cur.execute("INSERT INTO prop(name) VALUES('麻痺持続')")
    cur.execute("INSERT INTO prop(name) VALUES('毒持続')")
    cur.execute("INSERT INTO prop(name) VALUES('発火ダメージ')")
    cur.execute("INSERT INTO prop(name) VALUES('出血ダメージ')")
    cur.execute("INSERT INTO prop(name) VALUES('毒効果')")
    cur.execute("INSERT INTO prop(name) VALUES('生産ロスト率')")
    cur.execute("INSERT INTO prop(name) VALUES('生産大成功率')")
    cur.execute("INSERT INTO prop(name) VALUES('鍛冶の成功確率')")
    cur.execute("INSERT INTO prop(name) VALUES('木工の成功確率')")
    cur.execute("INSERT INTO prop(name) VALUES('裁縫の成功確率')")
    cur.execute("INSERT INTO prop(name) VALUES('彫金の成功確率')")
    cur.execute("INSERT INTO prop(name) VALUES('錬金術の成功確率')")
    cur.execute("INSERT INTO prop(name) VALUES('調理の成功確率')")

def exists_table(cur, table_name):
    cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='{table_name}'")
    if cur.fetchone()[0] == 0:
        return False
    return True

def execute(query):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

def get_connection():
    return sqlite3.connect(dbname)

if __name__ == '__main__':
    main()
