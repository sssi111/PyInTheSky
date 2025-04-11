import aiohttp
import asyncio
import os
import time
import random
import re
from urllib.parse import urljoin
from typing import List, Tuple, Optional


class AsyncImageDownloader:
    def __init__(self, output_dir: str, max_concurrent: int = 10):
        self.output_dir = output_dir
        self.max_concurrent = max_concurrent
        self.base_url = "https://thisxdoesnotexist.com/"
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        os.makedirs(output_dir, exist_ok=True)
    
    async def download_image(
        self,
        session: aiohttp.ClientSession,
        url: str,
        save_path: str,
    ) -> bool:
        async with self.semaphore:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://thisxdoesnotexist.com/",
                }
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        content = await response.read()
                        with open(save_path, "wb") as f:
                            f.write(content)
                        print(f"Downloaded: {save_path}")
                        return True
                    else:
                        print(f"Failed to download {url}: HTTP {response.status}")
            except Exception as e:
                print(f"Error downloading {url}: {str(e)}")
            return False
    
    async def get_image_urls(self, session: aiohttp.ClientSession) -> List[str]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        try:
            async with session.get(self.base_url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    img_pattern = r'<img[^>]+src="([^">]+)"'
                    img_urls = re.findall(img_pattern, html)
                    
                    image_urls = []
                    for url in img_urls:
                        if url.startswith('http'):
                            image_urls.append(url)
                        else:
                            image_urls.append(urljoin(self.base_url, url))
                    
                    print(f"Found {len(image_urls)} images on the website")
                    return image_urls
                else:
                    print(f"Failed to fetch the website: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"Error fetching the website: {str(e)}")
            return []
    
    def generate_urls(self, num_images: int, available_urls: List[str]) -> List[Tuple[str, str]]:
        urls = []
        
        for i in range(num_images):
            if available_urls:
                url = available_urls[i % len(available_urls)]
                filename = os.path.join(self.output_dir, f"image_{i+1}.jpg")
                urls.append((url, filename))
            else:
                width = 800 + (i % 20)
                height = 600 + (i % 15)
                image_url = f"https://picsum.photos/{width}/{height}?random={i}"
                filename = os.path.join(self.output_dir, f"image_{i+1}.jpg")
                urls.append((image_url, filename))
        
        return urls
    
    async def download_images(self, num_images: int) -> int:
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            available_urls = await self.get_image_urls(session)
            
            urls = self.generate_urls(num_images, available_urls)
            
            tasks = [
                self.download_image(session, url, filename) 
                for url, filename in urls
            ]
            results = await asyncio.gather(*tasks)
        
        success = sum(results)
        elapsed = time.time() - start_time
        
        print(f"\nDownloaded {success}/{num_images} images in {elapsed:.2f} seconds")
        print(f"Average speed: {num_images/elapsed:.2f} images/sec")
        
        return success


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Asynchronous image downloader from thisxdoesnotexist.com"
    )
    parser.add_argument(
        "num_images", type=int, help="Number of images to download"
    )
    parser.add_argument(
        "output_dir", type=str, help="Directory to save images"
    )
    parser.add_argument(
        "--concurrent",
        type=int,
        default=10,
        help="Maximum number of concurrent downloads",
    )
    
    args = parser.parse_args()
    
    downloader = AsyncImageDownloader(args.output_dir, args.concurrent)
    await downloader.download_images(args.num_images)


if __name__ == "__main__":
    asyncio.run(main()) 