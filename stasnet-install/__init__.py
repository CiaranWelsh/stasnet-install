import os, glob
import subprocess
import requests
from tqdm import tqdm
import urllib.parse
import zipfile
from easygui import passwordbox

def download_url(url):
    """
    Downloads a url and saves to INSALL_DIRECTORY
    :param url:
    :return:
    """
    url_obj = urllib.parse.urlparse(url)
    fname = os.path.split(url_obj.path)[1]
    install_location = os.path.join(INSTALL_DIRECTORY, fname)

    if os.path.isfile(install_location):
        return install_location

    print(f'\ndownloading "{url}"\n')
    response = requests.get(url, stream=True)
    with open(install_location, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

    if not os.path.isfile(install_location):
        raise ValueError('could not download "{}"'.format(url))

    return install_location


# /home/ncw135/Documents/stasnet-install/__init__.py
def get_cln():
    """
    Download cln from weblink. I would also put this file into your
    own repository somewhere so that you can control the link, i.e. so
    it doesn't go out of date.
    :return:
    """
    url = r'https://www.ginac.de/CLN/cln-1.3.4.tar.bz2'
    return download_url(url)


def get_ginac():
    url = r'https://www.ginac.de/ginac-1.7.5.tar.bz2'
    return download_url(url)


def get_stasnet():
    url = r'https://itbgit.biologie.hu-berlin.de/dorel/MRA_project/-/archive/master/MRA_project-master.zip'
    return download_url(url)


def build_cln(cln_file):
    print('building cln')
    cln_dir = cln_file[:-4]
    if not os.path.isdir(cln_dir):
        os.makedirs(cln_dir)
        import tarfile
        tar = tarfile.open(cln_file, "r:bz2")
        tar.extractall(cln_dir)
        tar.close()

    cln_dir = os.path.join(cln_dir, os.path.split(cln_dir)[1][:-4])

    assert os.path.isdir(cln_dir)

    os.chdir(cln_dir)

    subprocess.check_call(['./configure'], shell=True)
    subprocess.check_call(['make'], shell=True)
    subprocess.check_call(['make', 'check'], shell=True)
    pwd = subprocess.Popen(['echo', PWD], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S', 'make', 'install'], stdin=pwd.stdout, stdout=subprocess.PIPE)
    output = cmd2.stdout.read().decode()
    print(output)


def build_ginac(ginac_file):
    print('building ginac')
    ginac_dir = ginac_file[:-4]
    if not os.path.isdir(ginac_dir):
        os.makedirs(ginac_dir)
        import tarfile
        tar = tarfile.open(ginac_file, "r:bz2")
        tar.extractall(ginac_dir)
        tar.close()

    ginac_dir = os.path.join(ginac_dir, os.path.split(ginac_dir)[1][:-4])

    assert os.path.isdir(ginac_dir)

    os.chdir(ginac_dir)
    subprocess.check_call(['./configure'], shell=True)
    subprocess.check_call(['make'], shell=True)
    subprocess.check_call(['make', 'check'], shell=True)
    pwd = subprocess.Popen(['echo', PWD], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S', 'make', 'install'], stdin=pwd.stdout, stdout=subprocess.PIPE)
    output = cmd2.stdout.read().decode()
    print(output)

def build_stasnet(stasnet_file):
    stasnet_dir = stasnet_file[:-4]
    if not os.path.isdir(stasnet_dir):
        zip_ref = zipfile.ZipFile(stasnet_file, 'r')
        zip_ref.extractall(os.path.dirname(stasnet_dir))
        zip_ref.close()
    os.chdir(stasnet_dir)
    subprocess.check_call(f'R CMD INSTALL ./', shell=True)


def main():
    cln_file = get_cln()
    ginac_file = get_ginac()
    stasnet_file = get_stasnet()
    build_cln(cln_file)
    build_ginac(ginac_file)
    build_stasnet(stasnet_file)


if __name__ == '__main__':
    PWD = passwordbox('[sudo] password:')

    INSTALL_DIRECTORY = os.path.dirname(__file__)
    main()

