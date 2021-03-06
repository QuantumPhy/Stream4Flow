## Host statistics

### Description
An application for computing statistics for all hosts in network. Computed statistics for each host in each window are following:
- **Basic Characteristics**: sum of flows, packets and bytes
- **Port Statistics**: number of distinct destination ports
- **Communication Peers**: number of distinct communication peers
- **Average Flow Duration**: average duration of flows
- **TCP Flags Distribution**: number of each individual TCP flags 

### Usage
- General:
 
`  host_stats.py -iz <input-zookeeper-hostname>:<input-zookeeper-port> -it <input-topic>  -oz <output-hostname>:<output-port> -ot <output-topic> --ln <CIDR network range> -w <window duration> -m <microbatch>`

- Stream4Flow example (using network range 10.10.0.0/16):

`/home/spark/applications/run-application.sh /home/spark/applications/host_statistics/host_stats.py -iz producer:2181 -it ipfix.entry -oz producer:9092 -ot host.stats -ln "10.0.0.0/24" -w 10 -m 10`


## Top N Host statistics

### Description
An application for collecting the top N characteristics for all hosts, particularly:

- **Top N destination ports**: ports of the highest number of flows on given ports from each source IP
- **Destination IPs**: destination IP addresses with the highest number of flows from each source IP
- **HTTP Hosts**: destination HTTP addresses with the highest number of flows for each source IP

## Usage
- General:

`top_n_host_stats.py --iz <input-zookeeper-hostname>:<input-zookeeper-port> -it <input-topic> -oz <output-zookeeper-hostname>:<output-zookeeper-port> -ot <output-topic> -n <CIDR network range> -wd <window duration> -ws <window slide> -c <count of top_n>
`

- Stream4Flow example (using network range 10.10.0.0/16):

`/run-application.sh statistics/hosts_statistics/spark/application_template.py -iz producer:2181 -it ipfix.entry -oz producer:9092 -ot results.output -n 10.10.0.0/16 -wd 10 -ws 10 -c 10`
