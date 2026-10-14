# NER処理とは別にいくつかの特定のタームを検索する
NER結果はタームが改行でバラされるので、xmlもしくはテキストベースであらかじめ検索しておくターム（あるいはフレーズ）を設定する。
## Kagoshima University
- Term: "Kagoshima University"
- Target: 「材料・方法」および「謝辞」パート
  - /Volumes/Public/BANK/PMC/2026/xml/element/ack/PMC\<NNN\>xxxxxx/*xml
  - /Volumes/Public/BANK/PMC/2026/xml/element/material_method_other/PMC\<NNN\>xxxxxx/*xml
- Result（ファイル名のみ）: /Volumes/Public/BANK/PMC/2026/search/Kagoshima_Univ/

## 検索例
ワイルドカードを用いると引数展開で上限数を超える。なのでfindで指定する：
find ./PMC003xxxxxx/ -type f -name '*xml' | xargs grep -l 'Kagoshima University' > /share/Public/BANK/PMC/2026/search/Kagoshima_Univ/ack/PMC003xxxxxx.list
