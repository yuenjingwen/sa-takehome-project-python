# Simple E-Commerce Application
This is a simple e-commerce application enabling users to seamlessly purchase books online using Stripe, including:

* **Browse and select** a book to purchase
* **Secured checkout** powered by Stripe Elements
* **Instant purchase confirmation** with payment details

## Table of Contents
- [How to Build, Configure, and Run](#how-to-build-configure-and-run)
- [How the Solution Works](#how-the-solution-works)
	- [Stripe API Usage](#stripe-api-usage)
	- [Application Architecture](#application-architecture)
- [Development Process](#development-process)
	- [Approach and Documentation Used](#approach-and-documentation-used)
	- [Challenges Encountered](#challenges-encountered)
- [Potential Extensions](#potential-extensions)

## How to Build, Configure, and Run
To get started, clone the respository and navigate into the project directory: 
```
git clone https://github.com/yuenjingwen/sa-takehome-project-python && cd sa-takehome-project-python
```
Install the necessary Python dependencies listed in `requirements.txt` using pip:
```
pip3 install -r requirements.txt
```

Configure Stripe API Keys:

1. Rename  `sample.env` to `.env`. Open the `.env` file and replace the placeholders with your Stripe account's Publishable and Secret API keys.
2. Open the `/public/js/custom.js` file. Locate the line where the `Stripe` object is initialized and replace the placeholder with your own Publishable Key.

Then run the application locally:

```
flask run
```

Navigate to [http://localhost:5000](http://localhost:5000) in your web browser to view the index page of the application.

## How the Solution Works
This application implements a simple e-commerce flow for puchasing a single book using Stripe Elements for payment processing. The key steps involved are:

1. **Book Selection:** 
	* The user browses the home page. The home route (`/`) in `app.py` renders the `index.html` page, displaying the available books.
	* The user selects a book they want to purchase by clicking on the "Purchase" button. This navigates them to the checkout page (`checkout.html`) with a query parameter indicating the selected item.

2. **Checkout Page:** 
	* The checkout route (`/checkout`) in `app.py` renders the `checkout.html` page, and retrieves details of the selected book (title and amount) using the query parameter to display on the page.
	* The total amount due is displayed on this page.
	* The Stripe Payment Element is integrated in this page via Javascript (`custom.js`).

3. **Payment Processing via Stripe Payment Element:**
	* When `checkout.html` loads, the `custom.js` script initializes Stripe with your publishable key.
	* Upon detecting a payment form, the `custom.js` executes the `initialize()` function which makes a `POST` request to the `/create-payment-intent` route on your server side (`app.py`).
	* The create payment intent route (`/create-payment-intent`) in `app.py` uses the Stripe Python library to create a Payment Intent instance with the amount of the selected book and the currency (in this case `sgd`). The `client_secret` from the Payment Intent is returned as a JSON response to the client side.
	* On the client side, the `initialize()` function uses the `client_secret` to configure and mount the Stripe Payment Element in the designated `#payment-element` div on the `checkout.html` page. This element provides a secure and customizable UI for collecting payment information.
	* When the user submits the payment form by clicking on the "Pay" button, the `handleSubmit()` function in `custom.js` calls `stripe.confirmPayment()` with the Payment Element. This securely sends the payment details to Stripe.
	* The `confirmParams` within `stripe.confirmPayment()` includes the `return_url` (`http://localhost:5000/success`), where Stripe will redirect the user to upon a successful payment.

4. **Payment Confirmation**
	* The success route (`/success`) in `app.py` retrieves the Payment Intent ID from the query parameter.
	* This Payment Intent ID is then used by the Stripe Python library to retrieve the corresponding Payment Intent instance, which holds comprehensive details about the payment. The amount paid is also extracted from this instance.
	* The retrieved Payment Intent ID and amount paid are passed to the `success.html` page, which is then being rendered and displayed to the user.
	* Additionally, when the user lands on the `success.html` page, the `checkStatus()` function in `custom.js` executes to retrieve and display the payment status on the page. 


### Stripe API Usage
This application uses the following Stripe APIs:

* **Server-Side API**	
	* **Payment Intents API in `app.py`:** 
		* The `stripe.PaymentIntent.create()` function is used in the `/create-payment-intent` route to initiate the payment transaction by creating a Payment Intent object. This object tracks the lifecycle of the payment.
		* The `stripe.PaymentIntent.retrieve()` function is used in the `/success` route to fetch details of a specific Payment Intent using the Payment Intent ID. This allows the application to display information about the payment to the user.
* **Client-Side API**
	* **Payment Elements API in `public/js/custom.js`:** The `stripe.elements().create()` function is used to create an instance of a Payment Element, which provides the UI embedded in the webpage to collect payment details from the user.
	* The `stripe.confirmPayment()` function in `public/js/custom.js` is used to confirm a Payment Intent collected by the Payment Element.

### Application Architecture
This application follows a basic web architecture with a Python backend using the [Flask framework](https://flask.palletsprojects.com/) and a static frontend using HTML, CSS and Javascript.

* **Frontend (`public/`, `views/`)**
	* **HTML (`index.html`, `checkout.html`, `success.html`, `layouts/main.html`):** Provides the structure and content of each web page, using Jinja2 for template inheritance and dynamic content rendering from the Flask backend.
	* **CSS (`public/css/style.css`):** Uses the [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) CSS framework to handle the layout and styling of the application.
	* **Javascript (`public/js/custom.js`):** Implements the client-side logic for interacting with the Stripe API (initializing the Payment Element, handling form submission, and checking payment status).
	* **Images (`public/images/`):** Contains static images used in the application.
* **Backend (`app.py`)**
	* Loads the configuration (Stripe Secret Key) from the `.env` file using `dotenv`.
	* Uses the Flask framework to handle routing and server-side logic.
	* Defines the routes for the home page (`/`), checkout (`/checkout`), creating Payment Intents (`/create-payment-intent`), and the success page (`/success`).
	* Calls the Payment Intents API from the Stripe Python library for creating and retrieving Payment Intents.
	* Renders the HTML templates using Jinja2.
* **Other Configurations (`.env`, `requirements.txt`)**
	* `.env`: Stores the Stripe Publishable Key and Stripe Secret Key which is loaded at runtime. 
	* `requirement.txt`: Lists the Python dependencies required to run the application.

## Development Process

This project was approached with a focus on understanding the core requirements of integrating Stripe Elements in the e-commerce purchase flow. The key stages of the development process are:

### Approach and Documentation Used

1. **Understanding the Requirements:** The project began with a careful analysis of the requirements, particularly the need to use Stripe Payment Element (instead of Stripe Checkout) and the required user actions: book selection, checkout using Stripe Elements, display payment confirmation.
2. **Stripe Account and API Keys:** A crucial early step involved setting up a Stripe account and obtaining the necessary Test API Keys (Publishable and Secret Keys).
3. **Basic Application Structure:** Consideration was given to the division of server-side and client-side responsibilities within the existing file structure to effectively meet the project requirements.
4. **Stripe Documentation Research:** To determine the appropriate server-side and client-side logic, a focused exploration of Stripe's documentation on implementing the Payment Element for payment processing was undertaken. Key documentation included: 
	* **[Build an advanced integration with Payment Element](https://docs.stripe.com/payments/quickstart):** An overview guide on how to embed a Stripe payment form in an application, covering both client-side (Payment Intent) and server-side (Payment Element).
	* **[Payment Intent API Reference](https://docs.stripe.com/api/payment_intents):** Explained how to create and manage Payment Intents on the server side using the Stripe API, including retrieving Payment Intents to fetch payment details.
	* **[Payment Element API Reference](https://docs.stripe.com/js/element/payment_element):** Detailed guide on how to create a Payment Element as an embedded component or secured payment details collection.
	* **[Stripe JavaScript Library Reference](https://docs.stripe.com/js):** Documented the functions available in Stripe’s browser-side JavaScript library `Stripe.js`, including [Creating an Element Object](https://docs.stripe.com/js/elements_object/create), [Creating a Payment Element](https://docs.stripe.com/js/elements_object/create_payment_element), and [Confirming a Payment Intent](https://docs.stripe.com/js/payment_intents/confirm_payment). 
5. **Iterative Prototyping and Troubleshooting:** The development followed an iterative approach. The Stripe Payment Element was first integrated in the checkout page to handle the UI. Following this, the backend logic for creating Payment Intents was implemented, and finally, the success page with payment status and details were added. **Throughout this process, console logging (using `console.log()` in JavaScript and `print` statements in Python) was actively used as a primary method for debugging and understanding the flow of data and potential issues.**
6. **Basic Security Considerations:** While this is a simplified application, a basic awareness of security best practices was maintained, such as handling the Secret Key on the backend and understanding how Stripe Elements securely handles the customer's payment information in their browser (client side).

### Challenges Encountered

1. **Dependency Incompatibility:** A major issue was the incompatibility between Flask (`2.0.0`) and the automatically installed Werkzeug (`3.1.3`), causing an `ImportError`. Flask relied on an older Werkzeug `url_quote` function. Resolution involved manually specifying a compatible Werkzeug version (`2.0.0`) in `requirements.txt` to fix the import error and ensure the Flask application ran.
2. **Understanding Stripe's Payment Flow & Server-Client Responsibilities:** A significant hurdle was gaining a clear understanding of Stripe's overall payment request flow and the appropriate division of responsibilities between the server-side and client-side. This involved determining which actions, such as creating Payment Intents, needed to be securely handled on the server using the Secret Key, and which UI-related tasks and payment confirmation steps were managed on the client-side using the Publishable Key and Stripe's JavaScript library.
3. **Data Formatting for Payment Intent Creation:** A key challenge was grasping the required input format for the `/create-payment-intent` endpoint, notably the `amount` parameter for Stripe's Payment Intents API. Correctly formatting `items_price` from client-side JavaScript into an integer representing the amount in cents for the `POST` request body demanded careful attention.
4. **Managing Asynchronous Operations for Payment Flow:** Ensuring a smooth and logical user experience required careful management of asynchronous operations, particularly when interacting with the Stripe API. A challenge was to structure the code using `async/await` to handle sequential steps correctly, such as waiting for the `client_secret` to be fetched from the server before initializing and mounting the Stripe Payment Element on the client-side. This was crucial to prevent errors and ensure that the payment UI was only presented when the necessary configuration data was available


## Potential Extensions
Here are some ideas on how this application can be made more robust by handling more complex e-commerce scenarios:

1. **Ensure Reliable Payments with Idempotent Keys**
	* Idempotent keys are essential for a reliable Stripe payment flow in this e-commerce application. Generate a unique key for each Payment Intent creation in the `/create-payment-intent` route such as concatenating the session ID with a UUID. Pass this generated key as the `idempotency_key` parameter within the `stripe.PaymentIntent.create()` function. This ensures Stripe processes each payment initiation only once, even if requests are retried, preventing duplicate charges and ensuring transaction integrity.

2. **Expanding Payment Intent Capabilities**
	* **`stripe.payment_intent.capture()`:** This function allows us to capture funds that were previously authorized, which can be used to handle the purchase process more effectively.  For example, when a customer clicks on the "Pay" button in the `/checkout` page, we could create a Payment Intent with `capture_method: 'manual'`. This authorizes their payment, ensuring they have sufficient funds, but does not yet charge them. Then, once we confirm the book is ready to ship, we use `stripe.payment_intent.capture()` to finalize the charge.  This prevents us from charging the customer if, for some reason, the book isn't available.
	* **`stripe.payment_intent.cancel()`:** This function is useful for handling order cancellations as it enables us to cancel a Payment Intent before it has been captured. If a customer cancels their order before we ship the book, we can use `stripe.payment_intent.cancel()` to release the authorization on their payment.  This ensures the customer isn't charged, simplifying our order management process and providing a better customer experience

3. **Use Webhook to Send Email Confirmation**
	* A webhook can be used to receive event notifications from Stripe and send an email confirmation after a successful payment. First, the email address captured on the `/checkout` page can be used to set the `receipt_email` parameter of the Payment Intent using `stripe.payment_intents.update()`. Then, when a customer completes the checkout process and Stripe confirms the payment, Stripe will send a `payment_intent.succeeded` event to our webhook endpoint. Our server can then use a library like `smtplib` to send a confirmation email. This process provides customers with prompt purchase confirmation and a transaction record.



