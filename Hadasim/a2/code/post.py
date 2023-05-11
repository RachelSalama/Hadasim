import requests

# Define the URL of the server
url = "http://localhost:5000/api/add_image/324863448"

# Read the image data from a file
with open('img.jpg', 'rb') as f:
    image_data = f.read()

# Define the files parameter of the request
files = {'image': image_data}

# Make the POST request to upload the image
response = requests.post(url, files=files)

# Print the response from the server
print(response.text)
