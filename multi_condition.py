from irunadblib import get_connection, make_db


conditions = [
    # ■ 防御系
    # ['物理耐性', '<=', '-30'],
    # ['魔法耐性', '<=', '-35'],

    # ['回避', '>=', '20'],
    # ['絶対回避', '>=', '10'],
    # ['魔法回避', '>=', '5'],

    # ['異常耐性', '>=', '10'],
    # ['割合軽減', '>=', '20'],
    # ['範囲軽減', '>=', '10'],
    # ['全ダメージ軽減', '>=', '1'],
    # ['全属性耐性', '>=', '1'],
    # ■ 物理系
    # ['ATK', '>=', '15'],
    # ['クリティカルダメージ', '>=', '15'],
    # ['物理貫通', '<', '0'],
    # ['ボスに物理', '>=', '1'],
    # ■ 魔法系
    # ['MATK', '>=', '10'],
    # ['ボスに魔法', '>=', '1'],
    # ['魔法貫通', '>=', '5'],
    # ['スペルバースト率', '>=', '7'],
    # ['魔法威力', '>=', '1'],
    # ['水魔法威力', '>=', '10'],
    # ['土魔法威力', '>=', '10'],
    # ['火魔法威力', '>=', '1'],
    # ['風魔法威力', '>=', '10'],
    # ['光魔法威力', '>=', '10'],
    # ['闇魔法威力', '>=', '1'],
    # ['無魔法威力', '>=', '10'],
    # ['水耐性', '>=', '10'],
    # ['土耐性', '>=', '10'],
    # ['火耐性', '>=', '1'],
    # ['風耐性', '>=', '10'],
    # ['光耐性', '>=', '10'],
    # ['闇耐性', '>=', '5'],
    # ['無耐性', '>=', '10'],
    #### ['全属性耐性', '>=', '1'],

    # ■ その他
    # ['MP消費', '<=', '-20'],
    # ['詠唱時間', '=', '-5'],
    # ['詠唱防御', '>', '5'],
    # ['オートスキル発動', '>=', '2'],
    # ['スキルディレイ', '<=', '-1.0'],
    # ['アイテムディレイ', '<=', '-1.0'],
    # ['ヘイト増加', '>=', '10'],
    # ['発火ダメージ', '>=', '10'],
    # ['出血ダメージ', '>=', '1'],
    # ['出血発生', '>=', '0'],
    # ['毒効果', '>=', '10'],
    # ['MaxHP', '>=', '20'],
    # ['MaxMP', '<=', '-20'],
    # ['CRT', '>=', '15'],
    # ['DEX', '>=', '15'],
    # ['INT', '>=', '10'],
    # ['VIT', '>=', '10'],
    # ['詠唱防御', '>=', '10'],
    ['ヒール回復', '>=', '10'],
    # ['アイテム回復', '>=', '15'],
    # ['ダメージ反射', '>=', '30'],
]

def main():
    conn = get_connection()
    cur = conn.cursor()
    query = make_query()
    print(query)
    cur.execute(query)
    results = cur.fetchall()

    # printではタブ文字が置換されるのでファイル出力
    with open('result.txt', mode="w", encoding="utf-8") as f:
        # 列名
        f.write(query[0: query.find(" from")].replace('select ', '').replace(', ', '\t').replace('x.', '').replace('eq.', '') + '\n')

        for res in results:
            f.write("\t".join(map(str,res))+"\n")



    print(f"{len(results)}件出力")


def make_query():
    cols = ""
    for cond in conditions:
        cols += f", x.{cond[0]}"
    s = f"select x.eqid, eq.type, eq.name{cols}, eq.ds"
    s += f" from equip as eq, ({make_multi_condition_query()}) as x"
    s += " where eq.id = x.eqid"
    return s

def make_multi_condition_query():
    cols = ""
    unions = ""
    havings = ""

    for i, cond in enumerate(conditions):
        # 列名
        name = cond[0]
        cols += f", max({name}) as '{name}'"

        # union
        if unions != "":
            unions += " union "
        unions += make_single_condition(i)

        # having
        if havings != "":
            havings += " and "
        havings += f"max({name} is not null)"

    return f"select eqid{cols} from ({unions}) group by eqid having {havings}"

def make_single_condition(index):
    # 指定された条件配列のクエリを生成
    s = "select eq_prop.eqid "
    for i, cond in enumerate(conditions):
        name= cond[0]
        if i == index:
            s += f", eq_prop.value as '{name}'"
        else:
            s += f", null as '{name}'"
    s += " from eq_prop, prop"
    s += " where prop.id = eq_prop.propid"
    name, op, val = conditions[index]
    s += f" and prop.name = '{name}' and eq_prop.value {op} {val}"
    return s


if __name__ == '__main__':
    main()
