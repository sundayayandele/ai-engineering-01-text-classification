# OpenShift deployment

The application is designed to run without root privileges and without a fixed runtime UID dependency. The base Kubernetes manifests disable service-account token automount, drop Linux capabilities, prevent privilege escalation and use RuntimeDefault seccomp.

## Deploy
Build/push an approved image, update the image reference, then:

```bash
oc apply -k openshift/
oc get pods,svc,route
```

The Route uses edge TLS termination with HTTP redirect. Production environments should integrate organizational certificates, identity/gateway policy, NetworkPolicy, quotas and approved image registries.

Do not grant the application privileged SCC access merely to make a container run. Fix the container/workload security assumptions instead.
