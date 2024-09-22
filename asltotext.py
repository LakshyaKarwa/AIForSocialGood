import cv2 as cv
import numpy as np


def draw_rectangle_frame(image, first_coordinate, second_coordinate, color):
    image = cv.rectangle(image, first_coordinate, second_coordinate, color, 2)
    return image


def compute_rectangle_coordinates(x_center, y_center, frame_height, frame_width):
    first_coordinate = (int(x_center - frame_width / 2), int(y_center - frame_height / 2))
    second_coordinate = (int(x_center + frame_width / 2), int(y_center + frame_height / 2))
    
    return first_coordinate, second_coordinate

def map_categorical_to_label(categorical_results):
    categorical_results = np.argmax(categorical_results, axis=-1)
    position = categorical_results[0]
    keys_list = list(labels_dict.keys())
    return keys_list[position]

vid = cv.VideoCapture(0)

x_center = vid.get(3) / 2
y_center = vid.get(4) / 2

frame_height = 200
frame_width = 200

first_coordinate, second_coordinate = compute_rectangle_coordinates(x_center, y_center, frame_height, frame_width)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    cropped_frame = frame[first_coordinate[1]: first_coordinate[1]+frame_height, first_coordinate[0]: first_coordinate[0]+frame_width]
    cropped_frame = cv.cvtColor(cropped_frame, cv.COLOR_BGR2GRAY)
    processed_cropped_frame = np.reshape(cropped_frame, (1, cropped_frame.shape[0], cropped_frame.shape[1], 1))

    frame = draw_rectangle_frame(frame, first_coordinate, second_coordinate, (252, 19, 3))

    results = cnn_asl_model.predict(processed_cropped_frame)
    label = map_categorical_to_label(results)
    
    frame = cv.putText(frame, 'The predicted value is: ' + label, (int(0), int(y_center*2)), cv.FONT_HERSHEY_SIMPLEX, int(1), (int(255),int(255),int(255)), 2)
    # Display the resulting frame
    cv.imshow('frame', cropped_frame)
    cv.imshow('frame2', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()