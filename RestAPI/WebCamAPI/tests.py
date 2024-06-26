from django.test import TestCase
import socket, cv2
import numpy as np

HOST = "127.0.0.1"
PORT = 8080


# Create your tests here.
def test_local_camera_stream():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'connect')
        while True:
            size_m = s.recv(1024)
            size = int(size_m.split()[-1])
            s.sendall(b'received frame size')
            frame = b""
            while len(frame) < size:
                frame += s.recv(size)
            image = cv2.imdecode(np.asarray(bytearray(frame)), -1)
            image = cv2.resize(image, (5000, 5000))
            cv2.imshow("image", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                s.sendall(b"close")
                break
            s.sendall(b'received frame')
        cv2.destroyAllWindows()


def test_2():
    # Refactored from:
    # https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Raspberry_Pi_Guide.md
    import tensorflow as tf
    import cv2
    import numpy as np

    min_conf_threshold = 0.5

    # Load the label map
    with open("/Users/sebash/CLionProjects/Camera/resources/detectlabelmap.txt", 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    if labels[0] == '???':
        del (labels[0])

    interpreter = tf.lite.Interpreter(model_path="/Users/sebash/CLionProjects/Camera/resources/detect.tflite")

    interpreter.allocate_tensors()

    # get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Check output layer name to determine if this model was created with TF2 or TF1,
    # because outputs are ordered differently for TF2 and TF1 models
    outname = output_details[0]['name']

    if ('StatefulPartitionedCall' in outname):  # This is a TF2 model
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
        print("is tflite2")
    else:  # This is a TF1 model
        boxes_idx, classes_idx, scores_idx = 0, 1, 2
        print("is not")

    # Open video file
    video = cv2.VideoCapture(0)
    imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while (video.isOpened()):

        # Acquire frame and resize to expected shape [1xHxWx3]
        ret, frame = video.read()
        if not ret:
            print('Reached the end of the video!')
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[
            0]  # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]  # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]  # Confidence of detected objects

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                print(scores[i])
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1, (boxes[i][0] * imH)))
                xmin = int(max(1, (boxes[i][1] * imW)))
                ymax = int(min(imH, (boxes[i][2] * imH)))
                xmax = int(min(imW, (boxes[i][3] * imW)))

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 4)

                # Draw label
                object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'

                # entry point to check lables
                #if "person" in label.lower():
                    #print("found person")
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                cv2.rectangle(
                    frame,
                    (xmin, label_ymin - labelSize[1] - 10),
                    (xmin + labelSize[0], label_ymin + baseLine - 10),
                    (255, 255, 255),
                    cv2.FILLED)  # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                            2)  # Draw label text

        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    test_local_camera_stream()
    #test_2()
