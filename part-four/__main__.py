import base64
import pulumi
import pulumi_awsx as awsx
import pulumi_eks as eks
import pulumi_kubernetes as k8s

# Create an EKS cluster with the default configuration.
cluster = eks.Cluster('my-cluster');

# Build and publish our app's container image:

repo = awsx.ecr.Repository("my-repo");

image = awsx.ecr.Image("image",
                       repository_url=repo.url,
                       path="./website")

# Create a NGINX Deployment and load balanced Service, running our app.
app_name = 'my-app'
app_labels = { 'app': app_name }
deployment = k8s.apps.v1.Deployment(f'{app_name}-dep',
    spec = k8s.apps.v1.DeploymentSpecArgs(
        selector = k8s.meta.v1.LabelSelectorArgs(match_labels = app_labels),
        replicas = 2,
        template = k8s.core.v1.PodTemplateSpecArgs(
            metadata = k8s.meta.v1.ObjectMetaArgs(labels = app_labels),
            spec = k8s.core.v1.PodSpecArgs(containers = [
                k8s.core.v1.ContainerArgs(
                    name = app_name,
                    image = image.image_uri
                )
            ]),
        ),
    )
)
service = k8s.core.v1.Service(f'{app_name}-svc',
    spec = k8s.core.v1.ServiceSpecArgs(
        type = 'LoadBalancer',
        selector = app_labels,
        ports = [ k8s.core.v1.ServicePortArgs(port = 80) ],
    )
)

# Export the URL for the load balanced service.
pulumi.export('ingress_ip', service.status.load_balancer.ingress[0].ip)

# Export the cluster's kubeconfig.
pulumi.export('kubeconfig', cluster.kubeconfig)