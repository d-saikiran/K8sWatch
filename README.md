# K8sWatch
## Description
K8sWatch is a Django-based application designed to manage Kubernetes resources. It provides a user-friendly interface to interact with Kubernetes clusters, offering features such as listing, updating, and migrating Kubernetes objects.
## Features
- List Objects: View all Kubernetes objects within a namespace.
- Update Objects: Modify existing Kubernetes resources.
- Download Objects: Download Kubernetes resources as a backup.
- Describe Objects: View detailed information about specific Kubernetes objects.
- Migrate Objects: Migrate Kubernetes resources to another cluster or namespace.
## Installation
- Create deployment with ```kubectl apply -f deployment.yaml```
- Create service so that details are visible outside cluster with ```kubectl apply -f service.yaml```
## Usage
- Login: Upload your kubeconfig file on the login page to authenticate.
- Home: Navigate to the home page to view the dashboard of Kubernetes resources.
- List Objects: View all resources in the selected namespace.
- Update Objects: Edit existing Kubernetes resources.
- Download Objects: Backup Kubernetes objects by downloading them.
- Describe Objects: See detailed information about a specific resource.
- Migrate Objects: Migrate resources to another cluster or namespace.

## Authentication
The application uses kubeconfig files provided by users for authentication. This ensures that users only have access to resources they are permitted to access based on their kubeconfig.


