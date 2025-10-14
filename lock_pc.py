import ctypes
import platform

def lock_windows_pc():
    """
    Locks the computer screen. This function is specific to Windows.
    """
    if platform.system() == "Windows":
        print("✅ Lock command received. Locking PC now!")
        try:
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            print(f"Error trying to lock the station: {e}")
    else:
        print(f"Warning: PC locking is only supported on Windows. Current OS: {platform.system()}")
