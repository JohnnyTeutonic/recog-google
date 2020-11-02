import sys, os, multiprocessing, urllib, csv
from PIL import Image
from io import BytesIO


def ParseData(data_file):
    csvfile = open(data_file, 'r')
    csvreader = csv.reader(csvfile)
    key_url_list = [line[:2] for line in csvreader][1:]
    return key_url_list


def DownloadImage(key_url):
    out_dir = os.path.join(os.getcwd(), 'output')

    (key, url) = key_url
    filename = os.path.join(out_dir, '%s.jpg' % key)

    if os.path.exists(filename):
        print('Image %s already exists. %%SVGkipping download.' % filename)
        return

    try:
        response = urllib.request.urlopen(url)
        image_data = response.read()
    except:
        print('Warning: Could not download image %s from %s' % (key, url))
        return

    try:
        pil_image = Image.open(BytesIO(image_data))
        pil_image = pil_image.resize((1200, 1200))
    except:
        print('Warning: Failed to parse image %s' % key)
        return


    try:
        pil_image.save(filename, format='JPEG', quality=90)
    except:
        print('Warning: Failed to save image %s' % filename)
        return


def Run():
    data_file = os.path.join(os.getcwd(), os.path.join('landmark-recognition-challenge', 'train.csv'))
    out_dir = os.path.join(os.getcwd(), 'output')

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    key_url_list = ParseData(data_file)[:8000]
    pool = multiprocessing.Pool(processes=4)
    pool.map(DownloadImage, key_url_list)


if __name__ == '__main__':
    Run()
