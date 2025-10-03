from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet


class BaseAPIView(APIView):
    """
    this is base class for all APIViews.
    automatically captures input and stores in self.input
    """

    def initial(self, request, *args, **kwargs):
        logged_data = {}

        if request.method in ["POST", "PUT", "PATCH"]:
            logged_data = request.data.copy()
            if "password" in logged_data:
                logged_data["password"] = "********"
        elif request.method == ["GET", "DELETE"]:
            logged_data = request.query_params.dict()
        else:
            logged_data = {}

        request.input = logged_data

        return super().initial(request, *args, **kwargs)
