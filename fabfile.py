import os
from fabric.api import env, sudo

from tasks import (
    delete_old_content_on_pi,
    copy_content_to_pi,
    move_content_to_www,
    git_clone_pull,
    _rsync_web_content,
    link_apache_conf,
)


def pi():
    env.user = 'pi'
    # host has to be set on the command line
    # variables for apache linking
    # env.apache = 'pi.conf'
    # env.linux = 'debian'


def mirror():
    if not env.hosts:
        env.hosts = ['lin-one.aptivate.org:48001']
    # variables for apache linking
    env.apache = 'pi_mirror.conf'
    env.linux = 'redhat'


def copy():
    pi()
    copy_content_to_pi()
    delete_old_content_on_pi()
    move_content_to_www()


def mirror_deploy():
    mirror()
    repo = 'git@git.aptivate.org:tessindia.git'
    base_dir = os.path.abspath(os.path.dirname(__file__))
    code_dir = '/var/www/tessindia/'
    content_relative_path = 'WebContent'

    git_clone_pull(code_dir, repo)

    local_webcontent = os.path.join(base_dir, content_relative_path) + '/'
    remote_webcontent = os.path.join(code_dir, content_relative_path)
    sudo("mkdir -p {}".format(remote_webcontent))
    sudo("chown -R {} {}".format(env.user, remote_webcontent))
    _rsync_web_content(local_webcontent, remote_webcontent)
    link_apache_conf(code_dir)
