# Lab 10
[Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repo and clone it to your machine to get started!

## Team Members
- Carl Campos

## Lab Question Answers

Question 1: 

Answer: If the processing task is computationally intensive, it would be better to offload the tasks to my local PC because it would process these tasks much faster than the limited memory and processing power of my RPi. Conversely, it would be better to process the tasks on the RPi if the task requires real-time processing, or if it is inconvenient to offload the processses to my PC.

Question 2:

Answer: The reason why we need to join the thread here is that we want to make sure that the offload_process1() function has finished executing and updated the value of data1 before we proceed to use data1 in the subsequent processing.

Question 3:

Answer: The functions process1() and process2() are executing concurrently, not in parallel. If they were executing in parallel, process1() and process2() would execute on a different processor or different core at the same time.

Note: I used the provided article to answer this question.

Question 4:

Answer: For the task we are given, offloading both processes would be the best offloading mode in terms of speed. As mentioned, our Rpi's have limited processing power and memory. Offloading the processing tasks when convenient or when we need to process these tasks as fast as possible, it makes the most sense to offload both tasks. If speed isn't a concern, then offloading just one process off the Rpi would be sufficient.

Question 5:

Answer: The worst offloading mode would be performing all tasks locally on the Rpi. This would be the worst in terms of speed and efficiency. It would always be beneficial to offload at least some of the processing load. However, for simple tasks, offloading locally would be ok even if it is the least efficient.

Question 6:

Answer: One recent example in a real-world setting is machine learning. This requires a lot of computational power to process a large amount of data. Offloading some of the tasks that would process a large amount of data would be neccesary.