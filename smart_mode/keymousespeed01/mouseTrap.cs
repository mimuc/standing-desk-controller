using System;
using System.Diagnostics;
using System.Runtime.InteropServices;


namespace keymousespeed01
{
    public  class mouseTrap
    {
        private const int WH_MOUSE_LL = 14;

        public static EventHandler<TRAPEVENT> MouseAction;

        public static void Start()
        {
            _hookID = SetHook(_proc);
        }

        public static void stop()
        {
            UnhookWindowsHookEx(_hookID);
        }

        private static LowLevelMouseProc _proc = HookCallback;
        private static IntPtr _hookID = IntPtr.Zero;

        private static IntPtr SetHook(LowLevelMouseProc proc)
        {
            // Console.WriteLine("....Set Hook Mouse");
            using (Process curProcess = Process.GetCurrentProcess())
            using (ProcessModule curModule = curProcess.MainModule)
            {
                return SetWindowsHookEx(WH_MOUSE_LL, proc,
                  GetModuleHandle(curModule.ModuleName), 0);
            }
        }

        private delegate IntPtr LowLevelMouseProc(int nCode, IntPtr wParam, IntPtr lParam);

        private static IntPtr HookCallback(
          int nCode, IntPtr wParam, IntPtr lParam)
        {
             
            if (nCode >= 0)  // && MouseMessages.WM_LBUTTONDOWN == (MouseMessages)wParam)
            {
                MSLLHOOKSTRUCT hookStruct = (MSLLHOOKSTRUCT)Marshal.PtrToStructure(lParam, typeof(MSLLHOOKSTRUCT));

                if (MouseAction != null)
                {
                    TRAPEVENT te = new TRAPEVENT();
                    te.hs = hookStruct;
                    te.ms = (MouseMessages)wParam;
                    te.ty = TrapEventType.TRAP_mouse;
                    te.timeStamp = timeFormat.timeStamp();
                    MouseAction(null, te);
                }

            }

            //  }
            return CallNextHookEx(_hookID, nCode, wParam, lParam);
        }



 
       

        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr SetWindowsHookEx(int idHook,
          LowLevelMouseProc lpfn, IntPtr hMod, uint dwThreadId);

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
