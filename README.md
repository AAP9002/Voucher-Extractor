# Automated Voucher Extractor

> Automate the extraction of vouchers from emails and generate PDFs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/AAP9002/Voucher-Extractor.svg)](https://github.com/AAP9002/Voucher-Extractor/issues)
[![GitHub Stars](https://img.shields.io/github/stars/AAP9002/Voucher-Extractor.svg)](https://github.com/AAP9002/Voucher-Extractor/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/AAP9002/Voucher-Extractor.svg)](https://github.com/AAP9002/Voucher-Extractor/network)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](CONTRIBUTING.md)

This project aims to automate the extraction of vouchers from emails, process them, and generate a PDF containing the extracted vouchers. The process involves creating a disposable email using an API, running automation scripts to create, confirm, screenshot, process, and unsubscribe from services that send vouchers via email. Additionally, there is a separate script to generate a PDF populated with the extracted vouchers.

## Features

- **Disposable Email Creation**: Utilizes an API to create disposable emails for receiving vouchers.
- **Automation**: Automatically handles the entire process from email creation to unsubscribing from services.
- **Voucher Extraction**: Extracts vouchers from received emails.
- **PDF Generation**: Generates a PDF file populated with the extracted vouchers.
  
![image](https://github.com/AAP9002/Voucher-Extractor/assets/42409957/448e174b-22b9-449b-b982-cfd10cfe8deb)


## Setup Instructions
We are using the [Temp Mail API](https://rapidapi.com/calvinloveland335703-0p6BxLYIH8f/api/temp-mail44)

1. Clone the repository to your local machine.
2. run `pip3 install -r requirements.txt` to install the required Python libraries.
3. Configure the API credentials for creating disposable emails.
3. Set up `.env` using the `.env.template` file.
4. Adjust the automation script settings according to your requirements.
5. Run the automation script to start the extraction process.
6. Use the separate script to generate a PDF containing the extracted vouchers.

## Usage

1. Run the automation script `./run.sh`.
2. Monitor the process as it creates disposable emails, confirms services, screenshots vouchers, processes them, and unsubscribes from services.
3. Find the pdf at `./bin/output.pdf` containing the extracted vouchers.

> **Note**: The run script will clear all files in the `./bin` directory before starting the process.

> **Warning**: Each request to the Temp Mail API costs 1 credit. Each run will use (n+1) requests with n being the number of voucher accounts. The free plan provides 100 credits per month. You can upgrade to a paid plan for more credits. Check quota usage on the [RapidAPI Dashboard](https://rapidapi.com/developer/billing/subscriptions-and-usage). Once quota reached, the API will return "quota reached" and the script will stop.

> **Note**: Each web request has a random delay to avoid bot detection. The delay can be adjusted in the automation script.

## Dependencies

- Python 3.x
- Required Python libraries (specified in `requirements.txt`)


## Contribution

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it according to your needs.
