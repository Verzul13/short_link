from drf_yasg import openapi


LIST_SHORT_LINK_PARAMETER = \
    {
        'responses': {
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='uuid'),
                    'long_url': openapi.Schema(type=openapi.TYPE_STRING, description='number'),
                    'subpart': openapi.Schema(type=openapi.TYPE_STRING, description='service'),
                }
            )
        },
    }


CREATE_SHORT_LINK_RESPONSE = \
    {
        'responses': {
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='uuid'),
                }
            )
        },
    }
