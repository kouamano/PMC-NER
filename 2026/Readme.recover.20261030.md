# 20261030
初見：
Mathematicaで計算・export中にNASの接続が切れている。
ノートブックは正常終了している様に見える。

概要：
昨晩中に接続が切れた模様、そのまま接続は切れたまま。
ssh接続も切れていたことからネットワークを疑う。
なお、NASのサーバー側・他のネットワーク機器は正常であることから、当該マシンのネットワーク機能異常である可能性が高い。

再発防止：
これと言って思いつかない。同時書き込みで高負荷になっていた可能性があり、プロセスの同時実行を控える。

## 対象スクリプト
- matmeth-compound-004.nb
- matmeth-compound-005.nb
- matmeth-compound-006.nb
- matmeth-compound-007.nb

まずマウントを回復する：OK

ひとつづつ、確認する：

### matmeth-compound-004.nb
マウントディレクトリからでは遅いのでQNAPにloginする。
- 対象dir: /share/Public/BANK/PMC/2026/ner/element/material_method_other/PMC004xxxxxx/
- ファイル数: 86909
- 対象ファイル:
  - *.con.json : OK
  ```
  $ find . -type f -name '*con.json'| wc
      86909     86909   1911998
  
  $ find . -type f -name '*con.json'| xargs ls -l
  -rwxrwx--- 1 kouamano everyone  26101 2026-10-29 17:47 ./PMC4973646.con.json
  -rwxrwx--- 1 kouamano everyone  24168 2026-10-29 17:08 ./PMC4974194.con.json
  
  $ find . -type f -name '*con.json' -size 0
   #出力なし
  ```
  
  - *.uxn.json : OK
  ```
  $ find . -type f -name '*uxn.json'| wc
    86909     86909   1911998

  $ find . -type f -name '*uxn.json'| xargs ls -l
   ...

  $ find . -type f -name '*uxn.json' -size 0
   #出力なし
  ```
- nbをsaveしてclose

### matmeth-compound-005.nb

- 対象dir: /share/Public/BANK/PMC/2026/ner/element/material_method_other/PMC005xxxxxx/
- ファイル数: 87129
- 対象ファイル:
  - *.con.json : OK
  ```
  $ find . -type f -name '*con.json'| wc
      87129     87129   1916838
  
  $ find . -type f -name '*con.json'| xargs ls -l
   ...
  
  $ find . -type f -name '*con.json' -size 0
   #出力なし
  ```
  
  - *.uxn.json : OK
  ```
  $ find . -type f -name '*uxn.json'| wc
      87129     87129   1916838

  $ find . -type f -name '*uxn.json'| xargs ls -l
   ...

  $ find . -type f -name '*uxn.json' -size 0
   #出力なし
  ```
- nbをsaveしてclose

### matmeth-compound-006.nb
途中でエラーが出ている。まず、エラー部分を再実行する。
再実行完了。
- 対象dir: /share/Public/BANK/PMC/2026/ner/element/material_method_other/PMC006xxxxxx/
- ファイル数: 98675
- 対象ファイル:
  - *.con.json : OK
  ```
  $ find . -type f -name '*con.json'| wc
      98675     98675   2170850
  
  $ find . -type f -name '*con.json'| xargs ls -l
   ...
  
  $ find . -type f -name '*con.json' -size 0
   #出力なし
  ```
  
  - *.uxn.json : OK
  ```
  $ find . -type f -name '*uxn.json'| wc
      98675     98675   2170850

  $ find . -type f -name '*uxn.json'| xargs ls -l
   ...

  $ find . -type f -name '*uxn.json' -size 0
   #出力なし
  ```
- nbをsaveしてclose

### matmeth-compound-007.nb
途中でエラーが出ている。まず、エラー部分を再実行する。

再実行中。
- 対象dir: /share/Public/BANK/PMC/2026/ner/element/material_method_other/PMC007xxxxxx/
- ファイル数: 91319
- 対象ファイル:
  - *.con.json : 
  ```
  $ find . -type f -name '*con.json'| wc
  
  
  $ find . -type f -name '*con.json'| xargs ls -l
   ...
  
  $ find . -type f -name '*con.json' -size 0
  
  ```
  
  - *.uxn.json : 
  ```
  $ find . -type f -name '*uxn.json'| wc
  

  $ find . -type f -name '*uxn.json'| xargs ls -l
   ...

  $ find . -type f -name '*uxn.json' -size 0
  
  ```
- nbをsaveしてclose
