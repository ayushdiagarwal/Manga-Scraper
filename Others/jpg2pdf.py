from PIL import Image
import os
im_list = []
count = 0
for i in sorted(os.listdir(), key=len):
	if i.endswith(".jpg"):
		img = Image.open(i)
		print(str(count) , img.mode)
		if img.mode != "P":
			if count == 0:
				first = img
			else:
				im_list.append(img)
			count += 1
first.save(f"Chapter 95.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=im_list)