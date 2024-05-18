from ultralytics import YOLO

model = YOLO("yolov8x.yaml").load('yolov8x.pt')
results = model.train(data='data.yaml', patience=20, epochs=250, workers=512, imgsz=640, name="dojo_test", device=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], pretrained=True, batch=260)
