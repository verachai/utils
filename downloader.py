import requests
from bs4 import BeautifulSoup
import urllib.request
import glob
import os


url_local_map = {
    "http://curriculum.cs2n.org/ev3/": "CMU_EV3_intro/",
    "http://education.rec.ri.cmu.edu/products/ev3_intermediate/": "CMU_EV3_intermediate/",
    "http://education.rec.ri.cmu.edu/products/vexiq_intermediate/": "CMU_VEX_IQ/",
    "http://www.education.rec.ri.cmu.edu/products/teaching_robotc_vexiq/": "CMU_VEX_IQ_intro/",
    "http://www.education.rec.ri.cmu.edu/products/cortex_video_trainer/": "CMU_EDR/"
}
url = "http://www.education.rec.ri.cmu.edu/products/cortex_video_trainer/"
local = 'cum_robotics/' + url_local_map[url]

### fetch all htmls ###
# r = requests.get(url)
# print(BeautifulSoup(r.content, 'lxml').prettify())
# with open(local+'index.html', 'wb') as f:
#     f.write(r.content)
# os.makedirs(local+'lesson', exist_ok=True)

# with open(local+'index.html', 'r') as indexf:
#     soup = BeautifulSoup(indexf.read(), 'lxml')
#     # print(soup.prettify())
#     links = [l for l in soup.find_all('a') if 'lesson' in l.get('href')]
#     lesson_name = set([l.get('href').split('#')[0] for l in links])
#
#     for lname in lesson_name:
#         print(lname)
#         sub_url = url + lname
#         r = requests.get(sub_url)
#         with open(local + lname, 'wb') as f:
#             f.write(r.content)

# EDR only
# html_parts = glob.glob(local+'lesson/*.html')
# for part in html_parts:
#     with open(part) as pf:
#         soup = BeautifulSoup(pf.read(), 'lxml')
#         links = [l for l in soup.find_all('a') if 'html' in l.get('href')]
#         lesson_name = set([l.get('href').split('#')[0] for l in links])
#         lesson_name = sorted([l for l in lesson_name if 'index' not in l])
#
#         for lname in lesson_name:
#             print(lname)
#             sub_url = url + 'lesson/' + lname
#             r = requests.get(sub_url)
#             with open(local + lname, 'wb') as f:
#                 f.write(r.content)

#######################

htmls = glob.glob(local + 'lesson/*.html')

all_files = set()
all_videos = set()
all_images = set()
for html in htmls:
    with open(html, 'r') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

        all_files |= set([e.get('href') for e in soup.find_all('a', recursive=True)])

        for e in soup.find_all('video', recursive=True):
            all_videos |= set([mp4.get('src') for mp4 in e.find_all('source')])

        all_images |= set([e.get('src') for e in soup.find_all('img', recursive=True)])

### download pdfs ###
# if None in all_files:
#     all_files.remove(None)
# for f in all_files:
#     if 'pdf' not in f and 'html' not in f:
#         print(f)

# pdfs = sorted(set([l.split('#')[0] for l in all_files if 'rbg' in l and not l.startswith('http')]))
# local_pdf = glob.glob(local+'lesson/media_files/Sensing/*.rbc')
# print(len(local_pdf))
# print(len(pdfs))
# for pdf in pdfs:
#     if local+'lesson/'+pdf not in local_pdf:
#         dest_url = url+'lesson/'+pdf.replace(' ', '%20')
#         local_dir = local+'lesson/'+pdf
#         print(pdf)
#         os.makedirs('/'.join(local_dir.split('/')[0:-1]), exist_ok=True)
#         try:
#             urllib.request.urlretrieve(dest_url, local_dir)
#         except Exception:
#             print('!!! Failed:', pdf)
#             continue
#######################

### download videos ###
# local_mp4 = glob.glob(local+'lesson/media_videos/*.mp4')
# print(local_mp4)
# os.makedirs(local+'lesson/media_videos', exist_ok=True)
# for video in sorted(all_videos):
#     if local+'lesson/'+video not in local_mp4:
#         print(video)
#         try:
#             urllib.request.urlretrieve(url+'lesson/' + video, local+'lesson/'+video)
#         except Exception:
#             print('!!! Failed:', video)
#             continue
#######################

### download images ###
local_img = glob.glob(local+'lesson/media_images/*.png')
os.makedirs(local+'lesson/media_images', exist_ok=True)
os.makedirs(local+'lesson/img', exist_ok=True)

# for img in all_images:
#     if not img.startswith('img') and not img.startswith('media_images'):
#         print(img)

for img in all_images:
    if img.startswith('img') or img.startswith('media_images') and (local+'lesson/'+img not in local_img):
        print(img)
        try:
            urllib.request.urlretrieve(url+'lesson/' + img, local+'lesson/'+img)
        except Exception:
            print('!!! Failed:', img)
            continue
