# market-screener-app

The project is a full-stack web application that interfaces with a cryptocurrency exchange via an API. Its purpose is to scrutinise the market meticulously and identify the best trading or investment opportunities based on predetermined criteria. This advanced tool provides a holistic view of the market, enabling users to make informed decisions in real-time.

## Features

- **Event-driven architecture:** backend logic based on the iTrader framework. It's a well-oiled machine that acts as the backbone of the application.
- **Minimalist admin User Interface:**  this gives you control over the back-end operations. From here, you can activate or deactivate screeners, gain a quick overview of the market with the best and worst-performing assets, and toggle telegram notifications.
- **Live price data via web-socket:** the application receives live price data from the exchange. It also sends price data updates to the User Interface, ensuring you have the most recent information at your fingertips.
- **Telegram bot notifications:** the app includes a handy telegram bot that sends a notification whenever a screener event is generated. This way, you're always in the loop about what's happening in the market.

## Architecture

The architecture of this project is based on the MVC (Model-View-Controller) design pattern, implemented using the versatile Flask framework. This design pattern compartmentalizes the application into three main components:

- **Model:** The heart of the application, representing the core data and logic. This is essentially the iTrader framework, which takes charge of data management and the integral logic of the program.
- **View:** This is the interface through which the user interacts with the application. It not only displays the data but also captures user input. HTML pages are dynamically rendered using the powerful Jinja templating engine, facilitating a seamless user experience.
- **Controller:** Acting as the central nervous system of the MVC pattern, the controller processes user requests from the view, engages with the model to process these requests, and subsequently instructs the view on how to update itself based on the response. It's the orchestrator ensuring everything works in harmony.

## Usage

**Prerequisites:**

* Python 3.12 ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* pip (Python package installer) - usually comes bundled with Python
* Flask ([https://flask.palletsprojects.com/](https://flask.palletsprojects.com/))

**Installation:**

1. Clone this repository:

```bash
git clone https://github.com/tiziaco/market-screener-app.git
```

2. Navigate to the project directory:

```bash
cd market-screener-app
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

**Running the application:**

1. Start the Flask development server:

```bash
flask run
```

2. The application will typically run on `http://127.0.0.1:5000/` by default (you can check the exact port number in the console output). Open this URL in your web browser to access the web app.

**Additional Notes:**
* The development server is for local testing and development purposes. For deployment in a production environment, a different server setup is recommended (e.g., Gunicorn with WSGI).

**Development:**

* Any changes to the code will be automatically reflected in the browser when running the development server.

I hope this helps!
