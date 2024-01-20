import time
from selenium import webdriver
from tqdm import tqdm

# Global delay for sleep between actions
global_delay = 0.8

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()
print('Program started...')

# Read URLs from a file
with open("urls.txt", "r") as f:
    urls = [url.rstrip() for url in f]

# Iterate through each URL
for url in tqdm(urls):
    try:
        # Visit the URL and navigate to the comments section
        driver.get(url + "/yorumlar")
        time.sleep(4)  # Allow time for the page to load

        # XPath to the container of comments
        element_str = "/".join([
            "", "html", "body", "div[1]", "div[3]", "div[1]",
            "div[1]", "div[1]", "div[1]", "div[3]", "div[1]", "div[1]", "div[3]", "div[2]"
        ])

        # Open a file to store comments
        comment_file = open("comment.tsv", "a", encoding='utf-8')

        i = 1
        # Loop through comments on the page
        while True:
            try:
                # Extract the score of the comment
                score = 0
                for j in range(1, 6):
                    score_text = driver.find_element('xpath', element_str + '/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[' + str(j) + "]/div[2]")
                    score_text = score_text.value_of_css_property("width")
                    score = score + 1 if score_text == "14px" else score

                # Extract the comment text
                comment = driver.find_element('xpath', element_str + '/div[' + str(i) + ']/div[2]/p').text
                comment_file.write(comment + "\t" + str(score) + "\t" + url + "\n")

                # Scroll down to load more comments
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(global_delay)
                i += 1
            except Exception as e:
                print(str(e))
                print("Done")
                break
    except Exception as e:
        print(str(e))
        print('Program ended')
        driver.quit()
        exit()
