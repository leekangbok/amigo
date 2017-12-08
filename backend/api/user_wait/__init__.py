import json

from backend.api.utils import refine_twisted_web_request
from backend.websocket import append_wait_user, delete_wait_user, get_wait_user, update_wait_user


class UserWait:
    @refine_twisted_web_request
    def user_wait_get_all(self, _):
        return json.dumps(get_wait_user())

    @refine_twisted_web_request
    def user_wait_create(self, request):
        user = json.load(request.content)
        append_wait_user(user)
        return json.dumps({'success': True})

    @refine_twisted_web_request
    def user_wait_delete(self, request, uid):
        delete_wait_user(uid)
        return json.dumps({'success': True})

    @refine_twisted_web_request
    def user_wait_update(self, request, uid):
        user = json.load(request.content)
        print('*' * 10)
        print(user)
        print('-' * 10)
        update_wait_user(user)
        return json.dumps({'success': True})


def add_user_wait_routes(app):
    user_wait = UserWait()
    app.route('/api/user_wait', methods=['GET'])(user_wait.user_wait_get_all)
    app.route('/api/user_wait', methods=['POST'])(user_wait.user_wait_create)
    app.route('/api/user_wait/<int:uid>', methods=['DELETE'])(user_wait.user_wait_delete)
    app.route('/api/user_wait/<int:uid>', methods=['PUT'])(user_wait.user_wait_update)
