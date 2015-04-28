from fabric.api import env

from tasks import (
    delete_old_content_on_pi, copy_content_to_pi, move_content_to_www,
    link_first_page
)

env.user = 'pi'


def copy(srcdir):
    delete_old_content_on_pi()
    copy_content_to_pi(srcdir)
    move_content_to_www()
    link_first_page()
