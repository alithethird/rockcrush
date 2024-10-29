#!/usr/bin/python3
import subprocess

def get_microk8s_image_list():
    result = subprocess.run(['microk8s', 'ctr', 'images', 'ls'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    images = output.splitlines()
    rock_images = []
    for image in images:
        if 'localhost:32000' in image:
            rock_images.append(image)
    return rock_images

def get_docker_image_list():
    result = subprocess.run(['docker', 'images'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    images = output.splitlines()
    rock_images = []
    for image in images:
        if image.startswith('localhost:32000'):
            rock_images.append(image)
    return rock_images

def get_microk8s_image_id(rock: str):
    return rock.split()[0]

def get_docker_image_id(rock: str):
    return rock.split()[2]

def remove_microk8s_rock(image_id: str):
    print(f'removing image {image_id}')
    result = subprocess.run(['microk8s', 'ctr', 'image', 'remove', image_id], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode('utf-8')

def remove_docker_rock(rock: str):
    image_id = get_image_id(rock)
    print(f'removing image {image_id}')
    result = subprocess.run(['docker', 'rmi', '-f', image_id], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode('utf-8')
    if 'image is being used by running container' in output:
        container_name = output.split()[-1]
        print(f'removing container {container_name}')
        result = subprocess.run(['docker', 'rm', '-f', container_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(output.splitlines())
        result = subprocess.run(['docker', 'rmi', '-f', image_id], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode('utf-8')

    print(output)
if __name__ == '__main__':
    print('Current rocks')
    rocks = get_microk8s_image_list()
    for rock in rocks:
        print(rock)
    for rock in rocks:
        remove_microk8s_rock(get_microk8s_image_id(rock))

    print('Final rocks')
    rocks = get_microk8s_image_list()
    for rock in rocks:
        print(rock)
