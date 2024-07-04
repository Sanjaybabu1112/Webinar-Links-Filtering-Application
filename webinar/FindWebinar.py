from flask import Flask, render_template, request
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os
import webbrowser
from threading import Timer

app = Flask(__name__)

API_KEY = 'YOUR API KEY'

async def google_search(query, api_key, num_results=10):
    url = f"https://serpapi.com/search.json?q={query}&num={num_results}&api_key={api_key}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
    except Exception as e:
        print(f"Error fetching search results: {e}")
    return {}

def filter_links(results, keywords):
    keyword_pattern = '|'.join(keywords)
    regex = re.compile(keyword_pattern, re.IGNORECASE)
    filtered_results = [{'title': result['title'], 'link': result['link']} for result in results if regex.search(result['title']) or regex.search(result['link'])]
    return filtered_results

async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return None

def parse_webinars(page_content, keywords):
    keyword_pattern = '|'.join(keywords)
    regex = re.compile(keyword_pattern, re.IGNORECASE)
    soup = BeautifulSoup(page_content, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        title = a.get_text().strip()
        href = a['href']
        if 'webinar' in href and (regex.search(title) or regex.search(href)):
            if not any(domain in href for domain in ['facebook.com', 'twitter.com', 'linkedin.com', 'calendar', 'outlook', 'email', 'Watch it now »', 'Sign Up', 'Register']) and not href.endswith('.pdf'):
                if href.startswith("http") and title:
                    links.append({'title': title, 'link': href})
    return links

async def fetch_and_parse(session, url, keywords):
    page_content = await fetch_page(session, url)
    if page_content:
        return parse_webinars(page_content, keywords)
    return []

@app.route('/', methods=['GET', 'POST'])
async def index():
    all_webinar_links = []
    search_query = ""

    if request.method == 'POST':
        form = request.form
        search_query = form['query']
        query = search_query + " " + 'Webinar'
        keywords = ['webinar', 'online event']

        search_results = await google_search(query, API_KEY)
        filtered_search_results = filter_links(search_results.get('organic_results', []), keywords)

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_and_parse(session, result['link'], keywords) for result in filtered_search_results]
            results = await asyncio.gather(*tasks)
            for links in results:
                for link in links:
                    if not any(d['link'] == link['link'] for d in all_webinar_links):
                        all_webinar_links.append(link)

        no_links_found = not all_webinar_links
    else:
        no_links_found = False

    return render_template('index.html', webinar_links=all_webinar_links, no_links_found=no_links_found, search_query=search_query)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(0, open_browser).start()
    app.run(debug=True)
