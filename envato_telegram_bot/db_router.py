class DbRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'custom_logs':
            return 'log_db'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'custom_logs':
            return 'log_db'
        else:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'custom_logs':
            return db == 'log_db'
        else:
            return db == 'default'



