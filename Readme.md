# PMC(2026)に対してNERをおこなう

## 目的
- 実験におけるアクター間の関係を整理する
- そのため、実験に使われる固有名詞に対してさらにアクタークラスを付与する

## 対象
Materials/Method/Acknowledgementに相当するセクション

## 方法
### 対象セクションのセレクション
#### まず、要素（タグ）の定義を確認
- https://jats.nlm.nih.gov/publishing/tag-library/1.4/index.html
- https://pmc.ncbi.nlm.nih.gov/tagging-guidelines/article/tags/
謝辞は<ack>タグ。
方法/材料はいずれもタグ名になっていない。
したがって<sec>の属性（sec-type）を検索する。
<sec>の直下の要素に章<title>がある場合がある。
#### 利用されているタグを確認
以下の一部の集計結果を確認する：
- /Volumes/Public/BANK/PMC/2026/stat/PMC001xxxxxx/Ty3.count
- /Volumes/Public/BANK/PMC/2026/stat/PMC003xxxxxx/Ty3.count

#### 抽出
タグ用の検索ターム：
- 謝辞
  - "ack"
- 方法
  - "method"
- 材料
  - "material"
  - "data"
  - "resource"
  - "object" <- 不採用

検索ポリシー：
- 謝辞：\<ack\>を検索
- 方法・材料：<sec>の属性sec-typeの属性値として検索

ツール：
xmllintでよさそう。 -> 抽出完了

クリーニング：
０バイトファイルがあるのでrmする。 -> クリーニング完了

結果：
/Volumes/Public/BANK/PMC/2026/xml/element/{ack|material_method_other} （ファイルリストまで作成済み）

```sh
$ for dir in *; do cd $dir; pwd; ls|wc; cd ../; done
/share/Public/BANK/PMC/2026/xml/element/ack/PMC000xxxxxx
       73        73      1095
/share/Public/BANK/PMC/2026/xml/element/ack/PMC001xxxxxx
     1554      1554     24864
/share/Public/BANK/PMC/2026/xml/element/ack/PMC002xxxxxx
    28137     28137    450192
/share/Public/BANK/PMC/2026/xml/element/ack/PMC003xxxxxx
    67671     67671   1082736
/share/Public/BANK/PMC/2026/xml/element/ack/PMC004xxxxxx
    74338     74338   1189408
/share/Public/BANK/PMC/2026/xml/element/ack/PMC005xxxxxx
    79362     79362   1269792
/share/Public/BANK/PMC/2026/xml/element/ack/PMC006xxxxxx
    89577     89577   1433232
/share/Public/BANK/PMC/2026/xml/element/ack/PMC007xxxxxx
    88049     88049   1408784
/share/Public/BANK/PMC/2026/xml/element/ack/PMC008xxxxxx
    99870     99870   1597920
/share/Public/BANK/PMC/2026/xml/element/ack/PMC009xxxxxx
   112118    112118   1793888
/share/Public/BANK/PMC/2026/xml/element/ack/PMC010xxxxxx
   117292    117292   1993964
/share/Public/BANK/PMC/2026/xml/element/ack/PMC011xxxxxx
   179586    179586   3052962
/share/Public/BANK/PMC/2026/xml/element/ack/PMC012xxxxxx
   163364    163364   2777188
```

```sh
$ for dir in *; do cd $dir; pwd; ls|wc; cd ../; done           
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC000xxxxxx
       95        95      1425
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC001xxxxxx
     1322      1322     21152
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC002xxxxxx
    27892     27892    446272
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC003xxxxxx
    72514     72514   1160224
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC004xxxxxx
    86909     86909   1390544
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC005xxxxxx
    87129     87129   1394064
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC006xxxxxx
    98675     98675   1578800
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC007xxxxxx
    91319     91319   1461104
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC008xxxxxx
   106733    106733   1707728
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC009xxxxxx
   125475    125475   2007600
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC010xxxxxx
   138561    138561   2355537
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC011xxxxxx
   193707    193707   3293019
/share/Public/BANK/PMC/2026/xml/element/material_method_other/PMC012xxxxxx
   174186    174186   2961162
```

XMLのクリーニング：
xmlタグの除去等のクリーニングを行う。-> タグを落とすとタームが接続されるので要素間に空白を挿入する必要がある。xmllintでは面倒なのでxtqとawkを使って整形する。
余分な空白が入ってもstanzaのパースに影響はない。

以下はNERまで一気に行うスクリプト：

```sh
xtq in=PMC466942.xml buff=100000000 -pBS -n|grep -e '\[Ty16\]' | awk -F']]]' '{print $5}' \
| /Users/kouamano/gitsrc/PMC-NER/2026/exec_command/stanza-cli-S.py --ner > /Users/kouamano/tmp/xtq.txt.ner
```

タグ除去テキストを作成する場合は /Volumes/Public/BANK/PMC/2026/xml/element/{ack|material_method_other}/ 配下に xxx.xml.txt として作成する。
