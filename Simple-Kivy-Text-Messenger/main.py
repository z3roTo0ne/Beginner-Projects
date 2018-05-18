from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from functools import partial
import threading
import socket
import re
import os
from kivy.config import Config


Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

# Find Address of Host
def find_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host_ip = s.getsockname()[0]
    s.close()
    return host_ip


# Find Free Port for Host
def find_free_port():
    s = socket.socket()
    s.bind(('', 0))            # Bind to a free port provided by the host.
    port = s.getsockname()[1]
    s.close()
    return port  # Return the port number assigned.


class All(BoxLayout):
    def __init__(self, **kwargs):
        super(All, self).__init__(**kwargs)

        # Setup socket
        self.host = find_host_ip()
        self.port = find_free_port()
        self.s = socket.socket()

        # Main UI of App
        # Orientation of main layout
        self.orientation = 'vertical'

        # Exit Button with 100% width and 100% height
        self.exit_btn = Button()
        self.exit_btn.text = 'Exit App'
        self.exit_btn.size_hint = 1, 0.1
        self.exit_btn.on_press = self.exit

        # Add Exit Button to Main BoxLayout
        self.add_widget(self.exit_btn)

        # Start App in Start Screen
        self.start_screen()

    # Start Screen Code
    def start_screen(self):

        # UI of main layout of Start Screen
        self.explanation_label = Label()
        self.explanation_label.text = """---How to use---\nThis is an experimental App which can be used to exchange text 
messages between to participants of an IPV4 Network.\n\nThe address of your device is: """ + self.host + ':' + str(self.port) + '\n'"""
If you want someone to call you with this App, you need to give the other participant your device address. Press Receive 
and wait for connections. Tell the other  participant to press Call on their device and to enter your address.
If successful you can start exchanging text with the other participant.\n\nIf you want to call someone press Call and 
enter their address while they wait for a connection by pressing Receive on their device.\n\n 
After you press call or receive you have to restart the app if you want to use the other button again."""
        self.explanation_label.size_hint = 1, 1.5

        # Navbar with 100% width and 10% height
        self.navbar = BoxLayout()
        self.navbar.orientation = 'horizontal'
        self.navbar.size_hint = 1, 0.1

        # Call Button with 50% width and 100% height
        self.call_btn = Button()
        self.call_btn.text = 'Call'
        self.call_btn.size_hint = 0.5, 1
        self.call_btn.on_press = self.caller

        # Receive Button with 50% width and 100% height
        self.receive_btn = Button()
        self.receive_btn.text = 'Receive'
        self.receive_btn.size_hint = 0.5, 1
        self.receive_btn.on_press = self.receiver

        # Add the 2 Buttons to Navbar
        self.explanation_label.text_size = 920, None
        self.add_widget(self.explanation_label)
        self.navbar.add_widget(self.call_btn)
        self.navbar.add_widget(self.receive_btn)
        self.add_widget(self.navbar)

    # Caller Code
    def caller(self):

        # UI of main layout of Caller
        self.horizontal_input_layout = BoxLayout()
        self.horizontal_input_layout.orientation = 'horizontal'
        self.address_input = TextInput()
        self.address_input.hint_text = 'Enter Address (Example: 192.168.1.27:9999)'
        self.address_input.size_hint = 0.8, 0.3
        self.continue_btn = Button(text='Continue', font_size='10sp')
        self.continue_btn.size_hint = 0.2, 0.3
        self.continue_btn.on_press = self.update_caller
        self.horizontal_input_layout.add_widget(self.address_input)
        self.horizontal_input_layout.add_widget(self.continue_btn)
        self.space = BoxLayout()
        self.space.size_hint = 1, 0.7
        self.add_widget(self.horizontal_input_layout)
        self.add_widget(self.space)

        # Remove Widgets from Start Screen
        amount = 4
        for number in range(0, amount):
            if number == 0:
                  self.remove_widget(self.explanation_label)
            if number == 1:
                self.remove_widget(self.call_btn)
            if number == 2:
                self.remove_widget(self.receive_btn)
            if number == 3:
                self.remove_widget(self.navbar)

    def update_caller(self):
        # Save Address Input
        self.address_input_string = str(self.address_input.text)

        # Reset Input if its wrong (n has to be because of on_dismiss
        def reset(n):
            self.address_input.text = ''

        # Evaluate Address Input
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', self.address_input_string):
            popup = Popup(title='(Click anywhere outside this message box to close it)', content=Label(text='Wrong Input'), size_hint=(None, None), size=(1100, 1100))
            popup.open()
            popup.bind(on_dismiss=reset)

        elif self.address_input_string.split(':')[0] == self.host:
                popup = Popup(title='(Click anywhere outside this message box to close it)',
                              content=Label(text='Host IP can not be\n the same as your listening IP'),
                              size_hint=(None, None), size=(1100, 1100))
                popup.open()
                popup.bind(on_dismiss=reset)

        else:
            # Delete old widgets of Caller Screen 1
            self.remove_widget(self.horizontal_input_layout)
            self.remove_widget(self.address_input)
            self.remove_widget(self.continue_btn)
            self.remove_widget(self.space)

            # UI of updated main layout of Caller
            self.Send_Label_caller = Label(text='Send Messages:')
            self.Send_Label_caller.size_hint = 1, 0.1
            self.Received_Label_caller = Label(text='Received Messages:')
            self.Received_Label_caller.size_hint = 1, 0.1
            self.messages1_caller = TextInput()
            self.messages2_caller = TextInput()
            self.messages1_caller.size_hint = 1, 0.5
            self.messages1_caller.focused = False
            self.messages1_caller.is_focusable = False
            self.messages1_caller.allow_copy = True
            self.messages2_caller.size_hint = 1, 0.5
            self.messages2_caller.focused = False
            self.messages2_caller.is_focusable = False
            self.messages2_caller.allow_copy = True

            # Add all element of main layout UI
            self.add_widget(self.Send_Label_caller)
            self.add_widget(self.messages1_caller)
            self.add_widget(self.Received_Label_caller)
            self.add_widget(self.messages2_caller)

            # Nested Boxlayout containing send button and Text Input Field
            self.nested_boxlayout_caller = BoxLayout()
            self.nested_boxlayout_caller.size_hint = 1, 0.1
            self.add_widget(self.nested_boxlayout_caller)

            # Text Input Field
            self.input_caller = TextInput()
            self.input_caller.hint_text = 'Enter Text here'
            self.input_caller.size_hint = 0.5, 1
            self.nested_boxlayout_caller.add_widget(self.input_caller)

            # Send Button
            self.send_btn_caller = Button()
            self.send_btn_caller.text = 'Send'
            self.send_btn_caller.size_hint = 0.1, 1
            self.send_btn_caller.on_press = self.send_caller
            self.nested_boxlayout_caller.add_widget(self.send_btn_caller)

            # Notification Label that appears when waiting for a connection
            self.notification_caller = Label(font_size='10sp')
            self.notification_caller.size_hint = 1, 0.1
            self.notification_caller.text = 'Error please restart App'
            self.add_widget(self.notification_caller)

            host = self.address_input_string.split(':')[0]
            port = int(self.address_input_string.split(':')[1])
            self.connect(host, port)

    def connect(self, host, port):
        conn_successful = True

        try:
            self.s = socket.socket()
            self.s.settimeout(2)
            try:
                self.s.connect((host, port))
            except socket.timeout:
                conn_successful = False

            if conn_successful:
                self.s.settimeout(None)
                try:
                    self.remove_widget(self.try_again)
                except AttributeError:
                    pass
                self.notification_caller.text = 'Connection with ' + host + ':' + str(port) + ' has been established.'
                self.run_thread_caller()
            else:
                self.notification_caller.text = 'Connection Timeout please try again'
        # ConnectionRefusedError but entering it will crash App
        except:
            self.notification_caller.text = 'Connection to ' + host + ':' + str(port) + ' was refused.'
            try:
                self.remove_widget(self.try_again)
            except AttributeError:
                pass
            self.try_again = Button(text='Try again')
            self.try_again.on_press = partial(self.connect, host, port)
            self.try_again.size_hint = 1, 0.1
            self.add_widget(self.try_again)

    def receive_caller(self):
        while True:
            try:
                received_message = self.s.recv(1024).decode('utf-8')
                if len(received_message) > 0:
                    self.messages2_caller.text += received_message + '\n'
            except ConnectionResetError:
                print('Error')
                self.notification_caller.text = 'Connection Aborted by other participant please try again'

    def send_caller(self):
        q = self.input_caller.text
        try:
            self.s.send(q.encode('ascii'))
        except OSError and socket.error:
            self.notification_caller.text = 'Connection Aborted by other participant please try again'
        self.input_caller.text = ''
        self.messages1_caller.text += q + '\n'

    def run_thread_caller(self):
        thread0 = threading.Thread(target=self.receive_caller, args=())
        thread0.daemon = True
        thread0.start()

    # Receiver Code
    def receiver(self):
        # UI of main layout of Receiver
        self.horizontal_input_layout_receiver = BoxLayout()
        self.horizontal_input_layout_receiver.orientation = 'horizontal'
        self.address_input_receiver = TextInput()
        self.address_input_receiver.hint_text = 'If you use port forwarding enter your forwarded port (Example 5555).\nOtherwise leave this field blank and you automatically get an port assigned.'
        self.address_input_receiver.size_hint = 0.8, 0.3
        self.continue_btn_receiver = Button(text='Continue', font_size='10sp')
        self.continue_btn_receiver.size_hint = 0.2, 0.3
        self.continue_btn_receiver.on_press = self.update_receiver
        self.horizontal_input_layout_receiver.add_widget(self.address_input_receiver)
        self.horizontal_input_layout_receiver.add_widget(self.continue_btn_receiver)
        self.space_receiver = BoxLayout()
        self.space_receiver.size_hint = 1, 0.7
        self.add_widget(self.horizontal_input_layout_receiver)
        self.add_widget(self.space_receiver)

        # Remove Widgets from Start Screen
        amount = 4
        for number in range(0, amount):
            if number == 0:
                self.remove_widget(self.explanation_label)
            if number == 1:
                self.remove_widget(self.call_btn)
            if number == 2:
                self.remove_widget(self.receive_btn)
            if number == 3:
                self.remove_widget(self.navbar)

    def update_receiver(self):
        # Save Address Input
        self.address_input_string_receiver = str(self.address_input_receiver.text)

        # Reset Input if its wrong (n has to be because of on_dismiss
        def reset(n):
            self.address_input_receiver.text = ''

        # Evaluate Address Input
        if not re.match(r'^\d{1,5}', self.address_input_string_receiver) and not self.address_input_string_receiver == '':
            popup = Popup(title='(Click anywhere outside this message box to close it)',
                          content=Label(text='Wrong Input'), size_hint=(None, None), size=(1100, 1100))
            popup.open()
            popup.bind(on_dismiss=reset)

        else:
            # Delete old widgets of Receiver Screen 1
            self.remove_widget(self.horizontal_input_layout_receiver)
            self.remove_widget(self.address_input_receiver)
            self.remove_widget(self.continue_btn_receiver)
            self.remove_widget(self.space_receiver)

            # UI of updated main layout of Receiver
            self.Send_Label = Label(text='Send Messages:')
            self.Send_Label.size_hint = 1, 0.1
            self.Received_Label = Label(text='Received Messages:')
            self.Received_Label.size_hint = 1, 0.1
            self.messages1 = TextInput()
            self.messages2 = TextInput()
            self.messages1.size_hint = 1, 0.5
            self.messages1.focused = False
            self.messages1.is_focusable = False
            self.messages1.allow_copy = True
            self.messages2.size_hint = 1, 0.5
            self.messages2.focused = False
            self.messages2.is_focusable = False
            self.messages2.allow_copy = True

            # Add all element of main layout UI
            self.add_widget(self.Send_Label)
            self.add_widget(self.messages1)
            self.add_widget(self.Received_Label)
            self.add_widget(self.messages2)

            # Nested Boxlayout containing send button and Text Input Field
            self.nested_boxlayout = BoxLayout()
            self.nested_boxlayout.size_hint = 1, 0.1
            self.add_widget(self.nested_boxlayout)

            # Text Input Field
            self.input = TextInput()
            self.input.hint_text = 'Enter Text here'
            self.input.size_hint = 0.5, 1
            self.nested_boxlayout.add_widget(self.input)

            # Send Button
            self.send_btn = Button()
            self.send_btn.text = 'Send'
            self.send_btn.size_hint = 0.1, 1
            self.send_btn.on_press = self.send
            self.nested_boxlayout.add_widget(self.send_btn)

            if self.address_input_string_receiver == '':

                # Notification Label that appears when waiting for a connection
                self.notification = Label(font_size='10sp')
                self.notification.size_hint = 1, 0.1
                self.notification.text = 'Waiting for connections on ' + self.host + ':' + str(self.port)
                self.add_widget(self.notification)

                thread0 = threading.Thread(target=self.wait_for_conn, args=(self.host, self.port))
                thread0.daemon = True
                thread0.start()

            else:
                port = int(self.address_input_string_receiver)

                # Notification Label that appears when waiting for a connection
                self.notification = Label(font_size='10sp')
                self.notification.size_hint = 1, 0.1
                self.notification.text = 'Waiting for connections on ' + self.host + ':' + str(port)
                self.add_widget(self.notification)

                thread0 = threading.Thread(target=self.wait_for_conn, args=(self.host, port))
                thread0.daemon = True
                thread0.start()

        # Remove Widgets from Start Screen
        amount = 4
        for number in range(0, amount):
            if number == 0:
                self.remove_widget(self.explanation_label)
            if number == 1:
                self.remove_widget(self.call_btn)
            if number == 2:
                self.remove_widget(self.receive_btn)
            if number == 3:
                self.remove_widget(self.navbar)

    def send(self):
        q = self.input.text
        try:
            self.c.send(q.encode('ascii'))
        except OSError and socket.error:
            self.notification.text = 'Connection Aborted by other participant please try again'
        self.input.text = ''
        self.messages1.text += q + '\n'

    def receive(self):
        while True:
            try:
                received_message = self.c.recv(1024).decode('utf-8')
                if len(received_message) > 0:
                    self.messages2.text += received_message + '\n'
            except ConnectionResetError and OSError:
                if OSError:
                    self.notification.text = 'Connection Aborted by other participant please try again'
                else:
                    self.notification.text = 'Waiting for connection...'

    def wait_for_conn(self, host, port):
        try:
            self.s.bind((host, port))
            self.s.listen(1)
            print('[Waiting for connection...]')
            self.c, self.address = self.s.accept()
            print('Got connection from', self.address)
            self.run_thread()
            self.notification.text = 'Connection coming from ' + str(self.address).replace(', ', ':').replace('(', '').replace(')', '').replace('\'', '') + ' has been established.'
        except OSError:
            self.notification.text = 'Restart App to make Receiving work again'

    def run_thread(self):
        thread1 = threading.Thread(target=self.receive, args=())
        thread1.daemon = True
        thread1.start()

    @staticmethod
    def exit():
        os._exit(0)


class MyApp(App):
    def build(self):
        return All()


instance = MyApp()

if __name__ == '__main__':
    MyApp.run(instance)
