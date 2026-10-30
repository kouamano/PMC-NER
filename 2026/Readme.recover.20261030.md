# 20261030
Mathematicaで計算・export中にNASの接続が切れている。
ノートブックは正常終了している様に見える。

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
マウントディレクトリからでは遅いのでQNAPにloginする。
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
  
  - *.uxn.json : 
  ```
  $ find . -type f -name '*uxn.json'| wc
      87129     87129   1916838

  $ find . -type f -name '*uxn.json'| xargs ls -l
   ...

  $ find . -type f -name '*uxn.json' -size 0
   #出力なし
  ```
- nbをsaveしてclose
