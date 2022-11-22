# -*- coding: utf-8 -*-

def keepAspectResizeToIo(Image, io, path, size):

    image = Image.open(path)

    width, height = size
    x_ratio = width / image.width
    y_ratio = height / image.height

    if x_ratio < y_ratio:
        resize_size = (width, round(image.height * x_ratio))
    else:
        resize_size = (round(image.width * y_ratio), height)

    resized_image = image.resize(resize_size)

    bio = io.BytesIO()
    resized_image.save(bio, format = 'PNG')
    
    return bio.getvalue()

def imageInvertColor(Image, ImageOps, io, im_path):
    img_bytes = io.BytesIO()

    im = Image.open(im_path)

    r,g,b,a = im.split()
    rgb_image = Image.merge('RGB', (r,g,b))
    inverted_image = ImageOps.invert(rgb_image)
    r2,g2,b2 = inverted_image.split()

    final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
    final_transparent_image.save(img_bytes, format = 'PNG')

    return img_bytes.getvalue()

def imageToIo(Image, io, im_path):
    img_bytes = io.BytesIO()

    im = Image.open(im_path)
    im.save(img_bytes, format = 'PNG')

    return img_bytes.getvalue()

def info_text_update(window_name, text):
    window_name['-announcement_text-'].update(value = text)
    window_name.refresh()