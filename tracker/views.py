from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Complaint
from datetime import datetime 

# ১. হোমপেজ ভিউ
def home_view(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'tracker/home.html', {'complaints': complaints})

# ২. নতুন কমপ্লেইন সাবমিট করার ভিউ (ছবি ছাড়াই সাবমিট করার সুযোগসহ)
def add_complaint_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image') # ইমেজ না থাকলে এটি None থাকবে
        
        # এখানে শুধুমাত্র title এবং description থাকলেই সাবমিট হবে (image অপশনাল)
        if title and description:
            Complaint.objects.create(
                title=title,
                description=description,
                image=image # image None হলেও কোনো সমস্যা করবে না
            )
            return redirect('home')
            
    return render(request, 'tracker/add_complaint.html')

# ৩. কাস্টম অ্যাডমিন লগইন ভিউ
def admin_login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
        
    error_message = None
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        user = authenticate(request, username=username_input, password=password_input)
        if user is not None and user.is_staff: # শুধুমাত্র স্টাফ বা সুপারইউজাররা ঢুকতে পারবে
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error_message = "ভুল ইউজারনেম অথবা পাসওয়ার্ড!"
            
    return render(request, 'tracker/admin_login.html', {'error': error_message})

# ৪. কাস্টম অ্যাডমিন ড্যাশবোর্ড ভিউ (সিকিউরড: লগইন ছাড়া ঢোকা যাবে না)
@login_required(login_url='admin_login')
def custom_admin_dashboard(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # ডাইনামিক কাউন্ট হিসাব করা
    total_count = complaints.count()
    pending_count = complaints.filter(status='Pending').count()
    progress_count = complaints.filter(status='In Progress').count()
    resolved_count = complaints.filter(status='Resolved').count()

    today_date = datetime.now().strftime('%d %b, %Y')

    context = {
        'complaints': complaints,
        'total_count': total_count,
        'pending_count': pending_count,
        'progress_count': progress_count,
        'resolved_count': resolved_count,
        'today_date': today_date,
    }
    return render(request, 'tracker/admin_dashboard.html', context)

# ৫. স্ট্যাটাস আপডেট ভিউ
@login_required(login_url='admin_login')
def update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'In Progress', 'Resolved']:
            complaint.status = new_status
            complaint.save()
    return redirect('admin_dashboard')

# ৬. লগআউট ভিউ
def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')