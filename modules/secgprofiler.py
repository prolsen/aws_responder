import json
import boto3
from Utils.Helpers import Utilities
from botocore.exceptions import ClientError

class Module(object):

    def __init__(self, dryrun, instanceids, sgids, vpcids, usernames, \
                            accesskeyids, values):
        
        self.dryrun = dryrun

    def execute(self):
        '''
        Security Group Basics/Limits:
        Security groups per network interface - 5
        Security groups per VPC (per region) - 500
        Inbound or outbound rules per security group - 60

        Ref. the url for specifics.
        https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html

        Network Interface Basics:
        Every instance in a VPC has a default network interface, called the primary
        network interface (eth0). You cannot detach a primary network interface from
         an instance. You can create and attach additional network interfaces.
        Limits on ENIs:
        https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI
        '''

        ec2_client = boto3.client('ec2')

        dryrun = Utilities().str_to_bool(self.dryrun)

        instances = Utilities().yieldInstances(dryrun)

        enis = self.yieldENIs(instances)
        ingress_dict = self.enumIngresList(enis)

        ip_perm_list = self.processIPPerms(ingress_dict)

        print(self.processSGs(ip_perm_list))


    def processSGs(self, ip_perm_list):
        sglist = []

        for e in ip_perm_list:

            sgs = dict(ENI=e[0], InstID=e[1], PublicIP=e[2], \
                        PrivateIP=e[3], SGId=e[4], FromPort=e[5], \
                        Protocol=e[6], ToPort=e[7], CidrRanges=e[8]
                        )
            sglist.append(sgs)

        return(json.dumps(sglist, indent=4))

    def processIPPerms(self, ingress_dict):
        ipPermList = []

        for k, v in ingress_dict.items():
            for i in v[4]:
                if 'FromPort' in i:
                    fromport = str(i['FromPort'])
                if 'ToPort' in i:
                    toport = str(i['ToPort'])
                if 'IpRanges' in i:
                    try:
                        ipv4_ranges = str(i['IpRanges'])
                    except IndexError:
                        ipv4_ranges = 'None'
                if 'Ipv6Ranges' in i:
                    try:
                        ipv6_ranges = str(i['Ipv6Ranges'])
                    except IndexError:
                        ipv6_ranges = 'None'
                if i['IpProtocol'] == '-1':
                    proto = 'All'
                else:
                    proto = i['IpProtocol']

                ipPermList.append([k, v[0], v[1], v[2], v[3], fromport, proto, toport, ipv4_ranges, ipv6_ranges])

        return(ipPermList)

    def enumIngresList(self, enis):
        ec2 = boto3.resource('ec2')

        ingressDict = {}

        for k, v in enis.items():
            for sg_id in v[3]:
                sg_info = ec2.SecurityGroup(sg_id)
                # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.ip_permissions
                ip_permissions = sg_info.ip_permissions
                ingressDict[k] = v[0], v[1], v[2], sg_id, ip_permissions
        
        return(ingressDict)
                

    def yieldENIs(self, instances):
        
        eniDict = {}

        for x in instances:
            for i in x['NetworkInterfaces']:
                try:
                    public_ip = i['PrivateIpAddresses'][0]['Association']['PublicIp']
                except KeyError:
                    public_ip = 'No Association'
                try:
                    private_ip = i['PrivateIpAddresses'][0]['PrivateIpAddress']
                except KeyError:
                    private_ip = 'No Association'

                sec_groups = [x['GroupId'] for x in i['Groups']]
                eniDict[i['NetworkInterfaceId']] = x['InstanceId'], public_ip, private_ip, sec_groups
        
        return(eniDict)