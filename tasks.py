import os
from fabric.api import sudo, put, run


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def delete_old_content_on_pi():
    sudo('rm -rf /var/www/*')


def copy_content_to_pi(srcdir):
    src = srcdir
    run('rm -rf /tmp/tess')
    run('mkdir /tmp/tess')
    if src[-1] != '/':
        src += '/'
    src += '*'
    put(src, '/tmp/tess')

    webcontent = os.path.join(BASE_DIR, 'WebContent/*')
    put(webcontent, '/tmp/tess')  # Copy index.html with resources


def move_content_to_www():
    sudo('mv /tmp/tess/* /var/www/')


def link_first_page():
    echo_cmd = 'Redirect 302 /tess.html /openlearnworks/course/view.php%3fid=1911.html'
    sudo('rm -f /var/www/.htaccess')
    sudo('echo "%s" > /tmp/.htaccess' % echo_cmd)
    sudo('mv /tmp/.htaccess /var/www/.htaccess')
    sudo('chown root /var/www/.htaccess')
    sudo('service apache2 restart')
