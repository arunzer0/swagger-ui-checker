import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class SwaggerUIChecker:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.swagger_paths = ['','/swagger', '/swagger-ui', '/api-docs', '/docs']
        self.results = []

    def load_urls(self):
        """Load URLs from the CSV file into a DataFrame."""
        df = pd.read_csv(self.input_file)

        if 'URL' not in df.columns:
            raise ValueError("The CSV file must have a column named 'URL'.")

        return df['URL'].tolist()

    def extract_domain(self, url):
        """Extract the domain from a URL."""
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return domain

    def check_swagger_ui(self):
        """Check each domain for Swagger UI across multiple common paths."""
        urls = self.load_urls()

        for url in urls:
            domain = self.extract_domain(url)

            for path in self.swagger_paths:
                full_url = domain.rstrip('/') + path
                result = {
                    "URL": url,
                    "Domain": domain,
                    "Swagger Path": path,
                    "Full URL": full_url,
                    "Status Code": None,
                    "Swagger Enabled": "No",
                    "DOM Confirmation": "No"
                }

                try:
                    response = requests.get(full_url)

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')

                        # Confirm Swagger UI presence with DOM elements
                        if soup.find('div', id='swagger-ui') or soup.find('title', string='Swagger UI'):
                            result["Swagger Enabled"] = "Yes"
                            result["DOM Confirmation"] = "Yes"
                        
                    result["Status Code"] = response.status_code

                except requests.exceptions.RequestException as e:
                    result["Status Code"] = f"Error: {e}"

                # Append result for this path
                self.results.append(result)
        
    def save_results(self):
        """Save the results to a CSV file."""
        df = pd.DataFrame(self.results)
        df.to_csv(self.output_file, index=False)
        print(f"Results saved to {self.output_file}")

    def run(self):
        """Run the complete check process."""
        self.banner()
        self.check_swagger_ui()
        self.save_results()
    
    def banner(self):
        # Define the banner with colors using ANSI escape codes
        banner_content = """
        \033[1;32m=================================================\033[0m
        \033[1;34mWelcome to Swagger UI Checker!\033[0m
        \033[1;32m=================================================\033[0m

        \033[1;36mConnect with me:\033[0m
        \033[1;35m- GitHub: \033[0m\033[4;33mhttps://github.com/arunzer0\033[0m
        \033[1;35m- LinkedIn: \033[0m\033[4;33mhttps://www.linkedin.com/in/arunkumaarg\033[0m
        \033[1;35m- My Profile: \033[0m\033[4;33mhttps://x.com/arunkumaar_g\033[0m

        \033[1;32m=================================================\033[0m
        """
        print(banner_content)

# Usage example
if __name__ == "__main__":
    input_file = 'urls.csv'  # The input CSV file containing URLs
    output_file = 'swagger_check_results.csv'  # The output CSV file to save the results

    checker = SwaggerUIChecker(input_file, output_file)
    checker.run()