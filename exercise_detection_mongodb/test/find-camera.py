import cv2

def get_connected_cameras():
    cameras = []

    index = 0
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)

        if not cap.isOpened():
            break
        
        camera_info = {
            "index": index,
            "name": cap.getBackendName(),  # Get the camera name
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }
        
        cameras.append(camera_info)
        
        cap.release()
        index += 1

    return cameras

connected_cameras = get_connected_cameras()

for camera in connected_cameras:
    print(f"Camera {camera['index']}: {camera['name']} - {camera['width']}x{camera['height']}")

cv2.destroyAllWindows()
