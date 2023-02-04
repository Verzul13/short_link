from rest_framework.response import Response
from rest_framework import status


def ValidationError(error: str):  # noqa
    return Response(data={"error": [error]},
                    status=status.HTTP_400_BAD_REQUEST)
