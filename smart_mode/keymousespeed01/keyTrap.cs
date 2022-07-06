using System;
using System.Diagnostics;
using System.Windows.Forms;
using System.Runtime.InteropServices;

namespace keymousespeed01
{
    class keyTrap
    {
        private const int WH_KEYBOARD_LL = 13;
        private const int WM_KEYDOWN = 0x0100;
        private static LowLevelKeyboardProc _proc = HookCallback;
        private static IntPtr _hookID = IntPtr.Zero;

   
        public static EventHandler<TRAPEVENT> KeyAction;

        public static void Start()
        {
            _hookID = SetHook(_proc);
        }
        public static void stop()
        {
            UnhookWindowsHookEx(_hookID);
        }


        private static IntPtr SetHook(LowLevelKeyboardProc proc)
        {
            // Console.WriteLine("....Set Hook Key");
            using (Process curProcess = Process.GetCurrentProcess())
            using (ProcessModule curModule = curProcess.MainModule)
            {
                return SetWindowsHookEx(WH_KEYBOARD_LL, proc,
                    GetModuleHandle(curModule.ModuleName), 0);
            }
        }

        private delegate IntPtr LowLevelKeyboardProc(
        int nCode, IntPtr wParam, IntPtr lParam);

        private static IntPtr HookCallback(
            int nCode, IntPtr wParam, IntPtr lParam)
        {
            if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN)
            {
                int vkCode = Marshal.ReadInt32(lParam);

               

                //Console.WriteLine((Keys)vkCode);
                if (KeyAction != null)
                {
                    TRAPEVENT te = new TRAPEVENT();
                    te.ks = (Keys)vkCode;
                    te.ms = (MouseMessages)wParam;
                    te.ty = TrapEventType.TRAP_key;
                    te.timeStamp = timeFormat.timeStamp();
                    KeyAction(null, te);
                }


            }

            return CallNextHookEx(_hookID, nCode, wParam, lParam);
        }

        // //    http://stackoverflow.com/questions/115868/how-do-i-get-the-title-of-the-current-active-window-using-c


        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr SetWindowsHookEx(int idHook,
            LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);

        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool UnhookWindowsHookEx(IntPtr hhk);
      

        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode,
            IntPtr wParam, IntPtr lParam);
        
        [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr GetModuleHandle(string lpModuleName);


    }
}
