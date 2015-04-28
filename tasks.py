from fabric.api import sudo, put, run


def delete_old_content_on_pi():
    sudo('rm -rf /var/www/tess')
    sudo('rm -f /var/www/index.html')


def copy_content_to_pi(srcdir):
    src = srcdir
    run('rm -rf /tmp/tess')
    run('mkdir /tmp/tess')
    if src[-1] != '/':
        src += '/'
    src += '*'
    put(src, '/tmp/tess')


def move_content_to_www():
    sudo('mv /tmp/tess /var/www/tess')


def link_first_page():
    echo_cmd = 'Redirect 302 /index.html /tess/openlearnworks/course/view.php%3fid=1911.html'
    sudo('rm -f /var/www/.htaccess')
    sudo('echo "%s" > /tmp/.htaccess' % echo_cmd)
    sudo('mv /tmp/.htaccess /var/www/.htaccess')
    sudo('chown root /var/www/.htaccess')
    sudo('service apache2 restart')
