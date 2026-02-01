from PIL import Image, ImageDraw
img = Image.new('RGB',(600,800),'white')
d = ImageDraw.Draw(img)
d.text((50,50),'Test PDF preview', fill='black')
img.save('test.pdf','PDF')
print('created test.pdf')
