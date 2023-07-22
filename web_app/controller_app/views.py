import socket
import csv
import time
from django.shortcuts import render
from datetime import datetime
from django.views.generic.base import View
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.models import User
from crccheck.crc import Crc16, CrcXmodem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import SLSCNetworkSettings
from django.http import HttpResponse
from django.views import View
from django.views.decorators.http import condition

from django.http import StreamingHttpResponse
from django.shortcuts import render
from .models import Satellite, SafeMode

@login_required
def satellite_list(request):
    satellites = Satellite.objects.all()
    return render(request, 'satellite_list.html', {'satellites': satellites})
@login_required
def get_satellite(request, satellite_id):
    slsc_ip_details = SLSCNetworkSettings.objects.first()
    if slsc_ip_details:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((slsc_ip_details.ip_address, int(slsc_ip_details.port_number)))

                command_to_slsc = bytearray([161, 2])
                crc_sha = Crc16.calc(command_to_slsc)
                command_to_slsc += crc_sha.to_bytes(2, "big")
                print(command_to_slsc)
                s.sendall(command_to_slsc)
                received_resp = s.recv(1000)
                if received_resp:
                    received_resp = received_resp.decode("utf-8")
                #received_resp = Crc16.calc(received_resp)
                print('Received', repr(received_resp))

            if received_resp:
                messages.success(request,
                                 'Get Satellite Command Sent. {}'.format(received_resp))


        except:
            messages.error(request, "Please check SLSC is not connecting..")
    else:
        messages.error(request, 'SLSC Is Not Configured. Please configure SLSC IP in Settings > SLSC Network Settings.')


    return redirect('satellite_list')

@login_required
def set_satellite(request, satellite_id):
    slsc_ip_details = SLSCNetworkSettings.objects.first()
    if slsc_ip_details:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((slsc_ip_details.ip_address, int(slsc_ip_details.port_number)))

                byte_code_cmd = bytearray([177, 1])

                satellite = Satellite.objects.get(id=satellite_id)
                sat_name = bytes(satellite.satellite_name, "utf-8")
                line1 = bytes(satellite.line1 + "\n", "utf-8")
                line2 = bytes(satellite.line2 + "\n", "utf-8")

                command_to_slsc = byte_code_cmd + sat_name + line1 + line2
                crc_sha = Crc16.calc(command_to_slsc)
                command_to_slsc += crc_sha.to_bytes(2, "big")
                print(command_to_slsc)
                s.sendall(command_to_slsc)
                received_resp = s.recv(10000)
                received_resp = Crc16.calc(received_resp)

            if not received_resp:
                messages.success(request,
                               'Set Satellite Command Sent.'.format(received_resp))
            else:
                messages.error(request,
                                 'Set Satellite Command Sent. But CRC Check Failed'.format(received_resp))
            print('Received', repr(data))
        except:
            messages.error(request, "Please check SLSC is not connecting..")
    else:
        messages.error(request, 'SLSC Is Not Configured. Please configure SLSC IP in Settings > SLSC Network Settings.')



    return redirect('satellite_list')

@login_required
def load_satellite(request, satellite_id):
    satellite = Satellite.objects.get(id=satellite_id)
    # Perform the "load satellite" action here
    return redirect('satellite_list')



data = '/Users/tracebackerror/Documents/GitHub/mccu_controller_web/oneoff/data.csv'


def stream_csv(request):
    def event_stream():
        # Replace 'path/to/your/csv/file.csv' with the actual path to your CSV file
        with open('/Users/tracebackerror/Documents/GitHub/mccu_controller_web/slsc/temp_data.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                yield 'data: {}\n\n'.format(",".join(row))
                #time.sleep(1)  # Delay between sending rows, adjust as needed

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['Content-Type'] = 'text/event-stream'
    response['X-Accel-Buffering'] = 'no'  # Disable buffering for nginx
    #response['Last-Modified'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    return response

@login_required
def restart_command(request):
    slsc_ip_details = SLSCNetworkSettings.objects.first()

    if slsc_ip_details:
        if request.method == "POST":
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((slsc_ip_details.ip_address, int(slsc_ip_details.port_number)))

                    msg = bytearray([177, 3])
                    crc = Crc16.calc(msg)
                    msg += crc.to_bytes(2, 'big')
                    print(msg)
                    s.sendall(msg)
                messages.success(request,
                               'Restart Command Sent.')
                print('Received', repr(data))
            except:
                messages.error(request, "Please check SLSC is not connecting..")
    else:
        messages.error(request, 'SLSC Is Not Configured. Please configure SLSC IP in Settings > SLSC Network Settings.')

    return redirect("/dashboard")


@login_required
def home_command(request):
    slsc_ip_details = SLSCNetworkSettings.objects.first()

    if slsc_ip_details:
        if request.method == "POST":
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((slsc_ip_details.ip_address, int(slsc_ip_details.port_number)))

                    msg = bytearray([177, 2])
                    crc = Crc16.calc(msg)
                    msg += crc.to_bytes(2, 'big')
                    print(msg)
                    s.sendall(msg)
                messages.success(request,
                               'Home Command Sent.')
                print('Received', repr(data))
            except:
                messages.error(request, "Please check SLSC is not connecting..")
    else:
        messages.error(request, 'SLSC Is Not Configured. Please configure SLSC IP in Settings > SLSC Network Settings.')

    return redirect("/dashboard")


@login_required
def safemode_command(request):
    slsc_ip_details = SLSCNetworkSettings.objects.first()

    if slsc_ip_details:
        if request.method == "POST":
            safe_mode_obj = SafeMode.objects.first()
            if safe_mode_obj and safe_mode_obj.password == request.POST.get("password", None):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                        s.connect((slsc_ip_details.ip_address, int(slsc_ip_details.port_number)))


                        msg = bytearray([177, 5])
                        crc = Crc16.calc(msg)
                        msg += crc.to_bytes(2, 'big')
                        print(msg)
                        s.sendall(msg)

                    messages.success(request,
                                   'SafeMode Command Sent.')
                except:
                    messages.error(request, "Please check SLSC is not connecting..")
            else:
                messages.error(request,
                                 'SafeMode Password Incorrect.')
    else:
        messages.error(request, 'SLSC Is Not Configured. Please configure SLSC IP in Settings > SLSC Network Settings.')

    return redirect("/dashboard")


@login_required
def shutdown_command(request):
    slsc_ip_details = SLSCNetworkSettings.objects.first()

    if slsc_ip_details:
        if request.method == "POST":
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((slsc_ip_details.ip_address, int(slsc_ip_details.port_number)))

                    msg = bytearray([177, 4])
                    crc = Crc16.calc(msg)
                    msg += crc.to_bytes(2, 'big')
                    print(msg)
                    s.sendall(msg)

                messages.success(request,
                               'Shutdown Command Sent.')
                print('Received', repr(data))
            except:
                messages.error(request, "Please check SLSC is not connecting..")
    else:
        messages.error(request, 'SLSC Is Not Configured. Please configure SLSC IP in Settings > SLSC Network Settings.')

    return redirect("/dashboard")

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = self.request.POST.get('old_password', None)
        new_password = self.request.POST.get('new_password', None)
        request.user.set_password('new password')
        request.user.save()
        messages.success(request, 'Your password has been successfully changed.')

    return render(request, 'body.html', {'form': form})



class MonitorPage(TemplateView):
    template_name = 'monitor.html'

    def get_context_data(self, **kwargs):
        kwargs = super(MonitorPage, self).get_context_data(**kwargs)

        #kwargs['foo'] = "bar"
        return kwargs

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # previous_foo = context['foo']
        # context['new_variable'] = 'new_variable' + ' updated'

        return self.render_to_response(context)


class LoginPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs = super(LoginPage, self).get_context_data(**kwargs)
        # Your code here
        kwargs['foo'] = "bar"
        return kwargs

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        username = self.request.POST.get('username', None)
        password = self.request.POST.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            messages.warning(request, "Incorrect username or password.")




        previous_foo = context['foo']
        context['new_variable'] = 'new_variable' + ' updated'

        return self.render_to_response(context)


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = "/"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        old_password = self.request.POST.get('old_password', None)
        new_password = self.request.POST.get('new_password', None)
        if request.user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()

            messages.success(request, 'Your password has been successfully changed.')
        else:
            messages.warning(request, 'Your old password is incorrect.')
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        kwargs = super(ProfilePage, self).get_context_data(**kwargs)
        kwargs["form"] = PasswordChangeForm(user=self.request.user)
        return kwargs



class DiagnosticPage(LoginRequiredMixin, TemplateView):
    template_name = 'diagnostic.html'
    login_url = "/"


class DashboardPage(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = "/"

    def get_context_data(self, **kwargs):
        kwargs = super(DashboardPage, self).get_context_data(**kwargs)

        kwargs['foo'] = "bar"
        return kwargs


def logout_view(request):
    logout(request)
    return redirect('/')



class SettingsPage(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'
    login_url = "/"

    def get_slsc_ip_details(self):
        port_number = ""
        ip_address = ["", "", "", ""]
        slsc_ip_details = SLSCNetworkSettings.objects.first()
        if slsc_ip_details:
            ip_address = slsc_ip_details.ip_address.split(".")
            ip_address = [each_ip_address for each_ip_address in ip_address if each_ip_address  != "."]
            port_number = slsc_ip_details.port_number


        return ip_address, port_number
    def get_context_data(self, **kwargs):
        kwargs = super(SettingsPage, self).get_context_data(**kwargs)
        slsc_ip, slsc_port = self.get_slsc_ip_details()
        kwargs['slsc_ip'] = slsc_ip
        kwargs['slsc_port'] = slsc_port
        return kwargs

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'slsc_settings_form' in request.POST:
            ip_address_1 = request.POST.get("ip_address_1").strip()
            ip_address_2 = request.POST.get("ip_address_2").strip()
            ip_address_3 = request.POST.get("ip_address_3").strip()
            ip_address_4 = request.POST.get("ip_address_4").strip()

            #ip_to_save = f"{ip_address_1}.{ip_address_2}.{ip_address_3}.{ip_address_4}"
            ip_to_save = "{}.{}.{}.{}".format(ip_address_1, ip_address_2, ip_address_3, ip_address_4)
            port = request.POST.get("port")
            SLSCNetworkSettings.objects.all().delete()
            models_to_save = SLSCNetworkSettings(ip_address=ip_to_save, port_number=port )
            models_to_save.save()

            messages.info(request, 'SLSC Network Settings is Saved.')

            slsc_ip, slsc_port = self.get_slsc_ip_details()

            kwargs['slsc_ip'] = slsc_ip
            kwargs['slsc_port'] = slsc_port
        return self.render_to_response(context)