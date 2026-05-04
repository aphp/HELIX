c.KubeSpawner.pod_security_context |  {
                'runAsNonRoot': True,
                'seccompProfile': {
                    "type": {{- .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.type | default "RuntimeDefault" }},
                    "localhostProfile": {{- .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.localhostProfile | default "" }},
                    },					
                },

c.KubeSpawner.container_security_context | {
					"allowPrivilegeEscalation": False,
					"capabilities": {
						"drop": ["ALL"],
					},
				},