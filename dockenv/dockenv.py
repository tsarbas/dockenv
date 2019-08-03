import fire
import yaml
from loguru import logger

DC_FILE = 'docker-compose.yml'


IMAGES_DATA = {
    'postgres': {
        'image': 'postgres',
        'volumes': ['./db:/var/lib/postgresql'],
        'ports': ['127.0.0.1:5432:5432'],
        'expose': ['5432'],
        'environment': [
            'POSTGRES_PASSWORD=postgres',
            'POSTGRES_USER=postgres',
            'POSTGRES_DB=postgres',
        ]
    },
    'redis': {
        'image': 'redis',
        'ports': ['127.0.0.1:6379:6379'],
        'expose': ['6379']
    }
}


def _dump_yaml(data):
    if 'version' in data:
        del data['version']
    return "version: '3'\n\n" + yaml.dump(data, default_flow_style=False)


def _save_data(data):
    string = _dump_yaml(data)
    with open(DC_FILE, 'w') as f:
        f.write(string)
    logger.info('File saved')


def _load_data():
    try:
        with open(DC_FILE) as f:
            return yaml.load(f.read())
    except IOError:
        return {}


def _get_service(image, images_data=IMAGES_DATA):
    if image in images_data:
        return images_data[image]
    else:
        return {
            'image': image,
        }


def add(service, image):
    data = _load_data()

    if not data.get('services'):
        data['services'] = dict()

    if service not in data.get('services', {}):
        data['services'][service] = _get_service(image)

    _save_data(data)
    logger.info(f'service {service} added')


def rm(service):
    data = _load_data()

    if service in data.get('services', {}):
        del data['services'][service]

    _save_data(data)


def main():
    fire.Fire({
        'add': add,
        'rm': rm,
    })


if __name__ == '__main__':
    main()
