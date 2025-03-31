import os
import cv2
import math
import numpy as np
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MeasureInputSerializer
from datetime import datetime

def midpoint(p1, p2):
    return ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

def calculate_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def measure_and_label(image_path, ratio):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise Exception("No contours found")

    largest = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest)
    box = cv2.boxPoints(rect)
    box = box.astype(int)

    for i in range(4):
        pt1 = tuple(box[i])
        pt2 = tuple(box[(i + 1) % 4])
        length_px = calculate_distance(pt1, pt2)
        length_mm = length_px * ratio
        mid = midpoint(pt1, pt2)
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)
        cv2.putText(image, f"{length_mm:.2f} mm", mid,
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    # Save output
    base = os.path.basename(image_path)
    name, ext = os.path.splitext(base)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_name = f"{name}_labeled_{timestamp}.jpg"
    output_path = os.path.join(settings.MEDIA_ROOT, output_name)
    cv2.imwrite(output_path, image)

    return os.path.join(settings.MEDIA_URL, base), os.path.join(settings.MEDIA_URL, output_name)

class MeasureObjectView(APIView):
    def post(self, request):
        serializer = MeasureInputSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            ratio = serializer.validated_data['pixel_to_mm_ratio']

            # Ensure media directory exists
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            # Save uploaded image
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            original_name = f"uploaded_{timestamp}.jpg"
            original_path = os.path.join(settings.MEDIA_ROOT, original_name)
            with open(original_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            try:
                original_url, labeled_url = measure_and_label(original_path, ratio)
                return Response({
                    'original_image': request.build_absolute_uri(original_url),
                    'labeled_image': request.build_absolute_uri(labeled_url)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

