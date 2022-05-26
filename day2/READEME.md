# 제 2과제 1일차 연습 문제

## 1. Kinesis Data Stream
### 다음과 같이 테이블을 구성합니다.
Name: stock_table

Connector: kinesis

Stream Name : wsi-data-stream-<비번호>

Region : us-east-1

Format : json

Column
- TICKER VARCHAR(4)
- EVENT_TIME TIMESTAMP(3)
- PRICE FLOAT

##### EVENT_TIME은 'ISO_8601'로 포맷되어야 합니다.

## 2. S3 Sink
### 다음과 같이 테이블(S3 Sink)을 구성합니다.

Name : s3_sink_table

Connector : filesystem

path : s3://wsi-kinesis-<비번호>/result

Format : json

Column
- TICKER VARCHAR(4)
- EVENT_TIME TIMESTAMP(3)
- PRICE FLOAT

S3로 Sink되는 데이터가 TICKER를 기준으로 폴더 단위로 분리되어야 합니다.


