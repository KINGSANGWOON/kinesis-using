# Usage Flink Stream SQL
### [ ] ⬅ 생략 가능
## Create Table
```
CREATE TABLE <table-name> (
    column1 type,
    column2 type,
    .
    .
    .
)
[COMMENT table_comment]
[PARTITIONED BY (partition_column_name1, partition_column_name2, ...)]
WITH (
    key1 = val1,
    key2 = val2,
    .
    .
    .
)
```

## WATERMARK
테이블에 데이터가 들어온 시간을 표시함

문법 - `WATERMARK FOR rowtime_column_name AS watermark_strategy_expression`
```
CREATE TABLE Orders (
    `user` BIGINT,
    product STRING,
    order_time TIMESTAMP(3),
    WATERMARK FOR order_time AS order_time - INTERVAL '5' SECOND
) WITH ( . . . );
```
`- INTERVAL '5' SECOND` : 딜레이(5초)를 제거한 타임스탬프를 찍기 위함 

## PARTITIONED BY
Partition the created table by the specified columns. A directory is created for each partition if this table is used as a filesystem sink

PARTITIONED BY 를 통해 테이블을 생성한 경우 Task를 수행할 때 PartitionCommitter 가 생성되고 PartitionCommitter가 Partition Key로 데이터를 한번 필터링 하여 스토리지에 적재함

`sink.partition-commit.policy.kind`, `sink.partition-commit.delay` 과 같은 옵션들은 PARTITIONED BY 를 통해 PartitionCommitter가 생성되어야지만 의미있음
## WITH OPTIONS
### [Formats](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/formats/overview/#formats)

### Amazon Kinesis Data Streams
[Amazon Kinesis Data Streams Connector Options](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/kinesis/#connector-options)

#### required options
- 'connector' = `'kinesis'`
- 'stream' = `'<stream-name>'`
- 'format' = `'...'`

```
CREATE TABLE <table-name> (
    .
    .
    .
)
WITH (
  'connector' = 'kinesis',
  'stream' = '<stream-name>',
  'aws.region' = '<region-name>',
  'scan.stream.initpos' = 'LATEST',
  'format' = '...'
)
```

### FileSystem(S3)
[File Formats](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/filesystem/#file-formats)

[Streaming Sink](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/filesystem/#streaming-sink)

[FileSystem SQL Connector](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/filesystem/#filesystem-sql-connector)
#### required options
- 'connector' = `'filesystem''`
- 'path' = `'s3://path/to/whatever'`
- 'format' = `'...'`
```
CREATE TABLE <table-name> (
    .
    .
    .
)
WITH (
  'connector' = 'filesystem',           
  'path' = 's3://path/to/whatever',     
  'format' = '...',                    
)
```

## About CheckPoint
- [Enabling and Configuring Checkpointing](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/fault-tolerance/checkpointing/#enabling-and-configuring-checkpointing)
- [The FileSystemCheckpointStorage](https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/checkpoints/#the-filesystemcheckpointstorage)
- [Checkpointing](https://nightlies.apache.org/flink/flink-docs-master/docs/concepts/stateful-stream-processing/#checkpointing)
- [Fixed Delay Restart Strategy](https://nightlies.apache.org/flink/flink-docs-master/docs/concepts/stateful-stream-processing/#checkpointing)

### How to Configure
```
%flink.pyflink
st_env.get_config().get_configuration().set_string(
    "restart-strategy", "fixed-delay"
)

st_env.get_config().get_configuration().set_string(
    "restart-strategy.fixed-delay.attempts", "3"
)

st_env.get_config().get_configuration().set_string(
    "restart-strategy.fixed-delay.delay", "30s"
)

st_env.get_config().get_configuration().set_string(
    "execution.checkpointing.mode", "EXACTLY_ONCE" -- "EXACTLY_ONCE" OR "AT_LEAST_ONCE"   
)

st_env.get_config().get_configuration().set_string(
    "execution.checkpointing.interval", "1min"    
)
```

## Time Series Analysis

Windowing table-valued functions(<b>Windowing TVFs</b>) return cols `window_start`, `window_end`

[Window Offset](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/sql/queries/window-tvf/#window-offset)
### TUMBLE
```
usage : TUMBLE(TABLE data, DESCRIPTOR(timecol), size [, offset ])
```
#### Example
- Window Size = 60s
```
%flink.ssql(type=update)

SELECT TICKER, COUNT(*), window_start, window_end
FROM TABLE(
    TUMBLE(TABLE stock_table, DESCRIPTOR(EVENT_TIME), INTERVAL '1' MINUTE)
)
GROUP BY TICKER, window_start, window_end

```
### HOP
```
usage : HOP(TABLE data, DESCRIPTOR(timecol), slide, size [, offset ])
```
#### Example 
- Window Size = 30s
- Sliding Time = 15s

슬라이딩 크기는 윈도우 사이즈의 절반을 넘어갈 수 없다.
```
%flink.ssql(type=update)

SELECT TICKER, COUNT(*) AS `COUNT`, window_start, window_end 
FROM TABLE(
    HOP(TABLE stock_table, DESCRIPTOR(EVENT_TIME), INTERVAL '15' SECOND, INTERVAL '30' SECOND) 
)
GROUP BY TICKER, window_start, window_end
```

## Set Server Time Zone
set table local time zone, using this command
```
%flink.ssql

SET table.local-time-zone = 'Asia/Seoul'
```

set time zone in EC2 instance, using this command
```
timedatectl
timedatectl list-timezones
sudo timedatectl set-timezone Asia/Seoul
```

set time zone by using `localtimestamp`
```
CREATE TABLE stock_table(
    `EVENT_TIME` AS LOCALTIMESTAMP + INTERVAL '9' HOUR
)
WITH(
.
.
.
)
```