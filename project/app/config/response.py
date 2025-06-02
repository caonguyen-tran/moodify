from rest_framework.response import Response

def success_response(data=None, message="Success"):
    return Response({
        "success": True,
        "data": data,
        "error": None,
        "message": message
    })

def error_response(error_detail, message="Error", status_code=400):
    return Response({
        "success": False,
        "data": None,
        "error": error_detail,
        "message": message
    }, status=status_code)