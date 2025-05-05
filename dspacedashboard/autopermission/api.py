from threading import Thread

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dspacedashboard.autopermission.serializers import AutoPermissionUserSerializer

@api_view(['POST'])
def autopermission_create(request):
    serializer = AutoPermissionUserSerializer(data=request.data)
    if serializer.is_valid():
        permission_user = serializer.save()
        
        thread = Thread(target=permission_user.update_dspace_user)
        thread.start()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)