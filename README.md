# The_Breakdown_Bot

Author: Menyukhov Vyacheslav | email: menyukhov@bk.ru

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Libraries Used](#libraries-used)
- [Project Setup and Configuration](#project-setup-and-configuration)
- [Conclusion](#conclusion)

## Introduction

This trading bot is designed to provide automated trading capabilities with strict money management and risk management strategy. Your task is only to determine the trend, support and resistance levels. The bot can be easily controlled through Telegram, allowing users to monitor and manage their trades conveniently from their mobile devices or computers.

## Features

1. **Automated Trading**: The bot is equipped with powerful algorithms that can execute trades automatically based on predefined strategy and market conditions.

2. **Telegram Integration**: Users can interact with the trading bot through Telegram commands, making it user-friendly and accessible.

3. **Money Management**: The bot emphasizes strict money management principles, ensuring that risks are managed effectively and capital preservation is prioritized.

4. **Risk Management**: Advanced risk management techniques are integrated into the bot to control position sizes and avoid overexposure.

5. **Customizable Strategies**: Users have the flexibility to customize their trading strategies based on their preferences and risk tolerance.

6. **Real-time Market Data**: The bot utilizes real-time market data to make informed trading decisions and keep track of the latest market trends.

## Libraries Used

The trading bot has been developed using the following key libraries:

1. **aiogram**
2. **asyncio**
3. **SQLAlchemy**
4. **aiohttp**
5. **pybit**
6. **WebSocket**

## Project Setup and Configuration

**Clone repository**

Clone the `the_breakdown_bot` repository to your computer:

```bash
git clone git@github.com:platsajacki/the_breakdown_bot.git
```

**Create a `.env` File**

Create a `.env` file in the project's root directory and add the following lines, replacing the values with your own:

```python
# API keys for ByBit exchange
API_KEY=your_key
API_SECRET=your_secret
TESTNET=False

# TG Bot Token
TOKEN=your_token

# My ID TG
MYID=your_id

# DATABASE
DATABASE=database_name
POSTGRES_LOGIN=your_login
POSTGRES_PASSWORD=your_password
HOST=db

# Docker
DOCKER_LOGIN=login
DEBUG=False
```

**Run the Project**

From the project directory, run the project using Docker Compose:

```bash
docker compose up -d
```

The project is now successfully set up and configured with your environment variables.

## Conclusion

This trading bot with Telegram control offers a reliable and efficient solution for automated trading with strict money management and risk management principles. Its user-friendly interface and customizable strategies make it a powerful tool for both novice and experienced traders. Get ready to automate your trading journey and achieve your financial goals with this cutting-edge trading bot.

---

If you're considering hiring me, I would be thrilled to discuss more about this trading bot project and how I can contribute to its success. I am confident in my skills and dedication to delivering high-quality software solutions. Thank you for considering my application!
