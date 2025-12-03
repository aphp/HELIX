# helix

![Version: 1.3.1](https://img.shields.io/badge/Version-1.3.1-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.0.0.beta1](https://img.shields.io/badge/AppVersion-1.0.0.beta1-informational?style=flat-square)

A Helm chart deploying the helix, a collection of research-oriented applications, organized in a cohesive way.

**Homepage:** <https://github.com/aphp/HELIX>

## Source Code

* <https://github.com/aphp/HELIX>

## Requirements

Kubernetes: `>=v1.24.0-0`

| Repository | Name | Version |
|------------|------|---------|
| https://hub.jupyter.org/helm-chart/ | jupyterhub | 4.3.1 |

## Deployment Architecture

This Chart allows the HELIX to be deployed as follows :

TODO

## Installing the Chart

The default Chart values allows the deployment of a working (although unsecure) version of the HELIX out-of-the-box.

To install the chart, just type  the following command:

```sh
helm upgrade --install helix ./helix
```

## Values

### Helm Release settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| nameOverride | string | `""` | Custom Helm Release name. |
| fullnameOverride | string | `""` | Custom Helm Release full name. |

### HELIX settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| configuration | object | Configuration fitting a standard context | HELIX settings. |
| configuration.jupyterhub | object | JupyterHub configuration override fitting a standard context | HELIX settings regarding JupyterHub. |
| configuration.jupyterhub.singleuser | object | No override of existing Z2JHK8S Chart Configuration. | HELIX settings regarding Jupyter Notebbok Singleuser (jovyan user inside pods). |
| configuration.jupyterhub.singleuser.ownership | object | No override of existing Z2JHK8S Chart Configuration. | Supports UID/GID manipulation to match custom volume persmisisons |
| configuration.jupyterhub.singleuser.ownership.uidOverride | int | `1000` | Overrides the default "jovyan" user UID |
| configuration.jupyterhub.singleuser.ownership.addToGroups | list | `[]` | Extra group binding for the default user (jovyan). Must be an array of GIDs of form [123,456] |
| configuration.jupyterhub.profiles | object | Single-ser and collaborative profiles fitting an standard context. | Specifies JupyterHub's available profile, containing the notebook's docker images. |
| configuration.jupyterhub.profiles.user | list | APHP EDS Base and OCAML notebook profiles, alongside Jupyter Project official  | Single-user profiles, used when a user spawns his own JLab environment.             minimal and datascience notebooks |
| configuration.jupyterhub.profiles.user[0].displayName | string | `"Jupyter EDS Base Notebook"` | Profile's name to be display to the user. |
| configuration.jupyterhub.profiles.user[0].slug | string | `"eds-base-notebook"` | Profile's slug. |
| configuration.jupyterhub.profiles.user[0].image | string | `"ghcr.io/aphp/base-eds-notebook:x86_64-ubuntu-24.04"` | Image to be used with that profile. |
| configuration.jupyterhub.profiles.user[0].imagePullPolicy | string | `"Always"` | Image's Pull Policy. |
| configuration.jupyterhub.profiles.collaboration | list | APHP EDS Base and OCAML notebook profiles. | Collaboration profiles, used when a user spawns a collaborative JLab. |
| configuration.jupyterhub.profiles.collaboration[0].displayName | string | `"Jupyter EDS Base Notebook"` | Image name to be displayed in the profile list. |
| configuration.jupyterhub.profiles.collaboration[0].slug | string | `"eds-base-notebook"` | Profile's slug. |
| configuration.jupyterhub.profiles.collaboration[0].image | string | `"ghcr.io/aphp/base-eds-notebook:x86_64-ubuntu-24.04"` | Image to be used with that profile. |
| configuration.jupyterhub.profiles.collaboration[0].imagePullPolicy | string | `"Always"` | Image's Pull Policy. |

### HELIX persistence settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| persistence.createPVC | list | `[]` | Creates PVCs to be used across the HELIX's applications. |

### HELIX ServiceAccount settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| serviceAccount | object | Creation of an automounted dedicated ServiceAccount | Settings related to the HELIX's Service Account. |
| serviceAccount.create | bool | true | Create ServiceAccount |
| serviceAccount.automount | bool | true | Automount ServiceAccount |
| serviceAccount.annotations | object | true | Custom Annotations for the ServiceAccount |
| serviceAccount.name | string | true | Name of the ServiceAccount |

### JupyterHub Chart settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| jupyterhub.enabled | bool | true | If true, enables the deployment of the JupyterHub Chart.  |
| jupyterhub.debug.enabled | bool | false | Increases the log level throughout the resources in the Helm chart. |
| jupyterhub.ingress.enabled | bool | true | Enable the creation of a Kubernetes Ingress to proxy-public service. |
| jupyterhub.ingress.ingressClassName | string | nginx | Maps directly to the Ingress resource’s `spec.ingressClassName``. |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/app-root" | string | nginx.ingress.kubernetes.io/app-root: "/jupyter" | Annotations to apply to the Ingress resource. |
| jupyterhub.ingress.hosts | list | localhost | List of hosts to route requests to the proxy. |
| jupyterhub.ingress.tls | list | [] | TLS configurations for Ingress. |
| jupyterhub.hub.image | object | Jupyterhub 4.1.6 | Set custom image name, tag, pullPolicy, or pullSecrets for the pod.  |
| jupyterhub.hub.image.pullPolicy | string | "Always" | Configures the Pod’s spec.imagePullPolicy. |
| jupyterhub.hub.authenticatePrometheus | bool | false | Enforce prometheus scrapper to be authenticated to this JupyterHub instance. |
| jupyterhub.hub.db.type | string | "sqlite-pvc" | Type of database backend to use for the hub database. The Hub requires a     persistent database to function, and this lets you specify where it should be stored. |
| jupyterhub.hub.db.pvc | object | 2GB RWX PVC | Customize the Persistent Volume Claim used when hub.db.type is sqlite-pvc. |
| jupyterhub.hub.extraEnv | object | Sets the default URL the user is redirected to, and the name of the project.  | Extra environment variables that should be set for the hub pod. |
| jupyterhub.hub.redirectToServer | bool | false | JupyterHub native configuration, see the JupyterHub documentation for more information. |
| jupyterhub.hub.extraVolumeMounts | list | Extra ConfigMap mapped in Jupyter Hub's config dir. | Additional volume mounts for the Container. Use a k8s native syntax. |
| jupyterhub.hub.extraVolumes | list | Extra ConfigMap mapped in Jupyter Hub's config dir. | Additional volumes for the Pod. Use a k8s native syntax. |
| jupyterhub.scheduling.userScheduler.enabled | bool | false | The user scheduler is making sure that user pods are scheduled tight on nodes,     this is useful for autoscaling of user node pools. |
| jupyterhub.scheduling.podPriority.enabled | bool | false | Pod Priority is used to allow real users evict user placeholder pods that in turn    by entering a Pending state can trigger a scale up by a cluster autoscaler. |
| jupyterhub.scheduling.userPlaceholder.enabled | bool | false | User placeholders simulate users but will thanks to PodPriority be evicted by the     cluster autoscaler if a real user shows up.  |
| jupyterhub.proxy.service.type | string | "ClusterIP" | Default ClusterIP. See the Kubernetes docs to learn more about service types. |
| jupyterhub.prePuller.continuous.enabled | bool | Disabled | See the optimization section for more details. |
| jupyterhub.prePuller.hook.enabled | bool | Disabled --  | See the optimization section for more details |
| jupyterhub.cull.enabled | bool | false | Enable/disable use of jupyter-idle-culler. |
| jupyterhub.cull.maxAge | int | 93600s (26 hours) | Maximum lifespan (in seconds) of a singleuser pod. |
| jupyterhub.singleuser.podNameTemplate | string | "jupyter-{unescaped_username}" | Passthrough configuration for KubeSpawner.pod_name_template. |
| jupyterhub.singleuser.storage.dynamic | object | Dynamic 5Gi PVC for the home volume. | Configures KubeSpawner.storage_class, which can be an explicit StorageClass to dynamically    provision storage for the PVC that KubeSpawner will create. |
| jupyterhub.singleuser.storage.dynamic.storageClass | string | "standard" | Configures KubeSpawner.storage_class, which can be an explicit StorageClass to dynamically     provision storage for the PVC that KubeSpawner will create. |
| jupyterhub.singleuser.storage.dynamic.volumeNameTemplate | string | "volume-{username}{servername}" | Configures KubeSpawner.storage_class, which can be an explicit StorageClass to dynamically     provision storage for the PVC that KubeSpawner will create. |
| jupyterhub.singleuser.storage.dynamic.storageAccessModes | list | "ReadWriteOnce" | Configures KubeSpawner.storage_access_modes. |
| jupyterhub.singleuser.storage.capacity | string | 5Gi | Configures KubeSpawner.storage_capacity. |

### Other Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| jupyterhub.hub.resources.requests.memory | string | `"2Gi"` |  |
| jupyterhub.hub.resources.requests.cpu | string | `"0.5"` |  |
| jupyterhub.hub.resources.limits.memory | string | `"4Gi"` |  |
| jupyterhub.hub.resources.limits.cpu | string | `"1.5"` |  |
| jupyterhub.hub.baseUrl | string | `"/jupyter"` |  |
| jupyterhub.proxy.chp.containerSecurityContext.allowPrivilegeEscalation | bool | `false` |  |
| jupyterhub.proxy.chp.resources.requests.memory | string | `"2Gi"` |  |
| jupyterhub.proxy.chp.resources.requests.cpu | string | `"0.5"` |  |
| jupyterhub.proxy.chp.resources.limits.memory | string | `"4Gi"` |  |
| jupyterhub.proxy.chp.resources.limits.cpu | string | `"1.5"` |  |
| jupyterhub.cull.timeout | int | `3600` |  |
| jupyterhub.cull.every | int | `300` |  |
| jupyterhub.singleuser.cloudMetadata.blockWithIptables | bool | `false` |  |
| jupyterhub.singleuser.extraEnv.PYDEVD_DISABLE_FILE_VALIDATION | string | `"1"` |  |
| jupyterhub.singleuser.cpu.limit | int | `5` |  |
| jupyterhub.singleuser.cpu.guarantee | int | `2` |  |
| jupyterhub.singleuser.memory.limit | string | `"16G"` |  |
| jupyterhub.singleuser.memory.guarantee | string | `"8G"` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)