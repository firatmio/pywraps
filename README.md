# PyWraps 🎁

<div align="center">

![PyWraps Banner](https://github.com/firatmio/pywraps/blob/main/assets/PyWraps.png)

**A collection of powerful Python decorators for enhanced functionality**

[![PyPI version](https://badge.fury.io/py/pywraps.svg)](https://badge.fury.io/py/pywraps)
[![Python Support](https://img.shields.io/pypi/pyversions/pywraps.svg)](https://pypi.org/project/pywraps/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Downloads](https://pepy.tech/badge/pywraps)](https://pepy.tech/project/pywraps)
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-brightgreen.svg)](https://github.com/pywraps/pywraps)

</div>

## 🚀 Features

PyWraps provides a comprehensive suite of decorators that enhance your Python functions with powerful capabilities:

- **🔄 Retry**: Automatically retry failed function calls with customizable attempts and delays
- **⏱️ Timeout**: Set execution time limits for both synchronous and asynchronous functions
- **🎯 Debounce**: Prevent rapid successive function calls, executing only the last one
- **🧵 Background**: Execute functions in separate threads without blocking the main thread

## 📦 Installation

```bash
pip install pywraps
```

## 🎯 Quick Start

```python
from pywraps import retry, timeout, debounce, background
import time
import random

@retry(tries=3, delay=1.0)
def unreliable_function():
    if random.random() < 0.7:
        raise Exception("Random failure!")
    return "Success!"

@timeout(seconds=5.0)
def slow_function():
    time.sleep(3)
    return "Completed within timeout"

@debounce(wait=2.0)
def search_function(query):
    print(f"Searching for: {query}")

@background
def heavy_computation():
    time.sleep(10)
    print("Background task completed!")
```

## 📚 Detailed Documentation

### 🔄 Retry Decorator

The `@retry` decorator automatically retries function execution when exceptions occur.

#### Parameters:
- `tries` (int): Number of retry attempts (default: 3)
- `delay` (float): Delay between retries in seconds (default: 1.0)
- `exceptions` (Exception or tuple): Exception types to catch (default: Exception)

#### Examples:

```python
from pywraps import retry
import requests
import random

@retry(tries=5, delay=2.0)
def fetch_data_from_api():
    response = requests.get("https://api.example.com/data")
    if response.status_code != 200:
        raise requests.RequestException("API request failed")
    return response.json()

@retry(tries=3, delay=0.5, exceptions=(ValueError, TypeError))
def parse_user_input(user_input):
    if not user_input.strip():
        raise ValueError("Empty input")
    return int(user_input)

@retry(tries=10, delay=1.0)
def database_operation():
    if random.random() < 0.8:
        raise ConnectionError("Database connection failed")
    return "Data saved successfully"

try:
    result = fetch_data_from_api()
    print("API data:", result)
except requests.RequestException as e:
    print(f"Failed after retries: {e}")
```

### ⏱️ Timeout Decorator

The `@timeout` decorator sets execution time limits for functions, supporting both synchronous and asynchronous operations.

#### Parameters:
- `seconds` (float): Maximum execution time in seconds

#### Examples:

```python
from pywraps import timeout
import time
import asyncio
import aiohttp

@timeout(seconds=3.0)
def cpu_intensive_task():
    total = 0
    for i in range(10000000):
        total += i * i
    return total

@timeout(seconds=5.0)
async def fetch_multiple_urls():
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1"
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(session.get(url))
        
        responses = await asyncio.gather(*tasks)
        return [resp.status for resp in responses]

@timeout(seconds=2.0)
def file_processing():
    with open("large_file.txt", "r") as f:
        lines = f.readlines()
    return len(lines)

try:
    result = cpu_intensive_task()
    print("Task completed:", result)
except TimeoutError as e:
    print(f"Operation timed out: {e}")

async def main():
    try:
        statuses = await fetch_multiple_urls()
        print("HTTP statuses:", statuses)
    except TimeoutError as e:
        print(f"Async operation timed out: {e}")

asyncio.run(main())
```

### 🎯 Debounce Decorator

The `@debounce` decorator prevents rapid successive function calls, executing only the last call after a specified delay.

#### Parameters:
- `wait` (float): Delay time in seconds before execution

#### Examples:

```python
from pywraps import debounce
import time

@debounce(wait=1.0)
def save_user_preferences(user_id, preferences):
    print(f"Saving preferences for user {user_id}: {preferences}")
    

@debounce(wait=0.5)
def search_suggestions(query):
    print(f"Fetching suggestions for: '{query}'")
    return [f"{query}_suggestion_{i}" for i in range(3)]

@debounce(wait=2.0)
def auto_save_document(document_id, content):
    print(f"Auto-saving document {document_id}")
    with open(f"doc_{document_id}.txt", "w") as f:
        f.write(content)

user_prefs = {"theme": "dark", "language": "en"}
save_user_preferences(123, user_prefs)
save_user_preferences(123, {**user_prefs, "theme": "light"})
save_user_preferences(123, {**user_prefs, "notifications": True})

for query in ["py", "pyt", "pyth", "pytho", "python"]:
    search_suggestions(query)
    time.sleep(0.1)

time.sleep(3)
```

### 🧵 Background Decorator

The `@background` decorator executes functions in separate threads, preventing blocking of the main thread.

#### Examples:

```python
from pywraps import background
import time
import logging

logging.basicConfig(level=logging.INFO)

@background
def send_email_notification(recipient, subject, body):
    print(f"Sending email to {recipient}...")
    time.sleep(2)
    print(f"Email sent to {recipient}: {subject}")

@background
def generate_report(report_type, data):
    print(f"Generating {report_type} report...")
    time.sleep(5)
    print(f"Report '{report_type}' generated with {len(data)} records")

@background
def cleanup_temp_files():
    print("Starting cleanup process...")
    time.sleep(3)
    print("Temporary files cleaned up")

@background
def log_user_activity(user_id, action, timestamp):
    logging.info(f"User {user_id} performed {action} at {timestamp}")
    time.sleep(0.5)
    logging.info(f"Activity logged for user {user_id}")

send_email_notification("user@example.com", "Welcome!", "Thank you for joining!")
generate_report("monthly_sales", list(range(1000)))
cleanup_temp_files()

for i in range(5):
    log_user_activity(f"user_{i}", "login", time.time())

print("All background tasks started!")
time.sleep(6)
print("Main thread continues...")
```

## 🔧 Advanced Usage

### Combining Decorators

You can combine multiple decorators for enhanced functionality:

```python
from pywraps import retry, timeout, background
import requests
import time

@background
@retry(tries=3, delay=1.0)
@timeout(seconds=10.0)
def robust_api_call(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@retry(tries=5, delay=0.5)
@timeout(seconds=30.0)
def critical_database_operation():
    time.sleep(2)
    return "Operation completed successfully"

robust_api_call("https://api.github.com/users/octocat")
result = critical_database_operation()
print(result)
```

### Error Handling Best Practices

```python
from pywraps import retry, timeout
import logging

logging.basicConfig(level=logging.INFO)

@retry(tries=3, delay=1.0, exceptions=(ConnectionError, TimeoutError))
@timeout(seconds=5.0)
def resilient_operation():
    import random
    if random.random() < 0.6:
        raise ConnectionError("Network issue")
    return "Success"

try:
    result = resilient_operation()
    logging.info(f"Operation successful: {result}")
except Exception as e:
    logging.error(f"Operation failed after all retries: {e}")
```

## 🎨 Use Cases

### Web Development
- **API Rate Limiting**: Use `@debounce` for search endpoints
- **Timeout Protection**: Apply `@timeout` to external API calls
- **Background Processing**: Use `@background` for email sending, file uploads
- **Retry Logic**: Implement `@retry` for database operations

### Data Processing
- **Batch Operations**: `@background` for large dataset processing
- **Network Resilience**: `@retry` for data fetching from unreliable sources
- **Resource Management**: `@timeout` to prevent memory leaks in long operations

### User Interface
- **Search Optimization**: `@debounce` for real-time search suggestions
- **Form Validation**: `@debounce` for input validation
- **Progress Tracking**: `@background` for long-running tasks with progress updates

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for simple, powerful decorators in Python
- Built with love for the Python community
- Special thanks to all contributors and users

---

<div align="center">

**Made with ❤️ by the [firatmio](https://github.com/firatmio)**

[⭐ Star us on GitHub](https://github.com/firatmio/pywraps) | [🐛 Report Issues](https://github.com/firatmio/pywraps/issues) | [📖 Documentation](https://github.com/firatmio/pywraps#readme)

</div>