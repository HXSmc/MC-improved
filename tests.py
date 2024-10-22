import threading
import time

def method_one():
    for i in range(5):
        time.sleep(1)  # Simulating some work with a delay
        print(f"Method One: {i}")

def method_two():
    for j in range(5):
        time.sleep(1)  # Simulating some work with a delay
        print(f"Method Two: {j}")

# Create threads
thread1 = threading.Thread(target=method_one)
thread2 = threading.Thread(target=method_two)

# Start threads
thread1.start()
thread2.start()

# Wait for threads to complete
thread1.join()
thread2.join()

print("Both methods have finished executing.")