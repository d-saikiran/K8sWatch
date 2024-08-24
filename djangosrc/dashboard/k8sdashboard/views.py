#Open issue: https://github.com/kubernetes-client/python/issues/1617 Implemented WA
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from kubernetes import client, config
from kubernetes.client import ApiException
# Load Kubernetes configuration
from django.shortcuts import render
import json
import datetime
import yaml
import subprocess
from django.views.decorators.csrf import csrf_exempt
import os
import tempfile

# Load Kubernetes config from default location
config.load_incluster_config()
#config.load_kube_config()

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

def get_all_resources(resource_name):
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
def remove_null_values(obj):
    """
    Recursively remove keys with null values from a dictionary.
    """
    if isinstance(obj, dict):
        return {k: remove_null_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_null_values(i) for i in obj]
    else:
        return obj
def convert_to_dict_with_metadata(obj, api_version, kind, clean_yaml):
    obj_dict = obj.to_dict()
    obj_dict['apiVersion'] = api_version
    obj_dict['kind'] = kind
    if clean_yaml:
        obj_dict = remove_null_values(obj_dict)
    return obj_dict

def kubernetes_resources(request):
   if request.method == 'POST':
       namespace = request.POST.get('namespace')

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
           if 'download' in request.POST:
               config_maps = v1.list_namespaced_config_map(namespace)
               secrets = v1.list_namespaced_secret(namespace)
               services = v1.list_namespaced_service(namespace)
               pods = v1.list_namespaced_pod(namespace)
               deployments = client.AppsV1Api().list_namespaced_deployment(namespace)

               clean_yaml = request.POST.get('clean_yaml') == 'true'

               # Convert the dictionary to YAML format
               # Convert objects to dictionaries with metadata
               k8s_objects = []
               k8s_objects.extend([convert_to_dict_with_metadata(obj, 'v1', 'ConfigMap', clean_yaml) for obj in config_maps.items])
               k8s_objects.extend([convert_to_dict_with_metadata(obj, 'v1', 'Secret', clean_yaml) for obj in secrets.items])
               k8s_objects.extend([convert_to_dict_with_metadata(obj, 'v1', 'Service', clean_yaml) for obj in services.items])
               k8s_objects.extend([convert_to_dict_with_metadata(obj, 'v1', 'Pod', clean_yaml) for obj in pods.items])
               k8s_objects.extend([convert_to_dict_with_metadata(obj, 'apps/v1', 'Deployment', clean_yaml) for obj in deployments.items])

               yaml_documents = "\n---\n".join([yaml.dump(obj, default_flow_style=False) for obj in k8s_objects])
               response = HttpResponse(yaml_documents, content_type='application/x-yaml')
               response['Content-Disposition'] = f'attachment; filename={namespace}_k8s_objects.yaml'

               return response
           return render(request, 'kubernetes_resources.html', context)

       except Exception as e:
           error_message = f"Error retrieving resources: {str(e)}"
           return render(request, 'error.html', {'error_message': error_message})

   else:
       # Handle GET request or initial load
       namespaces = get_namespaces()
       return render(request, 'kubernetes_form.html', {'namespaces': namespaces})
def get_namespaces():
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace()
    return [ns.metadata.name for ns in namespaces.items]
def dynamic_resource_view(request,namespace,key,name):
    try:
        output = subprocess.run(["kubectl", "describe", key, name, "-n", namespace], stdout=subprocess.PIPE, text=True).stdout
        #output="\n".join(line.strip() for line in output.splitlines())
        print(output)
        #return HttpResponse(output, content_type="text/plain")
        return render(request, 'kubernetes_describe.html', {'output': output})
    except Exception as e:
        return render(request, 'error.html', {'error_message': e})

def get_yaml(request,namespace,key,name):
    error_message = None
    success_message = None

    if request.method == 'POST':
        yaml_content = request.POST.get('yaml_content','')

        # Basic validation
        if not yaml_content.strip():
            error_message = "YAML content cannot be empty."
        else:
            # Perform YAML validation using kubectl dry run
            try:
                result = subprocess.run(
                    ['kubectl', 'apply', '-f', '-', '--dry-run=client'],
                    input=yaml_content,
                    text=True,
                    capture_output=True,
                    check=True
                )
                # Validation successful
                subprocess.run(
                    ['kubectl', 'apply', '-f', '-'],
                    input=yaml_content,
                    text=True,
                    capture_output=True,
                    check=True
                )
                success_message = "YAML content is valid and saved."
            except subprocess.CalledProcessError as e:
                error_message = f'Error validating YAML: {e.stderr}'
            except Exception as e:
                error_message = f'Unexpected error: {str(e)}'

    # Render the form
    yaml_content=subprocess.run(["kubectl", "get", key, name, "-n", namespace,"-o", "yaml"], stdout=subprocess.PIPE, text=True).stdout
    return render(request, 'kubernetes_manifest.html', {
        'yaml_content': yaml_content,
        'error_message': error_message,
        'success_message': success_message
    })
def migrate_to_cluster(request):
    namespace = request.GET.get('namespace')
    return render(request, 'migrate.html', {'namespace': namespace})

@csrf_exempt
def perform_migration(request):
    if request.method == 'POST':
        namespace = request.POST.get('namespace')
        target_namespace = request.POST.get('target_namespace')
        kubeconfig = request.FILES['kubeconfig']
        with tempfile.NamedTemporaryFile(delete=False) as temp_kubeconfig:
            for chunk in kubeconfig.chunks():
                temp_kubeconfig.write(chunk)
            temp_kubeconfig_path = temp_kubeconfig.name
        v1 = client.CoreV1Api()
        v1_apps = client.AppsV1Api()
        resources_to_migrate = {
            'pods': v1.list_namespaced_pod(namespace),
            'services': v1.list_namespaced_service(namespace),
            'configmaps': v1.list_namespaced_config_map(namespace),
            'secrets': v1.list_namespaced_secret(namespace),
            'deployments': v1_apps.list_namespaced_deployment(namespace),
        }
        config.load_kube_config(config_file=temp_kubeconfig_path)
        v1_target = client.CoreV1Api()
        v1_apps_target = client.AppsV1Api()
        for resource_type, resource_list in resources_to_migrate.items():
            for resource in resource_list.items:
                resource_yaml = client.ApiClient().sanitize_for_serialization(resource)
                resource_yaml.pop('status', None)
                resource_yaml['metadata'].pop('resourceVersion', None)
                # Remove fields that should not be carried over
                resource_yaml.pop('status', None)
                resource_yaml['metadata'].pop('resourceVersion', None)
                resource_yaml['metadata'].pop('selfLink', None)
                resource_yaml['metadata'].pop('uid', None)
                resource_yaml['metadata'].pop('creationTimestamp', None)
                resource_yaml['metadata'].pop('ownerReferences', None)
                if 'spec' in resource_yaml and 'clusterIP' in resource_yaml['spec']:
                    resource_yaml['spec'].pop('clusterIP', None)
                if 'spec' in resource_yaml and 'clusterIPs' in resource_yaml['spec']:
                    resource_yaml['spec'].pop('clusterIPs', None)
                # Remove the namespace or change it to the target namespace
                if 'namespace' in resource_yaml['metadata']:
                    resource_yaml['metadata']['namespace'] = target_namespace
                try:
                    if resource_type == 'pods':
                        v1_target.create_namespaced_pod(namespace=target_namespace, body=resource_yaml)
                    elif resource_type == 'services':
                        v1_target.create_namespaced_service(namespace=target_namespace, body=resource_yaml)
                    elif resource_type == 'configmaps':
                        v1_target.create_namespaced_config_map(namespace=target_namespace, body=resource_yaml)
                    elif resource_type == 'secrets':
                        v1_target.create_namespaced_secret(namespace=target_namespace, body=resource_yaml)
                    elif resource_type == 'deployments':
                            v1_apps_target.create_namespaced_deployment(namespace=target_namespace, body=resource_yaml)

                except ApiException as e:
                    print(f"Exception when migrating {resource_type}: {e}")
        os.remove(temp_kubeconfig_path)
        return HttpResponse("Migration completed successfully!")
    else:
        return HttpResponse("Invalid request method.", status=405)
