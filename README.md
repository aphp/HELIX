# HELIX HelmChart

## Présentation

Ce projet porte le HelmChart d'HELIX (Health and Exploration Lab for Innovative eXperiments). Il s'agit d'un Umbrella Chart contenant les outils qui sont inclus et packagés dans HELIX, soit pour la version bêta :
- JupyterHub
- INCEpTION (en cours de développement)

## Installation 

La documentation du Chart est décrite dans le fichier `helix/README.md.`

Le répertoire `examples` contient des templates de fichier `values.yaml` selon le type de déploiement que vous souhaitez effectuer.

## Contribution

Cette partie décrit les guidelines de contributions.

### Prérequis

Les prérequis suivants sont nécessaires pour un développement et des tests locaux :

#### Outils

Les outils suivants doivent être installés :

- [`Helm 3`](https://helm.sh/docs/intro/install/)
  - Plugin [`helm-docs`](https://github.com/norwoodj/helm-docs?tab=readme-ov-file#installation)
  - Plugin [`helm-values-schema-json`](https://github.com/losisin/helm-values-schema-json?tab=readme-ov-file#installation)
  - PLugin [`cm-push`](https://github.com/chartmuseum/helm-push?tab=readme-ov-file#install)
- [`Kubeconform`](https://github.com/yannh/kubeconform?tab=readme-ov-file#installation)
- [`Polaris`](https://polaris.docs.fairwinds.com/infrastructure-as-code/#install-the-cli)

#### Environment de développement

L'environnement recommandé est le suivant :

- IDE : [`VSCode`](https://code.visualstudio.com/) (ou [`VSCodium`](https://vscodium.com/))
  - Plugin [`Kubernetes`](https://github.com/vscode-kubernetes-tools/vscode-kubernetes-tools)
- [`Docker`](https://docs.docker.com/engine/install/)
- Custer Kubernetes local : [`KinD`](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
  - Cluster mono-noeud avec Ingress Controller -> voir [documentation dédiée](https://kind.sigs.k8s.io/docs/user/ingress/#setting-up-an-ingress-controller)

#### Configuration

Les configurations suivantes doivent être appliquées : 
- Polaris
  - Récupérer [le fichier de configuration dédié](https://gitlab.data.aphp.fr/ID/pfm/infrastructure/metier/helix/charts/helix/-/raw/main/.gitlab-ci/config/polaris/config.yaml?ref_type=heads), et indiquer son chemin dans el flag `--config` à l'exécution de Polaris (voir parie [Tests](#tests) ci-dessous).

### Déploiement local

Les outils ainsi que l’environnement de développement (à l'exception de l'IDE) sont disponibles dans un environnement ISO (VM) déployable via le [script de bootstrapping dédié](https://gitlab.data.aphp.fr/ID/pfm/infrastructure/metier/helix/bootstrap/-/tree/dev?ref_type=heads).

#### Tests

La CI du projet passe des outils de linting et de tests de conformance automatiques à chaque commit, mais il peut être utile de passer ces mêmes tests en local , afin d'aider au development.

- Helm Lint :
  ```sh
    helm lint ./helix \
      -f <votre_fichier_values> \
      --strict
  ```

- Kubeconform :
  ```sh
    helm template ./helix -f <votre_fichier_values> \
    | kubeconform \ 
        -strict \
        -verbose \
        -summary \
        -output text
  ```

- Polaris :
  ```sh
    polaris audit \
        --config <fichier_récupéré_à-l_étape_précédente> \
        --only-show-failed-tests \
        --set-exit-code-below-score=60 \
        --set-exit-code-on-danger=true \
        --helm-chart ./helix \
        --helm-values <votre_fichier_values> \
        --format=pretty \
        --color=false \
        --quiet
  ```

#### Build

La CI du projet utilise des outils et plugins dédiés pour générer la documentation et les schémas de validation à partir du fichier `values.yaml` du projet. 

Il est néanmoins nécessaire de vérifier la génération de ces fichiers avant de commiter sur la branche, afin d'voir une documentation à jour sur le repo git.

Pour cela, les actions suivantes sont à effectuer : 

- Helm Docs
  Ce plugin génère automatiquement la documentation en fonction du contenu et des commentaires présents dans le fichiers. 
  Le format des commentaires ainsi que de nombreux exemples peuvent être trouvées dans le [repository github du projet](https://github.com/norwoodj/helm-docs/tree/master/example-charts).
  ```sh
    helm-docs \
      --document-dependency-values \
      --sort-values-order=file
  ```

- Helm Values Schema JSON
  Ce plugin permets de générer un schéma de validation de paramètres de HelmChart.
  Le schéma se génère automatiquement à partir du fichier `values.json` indiqué par défaut.
  ```sh
      helm schema \
      -input ./helix/values.yaml \
      -output ./helix/values.schema.json
  ```

#### Publication

La CI utilise un script de publication se basant sur le plugin helm cm-push.

- Branche `main`
Le Chart est packagé et pushé sur le repository Harbor `public` avec les champs `version` et `appVersion` tels qu'indiqués dans la fichier `VERSIONS.txt`

- Branche `dev`
Le Chart est packagé et pushé sur le repository Harbor `public` avec le champs `appVersion` tel qu'indiqué dans la fichier `VERSIONS.txt`. 
La version du Chart (champs `version`) est crée à partir de la version indiquée dans le fichier `VERSIONS.txt`, à laquelle est préfixé `-dev.git.${CI_COMMIT_SHA}`

#### Workflow

Si vous souhaitez contribuer à ce projet, le workflow est le suivant : 

1. Créer une issue détaillant le besoin ainsi que la proposition
1. Présenter l'issue au PO HELIX (tous les lundis à 15h), afin d'être sûr que ce besoin n'est pas déjà priorisé en interne
1. Créer une branche à partir de la branche `dev` : `feat/ma_super_feature`
1. Créer une Merge Request en status `Draft` à partir de votre branche
1. Réaliser les développements jusqu'à ce que les étapes `test` et `build` de la CI passent
1. Pinger les les responsables du projets (KZG si vous ne savez pas) sur votre MR. 
  Une review de votre code sera alors priorisé en PO HELIX. Votre Merge Request sera mise à jours avec les informations quant à cette priorisation.
    * Il est possible que les responsables reviennent vers vous soit en PO HELIX, soit en commentaires de MR (ou les deux)
    avec des retours/questions/demandes de changements sur votre development
1. Une fois la review réalisée et validée, votre code sera mergé sur la branche principale, et une nouvelle release sera publiée.