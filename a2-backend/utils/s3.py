import boto3

class S3:
    def __init__(self):
        self.client = boto3.client('s3')
        self.bucketName = "ece1779t18a2"
        self.s3_resource = boto3.resource('s3')   
        
        self.file_counter = 0
        self.createBucket()
        
    def createBucket(self):
        if self.checkBucketExists():
            self.deleteAllFiles()
        else:
            self.client.create_bucket(Bucket = self.bucketName)
        
    def checkBucketExists(self):
        buckets = self.client.list_buckets()
        for item in buckets['Buckets']:
            if item['Name'] == self.bucketName:
                return True
        return False
    
    def deleteAllFiles(self):
        try:
            response = self.client.list_objects_v2(Bucket=self.bucketName)
            objects = response.get('Contents', [])
            for obj in objects:
                self.client.delete_object(Bucket=self.bucketName, Key=obj['Key'])
            self.file_counter = 0
        except Exception as e:
            print(f"Error deleting files from '{self.bucketName}' bucket: {e}")

    def deleteBucket(self):
        try:
            self.client.delete_bucket(Bucket=self.bucketName)
            print(f"Bucket '{self.bucketName}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting bucket '{self.bucketName}': {e}")

    # s3 api for manager

    def clear_images(self):
        self.deleteAllFiles()

    # generate a new filename for the image
    def get_new_filename(self):
        new_filename = str(self.file_counter)
        self.file_counter += 1
        return new_filename
            
    def store_image(self, file):
        new_filename = self.get_new_filename()
        self.client.put_object(Bucket=self.bucketName, Key=new_filename, Body=file.encode('utf-8'))
        return new_filename

    def read_image(self, filename):
        return self.client.get_object(Bucket=self.bucketName, Key=filename)['Body'].read().decode('utf-8')
        
    def delete_image(self, filename):
        self.client.delete_object(Bucket=self.bucketName, Key=filename)