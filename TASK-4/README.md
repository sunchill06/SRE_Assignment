---------------------------------------------------------------------------------------------------------------
SRE Assignment - TASK 4 - AWS highly available 3-tier architecture
---------------------------------------------------------------------------------------------------------------

The user of the application initiates traffic from a browser or mobile device and is taken to the Amazon's DNS Service i.e. Route 53.
Route 53 then redirects the request to relevant ALB endpoint, which then further distributes the traffic across multiple AWS EC2 instances.
This architecture diagram depicts two availability zones and having 1 public subnet each. Public Subnet in AZ1 serves the purpose for NAT Gateway
or NAT Instance whereas Public Subnet 2 is hosting Bastion host.

The Internet facing ALB then sends the requests to instances in Web tier group of Private Subnets which is under an Auto scaling group to cater high availability.
Any backend requests from these Web tier instances is passed onto App Tier instances (again in Private Subnets). This tier is also under Auto scaling group.

Multi-AZ RDS deployment is used in the database tier. Database instances are only allowing incoming tier on a specific port, 3306 in this case for MySQL DB.

---------------------------------------------------------------------------------------------------------------

AWS Services being used:

1. Route 53: DNS Service from AWS. This is a managed AWS service which is highly available. This can be used for domain registration, DNS routing and health check as well.
Route 53 allows you to create record sets for your resources e.g. ALBs and then can resolve them and route traffic to them on various policies, failover, latency routing are to name a few.

2. VPC: Virtual private cloud for creating a virtually isolated network in AWS's infrastructure. This can then be used to launch various AWS resources like EC2, RDS etc.
   Customer has to make sure that he secures his resources within VPC using concepts like Security groups, NACLs etc.

3. RDS: AWS RDS is a highly scalable and available database and support various flaviours like MySQL, PostgreSQL, Oracle etc. Its Multi-AZ deployment feature
   makes it a perfect candidate for high availability. AWS RDS Read-replicas feature also makes it easy to scale. AWS RDS also comes with build-in monitoring
   and backup solutions for database instances. 
   
4. CloudFront: This is Amazon's content delivery service which can service static, dynamic contents from various sources like ELBs, S3, EC2 etc. This improves
   the customer's experience a lot as it speeds up the content delivery via its several edge locations. This can also be used for S3 Transfer acceleration.

5. S3: AWS Simple Storage service is a managed AWS service which comes with features like durablity, scalibility, availability etc. This is an unlimited object
   storage, which can be used to store static contents like images/videos for any website or application. This is quite cheap as compared to in house storages.

AWS Components being used:

1. Internet Gateway (IGW): IGW assits communication between instances in VPC and internet. It also supports this for instances in Private Subnets via NAT gateways.
   Overall, for this communication to happen, route table of the subnet should mention a route to IGW and your VPC should be attached to an IGW.
   
2. NAT Gateway: NAT GW allows instances in the private subnet to talk to the internet for purposes like downloading some packages. However, inbound connection 
   from internet to private subnet instances is not allowed. This is a managed service. Route table of the NAT Gateway sends internet specific traffic to IGW and
   instances in private subnet update their route tables to send internet directed traffic to NAT gateway.
   
   Note: NAT Instances can also be used for this purpose. But this is a normal EC2 instance and customer has to be manage this.
   
3. Security Groups: This is like a virtual firewall for individual instances or subnets to allow traffic to/from the instances.

4. Bastion Hosts: Bastion host is an EC2 instance only but with the purpose of secure access to your infrastructure or private subnets over internet. Security Groups
   in bastion should only allow ingress to specific or known CIDR ranges, also only allowing port 22 for linux instances is highly recommened.
---------------------------------------------------------------------------------------------------------------
