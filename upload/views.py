from django.shortcuts import render,redirect
from django.views import View

from .models import Album,Document
from .forms import AlbumForm,DocumentForm

from django.contrib import messages

#import magic

ALLOWED_MIME    = [ "application/pdf" ]

class AlbumView(View):

    def get(self, request, *args, **kwargs):

        context             = {}
        context["albums"]   = Album.objects.all()

        return render(request,"upload/album.html",context)

    def post(self, request, *args, **kwargs):

        form    = AlbumForm(request.POST, request.FILES)
        
        if not form.is_valid():
            print("バリデーションNG")
            print(form.errors)
            return redirect("upload:album")

        print("バリデーションOK")
        form.save()

        return redirect("upload:album")

album   = AlbumView.as_view()

class DocumentView(View):

    def get(self, request, *args, **kwargs):

        context                 = {}
        context["documents"]    = Document.objects.all()


        document    = Document.objects.filter(id=1)

        if document:
            messages.info(request, document.file.url)

            with open(document.file.url, 'a') as f:
                f.write("追記されました\n")




        return render(request,"upload/document.html",context)

    def post(self, request, *args, **kwargs):

        form        = DocumentForm(request.POST,request.FILES)

        if not form.is_valid():
            print("バリデーションNG")
            print(form.errors)
            return redirect("upload:document")


        """
        mime_type   = magic.from_buffer(request.FILES["file"].read(1024) , mime=True)
        if not mime_type in ALLOWED_MIME:
            print("このファイルのMIMEは許可されていません。")
            print(mime_type)
            return redirect("upload:document")
        """


        print("バリデーションOK")
        form.save()

        return redirect("upload:document")

document    = DocumentView.as_view()

