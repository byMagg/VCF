'''Exploiting color (perceptual) redundancy with the YCoCg transform.'''

import argparse
from skimage import io # pip install scikit-image
import numpy as np

import logging
#FORMAT = "%(module)s: %(message)s"
FORMAT = "(%(levelname)s) %(module)s: %(message)s"
#logging.basicConfig(format=FORMAT)
logging.basicConfig(format=FORMAT, level=logging.INFO)
#logging.basicConfig(format=FORMAT, level=logging.DEBUG)

import entropy
import deadzone

# pip install "image_IO @ git+https://github.com/vicente-gonzalez-ruiz/image_IO"
#from image_IO import image_3 as color_image
# pip install "color_transforms @ git+https://github.com/vicente-gonzalez-ruiz/color_transforms"
from color_transforms.YCoCg import from_RGB
from color_transforms.YCoCg import to_RGB

class YCoCg(deadzone.Deadzone_Quantizer):
    
    def __init__(self, args): # ??
        super().__init__(args)

    def encode(self):
        img = self.read()
        img_128 = img.astype(np.int16) - 128
        YCoCg_img = from_RGB(img_128)
        k, rate = self.quantize(YCoCg_img)
        rate += self.save(k)
        return rate

    def decode(self):
        k = self.read()
        YCoCg_y = self.dequantize(k)
        y_128 = to_RGB(YCoCg_y.astype(np.int16))
        y = (y_128.astype(np.int16) + 128)
        y = np.clip(y, 0, 255).astype(np.uint8)
        rate = self.save(y)
        return rate

if __name__ == "__main__":
    logging.info(__doc__)
    #logging.info(f"quantizer = {gray_pixel_static_scalar_quantization.quantizer_name}")
    entropy.parser.description = __doc__
    args = entropy.parser.parse_known_args()[0]

    try:
        logging.info(f"input = {args.input}")
        logging.info(f"output = {args.output}")
    except AttributeError:
        logging.error("You must specify 'encode' or 'decode'")
        quit()

    codec = YCoCg(args)

    rate = args.func(codec)
    logging.info(f"rate = {rate} bits/pixel")

