from django.shortcuts import render
from django.views.decorators.cache import cache_control
from .models import *
from django.shortcuts import redirect
from datetime import datetime
from django.conf import settings
from django.contrib import messages
import secrets
import string
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import imgForm



# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userLogin(request): ##admin users
    if  request.method=='POST':
        email       = request.POST['email']
        password    = request.POST['password']
       
        var         = user_data.objects.all().filter(email=email,password=password)

        if var:
            for x in var:
                request.session['userId']=x.id
            return redirect('user-dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('user-login')
        
    else:
        if  request.session.has_key('userId'):
            return redirect('user-dashboard')
        else:
            return render(request,'users/pages/login.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userLogout(request):
    if request.session.has_key('userId'):
        del request.session['userId']

        userLogout(request)
    return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userDashboard(request):
    return render(request,'users/pages/dashboard.html')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listEntityType(request):
    if request.session.has_key('userId'):
        entity_type_list    = entity_type.objects.all().order_by('-id')

        return render(request,'users/pages/list_entity_type.html',{'entity_type_list' : entity_type_list})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewEntityType(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            type            = request.POST['type']
            description     = request.POST['description']
            now             = datetime.now()

            insert_data     = entity_type(type=type,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-entity-type')
        else:
            return render(request,'users/pages/add_entity_type.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateEntityType(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            type_id         = request.POST['id']
            type            = request.POST['type']
            description     = request.POST['description']
            now             = datetime.now()

            entity_type.objects.all().filter(id=type_id).update(type=type,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-entity-type')
        else:
            type_id         = request.GET['id']
            type_data       = entity_type.objects.get(id=type_id)
            
            return render(request,'users/pages/update_entity_type.html',{'type_data' : type_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteEntityType(request):
    if request.session.has_key('userId'):
        type_id     = request.POST['id']
        fromReg     = entity_type.objects.all().filter(id=type_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-entity-type')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-entity-type')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listEntity(request):
    if request.session.has_key('userId'):
        entity_list = entity_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_entity.html',{'entity_list' : entity_list})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewEntity(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            name            = request.POST['name']
            type_id         = request.POST['type_id']
            description     = request.POST['description']
            now             = datetime.now()

            get_entity_type = entity_type.objects.get(id=type_id)

            insert_data     = entity_data(name=name,entity_type_id=get_entity_type,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-entity')
        else:
            entity_types    = entity_type.objects.all()
            return render(request,'users/pages/add_entity.html',{'entity_types' : entity_types})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateEntity(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            entity_id       = request.POST['id']
            name            = request.POST['name']
            type_id         = request.POST['type_id']
            description     = request.POST['description']
            now             = datetime.now()

            get_entity_type = entity_type.objects.get(id=type_id)

            entity_data.objects.all().filter(id=entity_id).update(name=name,entity_type_id=get_entity_type,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-entity')
        else:
            entity_id       = request.GET['id']
            get_entity_data = entity_data.objects.get(id=entity_id)
            entity_types    = entity_type.objects.all()
            
            return render(request,'users/pages/update_entity.html',{'entity_data' : get_entity_data,'entity_types':entity_types})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteEntity(request):
    if request.session.has_key('userId'):
        entity_id   = request.POST['id']
        fromReg     = entity_data.objects.all().filter(id=entity_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-entity')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-entity')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listBanch(request):
    if request.session.has_key('userId'):
        branch_list = branch_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_branch.html',{'branch_list' : branch_list})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewBranch(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            name            = request.POST['name']
            entity_id       = request.POST['entity_id']
            branch_code     = request.POST['branch_code']
            address         = request.POST['address']
            city            = request.POST['city']
            state           = request.POST['state']
            country         = request.POST['country']
            pincode         = request.POST['pincode']

            now             = datetime.now()

            get_entity      = entity_data.objects.get(id=entity_id)

            insert_data     = branch_data(name=name,branch_code=branch_code,entity_id=get_entity,address=address,city=city,state=state,country=country,pincode=pincode,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-branch')
        else:
            get_entity      = entity_data.objects.all()

            latest_id       = 1 if not branch_data.objects.all().exists() else branch_data.objects.latest('id').id
            get_series      = series_data.objects.get(type="Branch")

            branch_code     = get_series.pre_text+str(latest_id)+get_series.post_text

            return render(request,'users/pages/add_branch.html',{'get_entity' : get_entity,'branch_code':branch_code})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateBranch(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id       = request.POST['id']
            entity_id       = request.POST['entity_id']
            name            = request.POST['name']
            branch_code     = request.POST['branch_code']
            address         = request.POST['address']
            city            = request.POST['city']
            state           = request.POST['state']
            country         = request.POST['country']
            pincode         = request.POST['pincode']
            now             = datetime.now()

            get_entity      = entity_data.objects.get(id=entity_id)

            branch_data.objects.all().filter(id=branch_id).update(name=name,branch_code=branch_code,entity_id=get_entity,address=address,city=city,state=state,country=country,pincode=pincode,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-branch')
        else:
            entity_id       = request.GET['id']
            get_branch_data = branch_data.objects.get(id=entity_id)
            get_entity_data = entity_data.objects.all()
            
            return render(request,'users/pages/update_branch.html',{'entity_data' : get_entity_data,'get_branch_data':get_branch_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteBranch(request):
    if request.session.has_key('userId'):
        branch_id   = request.POST['id']
        fromReg     = branch_data.objects.all().filter(id=branch_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-branch')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-branch')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listUserRole(request):
    if request.session.has_key('userId'):
        get_user_roles  = user_roles.objects.all().exclude(role="Super Admin").order_by('-id')

        return render(request,'users/pages/list_user_roles.html',{'get_user_roles' : get_user_roles})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewUserRole(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            role            = request.POST['role']
            description     = request.POST['description']
            now             = datetime.now()

            insert_data     = user_roles(role=role,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-user-roles')
        else:
            return render(request,'users/pages/add_user_role.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateUserRole(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            role_id         = request.POST['id']
            role            = request.POST['role']
            description     = request.POST['description']
            now             = datetime.now()

            user_roles.objects.all().filter(id=role_id).update(role=role,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-user-roles')
        else:
            role_id         = request.GET['id']
            role_data       = user_roles.objects.get(id=role_id)
            
            return render(request,'users/pages/update_user_role.html',{'role_data' : role_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteUserRole(request):
    if request.session.has_key('userId'):
        role_id     = request.POST['id']
        fromReg     = user_roles.objects.all().filter(id=role_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-user-roles')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-user-roles')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listUsers(request):
    if request.session.has_key('userId'):
        user_id     = request.session.get('userId')
        
        user_list   = user_data.objects.all().exclude(id=user_id).order_by('-id')

        return render(request,'users/pages/list_user.html',{'user_list' : user_list})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewUser(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            name                = request.POST['name']
            email               = request.POST['email']
            user_role_id        = request.POST['user_role_id']
            branch_id           = request.POST['branch_id']
            image_file          = imgForm(request.POST,request.FILES)
            now                 = datetime.now()

            get_user            = user_data.objects.all().filter(email=email)
            if get_user:
                messages.error(request, 'Email already exist')
                return redirect('list-user')

            get_branch          = branch_data.objects.get(id=branch_id)
            get_entity          = get_branch.entity_id
            get_user_role       = user_roles.objects.get(id=user_role_id)

            characters          = string.ascii_letters + string.digits
            random_string       = ''.join(secrets.choice(characters) for _ in range(8))

            password            = random_string
            hash_password       = make_password(password)
            
            profile_image       = None

            if image_file.is_valid():
                profile_image   = image_file.cleaned_data['image']

            insert_data         = user_data(name=name,email=email,branch_id=get_branch,entity_id=get_entity,user_role_id=get_user_role,password=hash_password,profile_image=profile_image,created_at=now,updated_at=now)
            insert_data.save()

            ### send email
            template            = 'email/password.html'
            send_email          = sendEmail(email,template,random_string)

            messages.success(request, 'Successfully added.')
            return redirect('list-user')
        else:
            list_branch         = branch_data.objects.all()
            get_user_roles      = user_roles.objects.all().exclude(role="Super Admin")
            return render(request,'users/pages/add_user.html',{'list_branch' : list_branch,'get_user_roles':get_user_roles})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateUser(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            user_id             = request.POST['id']
            name                = request.POST['name']
            email               = request.POST['email']
            user_role_id        = request.POST['user_role_id']
            branch_id           = request.POST['branch_id']
            active              = True if request.POST.get('active') == 'true' else False
            image_file          = imgForm(request.POST,request.FILES)
            now                 = datetime.now()

            get_branch          = branch_data.objects.get(id=branch_id)
            get_entity          = get_branch.entity_id
            get_user_role       = user_roles.objects.get(id=user_role_id)

            if image_file.is_valid():
                image                   = image_file.cleaned_data['image']
                mymodel                 = user_data.objects.get(id=user_id)
                mymodel.profile_image   = image
                mymodel.save()

            user_data.objects.all().filter(id=user_id).update(name=name,email=email,branch_id=get_branch,entity_id=get_entity,user_role_id=get_user_role,active=active,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-user')
        else:
            user_id             = request.GET['id']
            list_branch         = branch_data.objects.all()
            get_user_roles      = user_roles.objects.all().exclude(role="Super Admin")

            get_user_data       = user_data.objects.get(id=user_id)
            
            return render(request,'users/pages/update_user.html',{'list_branch' : list_branch,'get_user_roles':get_user_roles,'get_user_data':get_user_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteUser(request):
    if request.session.has_key('userId'):
        user_id     = request.POST['id']
        fromReg     = user_data.objects.all().filter(id=user_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-user')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-user')
    else:
        return redirect('user-login')



def sendEmail(email,template,password):
    html_template   = template
    html_message    = render_to_string(html_template,  {'password': password})
    subject         = 'Welcome to Spree'
    email_from      = settings.EMAIL_HOST_USER
    recipient_list  = [email]
    message         = EmailMessage(subject, html_message, email_from, recipient_list)
    message.content_subtype = 'html'
    message.send()

    return



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listAccountingGroup(request):
    if request.session.has_key('userId'):
        get_groups  = accounting_group_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_accounting_group.html',{'get_groups' : get_groups})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewAccountingGroup(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            name                = request.POST['name']
            under_group         = None if not request.POST.get('group_id') else accounting_group_data.objects.get(id=request.POST.get('group_id'))
            nature              = request.POST.get('nature')
            description         = request.POST.get('description')
            affect_gross_profit = request.POST.get('affect_gross_profit')
            now                 = datetime.now()

            branch_id           = branch_data.objects.get(id=branch_id)
            

            insert_data         = accounting_group_data(branch_id=branch_id,name=name,under_group=under_group,nature=nature,description=description,affect_gross_profit=affect_gross_profit,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-accounting-group')
        else:
            list_branch     = branch_data.objects.all()
            list_all_group  = accounting_group_data.objects.all()

            return render(request,'users/pages/add_accounting_group.html',{'list_branch':list_branch,'list_all_group':list_all_group})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateAccountingGroup(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            group_id            = request.POST['id']
            branch_id           = request.POST['branch_id']
            name                = request.POST['name']
            under_group         = None if not request.POST.get('group_id') else accounting_group_data.objects.get(id=request.POST.get('group_id'))
            nature              = request.POST.get('nature')
            description         = request.POST.get('description')
            affect_gross_profit = request.POST.get('affect_gross_profit')
            now                 = datetime.now()

            accounting_group_data.objects.all().filter(id=group_id).update(branch_id=branch_id,name=name,under_group=under_group,nature=nature,description=description,affect_gross_profit=affect_gross_profit,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-accounting-group')
        else:
            group_id        = request.GET['id']
            group_data      = accounting_group_data.objects.get(id=group_id)

            list_branch     = branch_data.objects.all()
            list_all_group  = accounting_group_data.objects.all().exclude(id=group_id)
            
            return render(request,'users/pages/update_accounting_group.html',{'group_data' : group_data,'list_branch':list_branch,'list_all_group':list_all_group})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteAccountingGroup(request):
    if request.session.has_key('userId'):
        group_id    = request.POST['id']
        fromReg     = accounting_group_data.objects.all().filter(id=group_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-accounting-group')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-accounting-group')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listAccountingLedger(request):
    if request.session.has_key('userId'):
        get_data    = accounting_ledger_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_accounting_ledger.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewAccountingLedger(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            name                = request.POST['name']
            accounting_group_id = accounting_group_data.objects.get(id=request.POST.get('accounting_group_id'))
            opening_balance     = 0.00 if not request.POST.get('opening_balance') else request.POST.get('opening_balance')
            entry_type          = request.POST.get('entry_type')
            bill_by_bill        = request.POST.get('bill_by_bill')
            now                 = datetime.now()

            insert_data         = accounting_ledger_data(name=name,accounting_group_id=accounting_group_id,opening_balance=opening_balance,entry_type=entry_type,bill_by_bill=bill_by_bill,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-accounting-ledger')
        else:
            list_all_group  = accounting_group_data.objects.all()

            return render(request,'users/pages/add_accounting_ledger.html',{'list_all_group':list_all_group})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateAccountingLedger(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            name                = request.POST['name']
            accounting_group_id = accounting_group_data.objects.get(id=request.POST.get('accounting_group_id'))
            opening_balance     = request.POST.get('opening_balance')
            entry_type          = request.POST.get('entry_type')
            bill_by_bill        = request.POST.get('bill_by_bill')
            now                 = datetime.now()

            accounting_ledger_data.objects.all().filter(id=get_id).update(name=name,accounting_group_id=accounting_group_id,opening_balance=opening_balance,entry_type=entry_type,bill_by_bill=bill_by_bill,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-accounting-ledger')
        else:
            get_id          = request.GET['id']
            get_data        = accounting_ledger_data.objects.get(id=get_id)

            list_all_group  = accounting_group_data.objects.all()
            
            return render(request,'users/pages/update_accounting_ledger.html',{'get_data' : get_data,'list_all_group':list_all_group})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteAccountingLedger(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = accounting_ledger_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-accounting-ledger')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-accounting-ledger')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listFinancialYear(request):
    if request.session.has_key('userId'):
        get_data    = financial_year_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_financial_year.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewFinancialYear(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            from_date           = request.POST['from_date']
            to_date             = request.POST['to_date']
            now                 = datetime.now()

            branch_id           = branch_data.objects.get(id=branch_id)
            

            insert_data         = financial_year_data(branch_id=branch_id,from_date=from_date,to_date=to_date,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-financial-year')
        else:
            list_branch     = branch_data.objects.all()
            return render(request,'users/pages/add_financial_year.html',{'list_branch':list_branch})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateFinancialYear(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            from_date           = request.POST['from_date']
            to_date             = request.POST['to_date']
            active              = True if request.POST.get('active') == 'true' else False
            now                 = datetime.now()

            financial_year_data.objects.all().filter(id=get_id).update(branch_id=branch_id,from_date=from_date,to_date=to_date,active=active,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-financial-year')
        else:
            get_id          = request.GET['id']
            get_data        = financial_year_data.objects.get(id=get_id)

            list_branch     = branch_data.objects.all()
            
            return render(request,'users/pages/update_financial_year.html',{'get_data' : get_data,'list_branch':list_branch})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteFinancialYear(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = financial_year_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-financial-year')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-financial-year')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listSeries(request):
    if request.session.has_key('userId'):
        get_data    = series_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_series.html',{'get_data' : get_data})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewSeries(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            type                = request.POST['type']
            pre_text            = request.POST['pre_text']
            post_text           = request.POST['post_text']
            now                 = datetime.now()

            insert_data         = series_data(type=type,pre_text=pre_text,post_text=post_text,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-series')
        else:
            return render(request,'users/pages/add_series.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateSeries(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            pre_text            = request.POST['pre_text']
            post_text           = request.POST['post_text']
            now                 = datetime.now()

            series_data.objects.all().filter(id=get_id).update(pre_text=pre_text,post_text=post_text,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-series')
        else:
            get_id          = request.GET['id']
            get_data        = series_data.objects.get(id=get_id)

            return render(request,'users/pages/update_series.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteSeries(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = series_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-series')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-series')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listCustomerType(request):
    if request.session.has_key('userId'):
        customer_type_list  = customer_type.objects.all().order_by('-id')

        return render(request,'users/pages/list_customer_type.html',{'customer_type_list' : customer_type_list})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewCustomerType(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            type            = request.POST['type']
            description     = request.POST['description']
            now             = datetime.now()

            insert_data     = customer_type(type=type,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-customer-type')
        else:
            return render(request,'users/pages/add_customer_type.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateCustomerType(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            type_id         = request.POST['id']
            type            = request.POST['type']
            description     = request.POST['description']
            now             = datetime.now()

            customer_type.objects.all().filter(id=type_id).update(type=type,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-customer-type')
        else:
            type_id         = request.GET['id']
            type_data       = customer_type.objects.get(id=type_id)
            
            return render(request,'users/pages/update_customer_type.html',{'type_data' : type_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteCustomerType(request):
    if request.session.has_key('userId'):
        type_id     = request.POST['id']
        fromReg     = customer_type.objects.all().filter(id=type_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-customer-type')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-customer-type')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listLocation(request):
    if request.session.has_key('userId'):
        get_data    = location_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_location.html',{'get_data' : get_data})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewLocation(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            location        = request.POST['location']
            now             = datetime.now()

            insert_data     = location_data(location=location,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-location')
        else:
            return render(request,'users/pages/add_location.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateLocation(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id          = request.POST['id']
            location        = request.POST['location']
            now             = datetime.now()

            location_data.objects.all().filter(id=get_id).update(location=location,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-location')
        else:
            get_id          = request.GET['id']
            get_data        = location_data.objects.get(id=get_id)
            
            return render(request,'users/pages/update_location.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteLocation(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = location_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-location')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-location')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listCustomer(request):
    if request.session.has_key('userId'):
        get_data    = customer_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_customer.html',{'get_data' : get_data})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewCustomer(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            customer_type_id    = request.POST['customer_type_id']
            customer_type_id    = customer_type.objects.get(id=customer_type_id)
            name                = request.POST['name']
            phone               = request.POST.get('phone')
            email               = request.POST.get('email')
            customer_code       = request.POST.get('customer_code')
            location_id         = request.POST['location_id']
            location_id         = location_data.objects.get(id=location_id)
            opening_balance     = request.POST.get('opening_balance')
            entry_type          = request.POST.get('entry_type')
            bill_by_bill        = request.POST.get('bill_by_bill')
            credit_period       = request.POST.get('credit_period')
            credit_limit        = request.POST.get('credit_limit')
            address             = request.POST.get('address')
            city                = request.POST.get('city')
            state               = request.POST.get('state')
            country             = request.POST.get('country')
            pincode             = request.POST.get('pincode')
            account_number      = request.POST.get('account_number')
            branch_name         = request.POST.get('branch_name')
            branch_code         = request.POST.get('branch_code')
            tin                 = request.POST.get('tin')
            pan                 = request.POST.get('pan')
            cst                 = request.POST.get('cst')
            active              = True if request.POST.get('active') == 'true' else False
            now                 = datetime.now()

            insert_data         = customer_data(
                                        branch_id           = branch_id,
                                        customer_type_id    = customer_type_id,
                                        name                = name,
                                        phone               = phone,
                                        email               = email,
                                        customer_code       = customer_code,
                                        location_id         = location_id,
                                        opening_balance     = opening_balance,
                                        entry_type          = entry_type,
                                        bill_by_bill        = bill_by_bill,
                                        credit_period       = credit_period,
                                        credit_limit        = credit_limit,
                                        address             = address,
                                        city                = city,
                                        state               = state,
                                        country             = country,
                                        pincode             = pincode,
                                        account_number      = account_number,
                                        branch_name         = branch_name,
                                        branch_code         = branch_code,
                                        tin                 = tin,
                                        pan                 = pan,
                                        cst                 = cst,
                                        active              = active,
                                        created_at          = now,
                                        updated_at          = now
                                    )
            insert_data.save()

            accounting_group_id = accounting_group_data.objects.get(name="Sundry Deptor")
            insert_data         = accounting_ledger_data(name=name,accounting_group_id=accounting_group_id,opening_balance=0.00,entry_type='Dr',created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-customer')
        else:
            list_branch         = branch_data.objects.all()
            list_customer_type  = customer_type.objects.all()
            list_location       = location_data.objects.all()

            latest_id           = 1 if not customer_data.objects.all().exists() else customer_data.objects.latest('id').id
            get_series          = series_data.objects.get(type="Customer")

            customer_code       = get_series.pre_text+str(latest_id)+get_series.post_text

            return render(request,'users/pages/add_customer.html',{'list_branch':list_branch,'list_customer_type':list_customer_type,'list_location':list_location,'customer_code':customer_code})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateCustomer(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            customer_type_id    = request.POST['customer_type_id']
            customer_type_id    = customer_type.objects.get(id=customer_type_id)
            name                = request.POST['name']
            phone               = request.POST.get('phone')
            email               = request.POST.get('email')
            customer_code       = request.POST.get('customer_code')
            location_id         = request.POST['location_id']
            location_id         = location_data.objects.get(id=location_id)
            opening_balance     = request.POST.get('opening_balance')
            entry_type          = request.POST.get('entry_type')
            bill_by_bill        = request.POST.get('bill_by_bill')
            credit_period       = request.POST.get('credit_period')
            credit_limit        = request.POST.get('credit_limit')
            address             = request.POST.get('address')
            city                = request.POST.get('city')
            state               = request.POST.get('state')
            country             = request.POST.get('country')
            pincode             = request.POST.get('pincode')
            account_number      = request.POST.get('account_number')
            branch_name         = request.POST.get('branch_name')
            branch_code         = request.POST.get('branch_code')
            tin                 = request.POST.get('tin')
            pan                 = request.POST.get('pan')
            cst                 = request.POST.get('cst')
            active              = True if request.POST.get('active') == 'true' else False
            now                 = datetime.now()

            update_data         = customer_data.objects.all().filter(id=get_id).update(
                                        branch_id           = branch_id,
                                        customer_type_id    = customer_type_id,
                                        name                = name,
                                        phone               = phone,
                                        email               = email,
                                        customer_code       = customer_code,
                                        location_id         = location_id,
                                        opening_balance     = opening_balance,
                                        entry_type          = entry_type,
                                        bill_by_bill        = bill_by_bill,
                                        credit_period       = credit_period,
                                        credit_limit        = credit_limit,
                                        address             = address,
                                        city                = city,
                                        state               = state,
                                        country             = country,
                                        pincode             = pincode,
                                        account_number      = account_number,
                                        branch_name         = branch_name,
                                        branch_code         = branch_code,
                                        tin                 = tin,
                                        pan                 = pan,
                                        cst                 = cst,
                                        active              = active,
                                        created_at          = now,
                                        updated_at          = now
                                    )

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-customer')
        else:
            get_id              = request.GET['id']
            get_data            = customer_data.objects.get(id=get_id)

            list_branch         = branch_data.objects.all()
            list_customer_type  = customer_type.objects.all()
            list_location       = location_data.objects.all()

            return render(request,'users/pages/update_customer.html',{'get_data' : get_data,'list_branch':list_branch,'list_customer_type':list_customer_type,'list_location':list_location})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteCustomer(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = customer_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-customer')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-customer')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listSupplierType(request):
    if request.session.has_key('userId'):
        supplier_type_list  = supplier_type.objects.all().order_by('-id')

        return render(request,'users/pages/list_supplier_type.html',{'supplier_type_list' : supplier_type_list})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewSupplierType(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            type            = request.POST['type']
            description     = request.POST['description']
            now             = datetime.now()

            insert_data     = supplier_type(type=type,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-supplier-type')
        else:
            return render(request,'users/pages/add_supplier_type.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateSupplierType(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            type_id         = request.POST['id']
            type            = request.POST['type']
            description     = request.POST['description']
            now             = datetime.now()

            supplier_type.objects.all().filter(id=type_id).update(type=type,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-supplier-type')
        else:
            type_id         = request.GET['id']
            type_data       = supplier_type.objects.get(id=type_id)
            
            return render(request,'users/pages/update_supplier_type.html',{'type_data' : type_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteSupplierType(request):
    if request.session.has_key('userId'):
        type_id     = request.POST['id']
        fromReg     = supplier_type.objects.all().filter(id=type_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-supplier-type')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-supplier-type')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listSupplier(request):
    if request.session.has_key('userId'):
        get_data    = supplier_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_supplier.html',{'get_data' : get_data})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewSupplier(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            supplier_type_id    = request.POST['supplier_type_id']
            supplier_type_id    = supplier_type.objects.get(id=supplier_type_id)
            name                = request.POST['name']
            phone               = request.POST.get('phone')
            email               = request.POST.get('email')
            supplier_code       = request.POST.get('supplier_code')
            opening_balance     = request.POST.get('opening_balance')
            entry_type          = request.POST.get('entry_type')
            bill_by_bill        = request.POST.get('bill_by_bill')
            credit_period       = request.POST.get('credit_period')
            credit_limit        = request.POST.get('credit_limit')
            address             = request.POST.get('address')
            city                = request.POST.get('city')
            state               = request.POST.get('state')
            country             = request.POST.get('country')
            pincode             = request.POST.get('pincode')
            account_number      = request.POST.get('account_number')
            branch_name         = request.POST.get('branch_name')
            branch_code         = request.POST.get('branch_code')
            tin                 = request.POST.get('tin')
            pan                 = request.POST.get('pan')
            cst                 = request.POST.get('cst')
            active              = True if request.POST.get('active') == 'true' else False
            now                 = datetime.now()

            insert_data         = supplier_data(
                                        branch_id           = branch_id,
                                        supplier_type_id    = supplier_type_id,
                                        name                = name,
                                        phone               = phone,
                                        email               = email,
                                        supplier_code       = supplier_code,
                                        opening_balance     = opening_balance,
                                        entry_type          = entry_type,
                                        bill_by_bill        = bill_by_bill,
                                        credit_period       = credit_period,
                                        credit_limit        = credit_limit,
                                        address             = address,
                                        city                = city,
                                        state               = state,
                                        country             = country,
                                        pincode             = pincode,
                                        account_number      = account_number,
                                        branch_name         = branch_name,
                                        branch_code         = branch_code,
                                        tin                 = tin,
                                        pan                 = pan,
                                        cst                 = cst,
                                        active              = active,
                                        created_at          = now,
                                        updated_at          = now
                                    )
            insert_data.save()

            accounting_group_id = accounting_group_data.objects.get(name="Sundry Creditor")
            insert_data         = accounting_ledger_data(name=name,accounting_group_id=accounting_group_id,opening_balance=0.00,entry_type='Cr',created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-supplier')
        else:
            list_branch         = branch_data.objects.all()
            list_supplier_type  = supplier_type.objects.all()
            list_location       = location_data.objects.all()

            latest_id           = 1 if not supplier_data.objects.all().exists() else supplier_data.objects.latest('id').id
            get_series          = series_data.objects.get(type="Supplier")

            supplier_code       = get_series.pre_text+str(latest_id)+get_series.post_text

            return render(request,'users/pages/add_supplier.html',{'list_branch':list_branch,'list_supplier_type':list_supplier_type,'list_location':list_location,'supplier_code':supplier_code})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateSupplier(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            supplier_type_id    = request.POST['supplier_type_id']
            supplier_type_id    = supplier_type.objects.get(id=supplier_type_id)
            name                = request.POST['name']
            phone               = request.POST.get('phone')
            email               = request.POST.get('email')
            supplier_code       = request.POST.get('supplier_code')
            opening_balance     = request.POST.get('opening_balance')
            entry_type          = request.POST.get('entry_type')
            bill_by_bill        = request.POST.get('bill_by_bill')
            credit_period       = request.POST.get('credit_period')
            credit_limit        = request.POST.get('credit_limit')
            address             = request.POST.get('address')
            city                = request.POST.get('city')
            state               = request.POST.get('state')
            country             = request.POST.get('country')
            pincode             = request.POST.get('pincode')
            account_number      = request.POST.get('account_number')
            branch_name         = request.POST.get('branch_name')
            branch_code         = request.POST.get('branch_code')
            tin                 = request.POST.get('tin')
            pan                 = request.POST.get('pan')
            cst                 = request.POST.get('cst')
            active              = True if request.POST.get('active') == 'true' else False
            now                 = datetime.now()

            update_data         = supplier_data.objects.all().filter(id=get_id).update(
                                        branch_id           = branch_id,
                                        supplier_type_id    = supplier_type_id,
                                        name                = name,
                                        phone               = phone,
                                        email               = email,
                                        supplier_code       = supplier_code,
                                        opening_balance     = opening_balance,
                                        entry_type          = entry_type,
                                        bill_by_bill        = bill_by_bill,
                                        credit_period       = credit_period,
                                        credit_limit        = credit_limit,
                                        address             = address,
                                        city                = city,
                                        state               = state,
                                        country             = country,
                                        pincode             = pincode,
                                        account_number      = account_number,
                                        branch_name         = branch_name,
                                        branch_code         = branch_code,
                                        tin                 = tin,
                                        pan                 = pan,
                                        cst                 = cst,
                                        active              = active,
                                        created_at          = now,
                                        updated_at          = now
                                    )

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-supplier')
        else:
            get_id              = request.GET['id']
            get_data            = supplier_data.objects.get(id=get_id)

            list_branch         = branch_data.objects.all()
            list_supplier_type  = supplier_type.objects.all()
            list_location       = location_data.objects.all()

            return render(request,'users/pages/update_supplier.html',{'get_data' : get_data,'list_branch':list_branch,'list_supplier_type':list_supplier_type,'list_location':list_location})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteSupplier(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = supplier_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-supplier')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-supplier')
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listUnit(request):
    if request.session.has_key('userId'):
        get_data    = unit_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_unit.html',{'get_data' : get_data})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewUnit(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            unit                = request.POST['unit']
            description         = request.POST['description']
            formal_name         = request.POST['formal_name']
            no_of_decimal_place = request.POST['no_of_decimal_place']
            now                 = datetime.now()

            insert_data         = unit_data(unit=unit,description=description,formal_name=formal_name,no_of_decimal_place=no_of_decimal_place,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-unit')
        else:
            return render(request,'users/pages/add_unit.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateUnit(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            unit                = request.POST['unit']
            description         = request.POST['description']
            formal_name         = request.POST['formal_name']
            no_of_decimal_place = request.POST['no_of_decimal_place']
            now                 = datetime.now()

            unit_data.objects.all().filter(id=get_id).update(unit=unit,description=description,formal_name=formal_name,no_of_decimal_place=no_of_decimal_place,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-unit')
        else:
            get_id      = request.GET['id']
            get_data    = unit_data.objects.get(id=get_id)
            
            return render(request,'users/pages/update_unit.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteUnit(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = unit_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-unit')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-unit')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listSize(request):
    if request.session.has_key('userId'):
        get_data    = size_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_size.html',{'get_data' : get_data})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewSize(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            size                = request.POST['size']
            description         = request.POST['description']
            now                 = datetime.now()

            insert_data         = size_data(size=size,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-size')
        else:
            return render(request,'users/pages/add_size.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateSize(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            size                = request.POST['size']
            description         = request.POST['description']
            now                 = datetime.now()

            size_data.objects.all().filter(id=get_id).update(size=size,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-size')
        else:
            get_id      = request.GET['id']
            get_data    = size_data.objects.get(id=get_id)
            
            return render(request,'users/pages/update_size.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteSize(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = size_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-size')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-size')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listBrand(request):
    if request.session.has_key('userId'):
        get_data    = brand_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_brand.html',{'get_data' : get_data})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewBrand(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            name                = request.POST['name']
            description         = request.POST['description']
            manufacture         = request.POST['manufacture']
            now                 = datetime.now()

            insert_data         = brand_data(name=name,description=description,manufacture=manufacture,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-brand')
        else:
            return render(request,'users/pages/add_brand.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateBrand(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            name                = request.POST['name']
            description         = request.POST['description']
            manufacture         = request.POST['manufacture']
            now                 = datetime.now()

            brand_data.objects.all().filter(id=get_id).update(name=name,description=description,manufacture=manufacture,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-brand')
        else:
            get_id      = request.GET['id']
            get_data    = brand_data.objects.get(id=get_id)
            
            return render(request,'users/pages/update_brand.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteBrand(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = brand_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-brand')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-brand')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listModelNumber(request):
    if request.session.has_key('userId'):
        get_data    = model_number_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_model_number.html',{'get_data' : get_data})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewModelNumber(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            model_number        = request.POST['model_number']
            description         = request.POST['description']
            now                 = datetime.now()

            insert_data         = model_number_data(model_number=model_number,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-model-number')
        else:
            return render(request,'users/pages/add_model_number.html')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateModelNumber(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            model_number        = request.POST['model_number']
            description         = request.POST['description']
            now                 = datetime.now()

            model_number_data.objects.all().filter(id=get_id).update(model_number=model_number,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-model-number')
        else:
            get_id      = request.GET['id']
            get_data    = model_number_data.objects.get(id=get_id)
            
            return render(request,'users/pages/update_model_number.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteModelNumber(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = model_number_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-model-number')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-model-number')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listGodown(request):
    if request.session.has_key('userId'):
        get_data    = godown_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_godown.html',{'get_data' : get_data})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewGodown(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            name                = request.POST['name']
            description         = request.POST['description']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            now                 = datetime.now()

            insert_data         = godown_data(name=name,description=description,branch_id=branch_id,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-godown')
        else:
            list_branch = branch_data.objects.all()

            return render(request,'users/pages/add_godown.html',{'list_branch':list_branch})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateGodown(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            description         = request.POST['description']
            now                 = datetime.now()

            godown_data.objects.all().filter(id=get_id).update(name=name,description=description,branch_id=branch_id,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-godown')
        else:
            get_id      = request.GET['id']
            get_data    = godown_data.objects.get(id=get_id)
            
            list_branch = branch_data.objects.all()
            return render(request,'users/pages/update_godown.html',{'get_data' : get_data,'list_branch':list_branch})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteGodown(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = godown_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-godown')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-godown')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listRack(request):
    if request.session.has_key('userId'):
        get_data    = rack_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_rack.html',{'get_data' : get_data})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewRack(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            description         = request.POST['description']
            godown_id           = request.POST['godown_id']
            godown_id           = godown_data.objects.get(id=godown_id)
            now                 = datetime.now()

            insert_data         = rack_data(branch_id=branch_id,name=name,description=description,godown_id=godown_id,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-rack')
        else:
            list_branch     = branch_data.objects.all()
            godown_list     = godown_data.objects.all()

            return render(request,'users/pages/add_rack.html',{'list_branch':list_branch,'godown_list':godown_list})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateRack(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            description         = request.POST['description']
            godown_id           = request.POST['godown_id']
            godown_id           = godown_data.objects.get(id=godown_id)
            now                 = datetime.now()

            rack_data.objects.all().filter(id=get_id).update(branch_id=branch_id,name=name,description=description,godown_id=godown_id,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-rack')
        else:
            get_id      = request.GET['id']
            get_data    = rack_data.objects.get(id=get_id)
            
            list_branch = branch_data.objects.all()
            list_godown = godown_data.objects.all()

            return render(request,'users/pages/update_rack.html',{'get_data' : get_data,'list_branch':list_branch,'list_godown':list_godown})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteRack(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = rack_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-rack')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-rack')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listProductGroup(request):
    if request.session.has_key('userId'):
        get_groups  = product_group_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_product_group.html',{'get_groups' : get_groups})
    else:
        return redirect('user-login')




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewProductGroup(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            name                = request.POST['name']
            under_group         = None if not request.POST.get('group_id') else product_group_data.objects.get(id=request.POST.get('group_id'))
            description         = request.POST.get('description')
            now                 = datetime.now()

            insert_data         = product_group_data(name=name,under_group=under_group,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-product-group')
        else:
            list_all_group      = product_group_data.objects.all()

            return render(request,'users/pages/add_product_group.html',{'list_all_group':list_all_group})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateProductGroup(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            group_id            = request.POST['id']
            name                = request.POST['name']
            under_group         = None if not request.POST.get('group_id') else product_group_data.objects.get(id=request.POST.get('group_id'))
            description         = request.POST.get('description')
            now                 = datetime.now()

            product_group_data.objects.all().filter(id=group_id).update(name=name,under_group=under_group,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-product-group')
        else:
            group_id        = request.GET['id']
            group_data      = product_group_data.objects.get(id=group_id)

            list_all_group  = product_group_data.objects.all().exclude(id=group_id)
            
            return render(request,'users/pages/update_product_group.html',{'group_data' : group_data,'list_all_group':list_all_group})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteProductGroup(request):
    if request.session.has_key('userId'):
        group_id    = request.POST['id']
        fromReg     = product_group_data.objects.all().filter(id=group_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-product-group')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-product-group')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listPricingLevel(request):
    if request.session.has_key('userId'):
        get_data    = pricing_level_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_pricing_level.html',{'get_data' : get_data})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewPricingLevel(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            description         = request.POST['description']
            now                 = datetime.now()

            insert_data         = pricing_level_data(branch_id=branch_id,name=name,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-pricing-level')
        else:
            list_branch     = branch_data.objects.all()

            return render(request,'users/pages/add_pricing_level.html',{'list_branch':list_branch})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updatePricingLevel(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            description         = request.POST['description']
            now                 = datetime.now()

            pricing_level_data.objects.all().filter(id=get_id).update(branch_id=branch_id,name=name,description=description,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-pricing-level')
        else:
            get_id      = request.GET['id']
            get_data    = pricing_level_data.objects.get(id=get_id)
            
            list_branch = branch_data.objects.all()

            return render(request,'users/pages/update_pricing_level.html',{'get_data' : get_data,'list_branch':list_branch})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deletePricingLevel(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = pricing_level_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-pricing-level')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-pricing-level')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listProducts(request):
    if request.session.has_key('userId'):
        get_data    = product_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_product.html',{'get_data' : get_data})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewProduct(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            product_code        = request.POST['product_code']
            product_group_id    = request.POST['product_group_id']
            product_group_id    = product_group_data.objects.get(id=product_group_id)
            brand_id            = request.POST.get('brand_id')
            brand_id            = None if not brand_id else brand_data.objects.get(id=brand_id)
            unit_id             = request.POST.get('unit_id')
            unit_id             = None if not unit_id else unit_data.objects.get(id=unit_id)
            size_id             = request.POST.get('size_id')
            size_id             = None if not size_id else size_data.objects.get(id=size_id)
            model_number_id     = request.POST.get('model_number_id')
            model_number_id     = None if not model_number_id else model_number_data.objects.get(id=model_number_id)
            godown_id           = request.POST.get('godown_id')
            godown_id           = None if not godown_id else godown_data.objects.get(id=godown_id)
            rack_id             = request.POST.get('rack_id')
            rack_id             = None if not rack_id else godown_data.objects.get(id=rack_id)
            purchase_rate       = request.POST.get('purchase_rate')
            mrp                 = request.POST.get('mrp')
            sales_rate          = request.POST.get('sales_rate')
            reorder_level       = request.POST.get('reorder_level')
            minimum_stock       = request.POST.get('minimum_stock')
            maximum_stock       = request.POST.get('maximum_stock')
            tax                 = request.POST.get('tax')
            bom                 = request.POST.get('bom')
            bar_code            = request.POST.get('bar_code')
            now                 = datetime.now()

            insert_data         = product_data(
                                    branch_id       = branch_id,
                                    name            = name,
                                    product_code    = product_code,
                                    product_group_id= product_group_id,
                                    brand_id        = brand_id,
                                    unit_id         = unit_id,
                                    size_id         = size_id,
                                    model_number_id = model_number_id,
                                    godown_id       = godown_id,
                                    rack_id         = rack_id,
                                    purchase_rate   = purchase_rate,
                                    mrp             = mrp,
                                    sales_rate      = sales_rate,
                                    reorder_level   = reorder_level,
                                    minimum_stock   = minimum_stock,
                                    maximum_stock   = maximum_stock,
                                    tax             = tax,
                                    bom             = bom,
                                    bar_code        = bar_code,
                                    created_at      = now,
                                    updated_at      = now
                                )
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-product')
        else:
            list_branch         = branch_data.objects.all()
            list_product_group  = product_group_data.objects.all()
            list_brand          = brand_data.objects.all()
            list_unit           = unit_data.objects.all()
            list_size           = size_data.objects.all()
            list_model_numbers  = model_number_data.objects.all()
            list_godown         = godown_data.objects.all()
            list_rack           = rack_data.objects.all()

            latest_id           = 1 if not product_data.objects.all().exists() else product_data.objects.latest('id').id
            get_series          = series_data.objects.get(type="Product")

            product_code        = get_series.pre_text+str(latest_id)+get_series.post_text

            return render(request,'users/pages/add_product.html',{'list_branch':list_branch,'list_brand':list_brand,'list_product_group':list_product_group,'list_unit':list_unit,'list_size':list_size,'list_model_numbers':list_model_numbers,'list_godown':list_godown,'list_rack':list_rack,'product_code':product_code})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateProduct(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            product_code        = request.POST['product_code']
            product_group_id    = request.POST['product_group_id']
            product_group_id    = product_group_data.objects.get(id=product_group_id)
            brand_id            = request.POST.get('brand_id')
            brand_id            = None if not brand_id else brand_data.objects.get(id=brand_id)
            unit_id             = request.POST.get('unit_id')
            unit_id             = None if not unit_id else unit_data.objects.get(id=unit_id)
            size_id             = request.POST.get('size_id')
            size_id             = None if not size_id else size_data.objects.get(id=size_id)
            model_number_id     = request.POST.get('model_number_id')
            model_number_id     = None if not model_number_id else model_number_data.objects.get(id=model_number_id)
            godown_id           = request.POST.get('godown_id')
            godown_id           = None if not godown_id else godown_data.objects.get(id=godown_id)
            rack_id             = request.POST.get('rack_id')
            rack_id             = None if not rack_id else godown_data.objects.get(id=rack_id)
            purchase_rate       = request.POST.get('purchase_rate')
            mrp                 = request.POST.get('mrp')
            sales_rate          = request.POST.get('sales_rate')
            reorder_level       = request.POST.get('reorder_level')
            minimum_stock       = request.POST.get('minimum_stock')
            maximum_stock       = request.POST.get('maximum_stock')
            tax                 = request.POST.get('tax')
            bom                 = request.POST.get('bom')
            bar_code            = request.POST.get('bar_code')
            now                 = datetime.now()

            update_data         = product_data.objects.all().filter(id=get_id).update(
                                    branch_id       = branch_id,
                                    name            = name,
                                    product_code    = product_code,
                                    product_group_id= product_group_id,
                                    brand_id        = brand_id,
                                    unit_id         = unit_id,
                                    size_id         = size_id,
                                    model_number_id = model_number_id,
                                    godown_id       = godown_id,
                                    rack_id         = rack_id,
                                    purchase_rate   = purchase_rate,
                                    mrp             = mrp,
                                    sales_rate      = sales_rate,
                                    reorder_level   = reorder_level,
                                    minimum_stock   = minimum_stock,
                                    maximum_stock   = maximum_stock,
                                    tax             = tax,
                                    bom             = bom,
                                    bar_code        = bar_code,
                                    updated_at      = now
                                )

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-product')
        else:
            get_id              = request.GET['id']
            get_data            = product_data.objects.get(id=get_id)

            list_branch         = branch_data.objects.all()
            list_brand          = brand_data.objects.all()
            list_product_group  = product_group_data.objects.all()
            list_unit           = unit_data.objects.all()
            list_size           = size_data.objects.all()
            list_model_numbers  = model_number_data.objects.all()
            list_godown         = godown_data.objects.all()
            list_rack           = rack_data.objects.all()
            
            return render(request,'users/pages/update_product.html',{'get_data' : get_data,'list_branch':list_branch,'list_brand':list_brand,'list_unit':list_unit,'list_size':list_size,'list_model_numbers':list_model_numbers,'list_godown':list_godown,'list_rack':list_rack,'list_product_group':list_product_group})
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteProduct(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = product_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-product')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-product')
    else:
        return redirect('user-login')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listVoucherType(request):
    if request.session.has_key('userId'):
        get_data    = voucher_type_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_voucher_type.html',{'get_data' : get_data})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewVoucherType(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            description         = request.POST['description']
            type_of_voucher     = request.POST.get('type_of_voucher')
            type_of_voucher     = None if not type_of_voucher else voucher_type_data.objects.get(id=type_of_voucher)
            start_index         = request.POST.get('start_index')
            now                 = datetime.now()

            insert_data         = voucher_type_data(branch_id=branch_id,name=name,description=description,type_of_voucher=type_of_voucher,start_index=start_index,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-voucher-type')
        else:
            list_branch         = branch_data.objects.all()
            list_voucher_types  = voucher_type_data.objects.all()

            return render(request,'users/pages/add_voucher_type.html',{'list_branch':list_branch,'list_voucher_types':list_voucher_types})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateVoucherType(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            name                = request.POST['name']
            description         = request.POST['description']
            type_of_voucher     = request.POST.get('type_of_voucher')
            type_of_voucher     = None if not type_of_voucher else voucher_type_data.objects.get(id=type_of_voucher)
            start_index         = request.POST.get('start_index')
            now                 = datetime.now()

            voucher_type_data.objects.all().filter(id=get_id).update(branch_id=branch_id,name=name,description=description,type_of_voucher=type_of_voucher,start_index=start_index,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-voucher-type')
        else:
            get_id              = request.GET['id']
            get_data            = voucher_type_data.objects.get(id=get_id)
            
            list_branch         = branch_data.objects.all()
            list_voucher_types  = voucher_type_data.objects.all().exclude(id=get_id)

            return render(request,'users/pages/update_voucher_type.html',{'get_data' : get_data,'list_branch':list_branch,'list_voucher_types':list_voucher_types})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteVoucherType(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = voucher_type_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-voucher-type')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-voucher-type')
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def listTaxData(request):
    if request.session.has_key('userId'):
        get_data    = tax_data.objects.all().order_by('-id')

        return render(request,'users/pages/list_tax_data.html',{'get_data' : get_data})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addNewTaxData(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            tax                 = request.POST['tax']
            rate_perc           = request.POST.get('rate_perc')
            description         = request.POST['description']
            now                 = datetime.now()

            insert_data         = tax_data(branch_id=branch_id,tax=tax,rate_perc=rate_perc,description=description,created_at=now,updated_at=now)
            insert_data.save()

            messages.success(request, 'Successfully added.')
            return redirect('list-tax-data')
        else:
            list_branch         = branch_data.objects.all()

            return render(request,'users/pages/add_tax_data.html',{'list_branch':list_branch})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateTaxData(request):
    if request.session.has_key('userId'):
        if request.method=="POST":
            get_id              = request.POST['id']
            branch_id           = request.POST['branch_id']
            branch_id           = branch_data.objects.get(id=branch_id)
            tax                 = request.POST['tax']
            description         = request.POST['description']
            rate_perc           = request.POST.get('rate_perc')
            active              = True if request.POST.get('active') == 'true' else False
            now                 = datetime.now()

            tax_data.objects.all().filter(id=get_id).update(branch_id=branch_id,tax=tax,rate_perc=rate_perc,description=description,active=active,updated_at=now)

            messages.success(request, 'Changes successfully updated.')
            return redirect('list-tax-data')
        else:
            get_id              = request.GET['id']
            get_data            = tax_data.objects.get(id=get_id)
            
            list_branch         = branch_data.objects.all()

            return render(request,'users/pages/update_tax_data.html',{'get_data' : get_data,'list_branch':list_branch})
    else:
        return redirect('user-login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteTaxData(request):
    if request.session.has_key('userId'):
        get_id      = request.POST['id']
        fromReg     = tax_data.objects.all().filter(id=get_id)
        fromReg.delete()

        if fromReg.delete():
            messages.success(request, 'Successfully Deleted.')
            return redirect('list-tax-data')
        else:
            messages.error(request, 'Something went to wrong')
            return redirect('list-tax-data')
    else:
        return redirect('user-login')