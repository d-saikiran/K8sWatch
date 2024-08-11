# K8sWatch
## Description
Django application that uses Kubernetes python client, kubectl to monitor Kubernetes objects in cluster
## Features
- List objects
- Update objects
- Download objects
- See describe output for objects
## Installation
- Create deployment with ```kubectl apply -f deployment.yaml```
Note: Deployment object in above uses default ServiceAccount in namespace that it is deployed in.
- Create service so that details are visible outside cluster with ```kubectl apply -f service.yaml```
- Create ClusterRole, ClusterRolebinding and give access to ServiceAccount used by deployment. Example file ```clusterrolebinding.yaml``` will give access to all ServiceAccounts in all namespaces


