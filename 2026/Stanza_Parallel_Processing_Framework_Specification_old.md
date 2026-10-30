# Stanza Parallel Processing Framework Specification (Old)

## 1. Purpose

本システムは、大量のテキストファイルを **Stanza**
を用いて高速に解析するための並列処理フレームワークである。

### 目的

-   Stanza Pipeline のロード回数を最小化する
-   CPUコアを有効利用する
-   大量ファイルを効率よく処理する
-   エラーが発生しても処理全体を停止させない
-   将来的な拡張（GPU・別NLPエンジン等）を容易にする

------------------------------------------------------------------------

## 2. System Architecture

``` text
                config.yaml
                     │
                     ▼
              run_workers.py
                     │
        ┌────────────┴────────────┐
        │                         │
     JobQueue                 ResultQueue
        │                         ▲
        ▼                         │
 Worker 1  Worker 2 ... Worker N
        │
        ▼
  Stanza Pipeline
        │
        ▼
 Output Files
```

------------------------------------------------------------------------

## 3. Components

### 3.1 run_workers.py

ユーザーが直接実行するプログラム。

責務

-   config.yaml を読み込む
-   JobQueue を生成する
-   ResultQueue を生成する
-   Worker を起動する
-   進捗を表示する
-   summary.log を生成する

### 3.2 stanza_worker.py

Workerプロセス。

責務

-   起動時に Pipeline を1回だけロードする
-   JobQueueからJobを取得する
-   ファイルを解析する
-   結果を書き出す
-   ResultQueueへ統計情報を返す
-   workerログを生成する

Workerは複数ファイルを連続処理する。

------------------------------------------------------------------------

## 4. Queue

-   `multiprocessing.Queue` を使用する。
-   外部Message Queue（RabbitMQ, Redis, ZeroMQ等）はVersion
    1では使用しない。

理由

-   同一マシンで動作
-   Python標準ライブラリのみ
-   通信オーバーヘッドが小さい

------------------------------------------------------------------------

## 5. Job

Queueへ流す単位。

``` text
Job
  input_file
  output_file
```

本文データはQueueへ流さない。

------------------------------------------------------------------------

## 6. Result

``` text
Result
  worker_id
  input_file
  output_file
  status
  elapsed_time
  sentence_count
  token_count
  error_message
```

status:

-   OK
-   ERROR
-   SKIPPED

------------------------------------------------------------------------

## 7. Input

config.yaml

``` yaml
input:
  file_list: /data/files.txt
```

files.txt

``` text
/data/a.txt<TAB>/result/a.tsv
/data/b.txt<TAB>/result/b.tsv
```

------------------------------------------------------------------------

## 8. Worker Processing

``` text
Pipelineロード（1回）

while True
    Job取得
    Job無しなら終了
    File読込
    Stanza解析
    出力保存
    Result返却
```

------------------------------------------------------------------------

## 9. Output

TSV列

-   DOC_ID
-   SENT_ID
-   TOKEN_ID
-   TEXT
-   LEMMA
-   UPOS
-   XPOS
-   NER
-   EOS

------------------------------------------------------------------------

## 10. Logging

### Worker Log

    logs/
        worker_001.log
        worker_002.log

### Summary Log

    summary.log

### Error File

    errors.tsv

------------------------------------------------------------------------

## 11. Progress Display

標準出力には進捗のみ表示する。

例

``` text
Processed: 1200 / 25000
Worker1: paper001
Worker2: paper532
Elapsed: 00:13:22
```

------------------------------------------------------------------------

## 12. Configuration

``` yaml
input:
  file_list:

output:
  directory:

stanza:
  lang:
  processors:

parallel:
  workers:

logging:
  directory:
```

------------------------------------------------------------------------

## 13. Error Handling

Workerで例外が発生した場合は

-   workerログへ記録
-   ResultQueueへERROR返却
-   次のJobを継続

親プロセスは停止しない。

------------------------------------------------------------------------

## 14. Future Extensions

-   resume
-   GPU
-   JSON出力
-   gzip出力
-   Dependency Parse
-   Constituency Parse
-   Coreference
-   REST Server
-   ZeroMQ
-   RabbitMQ

------------------------------------------------------------------------

## 15. Design Policy

優先順位

1.  シンプル
2.  高速
3.  保守性
4.  拡張性

Version 1では、大量テキスト解析への最適化を優先する。
