import os
from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=24)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def parents(self):
        parents = []
        active_parent = self
        while True:
            parents.append(active_parent)
            if active_parent.parent is not None:
                active_parent = active_parent.parent
            else:
                break
        parents.reverse()
        return parents
    
    def path(self):
        pth = '/'
        parents = self.parents()
        for parent in parents:
            pth += f'{parent.name}/'
        return pth
    


    def __str__(self):
        return f'{self.name}'

    def locate(self):
        if self.parent is not None:
            return self.parent.id
        else:
            return 0

class File(models.Model):
    def get_user_folder(self, filename):
        return f"files/{self.owner.id}/{filename}"

    name = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.FileField(upload_to=get_user_folder)
    date_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)


    def path(self):
        if self.parent is None:
            return f'{self.source.name}'
        else:
            return f'{self.parent.path()}/{self.filename()}'
    
    def artificial_path(self):
        if self.parent is None:
            return f'{self.source.name}'
        else:
            return f'{self.parent.path()}/{self.name}'

    def html(self):
        cntnt = ""
        with open(self.source.path, "r") as file:
            for line in file.readlines():
                cntnt += line + "<br>"
        return cntnt

    def content(self):
        cntnt = ""
        with open(self.source.path, "r") as file:
            for line in file.readlines():
                cntnt += line
        return cntnt

    def filename(self):
        name = os.path.basename(self.source.name)
        return name

    def is_binary(self):
        
        fin = open(self.source.path, 'rb')

        if os.stat(self.source.path).st_size == 0:
            return False
        
        try:
            CHUNKSIZE = 1024
            while True:
                chunk = fin.read(CHUNKSIZE)
                if b'\0' in chunk:
                    return True
                if len(chunk) < CHUNKSIZE:
                    break
        finally:
            fin.close()
        return False
        
    def __str__(self):
        return f'{self.source.name}'
    
    def locate(self):
        if self.parent is not None:
            return self.parent.id
        else:
            return 0

