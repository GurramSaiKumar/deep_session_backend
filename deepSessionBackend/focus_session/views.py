from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import NewFocusSession
from .serializers import FocusSessionSerializer


# 1️⃣ Start a session
class StartFocusSessionView(generics.CreateAPIView):
    serializer_class = FocusSessionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        active_session = NewFocusSession.objects.filter(user=request.user, status='active').first()
        if active_session:
            return Response({"detail": "You already have an active session."}, status=status.HTTP_400_BAD_REQUEST)

        goal_name = request.data.get('goal_name', '')
        target_duration = request.data.get('target_duration_seconds', 0)
        session = NewFocusSession.objects.create(
            user=request.user,
            goal_name=goal_name,
            target_duration_seconds=target_duration
        )
        return Response(FocusSessionSerializer(session).data, status=status.HTTP_201_CREATED)


# 2️⃣ End a session
class EndFocusSessionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        focus_session_id = request.data.get('focus_session_id')
        interrupted = request.data.get('interrupted', False)
        notes = request.data.get('notes', None)
        if not focus_session_id:
            return Response({"detail": "focus_session_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            session = NewFocusSession.objects.get(id=focus_session_id, user=request.user)
        except NewFocusSession.DoesNotExist:
            return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        if session.status != 'active':
            return Response({"detail": "Session already completed or paused."}, status=status.HTTP_400_BAD_REQUEST)

        session.end_time = timezone.now()
        session.complete_session(interrupted=interrupted, notes=notes)
        return Response(FocusSessionSerializer(session).data, status=status.HTTP_200_OK)


# 3️⃣ List user’s past sessions
class FocusSessionListView(generics.ListAPIView):
    serializer_class = FocusSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewFocusSession.objects.filter(
            user=self.request.user,
            is_deleted=False,
            status='completed').order_by('-start_time')
