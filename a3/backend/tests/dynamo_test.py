from service.dynamo import Dynamo

total = 100

def test_add():
    dynamo = Dynamo()
    # dynamo.clear()
    for i in range(1, total):
        labels = []
        for j in range(1, i):
            if i % j == 0:
                labels.append(f"test label {j}")
        dynamo.put_image(image_path=str(i), labels=labels, prompt=f"this is a test image_path: {i}")

def test_label():
    dynamo = Dynamo()
    for i in range(1, total):
        images = dynamo.labels_retrive([f"test label {i}"])       
        images = set(images)
        for k in range(i + 1, total):
            if k % i == 0:
                assert f"{k}" in images
                images.remove(f"{k}")
        assert len(images) == 0

def test_prompt():
    dynamo = Dynamo()
    for i in range(1, total):
        images = dynamo.prompt_retrive(f"this is a test image_path: {i}")       
        assert f"{i}" == images[0]
        assert len(images) == 1
   
if __name__ == '__main__':
    test_prompt()

    
