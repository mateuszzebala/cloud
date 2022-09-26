import os
import re
from os.path import exists
from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import File, Folder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import zipfile36 as zipfile

_render = render
def render(request, template, args, ct=None, st=None, us=None):
    message(request, "")
    args.update({"messages": request.session['messages'].copy()})
    request.session.pop('messages')

    return _render(request, template, args, content_type=ct, status=st, using=us)

def rename_extension(name_old, name_new):
    name_old_split = name_old.split(".")
    name_new_split = name_new.split(".")
    if len(name_old_split) > 1 and len(name_new_split) > 1:
        name_old_split[-1] = name_new_split[-1]
    else:
        return name_new
    name_new = ""
    for i in name_old_split:
        name_new += f"{i}"
        if i != name_old_split[-1]:
            name_new += '.'

    return name_new

def message(request, text, color='red'):
    mess = {'text':text, 'color':color}
    try:
        request.session['messages'].append(mess)
    except:
        request.session['messages'] = [mess]

def main(request):
    return redirect("index", id_folder=0)

def index(request, id_folder):
    if not request.user.is_authenticated:
        return redirect("login")
    back = False
    home = True
    if id_folder != 0:
        home = False
        folders = Folder.objects.filter(owner=request.user, parent=id_folder)
        files = File.objects.filter(owner=request.user, parent=id_folder)
        try:
            back = Folder.objects.filter(id=id_folder, owner=request.user).first().parent.id
        except:
            back = False
    else:
        folders = Folder.objects.filter(owner=request.user, parent=None)
        files = File.objects.filter(owner=request.user, parent=None)
    if not back:
        back = None
    active_folder = Folder.objects.filter(id=id_folder).first()
    if active_folder:
        active_folder_id = active_folder.id
    else:
        active_folder_id = 0

    return render(request, "index.html", {"folders": folders, "files": files, "back":back, "home":home, "active_folder":active_folder, "active_folder_id":active_folder_id})

def files(request, file_id):
    file = File.objects.filter(id=file_id).first()
    if file.owner == request.user:
        return FileResponse(open(f"{file.source.name}", "rb"))
    else:
        return render(request, "404.html")

def login_user(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        if request.POST.get('login') is not None and request.POST.get('password') is not None:
            username = request.POST.get('login')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)           
                return redirect('main')
    return render(request, 'login.html', {})

def add_number(name, number=0):
    sp = name.split(".")
    if len(sp) > 1:
        name = "".join([*sp[:-1], f"_{number}.", f"{sp[-1]}"])
    else:
        name = "".join([*sp, f"_{number}"])
    return name


def register(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        username = request.POST.get('login')
        if User.objects.filter(username=username).first():
            message(request, 'Username is in use')
            return redirect('register')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            message(request, 'Type valid e-mail')
            return redirect('register')
        if User.objects.filter(email=email).first():
            message(request, 'E-mail is in use')
            return redirect('register')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if password1 == password2:
            user = User(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()
            if not user:
                message(request, 'Server error')
                return redirect('register')
            login(request, user)        
            return redirect('main')
        else:
            message(request, 'Passwords have to be the same')
            return redirect('register')
    return render(request, 'register.html', {})


def logout_user(request):
    logout(request)
    return redirect('main')

def edit_file(request, file):
    file = File.objects.filter(id=file).first()
    if file.owner != request.user:
        message(request, "File is not yours")
        return redirect('main')
    if request.method == "POST":
        if request.POST.get('file_content') is not None and request.POST.get('file_id') is not None:
            content = request.POST.get('file_content').rstrip()
            file_id = request.POST.get('file')
            content = content.split('\r')
            ctnt = ""
            for line in content:
                line.rstrip()
                ctnt += line
            content = ctnt
            
            with open(file.source.path, "w") as active_file:
                active_file.write(content)
    
    if not file.is_binary():
        return render(request, 'edit.html', {'file': file})
    else:
        message(request, 'File is binary')
        return redirect('show', id=file.id)


def can_be_folder(name, parent, i):
    if i == 0 and len(Folder.objects.filter(name=name, parent=parent)) == 0:
        return name
    else:
        print(len(Folder.objects.filter(name=name, parent=parent)))
    if len(Folder.objects.filter(name=f"{name}_{i}", parent=parent)) >= 1:
        i+=1
        return can_be_folder(name, parent, i)
    else:
        
        return f"{name}_{i}"

def new_folder(request):
    id_folder = int(str(request.POST.get("parent")))
    name = request.POST.get("name")
    folder = Folder.objects.filter(id=id_folder, owner=request.user).first()
    if folder or id_folder == 0:
        if id_folder != 0:
            folder = Folder(owner=request.user, parent=folder, name=name)
        else:
            folder = Folder(owner=request.user, parent=None, name=name)
    folder.name = can_be_folder(folder.name, folder.parent, 0)
    folder.save()
    return redirect("index", id_folder=id_folder)

def change_file_name(user, name, i):
    fname = add_number(name, i)

    if exists(f'files/{user.id}/{fname}'):
        i+=1
        return change_file_name(user, name, i)
    else:
        return f"files/{user.id}/{fname}"

def can_be_name(name, parent, i):
    if i == 0 and len(File.objects.filter(parent=parent, name=f"{name}")) < 1:
        return f"{name}"
    if not len(File.objects.filter(parent=parent, name=add_number(name, i))) < 1:
        i+=1
        return can_be_name(name, parent, i)
    else:
        return add_number(name, i)

def new_file(request):
    id_folder = int(str(request.POST.get("parent")))
    files = request.FILES.getlist('file')
    print(len(files))
    for file in files:
        folder = Folder.objects.filter(id=id_folder, owner=request.user).first()
        name = file.name

        if folder or id_folder == 0:
            if id_folder == 0:
                folder = None
            file = File(owner=request.user, parent=folder, source=file)
            good_file_name = change_file_name(request.user, name, 0)
            file.name = can_be_name(name, folder, 0)
            file.save()
            os.rename(f"{file.source}", f"{good_file_name}")
            file.source = good_file_name
            file.save()
    return redirect("index", id_folder=id_folder)


def delete(request):
    to_delete = None
    f = request.POST.get('id')
    if request.POST.get('ff') == 'folder':
        to_delete = Folder.objects.filter(id=f).first()
    elif request.POST.get('ff') == 'file':
        to_delete = File.objects.filter(id=f).first()
        os.remove(to_delete.source.path)
    try:
        parent_id=to_delete.parent.id
    except:
        parent_id = 0
    to_delete.delete()
    return redirect('index', id_folder=parent_id)


def rename_file(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('file')
        file = File.objects.filter(id=id).first()
        new_name = rename_extension(file.filename(), name)
        os.rename(f"{file.source}", f"files/{file.owner.id}/{new_name}")
        file.source = f"files/{file.owner.id}/{new_name}"
        file.save()
        if file:
            file.name = can_be_name(name, file.parent, 0)
            file.save()
    
            
    return redirect('index', id_folder=file.locate())

def rename_folder(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id=request.POST.get('folder')
        folder = Folder.objects.filter(id=id).first()
        if folder:
            folder.name = can_be_folder(name, folder.parent, 0)
            folder.save()
    return redirect('index', id_folder=folder.locate())

def create_file(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('parent')
        if id == '':
            return redirect('main')
        if name == '':
            return redirect('index', id_folder=id)
        if id == 0:
            folder = None
        else:
            folder = Folder.objects.filter(id=id).first()
        if not os.path.exists(f"files/{request.user.id}"):
            os.makedirs(f"files/{request.user.id}")
        if exists(f"files/{request.user.id}/{name}"):
            new_name = change_file_name(request.user, name, 0)
        else:
            new_name = f'files/{request.user.id}/{name}'
        with open(f"{new_name}", "w") as f:
            f.write("")

        file = File(owner=request.user, parent=folder, source = f'{new_name}')
        file.name = can_be_name(name, folder, 0)
        file.save()
        
    if id != 0:
        return redirect('index', id_folder=id)
    else:
        return redirect('main')




def add_files(folder_id, files_to_zip):
    folder = Folder.objects.filter(id=folder_id)
    for file in File.objects.filter(parent=folder_id):
        files_to_zip.append([file.source.path, file.name, file.artificial_path()])
    for folder in Folder.objects.filter(parent=folder_id):
        add_files(folder.id, files_to_zip)
    return files_to_zip

def download_folder(request, id):
    files_to_zip = []
    empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    with open(f'zips/{id}.zip', 'wb') as zip:
        zip.write(empty_zip_data)
    pth = f'zips/{id}.zip'
    zipObj = zipfile.ZipFile(pth, "w")
    files_to_zip = add_files(id, files_to_zip)
    for file in files_to_zip:
        print(file)
        zipObj.write(file[0], str(file[2]))
        
    zipObj.close()
    return FileResponse(open(pth, 'rb'))

def create_folder_if_doesnt_exist(name, parent, owner):
    folder = Folder.objects.filter(name=name, parent=parent, owner=owner).first()
    if not folder:
        folder = Folder(name=name, parent=parent, owner=owner)
        folder.save()
    return folder

def send_folder(request):
    if request.method == 'POST':
        id_folder = int(str(request.POST.get("parent")))
        list_of_items = request.FILES.getlist('folder')
        paths = request.POST.get('paths').split(';;;')
        root = File.objects.filter(id=id_folder, owner=request.user).first()
        files = []
        for file, path in zip(list_of_items, paths):
            path = path.split('/')
            name = file
            last_folder = None
            for p in range(len(path) - 1):
                if p == 0:
                    last_folder = create_folder_if_doesnt_exist(path[p], parent=root, owner=request.user)
                else:
                    last_folder = create_folder_if_doesnt_exist(path[p], parent=last_folder, owner=request.user)
            file = File(parent=last_folder, source=file, owner=request.user)
            file.name = can_be_name(name, last_folder, 0)
            file.save()
            files.append([file, path])
        return redirect('index', id_folder=id_folder)
    return redirect('main')


def show(request, id):
    if request.user.is_authenticated:
        file = File.objects.filter(id=id).first()
        if file:
            if file.owner == request.user:
                name = file.filename().lower()
                type = None
                if name.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    type = "Image"
                if name.endswith(('.mp3', '.wav', '.flac', '.aiff', '.dsd', '.ogg')):
                    type = "Music"
                if name.endswith(('.mp4', '.mov', '.avi', '.flv', '.wmv', '.avchd')):
                    type = "Video"
                if not file.is_binary():
                    type = "Text"

                back = file.parent
                if back is not None:
                    back = back.id
                return render(request, 'show.html', {"file":file, "type":type, "back":back})
            else:
                message(request, "File is not yours", "red")
                return redirect('main')
        else:
            message(request, "File doesn't exist", 'red')
            return redirect('main')
    else:
        message(request, "You're not logged in", 'red')
        return redirect('login')