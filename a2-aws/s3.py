import boto3
import os

class s3:
    def __init__(self,client):
        self.s3 = client
        self.bucketName = "a2-bucket"    
        
        

    def createBucket(self):
        exist = self.s3.checkBucketExists()
        if exist == True:
            self.deleteBucket()
        else:
            self.s3.create_bucket(Bucket = "a2-bucket")
        
        
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


    def downloadFile(self, bucket_name, object_name, local_dir):
        # List all the objects in the S3 bucket
        response = self.s3.list_objects_v2(Bucket=bucket_name)
        object_list = response['Contents']

        # Check if the specified object name is present in the bucket
        if not any(obj['Key'] == object_name for obj in object_list):
            print(f"Error: File '{object_name}' not found in '{bucket_name}' bucket.")
            return

        # Extract the file name and extension from the object key
        object_name_parts = object_name.split('.')
        file_name = object_name_parts[0]
        file_ext = object_name_parts[1]

        # Construct the file path on the local machine
        file_path = os.path.join(local_dir, f"{file_name}.{file_ext}")

        try:
            self.s3.download_file(bucket_name, object_name, file_path)
            print(f"File '{object_name}' downloaded successfully to '{file_path}' on local machine.")
        except Exception as e:
            print(f"Error downloading file '{object_name}' from '{bucket_name}' bucket: {e}")

    def deleteFile(self, object_name):
        # List all the objects in the S3 bucket
        response = self.s3.list_objects_v2(Bucket=self.bucketName)
        object_list = response['Contents']

        # Check if the specified object name is present in the bucket
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
            
            # Print a success message when all objects have been deleted
            print(f"All files deleted successfully from '{self.bucketName}' bucket.")
        except Exception as e:
            print(f"Error deleting files from '{self.bucketName}' bucket: {e}")

    def deleteBucket(self):
        try:
            self.s3.delete_bucket(Bucket=self.bucketName)
            print(f"Bucket '{self.bucketName}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting bucket '{self.bucketName}': {e}")