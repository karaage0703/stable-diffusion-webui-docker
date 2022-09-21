# syntax=docker/dockerfile:1
FROM continuumio/miniconda3:4.12.0

SHELL ["/bin/bash", "-ceuxo", "pipefail"]

ENV DEBIAN_FRONTEND=noninteractive

RUN conda install python=3.8.5 && conda clean -a -y
RUN conda install pytorch==1.11.0 torchvision==0.12.0 cudatoolkit=11.3 -c pytorch && conda clean -a -y
RUN pip install diffusers==0.3.0 transformers scipy ftfy
# RUN apt-get update && apt install fonts-dejavu-core rsync -y && apt-get clean
RUN pip install -qq omegaconf einops pytorch-lightning transformers kornia invisible-watermark opencv-python==4.1.2.30
RUN 


RUN <<EOF
git clone https://github.com/CompVis/stable-diffusion
cd stable-diffusion
git reset --hard 69ae4b35e0a0f6ee1af8bb9a5d0016ccb27e36dc
pip install -e .
pip install -e git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers
pip install -e git+https://github.com/openai/CLIP.git@main#egg=clip
EOF

ENV WORKDIR=/stable-diffusion

WORKDIR ${WORKDIR}
RUN mkdir -p "${WORKDIR}/models/ldm/stable-diffusion-v1/"
RUN ln -sf /cache/models/model.ckpt "${WORKDIR}/models/ldm/stable-diffusion-v1/model.ckpt"
# CMD python scripts/txt2img.py --prompt "a photograph of an astronaut riding a horse" --plms --n_samples 1 --n_iter 1
