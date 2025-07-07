---
title: Terraform Deployment
layout: page
parent: AWS Infrastructure
nav_order: 1
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
## Terraform Deployment 
1. Download the Terraform configuration package from GitHub. Make sure you go through the release page and see what's included in
the current release on [CDCgov/NEDSS-Infrastructure](https://github.com/CDCgov/NEDSS-Infrastructure/releases)
2. Open bash/mac/cloudshell/powershell and unzip the current version file downloaded in the previous step named nbs-infrastructure-
vX.Y.Z zip.
3. Create a new directory with an easily identifiable name e.g <nbs7-mySTLT-test> in /terraform/aws/ to hold your environment specific
configuration files
4. Copy terraform/aws/samples/NBS7_standard to the new directory and change into the new directory (Note: the samples directory
contains other options than “standard”, view the README file in that directory to chose most appropriate starting point)
```bash
cp -pr terraform/aws/samples/NBS7_standard terraform/aws/nbs7-mySTLT-test
cd terraform/aws/nbs7-mySTLT-test
```
**NOTE**: Before editing **terraform.tfvars** and **terraform.tf** files below, you may reference detailed information for each TF module under the
“terraform/aws/app-infrastructure” in a readme file in each modules directory. Do not edit files in the individual modules.
5. Update the terraform.tfvars and terraform.tf with your environment-specific values by following the instructions [here](https://github.com/CDCgov/NEDSS-Infrastructure/blob/main/terraform/aws/samples/NBS7_standard/README.md)
6. Review the inbound rules on the security groups attached to your database instance and ensure that the CIDR you intend to use with your NBS 7 VPC (modern-cidr) is allowed to access the database.
    - a. For e.g if the modern-cidr is 10.20.0.0/16, there should be at least one rule in a security group associated to your database that allows MSSQL inbound access from your modern-cidr block
    ![mssql-inbound-from-modern-cidr](/just-the-doc/docs/3_base_application/images/myssql-inbound-from-modern-cidr.png)
7. Make sure you are authenticated to AWS. Confirm access to the intended account using the following command. (More information about authenticating to AWS can be found at the following [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).)
```
$ aws sts get-caller-identity
{
    "UserId": "AIDBZMOZ03E7R88J3DBTZ",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/lincolna"
}
```
8. Terraform stores its state in an S3 bucket. The commands below assume that you are running Terraform authenticated to the same AWS account that contains your existing NBS 6 application. Please adjust accordingly if this does not match your setup.
   - a. Change directory to the account configuration directory if not already, i.e. the one containing terraform.tfvars, and terraform.tf
    ```
    cd terraform/aws/nbs7-mySTLT-test
    ```
   - b. Initialize Terraform by running:
    ```
    terraform init
    ```
   - c. Run “terraform plan” to enable it to calculate the set of changes that need to be applied:
    ```
    terraform plan
    ```
    Note: One warning is expected (due to a bug in the Hashicorp EKS module):
    ```
    Warning: Argument is deprecated
    with module.eks_nbs.module.eks.aws_eks_addon.this["aws-ebs-csi-driver"],
    on .terraform/modules/eks_nbs.eks/main.tf line 392, in resource "aws_eks_addon" "this":
    392:   resolve_conflicts        = try(each.value.resolve_conflicts, "OVERWRITE")
    The "resolve_conflicts" attribute can't be set to "PRESERVE" on initial resource creation. Use "resolve_conflicts_on_create" and/or "resolve_conflicts_on_update" instead
    ```
    ![terraform-plan](/just-the-doc/docs/3_base_application/images/terraform-plan.png)
   - d. Review the changes carefully to make sure that they 1) match your intention, and 2) do not unintentionally disturb other configuration on which you depend. Then run “terraform apply”:
    ```
    terraform apply
    ```
    e. If terraform apply generates errors, review and resolve the errors, and then rerun step d.
9. Verify Terraform was applied as expected by examining the logs
10. Verify the [newly created VPC and subnets](https://us-east-1.console.aws.amazon.com/vpc/home?region=us-east-1#Home:) were created as expected and confirm that the CIDR blocks you defined exist in the Route Tables
11. Verify the [EKS Kubernetes cluster](https://us-east-1.console.aws.amazon.com/eks/home?region=us-east-1#/clusters) was created by selecting the cluster and inspecting Resources->Pods, Compute (expect 30+ pods at this point, and 3-5 compute nodes as per the min/max nodes defined in terraform/aws/app-infrastructure/eks-nbs/variables.tf)
12. Now that the infrastructure has been created using terraform, deploy Kubernetes (K8s) support services in the Kubernetes cluster via the following steps
    - a. Start the Terminal/command line:
        - i. Make sure you are still authenticated with AWS (reference the following [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)).
        - ii. Authenticate into the Kubernetes cluster (EKS) using the following command and the [cluster name you deployed in the environment](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
           ```bash
           aws eks --region us-east-1 update-kubeconfig --name <clustername> # e.g. cdc-nbs-sandbox
           ```
        - iii. If the above command errors out, check
           - There are no issues with the AWS CLI installation
           - You have set the correct AWS environment variables
           - You are using the correct cluster name (as per the EKS management console)
    - b. Run the following command to check if you are able to run commands to interact with the Kubernetes objects and the cluster.
      ```bash
      kubectl get pods --namespace=cert-manager
      ```
      The above command should return 3 pods.  If it doesn’t refresh the AWS credentials and repeat steps in 12 a.
      ```bash
      kubectl get nodes
      ```
13. Congratulations! You have installed your core infrastructure and Kubernetes cluster! Next, we will configure your cluster using helm charts.
