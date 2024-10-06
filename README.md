# Python Django Selenium Telegram Bot to Download and Serve Files from Envato with Subscription

This project is a Telegram bot developed with Python, Django, and Selenium that allows users to download and serve files from Envato Market. The bot features a subscription model, enabling users to access purchased items seamlessly through Telegram.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**: Secure user accounts using Telegram authentication with a subscription model.
- **Selenium Integration**: Utilize Selenium for automated interactions with the Envato website to download files.
- **File Serving**: Serve files to users based on their subscription status and purchased items.
- **Subscription Management**: Manage user subscriptions to control access to specific features or files.
- **Command List**: User-friendly commands for easy navigation of the bot's functionalities.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/telegram-envato-selenium-bot.git
    ```

2. Navigate into the project directory:
    ```bash
    cd telegram-envato-selenium-bot
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set up your Telegram Bot Token, Envato API credentials, and any necessary configurations in the configuration file.

## Usage

To start using the Telegram bot:

1. Run the Django server:
    ```bash
    python manage.py runserver
    ```
2. Open Telegram and find your bot using its username.
3. Start interacting with the bot to manage subscriptions and download files from Envato using Selenium.

## Contributing

Contributions are welcome! If you’d like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
