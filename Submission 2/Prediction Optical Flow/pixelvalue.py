# import matplotlib.pyplot as plt
import numpy as np
import cv2
from pydicom import dcmread


def dicom_to_numpy(ds):
    dcm_img = ds
    rows = dcm_img.get(0x00280010).value  # Get number of rows from tag (0028, 0010)
    cols = dcm_img.get(0x00280011).value  # Get number of cols from tag (0028, 0011)

    instance_number = int(dcm_img.get(0x00200013).value)  # Get actual slice instance number from tag (0020, 0013)

    window_center = int(dcm_img.get(0x00281050).value[0])  # Get window center from tag (0028, 1050)

    window_width = int(dcm_img.get(0x00281051).value[0])  # Get window width from tag (0028, 1051)

    window_max = int(window_center + window_width / 2)
    window_min = int(window_center - window_width / 2)

    if dcm_img.get(0x00281052) is None:
        rescale_intercept = 0
    else:
        rescale_intercept = int(dcm_img.get(0x00281052).value)

    if dcm_img.get(0x00281053) is None:
        rescale_slope = 1
    else:
        rescale_slope = int(dcm_img.get(0x00281053).value)

    new_img = np.zeros((rows, cols), np.uint8)
    pixels = dcm_img.pixel_array

    for i in range(0, rows):
        for j in range(0, cols):
            pix_val = pixels[i][j]
            rescale_pix_val = pix_val * rescale_slope + rescale_intercept

            if rescale_pix_val > window_max:  # if intensity is greater than max window
                new_img[i][j] = 255
            elif rescale_pix_val < window_min:  # if intensity is less than min window
                new_img[i][j] = 0
            else:
                new_img[i][j] = int(
                    ((rescale_pix_val - window_min) / (window_max - window_min)) * 255)  # Normalize the intensities

    return new_img


if __name__ == "__main__":
    data_set = dcmread("./images/0266.dcm")
    #img_array = data_set.pixel_array * 24
    image = dicom_to_numpy(data_set)
    if data_set is None:
        print("Error: Couldn't read the image.")
    else:
        cv2.imshow('sample image dicom', image)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Press 'Esc' to exit
                break

        cv2.destroyAllWindows()
