from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from kubernetes import client, config
from kubernetes.client import ApiException
# Load Kubernetes configuration
from django.shortcuts import render


#Get method for resources
def show_resources(response):
    res='Check'
    resource_names = [
        "pods",
        "services",
        "configmaps",
        "secrets",
        "persistentvolumeclaims",
        "persistentvolumes",
        "namespaces",
        "replicationcontrollers",
        "deployments",
        "daemonsets",
        "statefulsets",
        "replicasets",
        "jobs",
        "cronjobs",
        "networkpolicies",
        "roles",
        "rolebindings",
        "clusterroles",
        "clusterrolebindings",
        "poddisruptionbudgets",
        "customresources"
    ]
    for resource_name in resource_names:
        resources = get_all_resources(resource_name)

        # Print the resources
        if resources:
            if resource_name.lower() == "customresources":
                import json
                resources = json.loads(resources.read())
                for item in resources["items"]:
                    res+=f"\n- {item['metadata']['namespace']}/{item['metadata']['name']}"
            else:
                res+=f"\n{resource_name.capitalize()}:"
                for item in resources.items:
                    res+=f"\n- {item.metadata.namespace}/{item.metadata.name}"

    return HttpResponse(res,content_type="text/plain")

def kubernetes_resources(request):
   if request.method == 'POST':
       namespace = request.POST.get('namespace')

       # Load Kubernetes config from default location
       config.load_incluster_config()

       # Create a Kubernetes API client
       v1 = client.CoreV1Api()
       core_v1 = client.CoreV1Api()
       apps_v1 = client.AppsV1Api()
       batch_v1 = client.BatchV1Api()
       networking_v1 = client.NetworkingV1Api()
       rbac_v1 = client.RbacAuthorizationV1Api()
       policy_v1beta1 = client.PolicyV1Api()
       custom_objects_api = client.CustomObjectsApi()

       try:
           # Retrieve resources (e.g., pods) in the selected namespace
           pods = core_v1.list_namespaced_pod(namespace=namespace)
           services = core_v1.list_namespaced_service(namespace=namespace)
           deployments = apps_v1.list_namespaced_deployment(namespace=namespace)
           replicasets = apps_v1.list_namespaced_replica_set(namespace=namespace)
           statefulsets = apps_v1.list_namespaced_stateful_set(namespace=namespace)
           daemonsets = apps_v1.list_namespaced_daemon_set(namespace=namespace)
           jobs = batch_v1.list_namespaced_job(namespace=namespace)
           cronjobs = batch_v1.list_namespaced_cron_job(namespace=namespace)
           configmaps = core_v1.list_namespaced_config_map(namespace=namespace)
           secrets = core_v1.list_namespaced_secret(namespace=namespace)
           serviceaccounts = v1.list_namespaced_service_account(namespace=namespace)
           pvcs = core_v1.list_namespaced_persistent_volume_claim(namespace=namespace)
           # Add more API calls as needed for other resources (services, deployments, etc.)

           # Prepare data to pass to template
           context = {
               'namespace': namespace,
               'resources': [
                   {'pods': pods.items},
                   {'services': services.items},
                   {'deployments': deployments.items},
                   {'replicasets': replicasets.items},
                   {'statefulsets': statefulsets.items},
                   {'daemonsets': daemonsets.items},
                   {'jobs': jobs.items},
                   {'cronjobs': cronjobs.items},
                   {'configmaps': configmaps.items},
                   {'secrets': secrets.items},
                   {'serviceaccounts': serviceaccounts.items},
                   {'pvcs': pvcs.items},
               ],  # Example with pods, adjust for other resource types
           }

           return render(request, 'kubernetes_resources.html', context)

       except Exception as e:
           error_message = f"Error retrieving resources: {str(e)}"
           return render(request, 'error.html', {'error_message': error_message})

   else:
       # Handle GET request or initial load
       return render(request, 'kubernetes_form.html')


def get_all_resources(resource_name):
    config.load_incluster_config()
    # Create an API client
    v1 = client.CoreV1Api()
    # Initialize the API clients
    core_v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    batch_v1 = client.BatchV1Api()
    networking_v1 = client.NetworkingV1Api()
    rbac_v1 = client.RbacAuthorizationV1Api()
    policy_v1beta1 = client.PolicyV1Api()
    custom_objects_api = client.CustomObjectsApi()

    # Mapping of resource names to API calls
    resource_map = {
        "pods": core_v1.list_pod_for_all_namespaces,
        "services": core_v1.list_service_for_all_namespaces,
        "configmaps": core_v1.list_config_map_for_all_namespaces,
        "secrets": core_v1.list_secret_for_all_namespaces,
        "persistentvolumeclaims": core_v1.list_persistent_volume_claim_for_all_namespaces,
        "persistentvolumes": core_v1.list_persistent_volume,
        "namespaces": core_v1.list_namespace,
        "replicationcontrollers": core_v1.list_replication_controller_for_all_namespaces,
        "deployments": apps_v1.list_deployment_for_all_namespaces,
        "daemonsets": apps_v1.list_daemon_set_for_all_namespaces,
        "statefulsets": apps_v1.list_stateful_set_for_all_namespaces,
        "replicasets": apps_v1.list_replica_set_for_all_namespaces,
        "jobs": batch_v1.list_job_for_all_namespaces,
        "cronjobs": batch_v1.list_cron_job_for_all_namespaces,
        "networkpolicies": networking_v1.list_network_policy_for_all_namespaces,
        "roles": rbac_v1.list_role_for_all_namespaces,
        "rolebindings": rbac_v1.list_role_binding_for_all_namespaces,
        "clusterroles": rbac_v1.list_cluster_role,
        "clusterrolebindings": rbac_v1.list_cluster_role_binding,
        "poddisruptionbudgets": policy_v1beta1.list_pod_disruption_budget_for_all_namespaces,
        "customresources": custom_objects_api.list_cluster_custom_object
    }

    # Get the API call function based on the resource name
    api_call = resource_map.get(resource_name.lower())
    if not api_call:
        print(f"Resource {resource_name} is not supported.")
        return

    # Custom resource details (group, version, plural)
    custom_resource_details = {
        "group": "example.com",  # Replace with actual group name
        "version": "v1",         # Replace with actual version
        "plural": "customresources"  # Replace with actual plural name
    }

    # Make the API call and return the results
    try:
        if resource_name.lower() == "customresources":
            resources = api_call(
                group=custom_resource_details["group"],
                version=custom_resource_details["version"],
                plural=custom_resource_details["plural"],
                _preload_content=False
            )
        else:
            resources = api_call(watch=False)
        return resources
    except ApiException as e:
        print(f"Exception when calling Kubernetes API: {e}")
        return None
