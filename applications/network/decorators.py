from functools import wraps

def handle_network_access(access_field):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            view = args[0]
            queryset = func(*args, **kwargs)
            if hasattr(view.queryset.model, "access_clients"):
                if queryset.filter(access_clients=True).exists():
                    return queryset
                else:
                    return queryset.none()

            return queryset.filter(**{access_field: True})

        return wrapper

    return decorator
