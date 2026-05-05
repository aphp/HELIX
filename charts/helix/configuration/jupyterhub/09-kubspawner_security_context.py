seccompProfileType = {{- .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.type | default "RuntimeDefault" }}
localhostProfile = {{- .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.localhostProfile | default "" }}'

seccompProfile = {
    'type': seccompProfileType,
}

if ( seccompProfileType == "Localhost" ):
    seccompProfile.update({
        'localhostProfile': localhostProfile,
    })

c.KubeSpawner.pod_security_context.update({
    'runAsNonRoot': True,
    'seccompProfile': seccompProfile
})

c.KubeSpawner.container_security_context.update({
    'allowPrivilegeEscalation': False,
    'capabilities': {
        'drop': ['ALL'],
    },
})