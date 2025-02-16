import requests
import os

def download_hero_image():
    # URL gambar dari Pexels
    image_url = "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=1920"
    
    # Pastikan direktori static/images ada
    os.makedirs("static/images", exist_ok=True)
    
    # Download gambar
    response = requests.get(image_url)
    if response.status_code == 200:
        with open("static/images/hero-image.jpg", "wb") as f:
            f.write(response.content)
        print("Hero image berhasil diunduh!")
    else:
        print(f"Gagal mengunduh gambar. Status code: {response.status_code}")

if __name__ == "__main__":
    download_hero_image() 