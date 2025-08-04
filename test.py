from pywraps import retry, timeout, debounce, background
import time
import random
import asyncio

print("🎁 PyWraps Test Script")
print("=" * 40)

# 1. Retry Decorator Test
print("\n🔄 Testing @retry decorator:")

@retry(tries=3, delay=1.0)
def unreliable_function():
    print("  Attempting operation...")
    if random.random() < 0.7:
        raise Exception("Random failure!")
    return "Success!"

try:
    result = unreliable_function()
    print(f"  ✅ {result}")
except Exception as e:
    print(f"  ❌ Failed after retries: {e}")

# 2. Timeout Decorator Test (Sync)
print("\n⏱️ Testing @timeout decorator (sync):")

@timeout(seconds=2.0)
def slow_sync_function():
    print("  Starting slow operation...")
    time.sleep(1.5)
    return "Completed within timeout"

try:
    result = slow_sync_function()
    print(f"  ✅ {result}")
except Exception as e:
    print(f"  ❌ {e}")

@timeout(seconds=1.0)
def very_slow_function():
    print("  Starting very slow operation...")
    time.sleep(2.0)
    return "This won't complete"

try:
    result = very_slow_function()
    print(f"  ✅ {result}")
except Exception as e:
    print(f"  ❌ {e}")

# 3. Timeout Decorator Test (Async)
print("\n⏱️ Testing @timeout decorator (async):")

@timeout(seconds=2.0)
async def slow_async_function():
    print("  Starting async operation...")
    await asyncio.sleep(1.0)
    return "Async completed within timeout"

async def test_async_timeout():
    try:
        result = await slow_async_function()
        print(f"  ✅ {result}")
    except Exception as e:
        print(f"  ❌ {e}")

asyncio.run(test_async_timeout())

# 4. Debounce Decorator Test
print("\n🎯 Testing @debounce decorator:")

@debounce(wait=1.0)
def search_function(query):
    print(f"  🔍 Searching for: '{query}'")

print("  Calling search function rapidly...")
for i, query in enumerate(["py", "pyt", "pyth", "pytho", "python"]):
    search_function(query)
    print(f"    Call {i+1}: {query}")
    time.sleep(0.2)

print("  Waiting for debounced execution...")
time.sleep(2)

# 5. Background Decorator Test
print("\n🧵 Testing @background decorator:")

@background
def heavy_computation(task_id):
    print(f"  🔄 Background task {task_id} started")
    time.sleep(2)
    print(f"  ✅ Background task {task_id} completed")

@background
def send_notification(message):
    print(f"  📧 Sending notification: {message}")
    time.sleep(1)
    print(f"  ✅ Notification sent!")

print("  Starting background tasks...")
heavy_computation(1)
heavy_computation(2)
send_notification("Test message")

print("  Main thread continues immediately!")
print("  Waiting for background tasks to complete...")
time.sleep(3)

# 6. Combined Decorators Test
print("\n🔧 Testing combined decorators:")

@background
@retry(tries=2, delay=0.5)
@timeout(seconds=3.0)
def robust_operation(task_name):
    print(f"  🚀 Starting robust operation: {task_name}")
    if random.random() < 0.5:
        raise Exception("Random failure in combined test")
    time.sleep(1)
    print(f"  ✅ Robust operation '{task_name}' completed")

print("  Starting combined decorator test...")
robust_operation("Combined Test")

print("\n  Main thread finished!")
time.sleep(2)

print("\n" + "=" * 40)
print("🎉 PyWraps test completed!")
