# PMC(2026)に対してNERをおこなう

## 目的
- 実験におけるアクター間の関係を整理する
- そのため、実験に使われる固有名詞に対してさらにアクタークラスを付与する

## 対象
Materials/Method/Ackknowledgementに相当するセクション

## 方法
### 対象セクションのセレクション
#### まず、要素（タグ）の定義を確認
- https://jats.nlm.nih.gov/publishing/tag-library/1.4/index.html
- https://pmc.ncbi.nlm.nih.gov/tagging-guidelines/article/tags/
いずれも、謝辞/方法/材料はタグ名になっていない。
したがって<sec>の属性（sec-type）を検索する。
<sec>の直下の要素に章<title>がある場合がある。
#### 利用されているタグを確認
以下の一部の集計結果を確認する：
- /Volumes/Public/BANK/PMC/2026/stat/PMC001xxxxxx/Ty3.count
- /Volumes/Public/BANK/PMC/2026/stat/PMC003xxxxxx/Ty3.count

タグ用の検索ターム：
- 謝辞
-- "acknowledgement"
- 方法
-- "method"
- 材料
-- "material"
-- "data"
-- "resource"
-- "object" <- 不採用

検索ポリシー：
謝辞を単体で検索、方法・材料はまとめて検索（後者は同一secの可能性があるので）

ツール：
xmllintでよさそう。
