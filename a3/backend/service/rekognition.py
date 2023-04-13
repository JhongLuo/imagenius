import boto3
from service.s3 import S3

class Rekognition:
    def __init__(self) -> None:
        self.s3 = S3()
        self.rek = boto3.client('rekognition')

    def detect_labels(self, image):
        response = self.rek.detect_labels(
            Image={
                'Bytes': image
            },
            MaxLabels=4,
            MinConfidence=80,
        )
        labels = []
        for label in response['Labels']:
            labels.append(label['Name'])
        return labels