class MasterSlaveRouter:
    def db_for_read(self, model, **hints):
        return "replica"  # Используем реплику для операций чтения

    def db_for_write(self, model, **hints):
        return "default"  # Используем мастер для операций записи

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"  # Разрешаем миграции только для мастера