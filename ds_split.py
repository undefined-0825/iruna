from irunadblib import get_connection
import re
import unicodedata

def main():
    # データベースからt_dsを取得して正規化し、ds_normalizedカラムを更新
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, t_ds FROM equip")
        rows = cur.fetchall()
        
        for row in rows:
            t_ds = row[1]
            t_ds_str = str(t_ds) if t_ds is not None else ""
            ds_normalized = remove_spaces_before_signs(zen_to_han(t_ds_str)).replace(' ', '\r\n').strip()
            print(ds_normalized)
            cur.execute("UPDATE equip SET ds_normalized = ? WHERE id = ?", (ds_normalized, row[0]))

    conn.commit()


def zen_to_han(text: str) -> str:
    # 全角英数・記号などを半角に正規化
    return unicodedata.normalize('NFKC', text)


def remove_spaces_before_signs(text: str) -> str:
    # 半角の「+」「-」の前にある1文字以上の半角スペースを削除
    return re.sub(r' +([+\-])', r'\1', text)


if __name__ == "__main__":
    main()