from drf_yasg import openapi

record_post_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'date': openapi.Schema(type=openapi.FORMAT_DATE, description='date'),
        'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='amount'),
        'in_ex': openapi.Schema(type=openapi.TYPE_STRING, description='income/expense'),
        'method': openapi.Schema(type=openapi.TYPE_STRING, description='cash/card/transfer'),
        'memo': openapi.Schema(type=openapi.TYPE_STRING, description='memo'),
    }
)


record_modify_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='amount'),
        'memo': openapi.Schema(type=openapi.TYPE_STRING, description='memo'),
    }
)