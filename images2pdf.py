import img2pdf, os
with open(f"Chapter 11.pdf", "wb") as f:
			f.write(img2pdf.convert([i for i in sorted(os.listdir(), key=len) if i.endswith(".jpg")]))