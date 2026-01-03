from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import ChatMessage, CourseComment
from .forms import MessageForm, CommentForm
from django.apps import apps

User = get_user_model()

@login_required
def chat_view(request, user_id=None):
    # --- AJAX: Get Unread Count ---
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('action') == 'unread_count':
        count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
        return JsonResponse({'unread_count': count})

    # --- AJAX: Handle Actions (Delete, Mark Unread) ---
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'delete_message':
                msg_id = data.get('message_id')
                # Ensure user owns the message
                msg = ChatMessage.objects.filter(id=msg_id, sender=request.user).first()
                if msg:
                    msg.delete()
                    return JsonResponse({'status': 'ok', 'deleted_id': msg_id})
                return JsonResponse({'status': 'error', 'message': 'Message not found'})
            
            if action == 'mark_unread':
                target_id = data.get('target_user_id')
                # Mark the last message from this user as unread
                last_msg = ChatMessage.objects.filter(sender_id=target_id, receiver=request.user).last()
                if last_msg:
                    last_msg.is_read = False
                    last_msg.save()
                    return JsonResponse({'status': 'ok'})
                return JsonResponse({'status': 'error', 'message': 'No messages to mark'})
        except json.JSONDecodeError:
            pass

    target_user = None
    if user_id:
        target_user = get_object_or_404(User, id=user_id)
        if not request.user.is_staff and not target_user.is_superuser:
            admin = User.objects.filter(is_superuser=True).first()
            if admin:
                return redirect('chat:chat_with', user_id=admin.id)
    
    # If no target user selected (e.g. admin viewing list), show contacts
    if not target_user:
        if request.user.is_staff:
            # Admins see students who messaged them
            contacts = User.objects.filter(
                id__in=ChatMessage.objects.filter(receiver=request.user).values_list('sender', flat=True)
            ).distinct()
        else:
            # Students see admins
            contacts = User.objects.filter(is_superuser=True)
            
        return render(request, 'chat/chat_list.html', {'contacts': contacts})

    # Chatting with target_user
    
    # --- AJAX Polling: Fetch new messages ---
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        last_id = request.GET.get('last_id', 0)
        new_msgs = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=target_user)) |
            (Q(sender=target_user) & Q(receiver=request.user)),
            id__gt=last_id
        ).order_by('timestamp')
        
        # Mark as read
        ChatMessage.objects.filter(sender=target_user, receiver=request.user, is_read=False).update(is_read=True)
        
        data = [{
            'id': msg.id,
            'message': msg.message,
            'sender_id': msg.sender.id,
            'timestamp': msg.timestamp.strftime('%H:%M')
        } for msg in new_msgs]
        return JsonResponse({'messages': data})
    # ----------------------------------------

    chat_history = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=target_user)) |
        (Q(sender=target_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    # Mark messages as read
    ChatMessage.objects.filter(sender=target_user, receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        # --- AJAX Send Message ---
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                msg_content = data.get('message')
            except:
                msg_content = None
            
            if msg_content:
                msg = ChatMessage.objects.create(
                    sender=request.user,
                    receiver=target_user,
                    message=msg_content
                )
                return JsonResponse({'status': 'ok', 'id': msg.id, 'message': msg.message, 'timestamp': msg.timestamp.strftime('%H:%M'), 'sender_id': msg.sender.id})
            return JsonResponse({'status': 'error'}, status=400)
        # -------------------------

        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = target_user
            msg.save()
            return redirect('chat:chat_with', user_id=target_user.id)
    else:
        form = MessageForm()

    return render(request, 'chat/chat_room.html', {
        'target_user': target_user,
        'chat_history': chat_history,
        'form': form
    })

@login_required
def add_comment(request, course_id):
    Course = apps.get_model('apply', 'Course')
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.course = course
            comment.save()
            # Redirect back to the previous page (Course Detail)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('/')

@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(CourseComment, id=comment_id)
    
    # Only owner can edit
    if comment.user != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # Redirect to the course page (using the comment's course ID if possible, or referer)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'chat/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(CourseComment, id=comment_id)
    
    # Owner or Staff can delete
    if comment.user == request.user or request.user.is_staff:
        comment.delete()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))