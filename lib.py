import re

def write_text(outputfile, text):
    # 指定されたファイルにテキストを出力
    with open(outputfile, mode='w', encoding='utf-8') as f:
        f.write(text)


def read_text(inputfile):
    with open(inputfile, mode='r', encoding='utf-8') as f:
        return f.read()


def unify_fluctuations(target, befor, after):
    # targetに含まれるbeforをafterに統一する
    # beforは大文字、小文字を区別しない
    cmp = re.compile(befor, re.IGNORECASE)
    return re.sub(cmp, after, target)


def included_lines(text, words):
    # 指定されたワードが含まれる行を抽出する
    return [line for line in text.splitlines() if exist_words(line, words)]


def exist_words(text, words):
    # いずれかのワードが含まれる場合は真
    for word in words:
        if word in text:
            return True
    return False


def find_first_index(s, words):
    # 全ての単語の開始位置を探索
    first_word_pos = [s.find(word) for word in words]

    # 有効な位置が存在する場合は一番先頭の位置を返却、存在しなかった場合は-1
    valid_pos = [pos for pos in first_word_pos if pos >=0]
    if valid_pos == []:
        return -1
    return min(valid_pos)
