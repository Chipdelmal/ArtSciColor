#!/usr/bin/env python
# -*- coding: utf-8 -*-

from super_image import EdsrModel, ImageLoader


def superscale(img):
    model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=2)
    inputs = ImageLoader.load_image(Image.fromarray(img.astype('uint8'), 'RGB'))
    preds = model(inputs)
    return preds