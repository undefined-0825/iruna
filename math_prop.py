import re
from irunadblib import get_connection
import re
import unicodedata

def main():
    split_math()

def split_math():
    # データベースからmathを取得して正規化し、ds_normalizedカラムを更新
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, math FROM equip where math <> ''")
        rows = cur.fetchall()
        
        for row in rows:
            math = row[1]
            # print("--------------------")
            # print(math)
            results = split_property_blocks(math)
            # for line in results:
            #     print(f"- {line}")
            math_normalized = "\r\n".join(results).strip()
            cur.execute("UPDATE equip SET math_normalized = ? WHERE id = ?", (math_normalized, row[0]))

    conn.commit()



def split_property_blocks(text: str) -> list[str]:
    if not text:
        return []

    text = normalyse_text(text)
    blocks = []
    if_block = False
    bracket_block_count = 0
    token = ''

    for i in range(len(text)):
        c = text[i]
        token += c

        if c == '[':
            bracket_block_count += 1
        elif c == ']':
            bracket_block_count -= 1

        if len(token) > 2:
            if token[-3:] == 'if ':
                if_block = True

            if if_block:
                if token[-5:] == ' then':
                    blocks.append(token.strip())
                    token = ''
                    if_block = False
            else:
                if (c == ']' or c == ' ') and bracket_block_count == 0:
                    blocks.append(token.strip())
                    token = ''

    blocks.append(token.strip())  # 最後のトークンを追加
    return blocks


def normalyse_text(text: str) -> str:
    # 全角英数・記号などを半角に正規化
    normalized = unicodedata.normalize('NFKC', text)
    #[,]前後の半角空白を正規化
    normalized = normalized.replace('[ ', '[').replace(' ]', ']')
    # 連続する空白を1つの半角スペースにまとめ、前後の余計な空白も除去
    normalized = " ".join(normalized.split())
    # 算術記号の前後にある1文字以上の半角スペースを削除
    normalized = re.sub(r' *([+\-*/=]) *', r'\1', normalized)
    # Ifを統一
    normalized = normalized.replace('If', 'if')
    # # %の後のif, [の前に半角スペースを追加
    # normalized = re.sub(r'(%)(if|\[)', r'\1 \2', normalized)
    return normalized.strip()



# # --- 動作確認 ---
# test_cases = [
#     # ケース1: 単一のタグ/計算式
#     "[Minstrel] ATK +6% クリティカルダメージ +3% [ up by Lv] +100 ASPD +10% オートスキル発動",
    
#     # ケース2: If〜then 条件式
#     "If [STR > 256] then MATK +6% If [VIT > 256] then 詠唱防御 +10% If [AGI > 256] then スキルディレイ -0.5s If [CRT > 256] then スペルバースト率 +5%",
    
#     # ケース3: 複数連結 [計算式1] [計算式2]
#     "If [STR > 400] then シェルブレイク率 +10% [X = 5.00 * Lv] [ up by X] 魔法耐性 -10%",
#     # ケース4: [の後に半角空白があるケース
#     "[ up by Lv]",
#     # ケース5: 半角空白が連続
#     "[X = 0.20 * VIT] [回避 up by X] [X = X / 2] [回避時反撃率 up by X] [X = X  -3] [VIT up by X]",
# ]

# for idx, case in enumerate(test_cases, 1):
#     print(f"--- Case {idx} ---")
#     print(f"Input: {case}")
#     results = split_property_blocks(case)
#     for line in results:
#         print(line)


    


if __name__ == "__main__":
    main()