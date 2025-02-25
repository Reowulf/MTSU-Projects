import tkinter as tk
import urllib.request
import urllib.parse
import io
import os
from PIL import Image, ImageTk
from urllib.parse import urljoin

root = tk.Tk()
root.title("Web Image Viewer")
url_entry = tk.Entry(root, width=50)#Input field
url_entry.pack(pady=10)
url_entry.insert(0, 'https://www.cs.mtsu.edu/~untch/')#Default address

frame = tk.Frame(root)
frame.pack()

frame = tk.Frame(root)
frame.pack()

def display_image(iURL):
    try:
        with urllib.request.urlopen(iURL) as i:
            data = i.read()
            image = Image.open(io.BytesIO(data))
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(frame, image=photo)
            label.image = photo
            label.pack()
    except Exception as e:
        print(f"Error loading {iURL}: {e}")

def display_images():
    url = url_entry.get().strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            for bline in data.split():
                line = bline.decode('utf-8')
                src_pos = line.find('src="')
                href_pos = line.find('href="')
                if line.lower().endswith('.jpg"') or line.lower().endswith('.png">'):
                    if src_pos != -1:
                        start_index = line.find('src="') + len('src="')
                    elif href_pos != -1:
                        start_index = line.find('href="') + len('href="')
                    end_index = line.find('"', start_index)
                    image_path = line[start_index:end_index]
                    if image_path.startswith('~untch'):
                        image_path = image_path[len('/~untch'):]

                    full_url = urljoin(url, image_path)
                    display_image(full_url)
    except Exception as e:
        print(f"Error fetching images from {url}: {e}")

def download_images():
    url = url_entry.get().strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            for bline in data.split():
                line = bline.decode('utf-8')
                src_pos = line.find('src="')
                href_pos = line.find('href="')
                if line.lower().endswith('.jpg"') or line.lower().endswith('.png">'):
                    if src_pos != -1:
                        start_index = line.find('src="') + len('src="')
                    elif href_pos != -1:
                        start_index = line.find('href="') + len('href="')
                    end_index = line.find('"', start_index)
                    image_path = line[start_index:end_index]
                    if image_path.startswith('~untch'):
                        image_path = image_path[len('/~untch'):]

                    full_url = urljoin(url, image_path)
                    download_image(full_url)
    except Exception as e:
        print(f"Error fetching images from {url}: {e}")

def download_image(iURL):
    try:
        with urllib.request.urlopen(iURL) as i:
            data = i.read()
            image_name = os.path.basename(iURL)
            with open(image_name, 'wb') as f:
                f.write(data)
            print(f"Downloaded {image_name}")
    except Exception as e:
        print(f"Error downloading {iURL}: {e}")

retrieve_button = tk.Button(root, text="Retrieve Images", command=display_images)
retrieve_button.pack()

download_button = tk.Button(root, text="Download Images", command=download_images)
download_button.pack(pady=5)

root.mainloop()