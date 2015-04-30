import os
from fabric.api import sudo, run
from fabric.contrib.project import rsync_project


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def copy_content_to_pi():
    run('rm -rf /tmp/tess')
    run('mkdir /tmp/tess')

    webcontent = os.path.join(BASE_DIR, 'WebContent/')
    # --copy-links means copy the content from the symlink target
    # which means we'll copy the optimized archive, which is what
    # we want
    rsync_project(
        '/tmp/tess',
        local_dir=webcontent,
        delete=True,
        extra_opts="--copy-links",
    )


def delete_old_content_on_pi():
    sudo('rm -rf /var/www/*')


def move_content_to_www():
    sudo('mv /tmp/tess/* /var/www/')
