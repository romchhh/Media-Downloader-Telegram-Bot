# Telegram Media Downloader Bot

## Description

This Telegram bot allows users to download media from various social media platforms, including Instagram, TikTok, YouTube Shorts, Pinterest, and Twitter. It features interactive functions such as subscription checks, download statistics, user assistance, and customizable settings.

## Features

- **Media Download:** Send a link to a post or video from social media to download media.
- **View Statistics:** Check download statistics.
- **Assistance:** Get instructions on how to use the bot.
- **Language Settings:** Choose your preferred interface language.

## How It Works

1. **Subscription Check:** The bot verifies whether the user is subscribed to the channel. If not, it prompts them to subscribe.
2. **Link Processing:** Upon receiving a media link, the bot identifies the platform (Instagram, TikTok, YouTube Shorts, Pinterest) and proceeds to download the media.
3. **Media Delivery:** The bot sends the downloaded media to the user and deletes temporary files.
4. **Statistics and Help:** Users can view their download statistics and receive assistance.

## Technologies Used

- **Python:** The main programming language used to build the bot.
- **Telegram Bot API:** Used for bot interaction with Telegram users.
- **Requests Library:** For making HTTP requests to social media platforms.
- **BeautifulSoup:** For web scraping and parsing HTML.
- **SQLite:** For managing and querying download statistics.
- **Pillow:** For image processing tasks.
- **PyTelegramBotAPI:** Python wrapper for the Telegram Bot API.
- **Instaloader (alternative):** For downloading media from Instagram, if not using SnapInsta API.
- **SnapInsta API:** For Instagram media retrieval and downloading.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/telegram-media-downloader-bot.git
    cd telegram-media-downloader-bot
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Settings:**
   
   Edit the `data/config.py` file to include your bot token, admin ID, and channel ID.

4. **Run the Bot:**

    ```bash
    python main.py
    ```

## Screenshots

![image](https://github.com/user-attachments/assets/df33c2f5-1bb9-4c66-b74a-632dd0ca46a4)
![image](https://github.com/user-attachments/assets/9a794cd3-5f8e-4559-8c77-d53f776f3132)
![image](https://github.com/user-attachments/assets/0263e42d-a2dd-4894-ba42-aad3ef5435dd)
![image](https://github.com/user-attachments/assets/9356cae6-323a-4c79-8ea0-49071ff37c36)
![image](https://github.com/user-attachments/assets/90a50596-1dae-460c-ac51-4ba97b45b9bb)
![image](https://github.com/user-attachments/assets/bef53c41-c8c6-45fc-87f4-9f425e4a4408)


## Bot Link

[Your Bot on Telegram](https://t.me/media_easy_bot)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For additional questions, please reach out via Telegram: [@TeleBotsNowayrm](https://t.me/TeleBotsNowayrm)
