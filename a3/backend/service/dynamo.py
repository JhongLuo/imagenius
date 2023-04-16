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
            self.dy.get_waiter('table_exists').wait(TableName=self.image_table_name)
    
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
            'AttributeName': 'tag',
            'KeyType': 'HASH'
        }
        sort_key = {
            'AttributeName': 'image_path',
            'KeyType': 'RANGE'
        }
        attribute_definitions = [
            {'AttributeName': 'image_path', 'AttributeType': 'S'},
            {'AttributeName': 'prompt', 'AttributeType': 'S'},
            {'AttributeName': 'tag', 'AttributeType': 'S'},
            {'AttributeName': 'root', 'AttributeType': 'S'},
            {'AttributeName': 'father', 'AttributeType': 'S'},
        ]
        
        prompt_gsi = {
            'IndexName': 'prompt_index',
            'KeySchema': [
                {
                'AttributeName': 'prompt',
                'KeyType': 'HASH'
                }, 
                {
                'AttributeName': 'image_path',
                'KeyType': 'RANGE'
                }
            ],
            'Projection': {
                'ProjectionType': 'KEYS_ONLY'
            },
            'ProvisionedThroughput': self.provisioned_throughput
        }
        
        root_gsi = {
            'IndexName': 'root_index',
            'KeySchema': [
                {
                'AttributeName': 'root',
                'KeyType': 'HASH'
                }, 
                {
                'AttributeName': 'image_path',
                'KeyType': 'RANGE'
                }
            ],
            'Projection': {
                'ProjectionType': 'KEYS_ONLY'
            },
            'ProvisionedThroughput': self.provisioned_throughput
        }
        
        father_gsi = {
            'IndexName': 'father_index',
            'KeySchema': [
                {
                'AttributeName': 'father',
                'KeyType': 'HASH'
                }, 
                {
                'AttributeName': 'image_path',
                'KeyType': 'RANGE'
                }
            ],
            'Projection': {
                'ProjectionType': 'KEYS_ONLY'
            },
            'ProvisionedThroughput': self.provisioned_throughput
        }
        
        self.dy.create_table(
            TableName=self.image_table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=[primary_key, sort_key],
            ProvisionedThroughput=self.provisioned_throughput,
            GlobalSecondaryIndexes=[prompt_gsi, root_gsi, father_gsi]
        )
        self.dy = boto3.client('dynamodb')

    # retrieve all images with the same tag
    def tags_retrive(self, tags):
        images = set()
        is_first = True
        for tag in tags:
            images_per_tag = set()
            response = self.dy.query(
                TableName=self.image_table_name,
                KeyConditionExpression='tag = :tag',
                ExpressionAttributeValues={
                    ":tag": {'S': tag}
                },
            )
            
            for item in response['Items']:
                images_per_tag.add(item['image_path']['S'])
            if is_first:
                images = images_per_tag
                is_first = False
            else:
                images.intersection_update(images_per_tag)
        images = list(images)
        images.sort()
        return images
    
    def prompt_retrive(self, prompt):
        response = self.dy.query(
            TableName=self.image_table_name,
            IndexName='prompt_index',
            KeyConditionExpression='prompt = :prompt',
            ExpressionAttributeValues={
                ":prompt": {'S': prompt}
            },
        )
        images = set()
        for item in response['Items']:
            images.add(item['image_path']['S'])
        images = list(images)
        images.sort()
        return images
    
    def root_retrive(self, root):
        response = self.dy.query(
            TableName=self.image_table_name,
            IndexName='root_index',
            KeyConditionExpression='root = :root',
            ExpressionAttributeValues={
                ':root': {'S': root}
            },
        )
        images = set()
        for item in response['Items']:
            images.add(item['image_path']['S'])
        images = list(images)
        return images
        
    def get_image_root(self, image_path):
        response = self.dy.get_item(
            TableName=self.image_table_name,
            Key={
                'tag': {'S': 'All'},
                'image_path': {'S': image_path}
            },
            ProjectionExpression='root'
        )
        return response['Item']['root']['S']

    def get_image_descendants(self, image_path):
        response = self.dy.query(
            TableName=self.image_table_name,
            IndexName = 'father_index',
            KeyConditionExpression='father = :father',
            ExpressionAttributeValues={
                ':father': {'S': image_path}
            },
        )
        images = set()
        for item in response['Items']:
            images.add(item['image_path']['S'])
        images = list(images)
        images.sort()
        return images

    def get_image_prompt(self, image_path):
        response = self.dy.get_item(
            TableName=self.image_table_name,
            Key={
                'tag': {'S': 'All'},
                'image_path': {'S': image_path}
            },
            ProjectionExpression='prompt'
        )
        return response['Item']['prompt']['S']
    
    def put_image(self, image_path, tags, prompt, father_image_path=None):
        if father_image_path is None:
            root = image_path
            father = 'None'
        else:
            root = self.get_image_root(father_image_path)
            father = father_image_path
        
        tags.append('All')
        item_list = []
        for tag in tags:
            item = {
                'PutRequest': {
                    'Item': {
                        'tag': {'S': tag},
                        'image_path': {'S': image_path},
                        'prompt': {'S': prompt},
                        'root': {'S': root},
                        'father': {'S': father},
                    }
                }
            }
            item_list.append(item)

        request_items = {}
        request_items[self.image_table_name] = item_list
        response = self.dy.batch_write_item(RequestItems=request_items)
        if 'UnprocessedItems' in response and response['UnprocessedItems']:
            print("Some items were not processed:")
            print(response['UnprocessedItems'])
        else:
            print(f"Successfully inserted image_path {image_path} with tags {', '.join(tags)} for prompt {prompt}")

    def list_images(self):
        response = self.dy.scan(
            TableName=self.image_table_name,
            ProjectionExpression='image_path',
        )
        images = set()
        for item in response['Items']:
            images.add(item['image_path']['S'])
        images = list(images)
        images.sort()
        return images
    
    def list_tags(self):
        response = self.dy.scan(
            TableName=self.image_table_name,
            ProjectionExpression='tag',
        )
        tags = set()
        for item in response['Items']:
            tags.add(item['tag']['S'])
        tags = list(tags)
        tags.sort()
        return tags
    
    def list_prompts(self):
        response = self.dy.scan(
            TableName=self.image_table_name,
            ProjectionExpression='prompt',
        )
        prompts = set()
        for item in response['Items']:
            prompts.add(item['prompt']['S'])
        prompts = list(prompts)
        prompts.sort()
        return prompts

    def get_image_tags(self, image_path):
        response = self.dy.scan(
            TableName=self.image_table_name,
            FilterExpression='image_path = :image_path',
            ExpressionAttributeValues={
                ':image_path': {'S': image_path}
            }
        )
        tags = set()
        for item in response['Items']:
            tags.add(item['tag']['S'])
        return list(tags)

        
    def delete_image(self, image_path):        
        descendants = self.get_image_descendants(image_path)
        print('descendants', type(image_path))
        print(descendants, image_path)
        for descendant in descendants:
            self.delete_image(descendant)
        tags = self.get_image_tags(image_path)
        print('tags')
        print(tags)
        for tag in self.get_image_tags(image_path):
            self.dy.delete_item(
                TableName=self.image_table_name,
                Key={
                    'tag': {'S': tag},
                    'image_path': {'S': image_path}
                },
            )
    
            