# This file contains a wrapper for FastSam that implements the interface specified in SamModel.py
# FastSAM: Zhao, Xu, et al. "Fast Segment Anything." arXiv preprint arXiv:2306.12156 (2023).

from SamModel import SamModel
from FastSAM.fastsam import *
from segment_anything import *
from ultralytics import SAM

class SamWrapper(SamModel):
    def __init__(self, pathToCheckpoint, device, conf, iou):
        self.SamModel = SAM(pathToCheckpoint)
        self.device = device
        self.conf = conf
        self.iou = iou
    
    def segmentFrame(self, image):
        everything_results = self.SamModel(image, device=self.device, retina_masks=True, imgsz=1024, conf=self.conf, iou=self.iou,)
        prompt_process = FastSAMPrompt(image, everything_results, device=self.device)
        segmask = prompt_process.everything_prompt()

        if (len(segmask) > 0):
            segmask = segmask.cpu().numpy()
        else:
            segmask = None

        return segmask