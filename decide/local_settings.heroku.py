ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

APIS = {
    'authentication': 'https://decide-palkia-django.herokuapp.com',
    'base': 'https://decide-palkia-django.herokuapp.com',
    'booth': 'https://decide-palkia-django.herokuapp.com',
    'census': 'https://decide-palkia-django.herokuapp.com',
    'mixnet': 'https://decide-palkia-django.herokuapp.com',
    'postproc': 'https://decide-palkia-django.herokuapp.com',
    'store': 'https://decide-palkia-django.herokuapp.com',
    'visualizer': 'https://decide-palkia-django.herokuapp.com',
    'voting': 'https://decide-palkia-django.herokuapp.com',
}

BASEURL = 'https://decide-palkia-django.herokuapp.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256