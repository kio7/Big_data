import numpy as np


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

    return new_img, pixels
