# Start2Impact Django + MongoDB project: Btc_exchange

### Introduction
The project I developed is a simple, yet powerful peer-to-peer Bitcoin exchange platform. Upon registration, users are able to receive a variable amount of bitcoins, ranging from 1 to 10. This allows users to have a starting balance to begin trading on the platform.
The platform's user-friendly interface makes it easy for users to place both buy and sell orders, view active orders in real-time, and track their profits and losses from their operations. Each user can post one or more buy or sell orders for a certain amount of bitcoins at a certain price. At the time of posting, if the buy order's price is equal to or higher than the sell order of any other user, the transaction is recorded and both orders are marked as executed.

### Features:
- A landing page that welcomes the user and explains the platform's functionality
- A registration form and a login form for authentication 
- A dashboard that will display the user's respective balances in bitcoin and dollars, their profit/loss from transactions, and where they can view active orders and place orders to buy or sell.

### Requirements:
- [Django](https://docs.djangoproject.com/it/4.0/)
- [Djongo](https://www.djongomapper.com/integrating-django-with-mongodb/)
- pymongo==3.12.3


[![Top Langs](https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/top-langs/?username=DeveloPerini)](https://github.com/DeveloPerini/github-readme-stats)


### Installation:
1) Clone the repo
   ```sh
   git clone https://github.com/DeveloPerini/Bitcoin-exchange.git
   ```
2) Create your virtualenvironment with
   ```sh
   python -m venv myvenv
   ```
3) Install the required dipendencies 
   ```sh
   pip install r-requirements.txt
   ```
4) Run the server 
   ```sh
   python manage.py runserver
   ```

### Usage
Just go to http://localhost:8000, register and enjoy your free Bitcoins! 
