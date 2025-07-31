import cv2
import torch
from PIL import Image
import numpy as np

model = torch.hub.load("ultralytics/yolov5", "yolov5s")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device")
    exit()

selected_object_coords = None
prev_object_coords = None
tolerance = 100

def select_object(event, x, y, flags, param):
    global selected_object_coords, prev_object_coords
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 < x < 110 and 10 < y < 60:
            selected_object_coords = None
            prev_object_coords = None
            print("Reset to any type")
        else:
            for det in results.xyxy[0]:
                if det[0] < x < det[2] and det[1] < y < det[3]:
                    prev_object_coords = selected_object_coords
                    selected_object_coords = tuple(det[:4].cpu().numpy())
                    print(f"Selected object coordinates: {selected_object_coords}")
                    break

cv2.namedWindow("YOLOv5 Detection")
cv2.setMouseCallback("YOLOv5 Detection", select_object)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_pil = Image.fromarray(frame_rgb)

    with torch.amp.autocast('cuda'):
        results = model(frame_pil)

    results.xyxy[0] = results.xyxy[0][results.xyxy[0][:, 4] >= 0.5]
    if selected_object_coords is not None:
        for det in results.xyxy[0]:
            if (abs(det[0] - selected_object_coords[0]) <= tolerance and
                abs(det[1] - selected_object_coords[1]) <= tolerance and
                abs(det[2] - selected_object_coords[2]) <= tolerance and
                abs(det[3] - selected_object_coords[3]) <= tolerance):
                prev_object_coords = selected_object_coords
                selected_object_coords = tuple(det[:4].cpu().numpy())
                break
        results.xyxy[0] = results.xyxy[0][
            (abs(results.xyxy[0][:, 0] - selected_object_coords[0]) <= tolerance) &
            (abs(results.xyxy[0][:, 1] - selected_object_coords[1]) <= tolerance) &
            (abs(results.xyxy[0][:, 2] - selected_object_coords[2]) <= tolerance) &
            (abs(results.xyxy[0][:, 3] - selected_object_coords[3]) <= tolerance)
        ]

    results_img = np.array(results.render()[0])
    results_img = cv2.cvtColor(results_img, cv2.COLOR_RGB2BGR)

    if prev_object_coords is not None and selected_object_coords is not None:
        prev_center = (
            int((prev_object_coords[0] + prev_object_coords[2]) / 2),
            int((prev_object_coords[1] + prev_object_coords[3]) / 2)
        )
        curr_center = (
            int((selected_object_coords[0] + selected_object_coords[2]) / 2),
            int((selected_object_coords[1] + selected_object_coords[3]) / 2)
        )
        cv2.arrowedLine(results_img, prev_center, curr_center, (0, 255, 255), 4, tipLength=0.3)

    cv2.rectangle(results_img, (10, 10), (110, 60), (0, 0, 255), -1)
    cv2.putText(results_img, "Exit", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("YOLOv5 Detection", results_img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()