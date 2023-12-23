import aws_cdk as core
import aws_cdk.assertions as assertions

from ec2_test.ec2_test_stack import Ec2TestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ec2_test/ec2_test_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Ec2TestStack(app, "ec2-test")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
