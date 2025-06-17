# ซอร์สโค้ดนี้ ใช้สำหรับเป็นตัวอย่างเท่านั้น ถ้านำไปใช้งานจริง ผู้ใช้ต้องจัดการเรื่องความปลอดภัย และ ประสิทธิภาพด้วยตัวเอง

# Minimart Expire Notifications

This n8n workflow is designed to monitor product expiration dates for a minimart and send Telegram notifications for items expiring today or within the next 10 days.

---

## Workflow Description

This workflow automates the process of checking product expiration dates and sending alerts. It consists of the following nodes:

1.  **Schedule Trigger 5pm**: This node acts as the starting point of the workflow. It's configured to trigger the workflow daily at 5:00 PM.

2.  **HTTP Request**: This node makes an HTTP request to `http://localhost:8000/data` to retrieve product data. It's assumed that this endpoint provides a list of products with their details, including an "Expire Date" and "ItemName (TH)".

3.  **If**: This conditional node checks if the `Expire Date` of an item from the retrieved data is **equal to today's date**.
    * If true, the workflow proceeds to the "Telegram" node to send an immediate expiration alert.
    * If false, it moves to the next "If1" node to check for upcoming expirations.

4.  **Telegram**: This node sends a Telegram message to the specified `chatId` (1234567890). The message notifies about items expiring **today**, including their `ItemID` and `ItemName (TH)`.

5.  **If1**: This conditional node checks if the `Expire Date` of an item is **equal to 10 days from today's date**. This means it's looking for items that will expire exactly 10 days from the current date.
    * If true, the workflow proceeds to the "Telegram1" node.

6.  **Telegram1**: This node sends a Telegram message to the specified `chatId` (1234567890). The message notifies about items expiring **within 10 days**, including their `ItemID` and `ItemName (TH)`.

---

## Setup Instructions

To use this workflow, you'll need to set up the following:

### 1. Telegram API Credentials

You need to configure your Telegram API credentials within n8n.

* In the "Telegram" and "Telegram1" nodes, you'll see a `credentials` section. Ensure that the `id` and `name` fields for `telegramApi` are correctly set up with your Telegram Bot Token. If you haven't already, you'll need to create a new Telegram Bot via BotFather and obtain your API token.

### 2. Data Endpoint

Ensure that the `HTTP Request` node can successfully access your product data at `http://localhost:8000/data`. This endpoint should return data in a format that includes at least:

* `Expire Date` (in ISO 8601 format, e.g., `YYYY-MM-DD`)
* `ItemID`
* `ItemName (TH)`

### 3. Local Data Server (`main.py` and `index.html`)

The `main.py` script acts as a simple HTTP server that serves product data from a SQLite database (`data.db`) and also provides the `index.html` file.

*   **`main.py`**: This Python script sets up a basic web server using `http.server`.
    *   It serves the `index.html` file when you access the root URL (`/`).
    *   It exposes a `/data` endpoint that returns product data in JSON format. This data is fetched from the `items` table in `data.db`.
    *   To run the server, execute `python main.py` in your terminal.

*   **`index.html`**: This HTML file is a simple web page that fetches data from the `/data` endpoint (served by `main.py`) and displays it in an HTML table. This provides a quick way to visualize the data being served.

### 4. Telegram Chat ID

The `chatId` in both Telegram nodes is currently set to `1234567890`. You will need to replace this with your actual Telegram chat ID where you want to receive the notifications. You can find your chat ID by sending a message to your bot and then accessing `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`.

---

## How it Works

Once activated, the workflow will perform the following actions daily at 5:00 PM:

1.  It fetches all product data from your specified HTTP endpoint.
2.  For each product, it first checks if the `Expire Date` is today. If it is, a "Today Expiring" notification is sent to Telegram.
3.  Regardless of whether it expires today, it then checks if the `Expire Date` is exactly 10 days from today. If it is, an "Expiring Within 10 Days" notification is sent to Telegram.

---

## Customization

* **Notification Time**: Adjust the `triggerAtHour` in the **Schedule Trigger 5pm** node to change the time when the workflow runs.
* **Expiration Threshold**: Modify the `rightValue` in the `If1` node's condition to change the "within X days" notification threshold. For example, to check for items expiring within 7 days, you would change `+ 10` to `+ 7`.
* **Telegram Message Content**: You can customize the `text` field in both Telegram nodes to change the content and formatting of the notification messages.
* **Data Source**: If your product data is available from a different source (e.g., a database, Google Sheets, another API), you can replace the `HTTP Request` node with the appropriate n8n node for that service.
