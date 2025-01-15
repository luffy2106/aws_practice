# AWS_Practices

### 1. AWS infracstructure
- Infracstructure by regions, zone ...
- Console and services
### 2. IAM(Identity and Access Management)
- User, group and policies. All user follow the same policy in a group.
- Set up the policy by JSON file.
- Each root account can link to one IAM user. We can sign in by root user or IAM user. 
- Root user can set up the policy for IAM user but not on reverse.
- Set up MFA(2 layer authentication) for root account and user account

### 3. AWS CLI
#### How to access AWS:
- AWS management console(protected by password + MFA)
- AWS Command Line Interface (CLI): protected by access key
- AWS Software Developer Kit(SDK)-for code: Protected by access Key

To set up access key, you can set up access key to many account(root user, IAM user), just need to open file .aws/credentials:
- You will see that each profile has a presentation like [profile_name]
- when you configure profile without specify name, then the configuration will be set up in "default" profile
- Root account have additional token name "aws_session_token"
- If you want to list IAM users in your account(profile), type : aws list-users --profile [profile_name]
- aws list-users --profile will give the output of "default" profile.
- If you delete user in your account in [profile_name], then the command : aws list-users --profile [profile_name] will show the access denied error or show nothing because this time the user does not exist any more.

#### AWS CloudShell : 
To help you interact with the server without using CLI

#### IAM POLICY

A statement in an IAM Policy consists of Sid, Effect, Principal, Action, Resource, and Condition. The POLICY is used to set up permission for user

#### IAM ROLE

The POLICY is used to set up permission for user. On the other hand, ROLE is used to set up permission for the physical object(virtual machine, service ...). For example, a virtual machine need to have some permissions to interact with amazon services, or some Amazon serice to other Amazon service. Some common roles are:
- EC2 Instance Roles
- Lambda Functions Roles
- Roles of CloudFormation

##### IAM security tools
- IAM Credentials Report(account-level): A report that list all your account's users and the status of their various credentials.
- IAM Access Advisor(user-level): show the services permissions granted to a user adn when those services were last accessed.

### 4. EC2 Fundamentals

##### AWS budget setup
- You can see the summary of the bill  for the services you use.
- You can set up a budget, when the fee higher than the threshold, it will send an email to you.

##### EC2 basics

EC2 = Elastic Compute Cloud = Infrastructure as a Service. It mainly consists the capability of:
- Renting Virtual Machine(EC2). You can choose : #CPU cores, RAM, how nuch storeage space, network card, firewall rules(by choosing different type of EC2 instancs : t2.micro, t2.xlarge ...). You can configure the first launch using bootstrap script: EC2 user data(for instance, run an webserver when the instance was launch)
- Storing data on virtual driver(EBS).
- Distributing load across machines(ELB).
- Scaling the services using an auto-scaling group(ASG).

Remember, the longer you keep instance run, the more you pay. If you stop instance, AWS stop charging.

##### Security groups and classic ports
- Can be attached to multiple instances
- Locked down to a region
- It's good to maintain one separate security group for SSH access
- If your application is not accessible(time out), then it's security issue
- If your application gives a "connection refused" error, then it's an application error or it's not launched
- All inbound traffic is blocked by default.
- All outboud traffic is authorized by default.

Classic ports to know:
- 22 = SSH(Secure Shell) - log into a Linux instance
- 21 = FT(File Transfer Protocol) - upload files into a file share
- 22 = SFTP(Secure File Transfer Protocol) - upload files using SSH
- 80 = HTTP - access unsecured websites
- 443 = HTTPS - access secured websites
- 3389 = RDP(Remote Desktop Protocol) - log into a Windows instance.

##### SSH - Instance Connect

You can use SSH to access the instance server by terminal(with the key) or by the browser

##### EC2 Instance Roles Demo

You can set up the role for your EC2 instances by attaching the policy.  

### 5. EC2 Instance Storage

Overview :

EBS volumn can be used to store data of one EC2 instance(we call in root volum), it can be detached from an EC2 instance and attached to another one quickly.
If you create additional EBS volumn for your instance, you have to make this EPS volumn available for use on Linux(need to do some set up, take a look at : https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html)

You have launched an EC2 instance with two EBS volumes, the Root volume type and the other EBS volume type to store the data. Then if you terminate this EC2 instance, then the root volumn will be deleted but the EBS volumn will not be deleted.
##### EBS Snapshots

Make a backup(snapshot) of your EBS volumn at a point in time. Can copy snapshots across Region. Some feautures of EBS snapshots:
- EBS Snapshot archive and restore it later(take around 1-3 days)
- Recycle Bin for EBS Snapshots : setup rules to retain deleted snapshots so you recover them after an accidental deletion
- Initialize and recover full snapshot with no latency(cost a lot of money).

##### AMI(Amazon Machine Image)

AMI are customization of an EC2 instance
- You add your own software, configuration, OS ...
- Faster boot/configuration time because all your software is pre-packed
- AMI are built for a specific region(and can be copied across regions)
- You can launch EC2 instances from :
* A public AMI: AWS provided
* Your own AMI: you make and maintain them your self
* An AWS Marketplace AMI: an AMI someone else made(and potentially sells)

AMI process:
- Start and EC2 instance and customize it.
- Stop the instance(for data integrity)
- Build an AMI - this will also create EBS snapshots
- Launch instances from other AMIs

For example, you can run ChainLink solution in different region by creating AMI from one instance in one region(install package, configure ...), then from this AMI, lanuch another instance in another region. This approach is extremly fast because you don't have to reinstall all software and package again. 

##### EC2 instance storage

EBS volumes has limited performance, if you need high-performance hardware disk, use EC2 Instance Store. It has better I/O performance but EC2 instance storage
lose their storage if they are stopped => it's good for buffer/cache/temporary content. Also, there is a risk of data loss if hardware fails. If you use EC2 instance store, make sure you backup and replicate in somewhere.

##### EBS volumn type
- io1/io2 - Highest performance SSD : for mission-critical low-latency. Max IOPS(input/output per second): 64000
- gp2/gp3 - General SSD. Max IOPS(input/output per second): 16000
- st1(HDD): low cost HDD for frequently accessed. Max IOPS(input/output per second): 500
- sc1(HDD): lowest cost HDD for less frequently accessed. Max IOPS(input/output per second): 250

Remember that only gp2/gp3 and io1/io2 can be used as boot volumes.

##### EBS multi attach
Attach the same EBS volume to multiple EC2 instances in the same AZ. Each instance has full read & write permissions to the high-performance volume. Maximum 16 EC2 instances is attached to the same volume. You must use a file system that's cluster-aware(not XFS, EX4 ...)

##### Amazon EFS
- Managed NFS(network file system) that can be mounted on many EC2(many EC2 in different AZ can access the same NFS space)
- EFS works with EC2 instances in multi-AZ(Availibility Zone).

For example, you have EFS file system which surround by a security group, then you can have many EC2 instances i us-east-1a AZ, many EC2 instances i us-east-1b AZ and 
many EC2 instances i us-east-1c AZ. And they call all connect at the same time, to the same network file system through EFS. 

Features:
- Use cases : Content management, web serving, data sharing
- Use NFSv4.1 protocol
- Uses security groupto control access to EFS
- Compatible with Linux based AMI, not window
- EFS is a file system in linux that has standard API by default
- File system scales automatically when the system get bigger and it's pay oer use, you don't have to plan any thing in advance.

EFS performance and storage:
- EFS scale : 1000 of concurrent NFS clients
- You can set up performance mode for NFS:
* General purpose(default): latency-sensitive use cases(web server, CMS).
* MAX I/O: higer latency, highly parallel(really helpful for big data, media processing).
* Throughput mode : By default you have the bursting mode, data transfer speed is corresponding to the storage size(for example, 1TB storage is corresponding to 50mbs/s for data transfer). However, with the provisioned mode, you can set your throughput regardless of storage size, for example, you can set even 1GPB/s for ony 1 TB storage on your EFS network file system.
- You can also have setting for storage classes:
* Storage Tiers : move files after N days from EFS standard to EFS IA(in Amazon EFS file system, there are alway 2 spaces : EFS standard,to store high frequency access file and EFS IA, to store less frequency access file). For example, If you have a file which you didn't access in 60 days, then based on the storage tiers lifecycle policy, this file will be moved from EPS standard to EPS IA. It will help reduce store size and save cost.
* Availibiliry : you can set up on standard mode(multi AZ), good for deploying the product in different zone. Or you can set up  for one AZ, good for development, back up enabled by default, over 90% cost saving.

##### The difference between EBS and EFS
###### EBS volumes: 
- can be attached to only one EC instance at a time
- are locked at Availibility Zone(AZ) level
- gp2: IO inscreases if the disk size increase
- io1: can increase IO independently
- To be able to migrate an EBS volume across AZ, you have to:
* take a snapshot
* Restore snapshot to another AZ
EBS backups use IO and you shouldn't run them while your application is handling a lot of traffic.
- Root EBS volumes of instances get terminated by default if the EC2 instance gets terminated(but you can disable this function if you want), however, the EBS volumn type will not be deleted.
###### EFS Elastic File System:
- Can be monuted to 100-1000 of EC instances across different AZ. So you can use EFS to share web server, wordpress .. to different instances
- Only for Linux Instances
- EFS are more expensive, but you can leverage EFS IA for cost saving(move less used file from EFS standard to EFS IA)


### 6. AWS Fundamentals: ELB + ASG

###### High availibility and Scalability
- Scalability means that an application/system can handle greater loads by adapting. There are two kinds of scalability:
* Vertical scalability: Increasing the size of the instance/system. For example, your application runs on t2.micro, you can scale up this application to t2.large.
* Horizontal scalability: Increasing the number of instances/system for your application(Create many small EC2 instances to run in parallel instead of create a big EC2), it implies distributed system. It's easy to horizontially scale thanks to the cloud offerings such as Amazon EC2.
- High Availibility means that running your application/system in at least 2 data centers(Availibility Zones), in case one data center loss, another data center can
still run the application.

###### Elastic Load Balancing(ELB)
- Load balancer or Elastic Load Balancer are servers that forward traffic to multiple servers(EC2 instances) downstream. The idea is that your users do not know which backend instances they are connected to, they just know that they have to connect to your elastic load balancer which gives them one end point of connectivity only.

Why use a load balancer:
- Spread load across multiple downstream instances
- Expose a single point of access(DNS) to your application
- Seamlessly handle failures of downstream instances because load balancer has health check mechanisms and can understand which EC2 can not send traffic to and stop sending traffic there. 
- Encryt the request to the website by SSL(transform http to https)
- Enforce cookies(remember the information of visitor when they connect to the tool)
- Seperate public traffic from private traffic on the cloud.

The security group of EC2 insances is linked to security group of Load Balancer, so it's only accept traffic from load balancer. 

There is 4 kinds of managed Load Balancers
- Classic Load Balancer - CLB: HTTP, HTTPS, TCP, SSL 
- Application Load Balancer - ALB: HTTP, HTTPS, Websocket (don't have static IP address, it used static DNS instead, however you could place an NLB infront of an ALB)
- Network Load Balancer - NLB: TCP, TLS(secured TCP), UDP (provide both static DNS name and static IP)
- Gateway Load Balancer - GWLB: Operate at network layer.

Note that HTTP has port 80 while HTTPS has port 443.

###### 1. Classic Load Balancing(CLB)
- Support TCP(Layer 4), HTTP & HTTPS(Layer 7).
- Health checks are TCP or HTTP based.
- Fixed host name(DNS) : xxx.region.elb.amazonaws.com

You can configure the client access only by Load Balancer(you can not access directly to the IP address of EC2 instance)

###### 2. Application Load Balancer(ALB)
Prequisite : What is the difference between HTTP and Websocket:
- HTTP is unidirectional where the client sends the request and the server sends the response. Let’s take an example when a user sends a request to the server this request goes in the form of HTTP or HTTPS, after receiving a request server send the response to the client, each request is associated with a corresponding response, after sending the response the connection gets closed, each HTTP or HTTPS request establish the new connection to the server every time and after getting the response the connection gets terminated by itself. 
- WebSocket is bidirectional, a full-duplex protocol that is used in the same scenario of client-server communication, unlike HTTP it starts from ws:// or wss://. It is a stateful protocol, which means the connection between client and server will keep alive until it is terminated by either party (client or server). After closing the connection by either of the client and server, the connection is terminated from both ends. Real-time web application uses a web socket to show the data at the client end, which is continuously being sent by the backend server(client don't have to send request again then establish 3 hand shake steps to be able to get the response everytime). For e.g. in a trading website or bitcoin trading, for displaying the price fluctuation and movement data is continuously pushed by the backend server to the client end by using a WebSocket channel. 

Back to Application Load Balancer(ALB):

- Application load balancers is Layer 7 - Application Layer(HTTP, SSH, DNS ...)=> you can configure HTTP, HTTPS, SSH as an option.
- Load balancing to multiple HTTP applications across machines(target group)
- Load balancing to multiple applications on the same machine(ex: containers)
- Support for HTTP/2 and WebSocket
- Support redirect(from HTTP to HTTPS for example)
- Routing tables to different target groups:
* Routing based on path in URL(example.com/users and example.com/posts)
* Routing based on hostname in URL(one.example.com & other.example.com)
* Routing based on Query String, Headers(example.com/users?id=123&order=false)

ALB are a great fit for micro services and container-based application(example: Docker & Amazon ECS). For example, suppose we have one target group with many
EC2 instances for user application(micro service 1), and one target group with many EC2 instances for search application(micro service 2). Both 2 micro services are access by ALB which route user to these target groups based on the route that is being used in the URL 

ALB target group can be :
- EC2 instances
- EC2 tasks
- lambda functions
- IP address
ALB can route to multiple target groups and health checks are at the target group level

Application Load Balancer (v2)
Good to Know
• Fixed hostname (XXX.region.elb.amazonaws.com, example : users.region.elb.amazonaws.com, api.external.region.elb.amazonaws.com, and checkout.region.elb.amazonaws.com
• When using an Application Load Balancer to distribute traffic to your EC2 instances, the IP address you'll receive requests from will be the ALB's private IP addresses.The application servers don’t see the IP of the client directly.
- The true IP of the client is inserted in the header X-Forwarded-For
- We can also get Port (by X-Forwarded-Port) and proto(col) (by X-Forwarded-Proto)

###### 3. Network Load Balancer(NLB)

Prequisite : 
1. What is the difference between fixed IP and static IP ?
A fixed or static IP address never changes, it remains the same also when it moves or changes function. Every time the device connects and disconnects it will be using this same address. On the opposite, the dynamic IP address will change each time the device connects to the internet/network.
2. What is the difference between HTTP and TCP ?
- HTTP is work on application layer, which is used to access website.
- TCP is work on Transport layer, TCP is used as a session establishment protocol between client and server.   


- Application Load Balancer is Layer 4 - Transport Layer, end to end connection(Deal with TCP, UDP) => you can configure UDP, TCP, TLS as an option.
- High performance, can handle million request per second(much faster than ALB), check (*)
- LNP has only one static IP for on Availibility Zone(AZ) and you can assign Elastic IP to each AZ=>It's helpful if you want to explore your application with set of
static IP(example : you only allow user to connect to your application within 2 or 3 different IPs)
- The target of Network Load Balancer could be :
* EC2 instances
* Private IP address
* An Application Load Balancer. Thanks to Network Load Balancer you will have fixed IP addresses, and thanks to An Application Load Balancer, you can have all the rules 
that you have around handling HTTP type traffic.
- Health check support the TCP, HTTP and HTTPS protocol


When do you want to use NLB but not ALB?(*)
The ALB operates on layer 7, which means the ALB inspects the details of every incoming HTTP request. In contrast, the NLB works on layer 4. All the NLB cares about is forwarding the incoming TCP or UDP connection to a target. The NLB does not inspect an incoming HTTP request, for example.

Therefore, the NLB has much less work to do than an ALB. As a result, the NLB needs significantly less time to forward an incoming request. So when performance is crucial to your workload, you should consider using an NLB to reduce latency.

###### 4. Gateway Load Balancer(GWLB)
Deploy, scale and manage a fleet of 3rd party network virtual appliances in AWS.

You want Gateway Load Balancer when you want all traffic of your network to go through a firewall that you have, or an intrusion detection and prevention system,
deep packet inspection or do some payload manipulation

Story :
The user want to send traffic to your application. These traffic has to go through Gateway Load Balancer, then Gateway Load Balancer then spread that traffic across a target group of your virtual appliances. Then these virtual appliances will analyze the traffic(then firewall again or intruder detection ...), if not, they are not happy wit it, they will drop the traffic, if they are happy with it, they will send it back to the Gateway Load Balancer. Then the Gateway Load Balancer will forward a traffic all the way to your application. 

- Gateway Load Balancer operate at Layer 3(Network Layer) - IP packets
- Combines the following functions:
* Transparent Network Gateway : Single entry/exit for all traffic.
* Load Balancer : Distributes traffic to your virtual appliances.
- Use the GENEVE protocol on port 6081.

###### Elastic Load Balancer - Sticky Sessions
It is possible to implement stickiness so that the same client is always redirected to the same instance behind a load balancer.
- This works only for Classic Load Balancers and Application Load Balancers. There is a cookie to remeber the path of traffic from a user to specific EC2 and it has an expiration date that you can control. The use case for this is make sure the user doesn't lose his session data which can take some important information such as the login of the user, for example. 
- Enable stickiness may bring imbalance to the load over the backend EC2 instances. 

There are 2 type of cookies that you can have:
- Application-based cookies:
* Custom cookie: Generated by the target. Cookie name must be specified individually for each target group, use APPUSERC. Don't use AWSALB, AWSALBAPP or AWSALBTG(reseverd for use by the ELB)
* Application cookie : Generated by the load balancer. 
- Duration based cookies:
* Cookie generated by the load balancer
* Cookie name is AWSALB for ALB, AWSELB for ELB

###### Elastic Load Balancer - Cross-Zone Load Balancing
Each load balancer instance distributes evenly across all registered instances in all AZ. Ex, if you have 10 instances, 8 instances are in zone 1, 2 instances in zone 2, then each instance still get 10% of total traffic each. 

ALB alway turn on Cross-Zone Load Balancing by default, while NLB and CLB are not. 

###### Elastic Load Balancer - SSL Certificates
Prequisite: What is the difference between web server and website ?
A web server is a computer hosting one or more websites. "Hosting" means that all the web pages and their supporting files are available on that computer. The web server will send any web page from the website it is hosting to any user's browser, per user request.


- SSL certificate allow traffic between clients and your load balancer to be encrypted in transit by SSL(Secure Socket Layer)
- TLS refer to Transport Layer Security, which is a newer version of SSL
- Nowadays, TLS certificates are mainly used, but people still refer as SSL.
- SSL was attached to Load Balancer. 
- Whenever you go to the website and you see a lock(or it's start with HTTPS instead of HTTP), it means that your data was encrypted, otherwise it's not encrypted, do not put your personal info like credit card there.
- SSL certificates hava an expiration date(you set) and must be renewed.
- Nowaday, almost all websites has SSL certificate, to secure the login information of user
- Server Name Indication (SNI) allows you to expose multiple HTTPS applications each with its own SSL certificate on the same listener

SNI-Server Name Indication
- SNI solve the problem of loading multiple SSL certificate onto one web server(to serve multiple websites)
- It require the client to indicate the hostname of the target server in the initial SSL handshake, the server will then find the correct certificate, or return the default one. 
- Only work for ALB,NLB and CloudFront.

To sum up:
- CLB : support only one SSL certificate
- ALB : support multiple SSL certificate for different host name(by SNI)
- NLB : support multiple SSL certificate for different host name(by SNI)

###### Connection Draining
Connection Draining refer to the time finish on-going request while the instance is de-registering or unhealthy(can be set between 1-3600s, should be set to low value if the request is short). In this duration, request sending to EC2 instance which is  de-registering also be stopped. 

Feature naming(how it call):
- for CLB : It is called connection Draining. 
- for ALB & NLB: It is called Deregistration Delay.

###### Auto Scaling Group(ASG)
In real-life, the load on your websites and application can change(the # users, database ...). So the goal of an Auto Scaling Group(ASG) is 
- To scale out(add EC2 instances) to match an increase load.
- To scale in(remove EC2 instances) to match a decreased load.
- Ensure the minimum and maximum number of EC2 instances running.
- Automatically register new instances to a load balancer.

Auto scaling group can be combined with ELB to distribute traffic to EC2 instances. ELB can check the health of EC2 instances and notify ASG to terminater an EC2 instance
if it finds out that this EC2 instance is unhealthy.

Auto Scaling Template is set up by a Launch Template.

It is possible to scale an ASG based on CloudWatch alarm, based on some metric such as: Average CPU(If the average CPU for the whole ASG is too high, CloudWatch alarm will be trigger to add more EC2 instances).

Note: The Auto Scaling Group can't go over the maximum capacity (you configured) during scale-out events.

###### Auto Scaling Group - Scaling Policies
1. Dynamic Scaling policies:
- Target Tracking, Ex : I want the average ASG CPU to stay around 40%
- Simple/Step Scaling, Ex : When a CloudWatch alarm is triggered(ex CPU > 70%), then add 2 units and When a CloudWatch alarm is triggered(ex CPU < 30%), then remove unit
- Scheduled actions : Anticipate a scaling based on usage pattern. Ex : increase the min capacity to 10 at 5 P.M on Fridays.
- Predictive scaling : continously forcast load(using machine learning) and schedule scaling ahead. 

Metrics to scale on
- CPU untilization : if CPU usage is too high, add more instance
- RequestCountPerTarget : to make sure the number of requests per EC2 instances is stable. For example you want EC2 instance operate at an optimal request of 1000 per target at a time.
- Average network in/out (if your app is network bound)
- Custome metric : you can set up any rules using CloudWatch.
2. Scaling cooldowns 
- After a scaling activity happens, you are in the cooldown period(default 300 seconds)
- During cooldown period, ASG can not launch or terminate additional instances
=> Need to use predefined AMI to reduce configuration time in order to be serving request fasters and reduce the cooldown period.

### 8. AWS Fundamentals: RDS + Aurora + ElasticCache

###### Amazon RDS 
RDS - Relational Database Service allows you to create databases in the cloud that are managed by AWS. The database engine are managed by AWS are : 
- Postgres
- MySQL
- MariaDB
- Oracle
- Microsoft SQL Server
- Aurora (AWS Propriety database)

Advantage over using RDS versus deploying DB on EC2:
- Automated provisioning : deliver computing capacity on-demand without manual intervention
- Continous backups and restore to specific timestamp(Point in Time Restore)!
- Auto scale up when RDS detects you are running out of free databased storage.

RDS Read Replicas for read scalability
- For each RDS DB instance, 5 Read Replica can be created(can be within AZ, CrossAZ or Cross Region)
RDS Read Replicas - Use Cases
- Suppose there is Production Application which is plug into your RDS DB instance. Suppose that data analyst team want to do some analyze on top of your data, so the create a reporting application to plug into your RDS DB instance. In this case, it could lead to overload because one DB instance was read from 2 application. So instead, we create a replica of the original DB instance and let the reporting application plug into this replica. 
- Read Replica is only for read(SELECT only, not for INSERT, UPDATE, DELETE).

RDS Read Replicas - Network Cost
- There is a network cost when data goes from one AZ to another, except Read Replicas
- For RDS Read Replicas within the same region, you don’t pay fee, but if they are in different region, you have to pay

You can set up RDS as multi AZ(mainly used for Disaster Recovery)
- Application connect to RDS DB through one DSN name only. Suppose there are many RDS DB instance in your database(one in AZ A and one in AZ B), one of them is assigned as master DB and the application read and write to this master DB, the database in master DB and other DB is synchronize. If the master DB die, another DB will be elected as a master DB automatically and your application will do read/write to this master DB.

How to make RDS from Single-AZ to Multi-AZ=>just need to click on "modify" for the database and enable Multi-AZ. Your RDS DB will be come master and there is a Standby DB is replicate.

###### Amazon Aurora
Aurora is better than RDS for the following reasons:
- Aurora is “AWS cloud optimized” and claims 5x performance improvement over MySQL on RDS, over 3x the performance of Postgres on RDS
- Aurora storage automatically grows in increments of 10GB, up to 128 TB
- Aurora can have 15 replicas while MySQL has 5, and the replication process is faster (sub 10 ms replica lag)
- Aurora costs more than RDS (20% more) – but is more efficient

###### RDS and Aurora Security
- At rest encryption
- In-flight encryption

###### ElaticCache
Prequisite :
- In-memory cache :  Memory caching (often simply referred to as caching) is a technique in which computer applications temporarily store data in a computer's main memory (i.e., random access memory, or RAM) to enable fast retrievals of that data.
- Redis : can be used with streaming solutions  as an in-memory data store to ingest, process, and analyze real-time data with sub-millisecond latency
- Memcache : Although Redis and Memcache are both easy to use and offer high performance, there are important differences to consider when choosing an engine. Memcached is designed for simplicity while Redis offers a rich set of features that make it effective for a wide range of use cases.
- Sharding : is a type of database partitioning that separates large databases into smaller, faster, more easily managed parts
ElastiCache is to get managed Redis or Memcached
The difference between Redis and Memcached(really important, check slide )

###### ElaticCache Strategy
Caching design pattern
- Lazy Loading/Cache-aside/Lazy population : for reading
- Write Through: for writting. Is usually combined with Lazy Loading as targeted for the queries or workloads that benefit from this optimization.

###### ElaticCache Redis Cluster Modes

There are 2 types of ElasticCache Replicaton you can have for Redis
- Cluster mode disabled : data in only one shard. Each shard has a primary and up to 5 replica nodes. Multi AZ
- Cluster mode enabled : data is partitioned across many shards. Each shard has a primary and up to 5 replica nodes. Multi AZ as long as primary node has to be on the same AZ with its replica nodes.

### 9. Route 53
Route 53 act like an DNS and we can update DNS records by ourself.

Record types of Route 53
- A : maps a hostname to Ipv4. Ex : www.example.com -> 1.2.3.4
- AAAA : maps a hostname to Ipv6. 
- CNAME : maps a hostname to another hostname. Then the (final)target hostname is a domain name which must have an A or AAAA record. You can' create a CNAME record for the top node of a DNS namespace. Ex : you can't create for example.com but you can create for www.example.com
- NS : Name Servers for the hosted Zone(which can respond to the DNS queries for your hosted zone and control how traffic is routed for a domain).
There are 2 types of hosted zone:
* Public Hosted Zone : contain records that specify how to route traffic on the internet (public domain names).
* Private Hosted Zones : contain records that specify how you route traffic within one or more VPCs (private domain names) application1.company.internal

If you want your VPC connect to internet, you need to create a Gateway with its own route table.


Routing policy can be routed by policy such as :
- Weight : request will be sent to EC2 instance which has higher weight.
- Latency : request will be sent to EC2 instance which has the least latency(Latency is based on traffic between users and AWS regions)
- Health Check : request will be sent to EC2 instance which has a good status of health check.
- Fail over : Amazon Route 53 has one mandatory health check with one EC2 instance(primary), when this EC2 instance is unhealthy, Route 53 will automatically fail over(connect) to second EC2 instance. 
- Geolocation : The routing based on the user location(ex :continent, country, US state ...). For example, people in Germany will go to EC2 instance in Germany ... Use cases : website localization, restrict content distribution, load balancing ..., can be associated with Health Checks. 
- Geoproximity : The traffic will go more to the resources(AWS resources, Non-AWS resources) which has higher bias. Use cases : when you want to shift traffic to a specific region, then you increase bias on the resource of this specific region.  
- Traffic flow : the traffic will be routed by the diagram you designed(the diagram can use many policy such as: weight, latenc, health check ...)
- multi value : can have up to 8 healthy records are returned for each Multi-value query. It can be associated with Health Checks(return only values for healthy resources)


If you buy your domain on a 3rd party registra, you can still use Route 53 as the DNS service provider. But every Domain Registra usually comes with some DNS features.


#### 11. Bucket S3 introduction
Use cases:
- Back up and storage

Main features:
- Bucket policy
- S3 versioning
- S3 replication
- S3 storage classes(different in term of retrivial fee and retrivial speed ...)



#### 10. VPC Fundamentals 

VPC = Virtual Private Cloud : private network to deploy your resources(regional resources)

Main features:
- Subnets : public subnet and private subnet
- Internet Gateway
- Nat Gateway
- Security groups
- Network Access Control List(NACL)
- VPC Flow Logs
- VPC Peering
- VPC Endpoints
- Site to site VPN & Direct connect(DX)


#### 16. ECS, ECR and Fargate - Docker in AWS

ECS - Amazon Elastic Container Service(Amazon’s own container platform). 
ECR - Amazon Elastic Container Registry
ECS - Amazo Elastic Container service (similar to docker volume)
There are 2 launch types of ECS:
- EC2 launch type : Need to provide EC2 and each EC2 Instance must run the ECS Agent to register in the ECS Cluster
- Fargate launch type : No need to provide EC2, just create tasks and AWS runs ECS tasks based on the CPU/RAM you need
 
ECS service auto scaling : automatically increase/decrease the desired number of ECS tasks.

ECS Rolling updates : update tasks version based on the capacity

ECS tasks can be:
- Invoked by Event Bridge
- Invoked Event Bridge schedule
- Handle by SQS queue

ECS tasks definition:
- Task definition are metadata in JSON form to tell ECS how to run a Docker container : Image Name, Port Binding for Container and Host, 
memory and CPU required, environment variables, networking information, IAM Role, logging configuration. 
- You can define up to 10 containers in a Task Definition

ECS task definition:
ECS - Loading Balancing(EC2 Launch Type) : each task map to dynamic IP(if you define only the container port in the task definition)
ECS - Loading Balancing(Fargate) : each task has unique private IP(only definie the container port, host port is not applicable)

ECS tasks definition components:
- One IAM role per task definition(definied in task definition)
- Environment variables :
    * Fixed by URL
    * store in SSM parameter store and fetch from it(sensitive values such as : API keys, shared configs ...)
    * store in Secrets Manager store and fetch from it : DB passwords)
    * load files from S3 bucket
- Data volumes : 
    * share data between multiple containers in the same Task Definition

EFS is a network attached storage, while EBS is a block level storage. EFS is suitable for applications requiring shared file storage, while EBS is better suited for applications requiring low latency access to a single instance.

ECS - Task Placements(only valid for ECS with EC2, not for Fargate): Task placement strategy and constraints to determine where to place containerds to the appropriate EC2 instance(depend on CPU memory and available ports)

ECS Task Placement Process
ECS Task Placement Strategies(can mix them together):
- Binpak : over EC2 instance one by one
- Random : randomly
- Spread(evenly)

ECS Task Placement Constraints:
- distinctInstance : Tasks are placed on a different EC2 instance
- memberOf: placed on EC2 instances that satisfy a specified expression(ex: place only on EC2 t2: t2.*)

ECS -  Elastic Container Registry : 
- Store and manage Docker iamges on AWS
- There are private and public repo(Amazon ECR Public Gallery)
- Access is controlled through IAM

EKS - Elastic Kubernetes Service 
- A way to launch managed Kubernetes clusters on AWS
- Kubernetes is open-source system to automatic deployment, scaling and management of containerized application
- Use case: if your company is already using Kubernetes on-premises or in another cloud, and wants to migrate to AWS using Kubernetes
- EKS supports EC2 if you want to deploy worker nodes or Fargate to deploy serverless containers
- Kubernetes is cloud-agnostic (can be used in any cloud – Azure, GCP…)
- For multiple regions, deploy one EKS cluster per region
- Collect logs and metrics using CloudWatch Container Insights

Node Types:
- Managed Node Groups : Created and manage Nodes(EC2 instances) for you, and nodes are part of an ASG managed by EKS
- Self-managed nodes : Node created by you and registered to the EKS cluster and managed by ASG
- AWS Fargate : no node managed

The difference between EFS volume and EBS volume:
EFS is a network attached storage, while EBS is a block level storage. EFS is suitable for applications requiring shared file storage, while EBS is better suited for applications requiring low latency access to a single instance.


#### AWS Monitoring & Audit: CloudWatch, X-Ray and CloudTrail
1. AWS CloudWatch
- AWS CloudWatch Metrics
- CloudWatch Logs
- CloudWatch Alarm:
• Stop, Terminate, Reboot, or Recover an EC2 Instance
• Trigger Auto Scaling Action
• Send notification to SNS (from which you can do pretty much anything)
- CloudWatch Events

2. Amazon EventBridge: (EventBridge is the next evolution of CloudWatch Events)
Amazon EventBridge is an event bus that works with services from many different AWS vendors, as well as with your custom applications. EventBridge takes event data from these sources and routes them to targets for immediate use. It also collects data from all sources and provides a unified view to analyze and act on the data.

3. X-Ray

Visual analysis of our applications, eay to debug(where and how many request failed ...)
- Troubleshooting performance(bottlenecks)
- Understand dependencies in a microservice architecture
- Find errors and exceptions

AWS X-Ray Leverages Tracing : an end-to-end way to follow a "request"

3.1 How to enable it ?

3.1.1 Your code must import the AWS X-Ray SDK and it should be modified. It will:
- Call AWS services
- HTTP/HTTPS requests
- Database Calls (MySQL, PostgreSQL,, DynamDB)
- Queue calls(SQS)

3.1.2 Install X-Ray daemon or enable X-Ray AWS Intergration

3.2 X-Ray Instrumentation in your code
3.3 X-Ray concepts
• Segments: each application / service will send them
• Subsegments: if you need more details in your segment
• Trace: segments collected together to form an end-to-end trace
• Sampling: decrease the amount of requests sent to X-Ray, reduce cost
• Annotations: Key Value pairs used to index traces and use with filters
• Metadata: Key Value pairs, not indexed, not used for searching
3.4 X-Ray Sampling Rules
Control the amount of data that you record
3.5 X-Ray API
- Read
- Write
3.6 X-Ray with Elastic Beanstalk
AWS Elastic Beanstalk platforms include the X-Ray daemon, You can run the daemon by setting an option in the Elastic Beanstalk console
or with a configuration file (in .ebextensions/xray-daemon.config)

3.7 Integrate ECS + X-Ray
- X-Ray Container as a Saemon
- X-Ray Container as a "Side car"
- X-Ray Container as a "Side car" inside Fargate Task

3.8 CloudTrail 
- Get an history of events/API calls made within your AWS account by : Console, SDK, CLI, AWS services
- Can put logs from CloudTrail into CloudWatch Logs or S3
- Can apply for all regions
- If a resource is deleted in AWS, investigate CloudTrail first!(who did what and when)

CloudTrail Events
- Management Events
- Data Events
- CloudTrail Insights Events


#### Understand lambda function



# Questions
#### What is the difference between IAM role and IAM policies?

IAM (Identity and Access Management) roles and IAM policies are both important components of AWS IAM, but they serve different purposes.

IAM Role:
- An IAM role is a set of permissions that determine what actions an AWS service or resource can perform on your behalf.
- Roles are not associated with a specific user or group, but rather with a trusted entity such as an EC2 instance, Lambda function, or another AWS service.
- Roles are used to grant temporary permissions to entities that assume the role, allowing them to access AWS resources securely without requiring long-term credentials like access keys.

IAM Policy:
- An IAM policy is a JSON document that defines permissions and access control rules for individual users, groups, or roles within AWS.
- Policies can be attached to IAM users, groups, or roles to define what actions they can perform and which resources they can access.
- Policies can be created and managed independently from the IAM entities they are attached to, making it easier to manage permissions across multiple users and resources.
- Policies can be used to grant or deny permissions for specific actions, resources, or services.

In summary, IAM roles are used to grant temporary permissions to trusted entities, while IAM policies are used to define permissions for individual users, groups, or roles. Roles are often used in scenarios where AWS services or resources need to access other AWS resources on your behalf, while policies are used to define fine-grained access control for specific IAM entities.

















