# To adjust the spawn options presented to the user, we must create a custom
# options_form function, and this example demonstrates how!
#
#
#
# profile_list (KubeSpawner class) can be configured as a convenience to
# generate set HTML for the options_form configuration (Spawner class).
#
# If options_form is set (or indirectly set through profile_list), it is the
# HTML that users are presented with when users have signed in and want to start
# a server.
#
# While options_form is allowed to be a HTML string, it can also be a callable
# function, that when called generates HTML. If a callable function return a
# falsy value, no form will be rendered.
#
# In this custom options_form function, we will make a decision based on user
# information, update profile_list, and rely on the profile_list logic to render
# the HTML for us.
#
async def generate_profile_list(spawner):

    # Declare the common profile list for all users
    profile_list = []

    user_name = spawner.user.name
    collab_user = os.environ.get('PROJECT', 'collaboration')

    if user_name == collab_user:

        spawner.log.info(f'Setting custom profile for collaboration user {user_name}.')
        profile_list.extend([
		{{- range $profile := .Values.configuration.jupyterhub.profiles.collaboration }}
		{
		    'display_name': '{{ $profile.displayName }}',
		    'slug': '{{ $profile.slug }}',
		    'kubespawner_override': {
		        'image':'{{ $profile.image }}',
		        'image_pull_policy': '{{ $profile.imagePullPolicy }}',
		    },
		},
		{{- end }}
        ])

    else:
        spawner.log.info(f'No custom profiles found, setting default profile for user {user_name}.')
        profile_list.extend([
		{{- range $profile := .Values.configuration.jupyterhub.profiles.user }}
		{
		    'display_name': '{{ $profile.displayName }}',
		    'slug': '{{ $profile.slug }}',
		    'kubespawner_override': {
		        'image':'{{ $profile.image }}',
		        'image_pull_policy': '{{ $profile.imagePullPolicy }}',
		    },
		},
		{{- end }}
	])

    return profile_list


# Don't forget to ask KubeSpawner to make use of this custom hook
c.KubeSpawner.profile_list = generate_profile_list
