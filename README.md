[![helix-helmchart-ci](https://github.com/aphp/HELIX/actions/workflows/chart-ci.yaml/badge.svg)](https://github.com/aphp/HELIX/actions/workflows/chart-ci.yaml)

# HELIX

Official Helm chart for deploying **HELIX** (Health and Exploration Lab for Innovative eXperiments) on Kubernetes.

HELIX is an AP‑HP project that groups together a coherent set of open‑source applications and tools, packaged as a single, easily deployable platform for data labs and clinical research environments.

HELIX provides a secure, container-based environment for health and clinical research at AP‑HP. This repository contains the Helm chart used to install and operate HELIX on a Kubernetes cluster.

> The Jupyter notebook environments used within HELIX are built from the images published in [`aphp/jupyter-eds-notebooks`](https://github.com/aphp/jupyter-eds-notebooks).

---

## Table of contents

- [Overview](#overview)
- [Architecture and scope](#architecture-and-scope)
- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)
  - [Add the Helm repository](#add-the-helm-repository)
  - [Install HELIX](#install-helix)
  - [Upgrade HELIX](#upgrade-helix)
  - [Uninstall HELIX](#uninstall-helix)
- [Configuration](#configuration)
  - [Common settings](#common-settings)
  - [Example values file](#example-values-file)
- [Local examples](#local-examples)
- [Development](#development)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

---

## Overview

This repository publishes the **`helix`** Helm chart on the AP‑HP Helm repository and provides:

- A **single entry point** to deploy the HELIX platform on Kubernetes.
- A **configurable chart** to adapt HELIX to various environments (local, pre‑production, production).
- Versioned **releases** of the chart, aligned with HELIX application releases.

The chart is published at:

- Helm repository: `https://aphp.github.io/HELIX`
- Chart name: `helix`

---

## Architecture and scope

The HELIX Helm chart is responsible for:

- Deploying the **core HELIX services** (application backend, web interface, jobs, etc.).
- Managing **Kubernetes resources** such as Deployments, Services, Ingress, ConfigMaps, Secrets, and Jobs.
- Exposing configuration hooks for:
  - Ingress and TLS termination.
  - External dependencies (databases, object storage, identity providers, etc.), when applicable.
  - Resource requests and limits and other operational settings.

The chart does **not** build any container images itself. It consumes images published by other projects (for example, HELIX application images and the Jupyter images from [`jupyter-eds-notebooks`](https://github.com/aphp/jupyter-eds-notebooks)).

---

## Prerequisites

To deploy HELIX using this chart, you need:

- A **Kubernetes cluster** (development, test, or production).
- **Helm 3.x** installed locally.
- Sufficient permissions to:
  - Create namespaces,
  - Install cluster‑scoped resources if required by your configuration.
- Optional but typical:
  - An ingress controller (e.g. NGINX Ingress, Traefik, …),
  - A way to manage TLS certificates (e.g. cert‑manager),
  - Existing external services you may connect HELIX to (database, identity provider, etc.).

---

## Quick start

### Add the Helm repository

```bash
helm repo add aphp-helix https://aphp.github.io/HELIX
helm repo update
```

### Install HELIX

Prepare a values file (for example `values-override.yaml`) with the configuration for your environment (see [Configuration](#configuration)).

Then install (or upgrade‑and‑install) HELIX:

```bash
helm upgrade helix aphp-helix/helix \
  --namespace <namespace> \
  --create-namespace \
  --install \
  -f values-override.yaml \
  --wait
```

Replace:

- `<namespace>` with the target Kubernetes namespace (e.g. `helix`),
- `values-override.yaml` with your own values file.

This command:

- Creates or upgrades the `helix` release,
- Creates the namespace if it does not exist,
- Waits for the resources to become ready before returning.

### Upgrade HELIX

To upgrade to a newer version of the chart (or of the underlying images, if you changed your values):

```bash
helm repo update

helm upgrade helix aphp-helix/helix \
  --namespace <namespace> \
  -f values-override.yaml \
  --wait
```

You can pin a specific chart version using `--version` if needed:

```bash
helm upgrade helix aphp-helix/helix \
  --namespace <namespace> \
  --version <chart-version> \
  -f values-override.yaml \
  --wait
```

### Uninstall HELIX

To remove the HELIX release and its resources from a namespace:

```bash
helm uninstall helix --namespace <namespace>
```

---

## Configuration

All configurable parameters for the chart are defined and documented in:

- [`charts/helix/values.yaml`](charts/helix/values.yaml)

Typical areas you will want to adapt include:

- **Images**
  - Container image repositories and tags.
  - Image pull secrets if you use private registries.
- **Ingress and networking**
  - Ingress enablement,
  - Public hostnames,
  - TLS configuration.
- **Persistence and storage**
  - Volumes and storage classes for persistent data, when applicable.
- **External services**
  - References to existing databases, message brokers, identity providers, object storage, etc., when the chart is configured to use them.
- **Resources and scaling**
  - CPU and memory requests/limits,
  - Replica counts for the main workloads.

Consult the comments in `values.yaml` for the authoritative list and detailed documentation of each setting.

### Example values file

Below is a *minimal* example to illustrate how you might structure an override file. The actual keys and defaults are those defined in `charts/helix/values.yaml`.

```yaml
# values-override.yaml (example – adapt to your environment)

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: helix.example.org
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: helix-tls
      hosts:
        - helix.example.org

resources:
  limits:
    cpu: "2"
    memory: "4Gi"
  requests:
    cpu: "500m"
    memory: "1Gi"

# Example of external service configuration (only if supported by the chart)
externalDatabase:
  enabled: true
  host: my-postgres.example.org
  port: 5432
  database: helix
  username: helix
  passwordSecretName: helix-db-credentials
```

> This example is illustrative; please refer to the actual `values.yaml` file in the repository for the exact structure and available options.

---

## Local examples

For local testing and experimentation, you can start from the examples provided in:

- [`examples/local`](examples/local)

These examples typically contain:

- A sample `values` file for local or development deployments (e.g. on kind or minikube),
- Additional notes or scripts to help you bootstrap a minimal HELIX instance.

---

## Development

This repository follows a standard Helm chart layout under `charts/helix`:

- `Chart.yaml` – chart metadata (name, version, dependencies).
- `values.yaml` – default values used by the chart.
- `templates/` – Kubernetes manifests rendered by Helm.
- `.github/workflows/` – CI workflows (linting, packaging, release, etc.).

To work on the chart locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/aphp/HELIX.git
   cd HELIX
   ```

2. Validate the chart:

   ```bash
   helm lint charts/helix
   ```

3. Render the manifests using your values:

   ```bash
   helm template helix charts/helix \
     -f examples/local/values.yaml
   ```

4. (Optional) Deploy to a local cluster for manual testing.

Please refer to [`CONTRIBUTING.md`](CONTRIBUTING.md) for more details on the development workflow, coding standards, and release process.

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

- Read the [contribution guidelines](CONTRIBUTING.md).
- Use GitHub Issues to:
  - Report bugs,
  - Propose improvements,
  - Ask questions about chart usage.

Before opening a pull request, please:

1. Open an issue (if one does not already exist) to discuss your change.
2. Add or update tests and/or examples when relevant.
3. Run the linters and Helm validation locally.

---

## Security

If you discover a security vulnerability affecting HELIX or this chart:

- **Do not** open a public GitHub issue.
- Follow the instructions described in [`SECURITY.md`](SECURITY.md) to contact the maintainers securely.

---

## License

This project is licensed under the **Apache License 2.0**.

- See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE) for details.

By contributing to this repository, you agree that your contributions will be licensed under the same terms.
