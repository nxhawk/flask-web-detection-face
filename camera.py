import threading
from utils import base64_to_pil_image, pil_image_to_base64
from time import sleep
from detection_face import Detection


class Camera(object):
    def __init__(self) -> None:
        self.to_process = []
        self.to_output = []

        thread = threading.Thread(target=self.keep_processing)
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            return

        # get image in top(to_process) to process
        input_str = self.to_process.pop(0)

        # convert to pil image
        input_img = base64_to_pil_image(input_str)

        # -----------------Processing--------------------
        # add your code here
        input_img = Detection(input_img)
        # -----------------------------------------------

        # output_img after process
        output_img = input_img

        # convert to base64 in ascii character
        output_str = pil_image_to_base64(output_img)

        # convert to base64 in ascii bytes
        self.to_output.append(output_str)

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.005)

    def add_img_to_process(self, input):
        if len(self.to_process) > 30:
            self.to_process.clear()
        self.to_process.append(input)

    def get_frame(self):
        # #  return alway have frame
        # while not self.to_output:
        #     sleep(0.05)
        if not self.to_output:
            return None
        return self.to_output.pop(0)
