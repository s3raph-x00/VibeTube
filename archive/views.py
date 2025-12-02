from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse, Http404, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .mongo_models import UserModel, PlaylistModel
import os
from pathlib import Path
from datetime import datetime
import mimetypes
import hashlib
import json

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'}

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def get_video_files(folder_path):
    videos = []
    if not os.path.exists(folder_path):
        return videos
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if Path(file).suffix.lower() in VIDEO_EXTENSIONS:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                
                try:
                    stat = os.stat(full_path)
                    videos.append({
                        'name': file,
                        'path': rel_path,
                        'size': format_size(stat.st_size),
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    })
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    
    return sorted(videos, key=lambda x: x['name'].lower())

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        
        if UserModel.username_exists(username):
            return render(request, 'archive/register.html', {'error': 'Username already exists'})
        
        UserModel.create(username, password, email)
        return redirect('login')
    
    return render(request, 'archive/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = UserModel.find_by_username(username)
        if user and UserModel.check_password(user, password):
            request.session['user_id'] = str(user['_id'])
            request.session['username'] = user['username']
            return redirect('index')
        else:
            return render(request, 'archive/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'archive/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

@login_required
def index(request):
    from django.middleware.csrf import get_token
    get_token(request)
    
    context = {
        'folder_path': settings.VIDEO_FOLDER,
        'username': request.session.get('username')
    }
    return render(request, 'archive/index.html', context)

@login_required
def get_videos(request):
    videos = get_video_files(settings.VIDEO_FOLDER)
    return JsonResponse(videos, safe=False)

@login_required
def serve_thumbnail(request, filename):
    try:
        import subprocess
        
        full_path = os.path.join(settings.VIDEO_FOLDER, filename)
        
        if not os.path.exists(full_path):
            raise Http404("Video not found")
        
        if not os.path.abspath(full_path).startswith(os.path.abspath(settings.VIDEO_FOLDER)):
            return HttpResponse("Access denied", status=403)

        video_hash = hashlib.md5(filename.encode()).hexdigest()
        thumb_path = os.path.join(settings.THUMBNAIL_FOLDER, f"{video_hash}.jpg")

        if os.path.exists(thumb_path):
            return FileResponse(open(thumb_path, 'rb'), content_type='image/jpeg')

        try:
            subprocess.run([
                'ffmpeg',
                '-i', full_path,
                '-ss', '00:00:03',
                '-vframes', '1',
                '-vf', 'scale=320:-1',
                '-y',
                thumb_path
            ], capture_output=True, timeout=10, check=True)
            
            if os.path.exists(thumb_path):
                return FileResponse(open(thumb_path, 'rb'), content_type='image/jpeg')
        except:
            pass
        
        from PIL import Image
        from io import BytesIO
        img = Image.new('RGB', (320, 180), color=(28, 33, 40))
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return HttpResponse(buffer, content_type='image/jpeg')
                
    except Exception as e:
        from PIL import Image
        from io import BytesIO
        img = Image.new('RGB', (320, 180), color=(28, 33, 40))
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return HttpResponse(buffer, content_type='image/jpeg')

@login_required
def serve_video(request, filename):
    try:
        full_path = os.path.join(settings.VIDEO_FOLDER, filename)
        
        if not os.path.exists(full_path):
            raise Http404("Video not found")
        
        if not os.path.abspath(full_path).startswith(os.path.abspath(settings.VIDEO_FOLDER)):
            return HttpResponse("Access denied", status=403)
        
        mime_type = mimetypes.guess_type(full_path)[0] or 'application/octet-stream'
        return FileResponse(open(full_path, 'rb'), content_type=mime_type)
    except Exception as e:
        return HttpResponse(str(e), status=500)

@login_required
@csrf_exempt
def create_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        playlist = PlaylistModel.create(
            request.session['user_id'],
            data['name'],
            data.get('description', '')
        )
        return JsonResponse({
            'id': str(playlist['_id']),
            'name': playlist['name'],
            'description': playlist['description'],
            'videos': playlist['videos']
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_playlists(request):
    playlists = PlaylistModel.find_by_user(request.session['user_id'])
    return JsonResponse([{
        'id': str(p['_id']),
        'name': p['name'],
        'description': p['description'],
        'videos': p['videos'],
        'video_count': len(p['videos'])
    } for p in playlists], safe=False)

@login_required
@csrf_exempt
def add_to_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        PlaylistModel.add_video(
            data['playlist_id'],
            request.session['user_id'],
            data['video']
        )
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def remove_from_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        PlaylistModel.remove_video(
            data['playlist_id'],
            request.session['user_id'],
            data['video_path']
        )
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def delete_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        PlaylistModel.delete(data['playlist_id'], request.session['user_id'])
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)
