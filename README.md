## Problem and Objectives
The next solution was created to analyze latency in a productive data center with a very restrictive scenario. Considering that the networks assets and the Operative systems are all productives, we have to face the problem without the oportunity to install any software.

It's important to clarify that we want to measure latencies between hosts and define witch assets or zones generate the latency. Because of that, we meassure latency throught days in diferent zones and with diferent hosts.

Constraints:
* We haven't an observability platform with proxyes or agents.
* We can't install or execute thrith party software in productive hosts

Facts:
* We decided to use native ping executable
* We have to deal with a lot of information
* We need to recognize diferent sources and destinations
* We need to calculate averages and maximuns by source, destiny, day, hour and minute
* Will be a nice to have if we could graph the latency by packet in the time

Connected with the first two facts or definitions, we build a realy simple bash and bat script or command to execute the ping, concatenating a timestamp by packet and defining the source IP. Then, we append all the information in a txt file.
After the execution we noticed that the script could be better if also appended the source IP but, with some  pandas lines we could solve the issues.

```
# !/bin/bash
ping xxx.xxx.xxx.xxx | xargs -n1 -i bash -c 'echo `date +%F\ %T`" {}"'>>/tmp/SrcIP_DstIP.txt
```

## Data source structure and details
* Output filename:
"SrcIP_DstIP.txt (ie: xxx.xxx.xxx.xxx_xxx.xxx.xxx.xxx.txt)"
* Data:
"2023-08-02 20:23:46 64 bytes from 10.70.128.75: icmp_seq=0 ttl=255 time=0 ms"
* Details: every time that the script start, a line without the structure previusly defined, was writed to the file, then, we need to recognize that line and erase it.

## Procesing files
As I said before, we have to deal with a lot of data. Then we decided to read, prepare and analize that data with the Python library Pandas. 
We use Colab as IDE and runtime environmen.
