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
        image_path = self.cache_s3.store_image(raw_image)
        self.pool[image_path] = {
            'father': father,
            'prompt': prompt,
            'raw_image': raw_image,
            'timestamp': time.time(),
        }
        return image_path
    
    def choose(self, cache_path):
        if cache_path not in self.pool:
            raise Exception("Key not found in pool or expired.")
        cached = self.pool[cache_path]
        father_path = cached['father']
        prompt = cached['prompt']
        raw_image = cached['raw_image']
        tags = self.rekognition.detect_labels(raw_image)
        image_path = self.s3.store_image(utils.url2image(self.cache_s3.path2url(cache_path)))
        self.dynamo.put_image(image_path, tags, prompt, father_path)
        self.search_engine.add_prompt(prompt)        
        return True
    
    def clean_expired(self, force=False):
        keys_for_delete = []
        for key in self.pool:
            timestamp = self.pool[key]['timestamp']
            # if user don't save the image in 10 minutes, images will lost
            if force or time.time() - timestamp > 600:
                self.cache_s3.delete_image(key)
                keys_for_delete.append(key)
        
        for key in keys_for_delete:
            del self.pool[key]
