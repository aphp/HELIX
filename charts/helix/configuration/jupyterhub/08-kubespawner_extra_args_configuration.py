c.Spawner.args = [
    '--VoilaConfiguration.enable_nbextensions=True',
    "--VoilaConfiguration.file_whitelist=['.*']",
    '--NotebookApp.tornado_settings={"headers":{"Content-Security-Policy":"frame-ancestors *;"}}'
]

c.VoilaConfiguration.show_tracebacks = True