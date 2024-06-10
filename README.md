## Problem Statement
Design a simple web crawler in python. Given a starting URL, the crawler should visit each URL it finds on the same domain. It should print each URL visited, and a list of links found on that page. The crawler should be limited to one subdomain - so when you start with *https://monzo.com/*, it would crawl all pages on the monzo.com website, but not follow external links, for example to facebook.com or community.monzo.com.
Do not use frameworks like scrapy or go-colly which handle all the crawling behind the scenes or someone else's code. You are welcome to use libraries to handle things like HTML parsing.

## Setup

### Python Requirements
- Python 3.10 or higher

### Pip and Poetry
- Ensure you have `pip` installed. If not, you can install it by following the instructions [here](https://pip.pypa.io/en/stable/installation/).
- Install `poetry` for Python package management by running `pip install poetry`.

### Redis (Optional)
If you want to use Redis as a cache, you can install and run it locally. Follow the instructions https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/ to install Redis on your machine.

## Sample Output
The output of the crawler is stored in a file named `monzo-links.txt` in the src directory of the project. The output file contains the URL visited and the list of links found after recursively crawling `https://monzo.com`.

### Running the Project
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages by running `poetry install`.
4. Run the web crawler by executing `python src/crawler.py`.