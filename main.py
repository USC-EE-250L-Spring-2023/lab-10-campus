import time
import numpy as np
from typing import List, Optional

import threading
import pandas as pd
import requests
import plotly.express as px

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """Looks at a list of inputs and finds the largest prime number for each element."""
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """Looks at a list of inputs and finds the largest perfect square for each element."""
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """Compute the mean difference between each list in process1 and process2."""
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://127.0.0.1:5000'

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        data1 = None
        def offload_process1(data):
            nonlocal data1
            response = requests.post(f"{offload_url}/process1", json=data)
            data1 = response.json()
        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        data2 = None
        def offload_process2(data):
            nonlocal data2
            response = requests.post(f"{offload_url}/process2", json=data)
            data2 = response.json()
        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1 = process1(data)
        thread.join()
    elif offload == 'both':
        data1 = None
        data2 = None
        def offload_both(data):
            nonlocal data1, data2
            response1 = requests.post(f"{offload_url}/process1", json=data)
            data1 = response1.json()
            response2 = requests.post(f"{offload_url}/process2", json=data)
            data2 = response2.json()
        thread = threading.Thread(target=offload_both, args=(data,))
        thread.start()
        thread.join()

    ans = final_process(data1, data2)
    return ans 

def main():
    # Run the program 5 times for each offloading mode, and record the total execution time
    results = {
        'local': [],
        'process1': [],
        'process2': [],
        'both': []
    }

    # Run the program 5 times for each offloading mode, and record the total execution time
    for i in range(5):
        start_time = time.time()
        run()
        end_time = time.time()
        results['local'].append(end_time - start_time)

        start_time = time.time()
        run(offload='process1')
        end_time = time.time()
        results['process1'].append(end_time - start_time)

        start_time = time.time()
        run(offload='process2')
        end_time = time.time()
        results['process2'].append(end_time - start_time)

        start_time = time.time()
        run(offload='both')
        end_time = time.time()
        results['both'].append(end_time - start_time)

    #   Compute the mean and standard deviation of the execution times
    mean = {k: np.mean(v) for k, v in results.items()}
    std = {k: np.std(v) for k, v in results.items()}
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference
    dataFrame = pd.DataFrame({'mean': mean, 'std': std})

    # Make sure to include a title and x and y labels
    fig = px.bar(dataFrame, y='mean', error_y='std', color=dataFrame.index)
    fig.update_layout(title='Execution time for offloading modes', xaxis_title='Offloading mode', yaxis_title='Execution time (s)')

    fig.write_image('makespan.png')

    print(dataFrame)


    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()