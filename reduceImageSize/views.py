from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ImageUploadForm
from django.http import FileResponse, HttpResponse
from PIL import Image
from io import BytesIO
from .forms import ContactForm
from .models import Contact, CustomPage, Blog
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator


def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image.open(form.cleaned_data['image'])
            if image.mode != 'RGB':
                image = image.convert('RGB')

            output_format = form.cleaned_data['output_format']
            resize_mode = form.cleaned_data['resize_mode']
            is_manual_resize = form.cleaned_data['is_manual_resize']
            quality = form.cleaned_data['quality']

            if is_manual_resize:
                # Manuel olarak yeniden boyutlandırma seçildiğinde
                new_width = form.cleaned_data['width']
                new_height = form.cleaned_data['height']
            else:
                # Yüzde olarak yeniden boyutlandırma seçildiğinde
                resize_percentage = form.cleaned_data['resize_percentage'] / 100.0
                new_width = int(image.size[0] * resize_percentage)
                new_height = int(image.size[1] * resize_percentage)

            if is_manual_resize:
                if resize_mode == 'crop':
                    image = crop_center(image, new_width, new_height)
                elif resize_mode == 'fit':
                    image = fit(image, new_width, new_height)
                elif resize_mode == 'stretch':
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                # Otomatik yüzde olarak yeniden boyutlandırma seçildiğinde, sadece yeniden boyutlandırma yapılır
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Görüntüyü bir BytesIO akış nesnesine kaydet
            buffer = BytesIO()
            image.save(buffer, format=output_format, quality=quality)
            buffer.seek(0)

            # İndirme için bir dosya yanıtı oluştur
            mime_type = 'image/png' if output_format == 'PNG' else 'image/jpeg'
            file_ext = 'png' if output_format == 'PNG' else 'jpg'
            file_name = f'processed_image.{file_ext}'
            return FileResponse(buffer, as_attachment=True, filename=file_name, content_type=mime_type)
    else:
        form = ImageUploadForm(initial={'resize_mode': 'stretch', 'is_manual_resize': False})

    return render(request, 'index.html', {'form': form})


def crop_center(image, new_width, new_height):
    original_width, original_height = image.size
    top = (original_height - new_height) // 2
    left = (original_width - new_width) // 2
    right = (original_width + new_width) // 2
    bottom = (original_height + new_height) // 2
    return image.crop((left, top, right, bottom))


def fit(image, new_width, new_height):
    return image.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! We will reach out to you as soon as possible.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def custom_page(request, slug=None):
    content = get_object_or_404(CustomPage, slug=slug)
    return render(request, 'custom.html', {'content': content})


def blog(request):
    blog_list = Blog.objects.all().order_by('-publish')  # Assuming there's a date_posted field
    paginator = Paginator(blog_list, 10)  # Show 10 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj})


def blog_detail(request, slug=None):
    blogDetail = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'post': blogDetail})


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Allow: /",
        "Sitemap: https://www.reduceimagesizer.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
