import boto3
import datetime
from utils.rds import StatsNames
class Watcher:
    def __init__(self) -> None:
        self.client = boto3.client('cloudwatch', region_name='us-east-1')
        self.namespace = 'a2'
    
    def put_metric(self, name : StatsNames, value):
        self.client.put_metric_data(
            Namespace=self.namespace,
            MetricData=[{
                "MetricName": name.value,
                "Timestamp": datetime.datetime.utcnow(),
                "Value": value,
                "Unit": "Count"
            }]
        )
        
    def get_metric(self, name : StatsNames, start_time, end_time):
        response = self.client.get_metric_statistics(
            Namespace=self.namespace,
            MetricName=name.value,
            StartTime=start_time,
            EndTime=end_time,
            Period=60,
            Statistics=["Sum"]
        )
        if (len(response['Datapoints']) == 0):
            return 0
        return int(response['Datapoints'][0]['Sum'])
    
    def get_missed_rate(self):
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=1)
        read = self.get_metric(StatsNames.read_requests, start, end)
        missed = self.get_metric(StatsNames.missed_requests, start, end)
        if read == 0:
            return 0
        return min(read, missed) / read
    
    def get_hit_rate(self):
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=1)
        read = self.get_metric(StatsNames.read_requests, start, end)
        missed = self.get_metric(StatsNames.missed_requests, start, end)
        if read == 0:
            return 0
        return max(read - missed, 0) / read
    
    def get_request_count(self):
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=1)
        return self.get_metric(StatsNames.total_requests, start, end)
        