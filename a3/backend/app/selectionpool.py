import uuid
import time
from service import s3, opensearch, rekognition, dynamo, utils
class SelectionPool:
    def __init__(self) -> None:
        self.pool = dict()
        self.cache_s3 = s3.S3("ece1779t18a3cache")
        self.s3 = s3.S3()
        self.search_engine = opensearch.OSearch()
        self.rekognition = rekognition.Rekognition()
        self.dynamo = dynamo.Dynamo()
        
    def add(self, prompt, raw_image, father = None):
        key = uuid.uuid4()
        image_path = self.cache_s3.store_image(raw_image)
        self.pool[key] = {
            'father': father,
            'prompt': prompt,
            'raw_image': raw_image,
            'timestamp': time.time(),
            'image_path': image_path,
        }
        return key
    
    def choose(self, key):
        if key not in self.pool:
            raise Exception("Key not found in pool or expired.")
        
        prompt = self.pool[key]['prompt']
        raw_image = self.pool[key]['raw_image']
        cache_path = self.pool[key]['image_path']
        tags = self.rekognition.detect_labels(raw_image)
        image_path = s3.store_image(utils.url2image(self.cache_s3.path2url(cache_path)))
        dynamo.put_image(image_path, tags, prompt)
        self.search_engine.add_prompt(prompt)        
        return True
    
    def clean_expired(self):
        keys_for_delete = []
        for key in self.pool:
            timestamp = self.pool[key]['timestamp']
            # if user don't save the image in 10 minutes, images will lost
            if time.time() - timestamp > 600:
                image_path = self.pool[key]['image_path']
                self.cache_s3.delete_image(image_path)
            keys_for_delete.append(key)
        
        for key in keys_for_delete:
            del self.pool[key]
