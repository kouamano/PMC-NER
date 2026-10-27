
#!/usr/bin/env python3

import argparse
import csv
import sys
from pathlib import Path

import stanza
from stanza.models.common.doc import Document


def read_morphology(input_file):
    """
    形態素解析済みTSVを読み込み、
    EOS=1を文末として文単位に分割する。

    元のNER値も各トークンのデータとして保持する。
    """
    sentences = []
    current_sentence = []

    with open(input_file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")

        required_columns = {
            "TEXT", "LEMMA", "UPOS", "XPOS", "NER", "EOS"
        }

        if reader.fieldnames is None:
            raise ValueError("入力ファイルにヘッダーがありません。")

        missing = required_columns - set(reader.fieldnames)
        if missing:
            raise ValueError(
                f"入力ファイルに必要なカラムがありません: "
                f"{', '.join(sorted(missing))}"
            )

        for line_no, row in enumerate(reader, start=2):
            if not row.get("TEXT"):
                continue

            # 元のNERを含むトークン情報を保持する
            token = {
                "TEXT": row["TEXT"],
                "LEMMA": row["LEMMA"],
                "UPOS": row["UPOS"],
                "XPOS": row["XPOS"],
                "NER": row["NER"],
            }

            current_sentence.append(token)

            eos = row["EOS"].strip()
            if eos == "1":
                sentences.append(current_sentence)
                current_sentence = []

            elif eos != "0":
                raise ValueError(
                    f"{line_no}行目のEOSが不正です: {eos!r}"
                )

    # 最終行がEOS=1でない場合も、残りのトークンを文として処理
    if current_sentence:
        sentences.append(current_sentence)

    return sentences


def make_document(sentences):
    """
    保存済みの形態素解析結果からStanza Documentを構築する。

    NERは元データ側で保持するため、Stanzaの解析用データには
    NERを含めない。
    """
    stanza_data = []

    for sentence in sentences:
        words = []

        for token_id, token in enumerate(sentence, start=1):
            words.append({
                "id": token_id,
                "text": token["TEXT"],
                "lemma": token["LEMMA"],
                "upos": token["UPOS"],
                "xpos": token["XPOS"],
            })

        stanza_data.append(words)

    return Document(stanza_data)


def write_dependency_tree(doc, original_sentences, output_file):
    """
    依存構造解析の結果と元のNERを対応付けてTSVに出力する。
    """
    fieldnames = [
        "SENT_ID",
        "TOKEN_ID",
        "TEXT",
        "LEMMA",
        "UPOS",
        "XPOS",
        "NER",
        "HEAD_ID",
        "HEAD_TEXT",
        "DEPREL",
    ]

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()

        for sent_id, sentence in enumerate(doc.sentences, start=1):
            # 同じ文の元トークン一覧。NERはここから取得する
            original_tokens = original_sentences[sent_id - 1]

            for word in sentence.words:
                token_id = word.id

                # 元のNERをトークンIDで対応付ける
                if token_id < 1 or token_id > len(original_tokens):
                    raise ValueError(
                        f"文{sent_id}のトークンIDが元データと"
                        f"対応しません: {token_id}"
                    )

                original_token = original_tokens[token_id - 1]

                # head=0はROOT。それ以外は同じ文内のトークンID
                if word.head == 0:
                    head_text = "ROOT"
                else:
                    head_word = next(
                        (
                            w for w in sentence.words
                            if w.id == word.head
                        ),
                        None,
                    )
                    head_text = head_word.text if head_word else ""

                writer.writerow({
                    "SENT_ID": sent_id,
                    "TOKEN_ID": token_id,
                    "TEXT": word.text,
                    "LEMMA": word.lemma or "",
                    "UPOS": word.upos or "",
                    "XPOS": word.xpos or "",
                    "NER": original_token["NER"],
                    "HEAD_ID": word.head,
                    "HEAD_TEXT": head_text,
                    "DEPREL": word.deprel or "",
                })


def main():
    parser = argparse.ArgumentParser(
        description="保存済み形態素解析TSVから依存構造木を作成する"
    )
    parser.add_argument(
        "input",
        help="入力TSVファイル（TEXT, LEMMA, UPOS, XPOS, NER, EOS）",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="出力TSVファイル（省略時は入力名_dependency.tsv）",
    )
    parser.add_argument(
        "--model-dir",
        default=None,
        help="Stanzaモデルのディレクトリ（省略時は既定の場所）",
    )

    args = parser.parse_args()

    input_file = Path(args.input)
    output_file = (
        Path(args.output)
        if args.output
        else input_file.with_name(
            input_file.stem + "_dependency.tsv"
        )
    )

    # 形態素解析結果を読み込み、元のNERを保持
    original_sentences = read_morphology(input_file)
    print(f"読み込んだ文数: {len(original_sentences)}")

    if not original_sentences:
        print("入力ファイルに処理対象の文がありません。")
        sys.exit(1)

    # 依存構造解析用のDocumentを構築
    doc = make_document(original_sentences)

    # dir=Noneを渡さないようにする
    pipeline_args = {
        "lang": "en",
        "processors": "depparse",
        "depparse_pretagged": True,
        "verbose": False,
    }

    if args.model_dir:
        pipeline_args["dir"] = args.model_dir

    nlp = stanza.Pipeline(**pipeline_args)

    # 既存の形態素解析結果に対して依存構造解析のみを実行
    doc = nlp(doc)

    # 解析結果と元のNERを統合して出力
    write_dependency_tree(
        doc,
        original_sentences,
        output_file,
    )

    print(f"出力ファイル: {output_file}")


if __name__ == "__main__":
    main()

