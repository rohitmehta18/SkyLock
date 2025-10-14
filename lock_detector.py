import ctypes
import time
import platform

def monitor_lock_state(stop_event):
    """
    Runs in a background thread to check if the Windows PC is locked.
    If a lock is detected, it triggers the application's stop_event.
    """
    # This feature is specific to Windows
    if platform.system() != "Windows":
        print("[Lock Detector] This feature is only available on Windows. Thread will not start.")
        return

    print("[Lock Detector] Background thread started. Monitoring for PC lock state.")
    
    while not stop_event.is_set():
        # The Windows API function OpenInputDesktop returns a handle.
        # If it returns 0 (a null handle), it means the input desktop is
        # not accessible, which happens on the lock screen or UAC prompt.
        h_desktop = ctypes.windll.user32.OpenInputDesktop(0, False, 0)
        
        if h_desktop == 0:
            # If we are on the lock screen, the desktop is not accessible.
            print("\n[Lock Detector] ✅ PC lock detected. Initiating graceful shutdown...")
            stop_event.set()
            break # Exit the loop immediately
        else:
            # It's important to close the handle to avoid resource leaks.
            ctypes.windll.user32.CloseDesktop(h_desktop)
            
        # Check the lock state every 2 seconds.
        time.sleep(2)
        
    print("[Lock Detector] Thread stopped.")