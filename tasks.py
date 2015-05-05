import os
from fabric.api import cd, env, run, settings, sudo
from fabric.contrib.project import rsync_project


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TMP_DIR = '/tmp/tess'


def _rsync_web_content(local_dir, remote_dir):
    # --copy-links means copy the content from the symlink target
    # which means we'll copy the optimized archive, which is what
    # we want
    rsync_project(
        remote_dir,
        local_dir=local_dir,
        delete=True,
        extra_opts="--copy-links",
    )


def copy_content_to_pi():
    run('rm -rf {}'.format(TMP_DIR))
    run('mkdir {}'.format(TMP_DIR))

    webcontent = os.path.join(BASE_DIR, 'WebContent/')
    _rsync_web_content(TMP_DIR, webcontent)


def delete_old_content_on_pi():
    sudo('rm -rf /var/www/*')


def move_content_to_www():
    sudo('mv {}/* /var/www/'.format(TMP_DIR))


def git_clone_pull(code_dir, repo):
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            sudo("git clone %s %s" % (repo, code_dir))
    with cd(code_dir):
        sudo("git pull")


def link_apache_conf(vcs_path):
    apache_conf = 'tessindia.conf'
    vcs_apache_path = os.path.join(vcs_path, 'apache', env.apache)
    if env.linux == 'redhat':
        apache_conf_path = '/etc/httpd/conf.d'
        service = 'httpd'
    elif env.linux == 'debian':
        apache_conf_path = '/etc/apache2/sites-enabled'
        service = 'apache2'
    else:
        raise Exception('You need to set env.linux')

    with cd(apache_conf_path):
        sudo('rm -f {}'.format(apache_conf))
        sudo('ln -s {} {}'.format(vcs_apache_path, apache_conf))
    sudo('service {} reload'.format(service))
