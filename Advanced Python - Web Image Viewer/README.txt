Web Image Viewer is a lightweight Python application that provides a graphical user interface (GUI) for fetching, displaying, and downloading images from a specified web page. Built using Tkinter and Pillow, this tool demonstrates simple web scraping techniques alongside image processing and GUI development.

Features
Retrieve Images: Fetches images from a given URL by scanning the HTML for links ending in .jpg or .png.
Display Images: Loads and displays the retrieved images in a Tkinter window.
Download Images: Saves the images to your local machine for offline use.
Simple Interface: A straightforward GUI with an entry field and action buttons for image retrieval and downloading.
Requirements:
	Python 3.x
	Tkinter: Included with standard Python installations.
	Pillow: Python Imaging Library fork (for image handling).
	Internet Connection: Required for fetching images from the web.

Installation:
	git clone https://github.com/yourusername/your-repo.git
	cd your-repo

Install Dependencies:
Ensure Pillow is installed using pip:
	pip install Pillow

Usage:
Execute the script using Python:
	python WebImageViewer.py
Using the Interface:
	URL Input: The application starts with a default URL. You can modify it by typing a new URL into the input field.
	Retrieve Images: Click the "Retrieve Images" button to parse the webpage and display any images found.
	Download Images: Click the "Download Images" button to download the images to your current working directory.

How It Works
	HTML Parsing: The script fetches the content of the specified URL using urllib.request and scans the HTML lines for image file references (i.e., URLs ending in .jpg or .png).
	Image Display: Using Pillow and Tkinter’s PhotoImage, each image is opened and displayed within the GUI.
	Image Downloading: The script saves the images locally, handling file naming based on the image URL.

Limitations:
	Basic Parsing: The current HTML parsing approach is rudimentary and might not handle all web page structures or dynamic content.
	File Types: Only images with URLs ending in .jpg or .png are processed. Future improvements could expand support to other image formats.
	Error Handling: While basic exceptions are caught and printed, more robust error handling could improve reliability.