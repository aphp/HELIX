from kubernetes_asyncio.client.models import V1EnvVar


def get_notebook_container(containers):
    """Retourne le conteneur 'notebook' (V1Container) ou None."""
    if not containers:
        return None
    return next(
        (c for c in containers if hasattr(c, "name") and c.name == "notebook"),
        containers[0],
    )


def get_mounted_volume_names(container):
    """Retourne la liste des noms des volumes montés dans le conteneur (str)."""
    if not hasattr(container, "volume_mounts") or container.volume_mounts is None:
        return []
    return [vm.name for vm in container.volume_mounts if hasattr(vm, "name")]


def is_pvc_volume(spawner, volume):
    """Vérifie si un volume est de type PersistentVolumeClaim et valide."""
    spawner.log.info(
        f"Checking volume: {volume.name if hasattr(volume, 'name') else 'unnamed'}"
    )
    has_pvc = (
        hasattr(volume, "persistent_volume_claim")
        and volume.persistent_volume_claim is not None
    )
    has_claim_name = (
        (volume.persistent_volume_claim["claimName"] is not None) if has_pvc else False
    )
    spawner.log.info(f"  - Is PVC: {has_pvc}, Has claim_name: {has_claim_name}")
    return has_pvc and has_claim_name


def is_mounted(spawner, volume, mounted_volume_names):
    """Vérifie si un volume est monté (présent dans mounted_volume_names)."""
    has_name = hasattr(volume, "name")
    spawner.log.info(
        f"  - Has name: {has_name}, Name: {volume.name if has_name else 'unknown'}"
    )
    is_in_mounted = volume.name in mounted_volume_names if has_name else False
    spawner.log.info(f"  - Is mounted: {is_in_mounted}")
    return has_name and is_in_mounted


def get_pvc_volumes(spawner, volumes, mounted_volume_names):
    """
    Retourne la liste des volumes de type PVC (V1Volume) montés.
    Args:
        volumes: Liste des objets V1Volume à filtrer.
        mounted_volume_names: Liste des noms de volumes montés.
    Returns:
        Liste des volumes de type PVC et montés.
    """
    spawner.log.debug(f"Mounted volume names: {mounted_volume_names}")
    spawner.log.debug(f"Number of volumes received: {len(volumes) if volumes else 0}")

    if not volumes:
        spawner.log.info("No volumes provided.")
        return []

    pvc_volumes = []
    for volume in volumes:
        spawner.log.info(
            f"\nProcessing volume: {volume.name if hasattr(volume, 'name') else 'unnamed'}"
        )
        if is_pvc_volume(spawner, volume) and is_mounted(
            spawner, volume, mounted_volume_names
        ):
            spawner.log.info(f"  -> Volume {volume.name} is a mounted PVC.")
            pvc_volumes.append(volume)
        else:
            spawner.log.info(
                f"  -> Volume {volume.name if hasattr(volume, 'name') else 'unnamed'} is not a mounted PVC."
            )

    spawner.log.info(f"Found {len(pvc_volumes)} mounted PVC volumes.")
    return pvc_volumes


def map_pvc_env_var(volume_name):
    """Détermine le nom de la variable d'environnement en fonction du nom du volume."""
    volume_name_lower = volume_name.lower()

    if "data-ssd" in volume_name_lower:
        return "MOUNTED_DATA_SSD_PVC"
    elif "data-hdd" in volume_name_lower:
        return "MOUNTED_DATA_HDD_PVC"
    elif "home" in volume_name_lower:
        return "MOUNTED_HOME_PVC"
    else:
        return None


def add_env_vars(container, env_var_name, env_var_value):
    """Ajoute les variables d'environnement au conteneur."""
    if not hasattr(container, "env"):
        container.env = []

    env_var = V1EnvVar(
        name=env_var_name,
        value=env_var_value
    )

    container.env.append(env_var)


def set_pvc_env_vars(container, pvc_volumes):
    """Ajoute les variables d'environnement pour chaque PVC au conteneur."""
    if not hasattr(container, "env"):
        container.env = []

    for volume in pvc_volumes:
        env_var_name = map_pvc_env_var(volume.name)
        if env_var_name is None:
            continue  # Ignore les volumes qui ne correspondent à aucun cas

        env_var_value = volume.persistent_volume_claim["claimName"]
        add_env_vars(container, env_var_name, env_var_value)


def set_mounted_pvc_names_as_env_vars(spawner, pod):
        # 1. Retrieving notebook container (V1Container)
        notebook_container = get_notebook_container(pod.spec.containers)

        # 2. Listing mounted volumes
        mounted_volume_names = get_mounted_volume_names(notebook_container)

        # 3. Retrieving PVC Volumes (V1Volume)
        pvc_volumes = get_pvc_volumes(spawner, pod.spec.volumes, mounted_volume_names)

        # 4. Injecting PVC names as env var
        set_pvc_env_vars(notebook_container, pvc_volumes)


def modify_pod_hook(spawner, pod):
    """Modifie le manifeste du pod singleuser pour inclure dans le conteneur notebook le nom des PVCs monté en variable d'envirronement."""

    try:

        spawner.log.info(
        f"Injecting PVC names bounded to user {spawner.user.name} as environment variables")
        set_mounted_pvc_names_as_env_vars(spawner, pod)


    except Exception as e:
        spawner.log.error("Erreur in modify_pod_hook: %s", e)

    return pod


c.KubeSpawner.modify_pod_hook = modify_pod_hook
