# Kinesis Data Analytics (Flink) 예제 코드

## Architecture
![image](https://user-images.githubusercontent.com/77256585/159214310-a0cb41aa-4bd7-4049-ab31-1ae6b49b8b11.png)
## Document
- <a href="https://docs.aws.amazon.com/ko_kr/kinesisanalytics/latest/java/examples-s3.html">Amazon Kinesis Data Analytics Docs</a>

## Pre-requisites
- You have to create Amazon Kinesis Data Stream name as `ExampleInputStream` in `us-east-1` region
- You have to create S3 Bucket name as `ka-app-<username>` in `us-east-1` region 

## Flink Application Source Code
#### From
```
git clone https://github.com/aws-samples/amazon-kinesis-data-analytics-java-examples
```

## Modify Source Code
#### Region
```
private static final String region = "us-east-1";
```
#### S3 Sink Path
```
private static final String s3SinkPath = "s3a://ka-app-<username>/data";
```

## Compile the Application Source Code
Install maven, using this command
```
sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
sudo yum install -y apache-maven
mvn --version
```
Compile the application source code, using this command
```
mvn package -Dflink.version=1.13.2
```

## Upload JAF File to S3 Bucket
1. Create S3 Bucket with any name
2. Upload JAR File to S3 Bucket

## How to Run Kinesis Data Analytics by Using AWS Console
1. Login to AWS Console
2. Create Kinesis Data Analytics Application as follows
   
   2-1. Select Apache Flink Runtime version = `1.13`
3. Click on Configure

   3-1. S3 Bucket = Choose the bucket you uploaded jar file above
   
   3-2. Path to Amazon S3 object = `aws-kinesis-analytics-java-apps-1.0.jar`
   
   3-3. Monitoring log level = `Info`
   
   3-4. Monitoring metrics level with CloudWatch = `Application`

   3-5. Click Save Change 

   3-6. Attach roles in `kinesis-analytics-YourApplicationName-us-east-1`
      1. `AmazonS3FullAccess`
      2. `AmazonKinesisFullAccess`
      3. `CloudWatchFullAccess`
      4. `CloudWatchLogsFullAccess`
   
4. Click on Run
   
## How to Test
### Test by using boto3
   1. Create EC2 Instance and Attach `AmazonKinesisFullAccess` Role
   2. Copy [stock.py](https://github.com/Jeromy0515/cloud-skills-sample-kinesis-analytics-flink-application/blob/main/stock.py) file to EC2 instance
   3. Run stock.py using this command
      ```
      python3 stock.py 
      ```
   4. Show Apache Flink Dashboard
   5. Check S3 URI `s3://ka-app-<username>/data`

### Test by using Kinesis Agent
   1. Create EC2 instance for install Kinesis Agent
   2. Attach roles in applied role to EC2 instance
      1. `AmazonKinesisFullAccess`
      2. `CloudWatchAgentServerPolicy`
   3. Install Kinesis Agent using this command
      ```
      yum install aws-kinesis-agent -y
      ```
   4. Configure `/etc/aws-kinesis/agent.json` like this
      ```
      {
         "cloudwatch.emitMetrics": true,
         "kinesis.endpoint": "https://kinesis.us-east-1.amazonaws.com",
         "firehose.endpoint": "",
         
         "flows": [
            {
                "filePattern": "/tmp/*.log",
                "kinesisStream": "ExampleInputStream",
                "partitionKeyOption": "RANDOM"
            }
         ]
      }
      ```
   5. Run Kinesis Agent using this command
      ```
      systemctl start aws-kinesis-agent
      ```
   6. Copy [agent.py](https://github.com/Jeromy0515/cloud-skills-sample-kinesis-analytics-flink-application/blob/main/agent.py) file to EC2 instance 
   7. Run `agent.py` using this command
      ```
      python3 agent.py
      ```
   8.  Check Kinesis Agent's logs using this command
       ```
       tail -f /var/log/aws-kinesis-agent/aws-kinesis-agent.log
       ```
   9. Show Apache Flink Dashboard
   10. Check S3 URI `s3://ka-app-<username>/data`