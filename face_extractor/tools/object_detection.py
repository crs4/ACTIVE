import cv2
import os

def background_subtraction_on_images(
        frame_seq, save_path=None, show_results=False):
    """
    Detect moving objects in a sequence of images by background subtraction

    :type frame_seq: list
    :param frame_seq: list of paths of frame sequence

    :type save_path: string
    :param save_path: path where images with detected objects will be saved.
                      If not provided, images will not be saved

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         images with detected moving objects

    :rtype image_masks: list
    :returns: list of masks with detected moving objects
    """

    image_masks = []
    fgmask = None
    pMOG2 = cv2.BackgroundSubtractorMOG2()
    for frame_path in frame_seq:

        # Read image
        frame = cv2.imread(frame_path)

        fgmask = pMOG2.apply(frame)

        image_masks.append(fgmask)

        # Extract frame name
        name = os.path.basename(frame_path)

        if save_path:
            # Save image
            save_im_path = os.path.join(save_path, name)
            cv2.imwrite(save_im_path, fgmask)

        if show_results:

            # Mask original frame
            mask_rgb = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
            masked_frame = frame & mask_rgb

            # Write frame name on image
            cv2.putText(masked_frame, name, (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Show frame
            cv2.imshow('frame', masked_frame)
            cv2.waitKey(0)

    return image_masks
