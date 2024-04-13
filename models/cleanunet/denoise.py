# Adapted from https://github.com/NVIDIA/waveglow under the BSD 3-Clause License.

# *****************************************************************************
#  Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of the NVIDIA CORPORATION nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL NVIDIA CORPORATION BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# *****************************************************************************


import numpy as np
import torch
import torch.nn as nn

# from torch.utils.tensorboard import SummaryWriter

import random

random.seed(0)
torch.manual_seed(0)
np.random.seed(0)

from .util import rescale, find_max_epoch, print_size, sampling
from .network import CleanUNet
import torchaudio

def get_config():
    return {
        "channels_input": 1,
        "channels_output": 1,
        "channels_H": 64,
        "max_H": 768,
        "encoder_n_layers": 8,
        "kernel_size": 4,
        "stride": 2,
        "tsfm_n_layers": 5,
        "tsfm_n_head": 8,
        "tsfm_d_model": 512,
        "tsfm_d_inner": 2048,
    }


def load_model(
    ckpt_path,
    config=get_config()
):
    # predefine model
    net = CleanUNet(**config).cuda()
    print_size(net)

    # load checkpoint
    checkpoint = torch.load(ckpt_path, map_location="cpu")
    net.load_state_dict(checkpoint["model_state_dict"])
    net.eval()
    return net


def denoise(net, waveform: torch.Tensor, sample_rate, batch_size=100_000) -> torch.Tensor:
    multi_channel = waveform.shape[0]!=1
    if multi_channel:
        # Get mean of all channel
        waveform = torch.mean(waveform, dim=0).unsqueeze(0) 
    noisy_audio = waveform.cuda()
    
    LENGTH = len(noisy_audio[0].squeeze())
    
    noisy_audio = torch.chunk(noisy_audio, LENGTH // batch_size + 1, dim=1)
    all_audio = []

    for batch in noisy_audio:
        with torch.no_grad():
            with torch.cuda.amp.autocast():
                generated_audio = net(batch)
                generated_audio = generated_audio.cpu().numpy().squeeze()
                all_audio.append(generated_audio)

    all_audio = np.concatenate(all_audio, axis=0)
    denoised_waveform = torch.from_numpy(all_audio).unsqueeze(0)
    return denoised_waveform
