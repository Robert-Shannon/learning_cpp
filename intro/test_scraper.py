from learncpp_scraper import LearnCppScraper

def test_single_page(url = 'https://www.learncpp.com/cpp-tutorial/introduction-to-these-tutorials/'):
    scraper = LearnCppScraper()
    url = url
    result = scraper.scrape_tutorial_page(url)
    print("Test result:", result)

def test_lesson_parser():
    from learncpp_scraper import LearnCppScraper
    
    scraper = LearnCppScraper()
    test_cases = [
        "0.1 -- Introduction to these tutorials",
        "1.2 Comments",
        "Chapter 1: C++ Basics",
        "2.1 -- Introduction to functions"
    ]
    
    print("Testing lesson parser:")
    for test in test_cases:
        chapter, lesson, title = scraper.get_lesson_info(test)
        print(f"\nInput: {test}")
        print(f"Chapter: {chapter}")
        print(f"Lesson: {lesson}")
        print(f"Title: {title}")

if __name__ == "__main__":
    test_single_page()
    test_lesson_parser()