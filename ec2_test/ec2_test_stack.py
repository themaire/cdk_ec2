from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    # aws_sqs as sqs,
)
from constructs import Construct

class Ec2TestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        vpc = ec2.Vpc(self, "ec2VPC",
            # 'IpAddresses' configures the IP range and size of the entire VPC.
            # The IP space will be divided based on configuration for the subnets.
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/21"),

            # 'maxAzs' configures the maximum number of availability zones to use.
            # If you want to specify the exact availability zones you want the VPC
            # to use, use `availabilityZones` instead.
            max_azs=2,

            # 'subnetConfiguration' specifies the "subnet groups" to create.
            # Every subnet group will have a subnet for each AZ, so this
            # configuration will create `3 groups × 3 AZs = 9` subnets.
            subnet_configuration=[ec2.SubnetConfiguration(
                # 'subnetType' controls Internet access, as described above.
                subnet_type=ec2.SubnetType.PUBLIC,

                # 'name' is used to name this particular subnet group. You will have to
                # use the name for subnet selection if you have more than one subnet
                # group of the same type.
                name="Ingress",

                # 'cidrMask' specifies the IP addresses in the range of of individual
                # subnets in the group. Each of the subnets in this group will contain
                # `2^(32 address bits - 24 subnet bits) - 2 reserved addresses = 254`
                # usable IP addresses.
                #
                # If 'cidrMask' is left out the available address space is evenly
                # divided across the remaining subnet groups.
                cidr_mask=24
            ), ec2.SubnetConfiguration(
                cidr_mask=24,
                name="virtMachine",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            )
            ]
        )
        vpc.add_flow_log("FlowLog")

        igw_id = vpc.internet_gateway_id

        my_security_group = ec2.SecurityGroup(self, "SecurityGroup",
            vpc=vpc,
            description="Allow ssh access to ec2 instances",
            allow_all_outbound=True
        )
        my_security_group.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(22), description="allow ssh access from the world")

        key_pair = ec2.CfnKeyPair(self, "KeyPair",
            key_name="defaultMacMiniKeyPair",
            public_key_material="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC0q1R8HcDI1xWciWHL6OMhcXao7pD4DBmDwopkWUzvWU9eDGf32mYzavjcxbFGXu8uu+3BnDxp9Ijp+Wa48gQYpn7EFi/wQccPp8hY2/ZURRbF8xkByhh2M2D5+umCSKaVpOUH+vuFo+ERjgDzH1hMtkO1v62qqce+r2ww9DNPwgyvcFXnpKW8KGYRDrfDN/eLr8ZfxxED6nXkA0Pwrz0quW8Q+Qg/8A+wyaJ78r2QGUNRZTxVcRaZTfgPeGIdjfhzyVPg+zc8EWEyde2/8vZKWbFdLZ+UcVqpfpdjWQtzMCMJ5kyWiMDVHINCEzHWGx8I36C8H9tkpjuJ1zgP0ihn nico@macmini.local"
        )
        ec2.Instance(self, "LatestAl2023",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2()
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Ec2TestQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
