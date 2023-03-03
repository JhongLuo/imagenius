import boto3
import os

class s3:
    def __init__(self,client):
        self.s3 = client
        self.bucketName = "a2-bucket1779"
        self.s3_resource = boto3.resource('s3')   
        
        

    def createBucket(self):
        exist = self.checkBucketExists()
        if exist == True:
            self.deleteAllFiles()
            self.deleteBucket()
     
        self.s3.create_bucket(Bucket = self.bucketName)
        
        
    def checkBucketExists(self):
        buckets = self.s3.list_buckets()
        for item in buckets['Buckets']:
            if item['Name'] == self.bucketName:
                return True
        return False
    
    def uploadFile(self, file_path):
        object_name = os.path.basename(file_path) #get the last part of the path    
        
        with open(file_path, 'rb') as f:
            file_contents = f.read()
    
        try:
            self.s3.put_object(Bucket=self.bucketName, Key=object_name, Body=file_contents)
            print(f"File '{object_name}' uploaded successfully to '{self.bucketName}' bucket.")
        except Exception as e:
            print(f"Error uploading file '{object_name}' to '{self.bucketName}' bucket: {e}")


    def downloadFile(self, object_name, local_dir, local_file_name=None):
        try:
            bucket = self.s3_resource.Bucket(self.bucketName)
            for obj in bucket.objects.all():
                if obj.key == object_name:
                    if local_file_name is None:
                        local_file_name = object_name
                    file_path = os.path.join(local_dir, local_file_name)
                    bucket.download_file(object_name, file_path)
                    print(f"File '{object_name}' downloaded successfully to '{file_path}'.")
                    return
            print(f"Error: File '{object_name}' not found in '{self.bucketName}' bucket.")
        except Exception as e:
            print(f"Error downloading file '{object_name}' from '{self.bucketName}' bucket: {e}")

    def deleteFile(self, object_name):
        response = self.s3.list_objects_v2(Bucket=self.bucketName)
        object_list = response['Contents']

        if not any(obj['Key'] == object_name for obj in object_list):
            print(f"Error: File '{object_name}' not found in '{self.bucketName}' bucket.")
            return

        try:
            self.s3.delete_object(Bucket=self.bucketName, Key=object_name)
            print(f"File '{object_name}' deleted successfully from '{self.bucketName}' bucket.")
        except Exception as e:
            print(f"Error deleting file '{object_name}' from '{self.bucketName}' bucket: {e}") 
    
    def deleteAllFiles(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucketName)
            objects = response.get('Contents', [])

            
            for obj in objects:
                self.s3.delete_object(Bucket=self.bucketName, Key=obj['Key'])
            
            print(f"All files deleted successfully from '{self.bucketName}' bucket.")
        except Exception as e:
            print(f"Error deleting files from '{self.bucketName}' bucket: {e}")

    def deleteBucket(self):
        try:
            self.s3.delete_bucket(Bucket=self.bucketName)
            print(f"Bucket '{self.bucketName}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting bucket '{self.bucketName}': {e}")