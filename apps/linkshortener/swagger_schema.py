from drf_yasg import openapi


TEST_RESPONSE = \
    {
        200: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'test': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )
        )
    }
