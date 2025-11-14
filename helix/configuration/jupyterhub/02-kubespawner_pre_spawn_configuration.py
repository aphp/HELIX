import os
import yaml

# Defining collaboration project variables
allow_private_jlab = os.environ.get("ALLOW_PRIVATE_JLAB", "false")
collab_user = os.environ.get("PROJECT", "collaboration")


j_hub_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "read:metrics",
            "delete:servers",
        ],
        "services": ["jupyterhub-idle-culler"],
    },
]

if allow_private_jlab.lower() == "true":
    j_hub_roles.extend(
        [
            {
                "name": "user",
                "description": "Overrides the default user role to allow access to the collaboration server as well as its own server",
                "scopes": [
                    "self",
                    "admin-ui",
                    "list:users",
                    "read:metrics",
                    "read:servers!user=user",
                    "access:servers!user=user",
                    "admin:servers!user=user",
                    f"read:servers!user={collab_user}",
                    f"access:servers!user={collab_user}",
                    f"admin:servers!user={collab_user}",
                ],
            },
        ]
    )
else:
    j_hub_roles.extend(
        [
            {
                "name": "user",
                "description": "Overrides the default user role to allow access to the collaboration server",
                "scopes": [
                    "self",
                    "admin-ui",
                    "list:users",
                    "read:metrics",
                    f"read:servers!user={collab_user}",
                    f"access:servers!user={collab_user}",
                    f"admin:servers!user={collab_user}",
                ],
            },
        ]
    )


c.JupyterHub.load_roles = j_hub_roles


def pre_spawn_hook(spawner):

    # Starting the lab in debug mode if required
    jlab_debug = collab_user = os.environ.get("JLAB_DEBUG", "FALSE")
    if jlab_debug.lower() == "true":
        spawner.args.append("--debug")

    # Activating the collaboration extension only if the user spawned is a collaborative one
    user_name = spawner.user.name
    if user_name == collab_user:
        spawner.log.info(f"Enabling RTC for user {user_name}")
        spawner.args.append("--LabApp.collaborative=True")

    # Activating hidden files serving
    spawner.args.append("--ContentsManager.allow_hidden=True")



c.KubeSpawner.pre_spawn_hook = pre_spawn_hook
