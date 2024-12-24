from controllers.ApiController import ApiController

class UserBaseController (ApiController):
    def do_get(self):
        return { 'users': self.db_context.user_dao.get_all_users() }