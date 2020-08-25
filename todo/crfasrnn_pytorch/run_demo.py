"""
MIT License

Copyright (c) 2019 Sadeep Jayasumana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pathlib
import sys

import torch

from todo.crfasrnn_pytorch.crfasrnn import util
from todo.crfasrnn_pytorch.crfasrnn.crfasrnn_model import CrfRnnNet

WEIGHTS_PATH = str(pathlib.Path(__file__).parent.parent.absolute()) 
print("Weights path: " + WEIGHTS_PATH + "/crfasrnn_pytorch/crfasrnn_weights.pth")

def get_labels(input_file):
    # Read the image
    img_data, img_h, img_w, size = util.get_preprocessed_image(input_file)

    model = CrfRnnNet()
    model.load_state_dict(torch.load(WEIGHTS_PATH + "/crfasrnn_pytorch/crfasrnn_weights.pth"))
    model.eval()
    out = model.forward(torch.from_numpy(img_data))

    probs = out.detach().numpy()[0]
    label_im = util.get_label_image(probs, img_h, img_w, size)
    label_im.save(WEIGHTS_PATH + 'labels.png')