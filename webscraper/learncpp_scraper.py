import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
import time
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LearnCppScraper:
    def __init__(self, base_url="https://www.learncpp.com"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.tutorials = {}

    def get_soup(self, url):
        try:
            logger.info(f"Fetching URL: {url}")
            time.sleep(1)  # Be polite to the server
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def clean_text(self, text):
        if not text:
            return ""
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return ' '.join(chunk for chunk in chunks if chunk)

    def scrape_tutorial_page(self, url):
        """Scrape individual tutorial page content"""
        soup = self.get_soup(url)
        if not soup:
            return None
        
        # Find the main content
        content = soup.find('article') or soup.find('div', class_='entry-content')
        if not content:
            logger.warning(f"Could not find content container for {url}")
            return None

        # Remove unwanted elements
        for element in content.select('script, style, .code-toolbar, .prevnext, .footer'):
            element.decompose()

        title = soup.find('h1')
        title_text = title.get_text().strip() if title else ''

        return {
            'url': url,
            'content': self.clean_text(content.get_text()),
            'title': title_text
        }

    def parse_lesson_tables(self, soup):
        """Parse lesson tables to get organized chapter and lesson information"""
        chapters = {}
        
        # Find all lesson tables
        lesson_tables = soup.find_all('div', class_='lessontable')
        
        for table in lesson_tables:
            # Get chapter header information
            header = table.find('div', class_='lessontable-header')
            if not header:
                continue
                
            chapter_div = header.find('div', class_='lessontable-header-chapter')
            title_div = header.find('div', class_='lessontable-header-title')
            
            if not chapter_div or not title_div:
                continue
                
            # Extract chapter number and title
            chapter_text = chapter_div.get_text().strip()
            chapter_match = re.search(r'Chapter\s*(\d+[A-Za-z]?)', chapter_text)
            if not chapter_match:
                continue
                
            chapter_num = chapter_match.group(1)
            chapter_title = title_div.get_text().strip()
            
            # Initialize chapter if not exists
            if chapter_num not in chapters:
                chapters[chapter_num] = {
                    'title': chapter_title,
                    'lessons': {}
                }
            
            # Get lessons
            lesson_list = table.find('div', class_='lessontable-list')
            if not lesson_list:
                continue
                
            for row in lesson_list.find_all('div', class_='lessontable-row'):
                number_div = row.find('div', class_='lessontable-row-number')
                title_div = row.find('div', class_='lessontable-row-title')
                
                if not number_div or not title_div:
                    continue
                    
                lesson_num = number_div.get_text().strip()
                link = title_div.find('a')
                
                if link:
                    lesson_title = link.get_text().strip()
                    lesson_url = link.get('href')
                    if lesson_url:
                        chapters[chapter_num]['lessons'][lesson_num] = {
                            'title': lesson_title,
                            'url': lesson_url
                        }
        
        return chapters

    def scrape_all_tutorials(self):
        """Scrape all tutorials using the lesson table structure"""
        logger.info("Starting to scrape main page")
        soup = self.get_soup(self.base_url)
        if not soup:
            return

        # Get organized chapter and lesson information
        chapters = self.parse_lesson_tables(soup)
        logger.info(f"Found {len(chapters)} chapters")

        # Scrape content for each lesson
        for chapter_num, chapter_data in chapters.items():
            logger.info(f"Processing Chapter {chapter_num}: {chapter_data['title']}")
            
            for lesson_num, lesson_info in chapter_data['lessons'].items():
                logger.info(f"Scraping lesson {lesson_num}: {lesson_info['title']}")
                content = self.scrape_tutorial_page(lesson_info['url'])
                
                if content:
                    lesson_info['content'] = content['content']
                    logger.info(f"Successfully scraped lesson {lesson_num}")
            
            self.tutorials[chapter_num] = chapter_data

    def save_tutorials(self, output_dir="learncpp_tutorials"):
        if not self.tutorials:
            logger.error("No tutorials to save!")
            return

        logger.info(f"Saving tutorials to {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the full structure as JSON
        json_path = os.path.join(output_dir, 'tutorials.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.tutorials, f, indent=2)
        
        # Save chapters with all lessons as subheaders
        for chapter_num, chapter_data in self.tutorials.items():
            chapter_filename = f"Chapter_{chapter_num}.md"
            chapter_path = os.path.join(output_dir, chapter_filename)
            
            with open(chapter_path, 'w', encoding='utf-8') as f:
                # Write chapter title
                f.write(f"# {chapter_data['title']}\n\n")
                
                # Sort lessons by number
                sorted_lessons = sorted(chapter_data['lessons'].items(), 
                                     key=lambda x: float(re.sub(r'[^\d.]', '', x[0])))
                
                # Write each lesson as a subheader
                for lesson_num, lesson_info in sorted_lessons:
                    f.write(f"\n## {lesson_num} - {lesson_info['title']}\n\n")
                    f.write(f"Source: {lesson_info['url']}\n\n")
                    if 'content' in lesson_info:
                        f.write(f"{lesson_info['content']}\n\n")
                    f.write("---\n")  # Add separator between lessons
                
                logger.info(f"Saved chapter: {chapter_path}")

def main():
    scraper = LearnCppScraper()
    logger.info("Starting scraper...")
    scraper.scrape_all_tutorials()
    
    if scraper.tutorials:
        logger.info(f"Found {len(scraper.tutorials)} chapters")
        scraper.save_tutorials()
        logger.info("Done! Check the 'learncpp_tutorials' directory for the results.")
    else:
        logger.error("No tutorials were scraped!")

if __name__ == "__main__":
    main()