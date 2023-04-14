import boto3
from service.utils import image2fileobj

class S3:
    def __init__(self, bucketName = "ece1779t18a3"):
        self.client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')   
        self.bucketName = bucketName
        self.createBucket()
        self.file_counter = self.get_largest_filename() + 1
    
    def get_largest_filename(self):
        all = self.s3_resource.Bucket(self.bucketName).objects.all()
        largest = -1
        for obj in all:
            if int(obj.key) > largest:
                largest = int(obj.key)
        return largest
    
    def createBucket(self):
        if self.checkBucketExists():
            pass
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

    def clear_images(self):
        self.deleteAllFiles()

    # generate a new filename for the image
    def get_new_filename(self):
        new_filename = str(self.file_counter)
        self.file_counter += 1
        return new_filename
            
    def store_image(self, raw_image):
        new_filename = self.get_new_filename()
        self.client.upload_fileobj(image2fileobj(raw_image), Bucket=self.bucketName, Key=new_filename, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'})
        return new_filename
    
    def path2url(self, path):
        return "https://s3.amazonaws.com/" + self.bucketName + "/" + path
    
    def delete_image(self, filename):
        self.client.delete_object(Bucket=self.bucketName, Key=filename)