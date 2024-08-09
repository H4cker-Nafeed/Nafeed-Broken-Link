import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from termcolor import colored
import pyfiglet
import re
import os
import sys

# Print banner with advanced font and colors
def print_banner():
    ascii_banner = pyfiglet.figlet_format("Nafeed")
    print(colored(ascii_banner, "red"))
    developer_info = "DEVELOPED BY H4CKER NAFEED"
    instagram_info = "FOLLOW ME ON INSTAGRAM: @h4cker_nafeed"
    print(colored(developer_info, "light_blue"))
    print(colored(instagram_info, "light_blue"))
    print("=" * 60)

visited_urls = set()

def is_social_media_link(url):
    social_media_domains = [
        "facebook.com", "instagram.com", "linkedin.com", 
        "snapchat.com", "discord.com", "discord.gg",
        "x.com", "pinterest.com", "github.com",
        "twitter.com", "reddit.com"
    ]
    return any(domain in url for domain in social_media_domains)

def clean_link(link):
    link = re.sub(r'[\'"<>]', '', link)
    link = link.split('?')[0]  # Remove query parameters
    link = re.sub(r'/\d+$', '', link)  # Remove trailing numbers
    return link

def is_same_domain(url, base_url):
    return urlparse(url).netloc == urlparse(base_url).netloc

def fetch_links(domain):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(domain, headers=headers)
        if response.status_code != 200:
            print(colored(f"Failed to access {domain}. Status code: {response.status_code}", "magenta"))
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        links += [link.get('href') for link in soup.find_all('link', href=True)]
        links += [meta.get('content') for meta in soup.find_all('meta', content=True)]
        links += [iframe.get('src') for iframe in soup.find_all('iframe', src=True)]
        links = [urljoin(domain, link) for link in links if link]
        return [clean_link(link) for link in links if is_same_domain(link, domain)]
    except Exception as e:
        print(colored(f"Error fetching links from {domain}: {e}", "yellow"))
        return []

def check_social_media_link(link):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.head(link, allow_redirects=True, headers=headers)
        final_url = response.url
        if 'twitter.com' in final_url:
            final_url = final_url.replace('twitter.com', 'x.com')
        response = requests.get(final_url, headers=headers)
        status_code = response.status_code
        return (link, status_code)
    except Exception as e:
        print(colored(f"Error checking link {link}: {e}", "yellow"))
        return (link, None)

def extract_social_media_links(soup, base_url):
    social_media_links = []
    for a in soup.find_all('a', href=True):
        link = urljoin(base_url, a['href'])
        cleaned_link = clean_link(link)
        if is_social_media_link(cleaned_link):
            social_media_links.append(cleaned_link)
    for meta in soup.find_all('meta', content=True):
        link = urljoin(base_url, meta['content'])
        cleaned_link = clean_link(link)
        if is_social_media_link(cleaned_link):
            social_media_links.append(cleaned_link)
    for iframe in soup.find_all('iframe', src=True):
        link = urljoin(base_url, iframe['src'])
        cleaned_link = clean_link(link)
        if is_social_media_link(cleaned_link):
            social_media_links.append(cleaned_link)
    return social_media_links

def crawl(domain):
    to_visit = [domain]
    while to_visit:
        current_url = to_visit.pop()
        if current_url not in visited_urls:
            visited_urls.add(current_url)
            print(f"Visiting: {current_url}")
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                response = requests.get(current_url, headers=headers)
                if response.status_code != 200:
                    print(colored(f"Failed to access {current_url}. Status code: {response.status_code}", "magenta"))
                    continue
                soup = BeautifulSoup(response.text, 'html.parser')
                social_media_links = extract_social_media_links(soup, current_url)
                if social_media_links:
                    print(f"Social media links found on {current_url}:")
                    for link in social_media_links:
                        link, status_code = check_social_media_link(link)
                        if status_code == 404:
                            print(colored(f"Vulnerable! Broken social media link found: {link}", "red"))
                        elif status_code == 200:
                            print(colored(f"Not vulnerable: {link} (Status code: {status_code})", "green"))
                        elif status_code == 403:
                            print(colored(f"Forbidden: {link} (Status code: {status_code})", "yellow"))
                        else:
                            print(colored(f"Other status: {link} (Status code: {status_code})", "blue"))
            except Exception as e:
                print(colored(f"Error accessing {current_url}: {e}", "yellow"))
            links = fetch_links(current_url)
            to_visit.extend(links)

if __name__ == "__main__":
    try:
        print_banner()
        user_input = input("Enter the domain/subdomain or the path to a file containing a list of domains: ")

        if os.path.isfile(user_input):  # Check if the input is a file
            with open(user_input, 'r') as file:
                domains = file.read().splitlines()
            for domain in domains:
                crawl(domain)
        else:
            crawl(user_input)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully...")
        sys.exit(0)
