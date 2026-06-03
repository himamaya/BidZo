from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserRegister
from django.contrib.auth.hashers import make_password, check_password
import re
from django.contrib.auth import logout
from .models import *
from django.db.models import Max, Count
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum
from django.db import transaction



def userregistration(request):

    if request.method == "POST":

        role = request.POST.get(
            'role', ''
        ).strip()

        first_name = request.POST.get(
            'first_name', ''
        ).strip()

        last_name = request.POST.get(
            'last_name', ''
        ).strip()

        email = request.POST.get(
            'email', ''
        ).strip()

        phone = request.POST.get(
            'phone', ''
        ).strip()

        image = request.FILES.get('image')

        address = request.POST.get(
            'address', ''
        ).strip()

        city = request.POST.get(
            'city', ''
        ).strip()

        state = request.POST.get(
            'state', ''
        ).strip()

        pincode = request.POST.get(
            'pincode', ''
        ).strip()

        password = request.POST.get(
            'password', ''
        ).strip()

        confirm_password = request.POST.get(
            'confirm_password', ''
        ).strip()

        id_proof = request.FILES.get(
            'id_proof'
        )

        # =========================
        # STORE FORM DATA
        # =========================

        context = {

            'data': request.POST

        }

        # =========================
        # ROLE VALIDATION
        # =========================

        if not role:

            context['role_error'] = \
            "Please select a role"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # EMPTY FIELD VALIDATION
        # =========================

        if not first_name:

            context['first_name_error'] = \
            "First name is required"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not last_name:

            context['last_name_error'] = \
            "Last name is required"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not email:

            context['email_error'] = \
            "Email is required"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not phone:

            context['phone_error'] = \
            "Phone number is required"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not address:

            context['address_error'] = \
            "Address is required"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not city:

            context['city_error'] = \
            "Please select city"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not state:

            context['state_error'] = \
            "Please select state"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not pincode:

            context['pincode_error'] = \
            "Pincode is required"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not password:

            context['password_error'] = \
            "Password is required"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not confirm_password:

            context['confirm_password_error'] = \
            "Confirm password is required"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # NAME VALIDATION
        # =========================

        if not first_name.isalpha():

            context['first_name_error'] = \
            "First name must contain letters only"

            return render(
                request,
                'userregistration.html',
                context
            )

        if not last_name.isalpha():

            context['last_name_error'] = \
            "Last name must contain letters only"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # EMAIL VALIDATION
        # =========================

        email_pattern = \
        r'^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,}$'

        if not re.match(
            email_pattern,
            email
        ):

            context['email_error'] = \
            "Invalid email format (lowercase only)"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # CAPITAL LETTER CHECK
        # =========================

        if email != email.lower():

            context['email_error'] = \
            "Email must be lowercase only"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # EMAIL EXISTS
        # =========================

        if UserRegister.objects.filter(
            email=email
        ).exists():

            context['email_error'] = \
            "Email already exists"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # PHONE VALIDATION
        # =========================

        if not phone.isdigit():

            context['phone_error'] = \
            "Phone number must contain digits only"

            return render(
                request,
                'userregistration.html',
                context
            )

        if len(phone) != 10:

            context['phone_error'] = \
            "Phone number must be 10 digits"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # PINCODE VALIDATION
        # =========================

        if not pincode.isdigit():

            context['pincode_error'] = \
            "Pincode must contain digits only"

            return render(
                request,
                'userregistration.html',
                context
            )

        if len(pincode) != 6:

            context['pincode_error'] = \
            "Pincode must be 6 digits"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # PASSWORD VALIDATION
        # =========================

        password_pattern = \
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{4,8}$'

        if not re.match(
            password_pattern,
            password
        ):

            context['password_error'] = \
            "Password must be 4 to 8 characters and contain uppercase, lowercase, number and special character"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # CONFIRM PASSWORD
        # =========================

        if password != confirm_password:

            context['confirm_password_error'] = \
            "Passwords do not match"

            return render(
                request,
                'userregistration.html',
                context
            )

        # =========================
        # SELLER VALIDATION
        # =========================

        if role in ['seller', 'both']:

            if not id_proof:

                context['id_proof_error'] = \
                "ID proof is required"

                return render(
                    request,
                    'userregistration.html',
                    context
                )

        # =========================
        # SAVE USER
        # =========================

        UserRegister.objects.create(

            role=role,

            first_name=first_name,
            last_name=last_name,

            email=email,
            phone=phone,

            image=image,

            address=address,
            city=city,
            state=state,

            pincode=pincode,

            password=make_password(password),

            id_proof=id_proof

        )

        messages.success(

            request,
            "Registration Successful"

        )

        return redirect(
            'userlogin'
        )

    return render(

        request,
        'userregistration.html'

    )
def userlogin(request):

    if request.method == "POST":

        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # =========================
        # EMPTY VALIDATION
        # =========================

        if not email or not password:

            messages.error(request,
            "All fields are required")

            return redirect('userlogin')

        # =========================
        # CHECK USER
        # =========================

        try:

            user = UserRegister.objects.get(email=email)

        except UserRegister.DoesNotExist:

            messages.error(request,
            "Invalid email")

            return redirect('userlogin')

        # =========================
        # PASSWORD CHECK
        # =========================

        if not check_password(password, user.password):

            messages.error(request,
            "Invalid password")

            return redirect('userlogin')

        # =========================
        # SESSION
        # =========================

        request.session['user_id'] = user.id
        request.session['user_name'] = user.first_name
        
        request.session['user_role'] = user.role

        # =========================
        # ROLE BASED LOGIN
        # =========================

        if user.role == "buyer":

           return redirect('buyerhome')

        elif user.role == "seller":

            return redirect('sellerdashboard')

        elif user.role == "both":

            return redirect('bothdashboard')

        elif user.role == "admin":
            return redirect('admindashboard')
    return render(request, 'userlogin.html')
def userdashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('userlogin')

    user = UserRegister.objects.get(id=user_id)

    return render(request, 'userdashboard.html', {'user': user})
def landing(request):

    return render(request, 'landing.html')


def profile(request):

    # ================= LOGIN CHECK =================
    if 'user_id' not in request.session:
        messages.error(request, "Please Login First")
        return redirect('/userlogin')

    try:
        user = UserRegister.objects.get(id=request.session['user_id'])

    except UserRegister.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('/userlogin')

    return render(request, 'profile.html', {
        'user': user,
        'role': user.role
    })





def editprofile(request):

    if 'user_id' not in request.session:
        messages.error(request, "Please Login First")
        return redirect('/userlogin')

    user = UserRegister.objects.get(id=request.session['user_id'])

    if request.method == "POST":

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        image = request.FILES.get('image')
        id_proof = request.FILES.get('id_proof')

        # ================= VALIDATIONS =================

        if not first_name.isalpha():
            messages.error(request, "First name must contain only letters")
            return redirect('editprofile')

        if not last_name.isalpha():
            messages.error(request, "Last name must contain only letters")
            return redirect('editprofile')

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            messages.error(request, "Invalid email format")
            return redirect('editprofile')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone must be 10 digits")
            return redirect('editprofile')

        if not pincode.isdigit() or len(pincode) != 6:
            messages.error(request, "Pincode must be 6 digits")
            return redirect('editprofile')

        # ================= UPDATE ONLY IF VALID =================

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.address = address
        user.city = city
        user.state = state
        user.pincode = pincode

        if image:
            user.image = image

        if user.role in ['seller', 'both'] and id_proof:
            user.id_proof = id_proof

        user.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    return render(request, 'editprofile.html', {'user': user})
def changepassword(request):

    # CHECK LOGIN
    if 'user_id' not in request.session:
        messages.error(request, "Please Login First")
        return redirect('/userlogin')

    user = UserRegister.objects.get(id=request.session['user_id'])

    # PASSWORD PATTERN (same as registration)
    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{4,8}$'

    if request.method == "POST":

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # ================= CURRENT PASSWORD CHECK =================
        if not check_password(current_password, user.password):
            messages.error(request, "Current Password is Incorrect")
            return redirect('changepassword')

        # ================= CONFIRM PASSWORD CHECK =================
        if new_password != confirm_password:
            messages.error(request, "New Password and Confirm Password do not match")
            return redirect('changepassword')

        # ================= REGEX PASSWORD VALIDATION =================
        if not re.match(password_pattern, new_password):
            messages.error(
                request,
                "Password must be 4-8 chars with uppercase, lowercase, number & special character"
            )
            return redirect('changepassword')

        # ================= UPDATE PASSWORD =================
        user.password = make_password(new_password)
        user.save()

        messages.success(request, "Password Changed Successfully")
        return redirect('profile')   # or userdashboard

    return render(request, 'changepassword.html')
# SELLER DASHBOARD

def sellerdashboard(request):

    if 'user_id' not in request.session:

        messages.error(request, "Please Login First")
        return redirect('/userlogin')

    
    seller = UserRegister.objects.get(
        id=request.session['user_id']
    )

    context = {

        'user': seller

    }

    return render(
        request,
        'sellerdashboard.html',
        context
    )
def logout_view(request):
    request.session.flush()   # clears all session data
    messages.success(request, "Logged out successfully")
    return redirect('/userlogin')
def bothdashboard(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('userlogin')

    user = UserRegister.objects.get(id=user_id)

    role = request.session.get('active_role', user.role)

    return render(request, 'bothdashboard.html', {
        'user': user,
        'role': role
    })


def admindashboard(request):

    user_id = request.session.get('user_id')

    
    if not user_id:
        return redirect('userlogin')

   
    try:
        user = UserRegister.objects.get(id=user_id)
    except UserRegister.DoesNotExist:
        return redirect('userlogin')

    
    if user.role != 'admin':
        return redirect('userlogin')

    
    total_users = UserRegister.objects.exclude(role='admin').count()

   
    try:
        total_products = Product.objects.count()
    except:
        total_products = 0

    context = {
        'user': user,
        'total_users': total_users,
        'total_products': total_products
    }

    return render(request, 'admindashboard.html', context)
# VIEW USERS

def viewusers(request):

    users = UserRegister.objects.exclude(role='admin')

    return render(request,
    'viewuser.html',
    {
        'users': users
    })


# BLOCK USER

def blockuser(request, id):

    user = UserRegister.objects.get(id=id)

    user.status = 'blocked'

    user.save()

    return redirect('viewusers')


# UNBLOCK USER

def unblockuser(request, id):

    user = UserRegister.objects.get(id=id)

    user.status = 'active'

    user.save()

    return redirect('viewusers')









def addproduct(request):

    # CHECK LOGIN

    if 'user_id' not in request.session:

        messages.error(request, "Please Login First")

        return redirect('/userlogin')

    # GET SELLER

    seller = UserRegister.objects.get(
        id=request.session['user_id']
    )

    # FETCH CATEGORIES

    categories = Category.objects.all()

    subcategories = SubCategory.objects.all()

    # FORM SUBMIT

    if request.method == "POST":

        category = Category.objects.get(
            id=request.POST.get('category')
        )

        subcategory = SubCategory.objects.get(
            id=request.POST.get('subcategory')
        )

        starting_bid = request.POST.get('starting_bid')

        Product.objects.create(

            seller=seller,

            product_name=request.POST.get('product_name'),

            description=request.POST.get('description'),

            condition=request.POST.get('condition'),

            category=category,

            subcategory=subcategory,

            starting_bid=starting_bid,

            current_bid=starting_bid,

            auction_end_time=request.POST.get('auction_end_time'),

            auction_status='live',

            product_image=request.FILES.get('product_image'),

        )

        messages.success(
            request,
            "Product Added Successfully"
        )

        return redirect('addproduct')

    # CONTEXT

    context = {

        'user': seller,

        'categories': categories,

        'subcategories': subcategories,

        'now': timezone.now(),

    }

    return render(

        request,

        'addproduct.html',

        context

    )
def pendingproducts(request):

    products = Product.objects.filter(
        status='pending'
    )

    context = {

        'products': products

    }

    return render(
        request,
        'pendingproducts.html',
        context
    )
def approveproduct(request, id):

    product = get_object_or_404(Product, id=id)

    product.status = 'approved'
    product.save()

    Notification.objects.create(
    user=product.seller,
    target_role='seller',
    notification_type='product_approved',
    title="Product Approved 🎉",
    message=f"Your product '{product.product_name}' has been approved."
)

    return redirect('pendingproducts')
def rejectproduct(request, id):

    product = get_object_or_404(Product, id=id)

    product.status = 'rejected'
    product.save()

    Notification.objects.create(
    user=product.seller,
    target_role='seller',
    notification_type='product_rejected',
    title="Product Rejected ❌",
    message=f"Your product '{product.product_name}' was rejected."
)

    return redirect('pendingproducts')


def myproducts(request):

    user_id = request.session.get('user_id')

    products = Product.objects.filter(
        seller_id=user_id
    )

    for product in products:

        bids = Bid.objects.filter(product=product)

        # highest bid (safe)
        highest_bid = bids.aggregate(
            Max('bid_amount')
        )['bid_amount__max']

        product.highest_bid = highest_bid or 0

        # total bids
        product.bid_count = bids.count()

        # auction ended
        product.is_ended = timezone.now() > product.auction_end_time

        # winner (ONLY if ended)
        if product.is_ended:

            highest_bid_obj = bids.order_by('-bid_amount', '-bid_time').first()

            product.winner = highest_bid_obj.bidder if highest_bid_obj else None

        else:

            product.winner = None

    return render(request, 'myproducts.html', {
        'products': products
    })
def edit_product(request, pid):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('userlogin')

    product = get_object_or_404(Product, id=pid, seller_id=user_id)

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    if request.method == "POST":

        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        product.category_id = request.POST.get('category')
        product.subcategory_id = request.POST.get('subcategory')
        product.condition = request.POST.get('condition')
        product.starting_bid = request.POST.get('starting_bid')
        product.auction_end_time = request.POST.get('auction_end_time')

        # image update only if new image uploaded
        if 'product_image' in request.FILES:
            product.product_image = request.FILES['product_image']

        product.save()

        return redirect('myproducts')

    return render(request, 'edit_product.html', {
        'product': product,
        'categories': categories,
        'subcategories': subcategories
    })


def delete_product(request, pid):

    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    # login check
    if not user_id:
        return redirect('userlogin')

    # =========================
    # ADMIN CAN DELETE ANY PRODUCT
    # =========================

    if user_role == 'admin':

        product = get_object_or_404(Product, id=pid)

        product.delete()

        return redirect('viewproduct')

    # =========================
    # SELLER CAN DELETE ONLY OWN PRODUCT
    # =========================

    else:

        product = get_object_or_404(
            Product,
            id=pid,
            seller_id=user_id
        )

        product.delete()

        return redirect('myproducts')
def viewproduct(request):

    # admin check
    if request.session.get('user_role') != 'admin':
        return redirect('userlogin')

    products = Product.objects.all().order_by('-created_at')

    return render(request, 'viewproduct.html', {
        'products': products
    })



def liveauctions(request):

    products = Product.objects.filter(

        status='approved',

        auction_end_time__gt=timezone.now()

    ).order_by('-created_at')

    context = {

        'products': products

    }

    return render(

        request,

        'liveauctions.html',

        context

    )


def auctiondetails(request, pid):

    # GET PRODUCT
    product = get_object_or_404(
        Product,
        id=pid
    )

    # GET BID HISTORY
    bids = Bid.objects.filter(
        product=product
    ).order_by('-bid_amount')

    # CHECK AUCTION STATUS
    auction_ended = product.auction_end_time < timezone.now()

    # GET WINNER
    winner = None

    if auction_ended and bids.exists():
        winner = bids.first()

    context = {
        'product': product,
        'bids': bids,
        'auction_ended': auction_ended,
        'winner': winner,
    }

    return render(
        request,
        'auctiondetails.html',
        context
    )
def placebid(request, pid):

    if 'user_id' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')

    if request.method == "POST":

        product = get_object_or_404(Product, id=pid)

        bidder = UserRegister.objects.get(id=request.session['user_id'])

        bid_amount = Decimal(request.POST.get('bid_amount'))

        current = product.current_bid or product.starting_bid

        minimum_bid = current + (current * Decimal('0.02'))

        if bid_amount < minimum_bid:
            messages.error(request, f"Next bid must be at least ₹{minimum_bid:.2f}")
            return redirect('auctiondetails', pid=pid)

        last_bid = Bid.objects.filter(product=product).order_by('-bid_time').first()

        if last_bid and last_bid.bidder == bidder:
            messages.error(request, "Wait for another bidder before bidding again")
            return redirect('auctiondetails', pid=pid)

        previous_highest = Bid.objects.filter(
            product=product
        ).order_by('-bid_amount', '-bid_time').first()

        Bid.objects.create(
            product=product,
            bidder=bidder,
            bid_amount=bid_amount
        )

        # =====================
        # NOTIFICATIONS
        # =====================

        # Buyer
        Notification.objects.create(
            user=bidder,
            notification_type='bid_success',
            target_role='buyer',
            title="Bid Placed Successfully",
            message=f"Your bid of ₹{bid_amount} has been placed on '{product.product_name}'."
        )

        # Seller
        Notification.objects.create(
            user=product.seller,
            notification_type='new_bid',
            target_role='seller',
            title="New Bid Received",
            message=f"{bidder.first_name} placed a bid of ₹{bid_amount} on '{product.product_name}'."
        )

        # Outbid
        if previous_highest and previous_highest.bidder != bidder:
            Notification.objects.create(
                user=previous_highest.bidder,
                notification_type='outbid',
                target_role='buyer',
                title="You Have Been Outbid",
                message=f"Another bidder placed a higher bid on '{product.product_name}'."
            )

        # ONLY update current bid
        product.current_bid = bid_amount
        product.bid_count += 1
        product.save()

        messages.success(request, "Bid placed successfully")

        return redirect('auctiondetails', pid=pid)

    return redirect('liveauctions')


def endedauctions(request):

    products = Product.objects.filter(
        auction_end_time__lt=timezone.now(),
        status='approved'
    )

    for product in products:

        # FIND HIGHEST BID
        highest_bid = Bid.objects.filter(
            product=product
        ).order_by(
            '-bid_amount',
            '-bid_time'
        ).first()

        # UPDATE PRODUCT DATA
        if highest_bid:

            product.winner = highest_bid.bidder
            product.current_bid = highest_bid.bid_amount
            product.auction_status = 'ended'

        else:

            product.winner = None
            product.current_bid = product.starting_bid
            product.auction_status = 'ended'

        # SEND NOTIFICATIONS ONLY ONCE
        if not product.auction_notification_sent:

            # =====================
            # AUCTION WITH BIDS
            # =====================
            if highest_bid:

                # WINNER NOTIFICATION
                Notification.objects.create(
                    user=highest_bid.bidder,
                    notification_type='auction_won',
                    target_role='buyer',
                    title="🏆 Congratulations! You Won",
                    message=f"You won the auction for '{product.product_name}' with ₹{highest_bid.bid_amount}."
                )

                # SELLER NOTIFICATION
                Notification.objects.create(
                    user=product.seller,
                    notification_type='auction_completed',
                    target_role='seller',
                    title="Auction Completed",
                    message=f"The auction for '{product.product_name}' has ended. Winner: {highest_bid.bidder.first_name}"
                )

                # LOSING BIDDERS
                losing_bidders = Bid.objects.filter(
                    product=product
                ).exclude(
                    bidder=highest_bid.bidder
                ).values_list(
                    'bidder',
                    flat=True
                ).distinct()

                for bidder_id in losing_bidders:

                    Notification.objects.create(
                        user_id=bidder_id,
                        notification_type='auction_lost',
                        target_role='buyer',
                        title="Auction Ended",
                        message=f"The auction for '{product.product_name}' has ended."
                    )

            # =====================
            # NO BIDS
            # =====================
            else:

                Notification.objects.create(
                    user=product.seller,
                    notification_type='auction_no_bids',
                    target_role='seller',
                    title="Auction Ended",
                    message=f"Your auction '{product.product_name}' ended with no bids."
                )

            product.auction_notification_sent = True

        # SAVE ALL CHANGES
        product.save()

    return render(
        request,
        'endedauctions.html',
        {
            'products': products
        }
    )
def viewbids(request, pid):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('userlogin')

    product = get_object_or_404(
        Product,
        id=pid,
        seller_id=user_id
    )

    bids = Bid.objects.filter(
        product=product
    ).select_related('bidder').order_by('-bid_amount')

    highest_bid = bids.first()

    winner = None
    auction_status = "Live"

    if product.  auction_end_time <= timezone.now():
        auction_status = "Ended"

        if highest_bid:
            winner = highest_bid.bidder

    context = {
        'product': product,
        'bids': bids,
        'highest_bid': highest_bid,
        'winner': winner,
        'auction_status': auction_status,
        'total_bids': bids.count(),
    }

    return render(request, 'sellerviewbids.html', context)
def mybids(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('userlogin')

    bids = Bid.objects.filter(
        bidder_id=user_id
    ).select_related(
        'product'
    ).order_by('-bid_time')

    return render(
        request,
        'mybids.html',
        {
            'bids': bids
        }
    )
def mywins(request):

    user_id = request.session.get('user_id')

    won_bids = []

    ended_products = Product.objects.filter(
        auction_end_time__lt=timezone.now()
    )

    for product in ended_products:

        highest_bid = Bid.objects.filter(
            product=product
        ).order_by('-bid_amount', '-bid_time').first()

        if highest_bid and str(highest_bid.bidder_id) == str(user_id):

            won_bids.append({
                'product': product,
                'bid_amount': highest_bid.bid_amount,
                'bid_time': highest_bid.bid_time,
            })

    return render(request, 'mywins.html', {
        'won_bids': won_bids
    })


def buyer_notifications(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('userlogin')

    notifications = Notification.objects.filter(
        user_id=user_id,
        target_role='buyer'   # ✅ better than filtering types
    ).order_by('-created_at')

    return render(request, 'buyer_notifications.html', {
        'notifications': notifications
    })
def seller_notifications(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('userlogin')

    notifications = Notification.objects.filter(
        user_id=user_id,
        target_role='seller'   # ✅ clean role-based filtering
    ).order_by('-created_at')

    return render(request, 'seller_notifications.html', {
        'notifications': notifications
    })
def ending_soon_auctions(request):

    now = timezone.now()
    next_24_hours = now + timedelta(hours=24)

    products = Product.objects.filter(
        status='approved',
        auction_end_time__gte=now,
        auction_end_time__lte=next_24_hours
    ).order_by('auction_end_time')

    return render(request, 'ending_soon.html', {
        'products': products
    })
def payment(request, oid):
    order = get_object_or_404(Order, id=oid)

    return render(request, 'payment.html', {
        'order': order
    })



def buyerhome(request):

    user_id = request.session.get('user_id')

    # Ending soon auctions
    ending_soon = Product.objects.filter(
        auction_end_time__gt=timezone.now(),
        auction_end_time__lte=timezone.now() + timedelta(hours=24)
    )

    won_products = []

    # Completed auctions
    ended_products = Product.objects.filter(
        auction_end_time__lt=timezone.now()
    )

    for product in ended_products:

        highest_bid = Bid.objects.filter(
            product=product
        ).order_by('-bid_amount', '-bid_time').first()

        if highest_bid and str(highest_bid.bidder_id) == str(user_id):

            won_products.append(product)

            # Show winner message only once per product
            session_key = f'winner_msg_{product.id}'

            if not request.session.get(session_key):

                messages.success(
                    request,
                    f"🏆 Congratulations! You won the auction for '{product.product_name}' with a bid of ₹{highest_bid.bid_amount}."
                )

                request.session[session_key] = True

    context = {
        'ending_soon': ending_soon,
        'won_products': won_products,
    }

    return render(
        request,
        'buyerhome.html',
        context
    )
def buyer_complaint(request):

    if request.method == "POST":

        Complaint.objects.create(
            user_id=request.session.get('user_id'),
            user_type='buyer',
            subject=request.POST.get('subject'),
            complaint=request.POST.get('complaint')
        )

        messages.success(
            request,
            "Complaint submitted successfully."
        )

        return redirect('buyer_complaint')

    complaints = Complaint.objects.filter(
        user_id=request.session.get('user_id'),
        user_type='buyer'
    ).order_by('-id')

    return render(
        request,
        'buyer_complaint.html',
        {
            'complaints': complaints
        }
    )
def seller_complaint(request):

    user_id = request.session.get('user_id')

    if request.method == "POST":

        Complaint.objects.create(
            user_id=user_id,
            user_type="seller",
            subject=request.POST.get('subject'),
            complaint=request.POST.get('complaint')
        )

        messages.success(request, "Complaint submitted successfully.")
        return redirect('seller_complaint')

    complaints = Complaint.objects.filter(
        user_id=user_id,
        user_type="seller"
    ).order_by('-id')

    return render(request, 'seller_complaint.html', {
        'complaints': complaints
    })
def category_page(request):

    categories = Category.objects.all()

    data = []

    for cat in categories:

        products = Product.objects.filter(category=cat)

        subcats = {}

        for p in products:

            # ✅ SAFE: use string of object (works always)
            subcat_name = str(p.subcategory)

            if subcat_name not in subcats:
                subcats[subcat_name] = []

            subcats[subcat_name].append(p)

        data.append({
            'category': cat,
            'subcategories': subcats
        })

    return render(request, 'category_page.html', {
        'data': data
    })
def admin_liveauctions(request):

    # only active (live) auctions
    products = Product.objects.filter(
        auction_end_time__gt=timezone.now()
    ).order_by('-auction_end_time')

    data = []

    for product in products:

        highest_bid = Bid.objects.filter(
            product=product
        ).order_by('-bid_amount', '-bid_time').first()

        data.append({
            'product': product,
            'highest_bid': highest_bid
        })

    return render(request, 'admin_liveauctions.html', {
        'data': data
    })
def admin_endedauctions(request):

    # auctions already ended
    products = Product.objects.filter(
        auction_end_time__lte=timezone.now()
    ).order_by('-auction_end_time')

    data = []

    for product in products:

        highest_bid = Bid.objects.filter(
            product=product
        ).order_by('-bid_amount', '-bid_time').first()

        data.append({
            'product': product,
            'highest_bid': highest_bid
        })

    return render(request, 'admin_endedauctions.html', {
        'data': data
    })
def delete_auction(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    product.delete()

    return redirect('admin_endedauctions')
from django.shortcuts import render, get_object_or_404, redirect
from .models import Complaint


def admin_complaints(request):

    # handle reply submit
    if request.method == "POST":

        complaint_id = request.POST.get('complaint_id')
        reply_text = request.POST.get('reply')

        complaint = get_object_or_404(Complaint, id=complaint_id)

        complaint.admin_reply = reply_text
        complaint.status = "Replied"
        complaint.is_read = False
        complaint.save()

        return redirect('admin_complaints')

    # list all complaints
    complaints = Complaint.objects.all().order_by('-created_at')

    return render(request, 'admin_complaints.html', {
        'complaints': complaints
    })