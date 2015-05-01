from fabric.api import env

from tasks import (
    delete_old_content_on_pi, copy_content_to_pi, move_content_to_www,
)

env.user = 'pi'


def copy():
    copy_content_to_pi()
    delete_old_content_on_pi()
    move_content_to_www()
