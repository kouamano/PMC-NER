
#!/usr/bin/env python3

import argparse
import csv
import stanza
from stanza.models.common.doc import Document


def read_morphology(path):
    """既存の形態素解析結果を読み込む。"""
    sentences = []
    current = []

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")

        required = {"TEXT", "LEMMA", "UPOS", "XPOS", "EOS"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                f"必要な列がありません。必要列: {sorted(required)}"
            )

        for line_no, row in enumerate(reader, start=2):
            if not row.get("TEXT"):
                continue

            # 既存のトークン順を維持する
            current.append({
                "id": len(current) + 1,
                "text": row["TEXT"],
                "lemma": row["LEMMA"],
                "upos": row["UPOS"],
                "xpos": row["XPOS"],
                "ner": row.get("NER", "O"),
            })

            eos = row["EOS"].strip()
            if eos == "1":
                sentences.append(current)
                current = []
            elif eos != "0":
                raise ValueError(
                    f"{line_no}行目: EOSは0または1である必要があります"
                )

    # 最終トークンにEOS=1がない場合も、残りを文として処理する
    if current:
        print(
            "警告: 最終文にEOS=1がありません。"
            "残りのトークンを1文として処理します。"
        )
        sentences.append(current)

    return sentences


def make_document(sentences):
    """既存のトークン・品詞情報からStanza Documentを構築する。"""
    data = []

    for sent in sentences:
        words = []
        for token in sent:
            words.append({
                "id": token["id"],
                "text": token["text"],
                "lemma": token["lemma"],
                "upos": token["upos"],
                "xpos": token["xpos"],
            })
        data.append(words)

    return Document(data)


def main():
    parser = argparse.ArgumentParser(
        description="保存済み形態素解析結果から依存構造木を作成"
    )
    parser.add_argument("input", help="入力TSVファイル")
    parser.add_argument(
        "-o", "--output",
        default="dependency.tsv",
        help="出力TSVファイル（既定: dependency.tsv）"
    )
    parser.add_argument(
        "--model-dir",
        default=None,
        help="Stanzaモデルの保存先（省略可）"
    )
    args = parser.parse_args()

    sentences = read_morphology(args.input)
    print(f"読み込んだ文数: {len(sentences)}")

    # 依存構造解析のみ実行する
    nlp = stanza.Pipeline(
        lang="en",
        processors="depparse",
        depparse_pretagged=True,
        verbose=False,
    )

    document = make_document(sentences)
    parsed = nlp(document)

    # 出現位置を区別できるよう、文IDとトークンIDを保存する
    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow([
            "SENT_ID", "TOKEN_ID", "TEXT", "LEMMA",
            "UPOS", "XPOS", "HEAD_ID", "HEAD_TEXT", "DEPREL"
        ])

        for sent_id, sentence in enumerate(parsed.sentences, start=1):
            words = sentence.words

            for word in words:
                head_id = word.head
                head_text = (
                    "ROOT" if head_id == 0
                    else words[head_id - 1].text
                )

                writer.writerow([
                    sent_id,
                    word.id,
                    word.text,
                    word.lemma,
                    word.upos,
                    word.xpos,
                    head_id,
                    head_text,
                    word.deprel,
                ])

    print(f"出力しました: {args.output}")


if __name__ == "__main__":
    main()

