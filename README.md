# Nafeed-Broken-Link

**Nafeed-Broken-Link** is a Python tool designed for identifying broken social media links on websites. It efficiently scans a given domain or subdomain for various social media links and checks their status codes to determine if they are broken or valid.

## Features

- Scans websites for social media links.
- Checks the status codes of social media links.
- Highlights the results with different colors for various status codes.
- Reports broken social media links specifically for platforms like Twitter (X.com), Facebook, LinkedIn, Instagram, GitHub, Reddit, Discord, and Pinterest.
- Provides clear output and easy-to-read results.

## Working
https://github.com/user-attachments/assets/4e6d97c7-e321-4dab-bec1-0f3cb5fef1ea

## Installation

To use the `Nafeed-Broken-Link` tool, follow these steps:

1. **Clone the Repository:**

       ```bash
       git clone https://github.com/H4cker-Nafeed/Nafeed-Broken-Link.git

2. **Navigate to the Directory:**
   
       ```bash
       cd Nafeed-Broken-Link

3. **Install Required Libraries:**

Install the necessary Python libraries using pip:  

    ```bash
    pip install requests beautifulsoup4

## Usage

1. **Run the Script:**

Execute the Python script to start the scanning process:

    ```bash
     python3 broken.py

2. **Enter the Domain or Subdomain:**

When prompted, enter the domain or subdomain you want to scan. For example:

    ```bash
    Enter the domain or subdomain: https://example.com

3. **View the Results:**

The tool will display the status of social media links found on the provided domain. Links will be categorized as either "Not vulnerable," "Forbidden," or "Vulnerable" based on their status codes. Errors in accessing pages will also be reported.

## Example Output

    ```bash
    Visiting: https://www.example.com
    Social media links found on https://www.example.com:
    Not vulnerable: https://twitter.com/example (Status code: 200)
    Forbidden: https://x.com/example (Status code: 403)
    Not vulnerable: https://github.com/example (Status code: 200)
    Vulnerable! Broken social media link found: https://www.facebook.com/example (Status code: 404)

 
