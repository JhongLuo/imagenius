import boto3

class Dynamo:
    def __init__(self) -> None:
        self.dy = boto3.client('dynamodb')
        self.image_table_name = 'ECE1779A3ImageInfo'
        self.provisioned_throughput = {
            'ReadCapacityUnits': 3,
            'WriteCapacityUnits': 3,
        }
        if not self.table_exists(self.image_table_name):
            self.create_image_table()
    
    def table_exists(self, table_name):
        try:
            response = self.dy.describe_table(TableName=table_name)
            return True if response['Table']['TableStatus'] in ['ACTIVE', 'UPDATING'] else False
        except self.dy.exceptions.ResourceNotFoundException:
            return False

    def clear(self):
        self.dy.delete_table(TableName=self.image_table_name)
        waiter = self.dy.get_waiter('table_not_exists')
        waiter.wait(TableName=self.image_table_name)
        self.create_image_table()
        print(f"Table '{self.image_table_name}' cleared.")

    def create_image_table(self):
        primary_key = {
            'AttributeName': 'label',
            'KeyType': 'HASH'
        }
        sort_key = {
            'AttributeName': 'image_path',
            'KeyType': 'RANGE'
        }
        gsi_partition_key = {
            'AttributeName': 'description',
            'KeyType': 'HASH'
        }
        gsi_sort_key = {
            'AttributeName': 'image_path',
            'KeyType': 'RANGE'
        }
        attribute_definitions = [
            {'AttributeName': 'image_path', 'AttributeType': 'S'},
            {'AttributeName': 'description', 'AttributeType': 'S'},
            {'AttributeName': 'label', 'AttributeType': 'S'},
        ]
        gsi = {
            'IndexName': 'DesIndex',
            'KeySchema': [gsi_partition_key, gsi_sort_key],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': self.provisioned_throughput
        }
        response = self.dy.create_table(
            TableName=self.image_table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=[primary_key, sort_key],
            ProvisionedThroughput=self.provisioned_throughput,
            GlobalSecondaryIndexes=[gsi]
        )
        self.dy = boto3.client('dynamodb')

    # retrieve all images with the same label
    def label_retrive(self, label):
        response = self.dy.query(
            TableName=self.image_table_name,
            KeyConditionExpression='label = :label',
            ExpressionAttributeValues={
                ":label": {'S': label}
            },
        )
        images = set()
        for item in response['Items']:
            images.add(item['image_path']['S'])
        images = list(images)
        images.sort()
        return images
    
    def description_retrive(self, description):
        response = self.dy.query(
            TableName=self.image_table_name,
            IndexName='DesIndex',
            KeyConditionExpression='description = :description',
            ExpressionAttributeValues={
                ":description": {'S': description}
            },
        )
        images = set()
        for item in response['Items']:
            images.add(item['image_path']['S'])
        images = list(images)
        images.sort()
        return images
    
    def put_image(self, image_path, labels, description):
        labels.append('all')
        item_list = []
        for label in labels:
            item = {
                'PutRequest': {
                    'Item': {
                        'label': {'S': label},
                        'image_path': {'S': image_path},
                        'description': {'S': description},
                    }
                }
            }
            item_list.append(item)

        request_items = {}
        request_items[self.image_table_name] = item_list
        print(item_list)
        response = self.dy.batch_write_item(RequestItems=request_items)
        if 'UnprocessedItems' in response and response['UnprocessedItems']:
            print("Some items were not processed:")
            print(response['UnprocessedItems'])
        else:
            print(f"Successfully inserted image_path {image_path} with labels {', '.join(labels)} for description {description}")

            

        