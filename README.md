threads-play
============

playing around with threads

Write a simulator for a HeartBeat Monitoring System to monitor the health of a large number of
machines based on the following description. (We have proposed a way of simulating this at the
end of this problem. You can use reasonable alternatives.)
a. when the program starts, it takes as input 'N' (the number of machines), 'f' (percentage
of machines that will fail every 5 seconds), and 't' (number of seconds taken by a failed machine
to recover)
b. the program provides a shell where we can enter certain commands (listed below); the
program only terminates when we enter the command 'quit'
c. your program should support the following commands: (1) add_machines m_1, m2,
..., (2) remove_machines m_1, m2, ..., (3) is_machine_alive m_1, prints 'True', 'False', or
'machine not present', (4) num_machines_alive, prints the number of machines that are alive,
(5) failure_trend, prints a list where each element is the number of machines that were alive
based on a probe done every second (e.g., 27 27 25 22 27 32 shows there were 27 machines
alive at the 1st second, 25 at the 3rd second, etc.)

