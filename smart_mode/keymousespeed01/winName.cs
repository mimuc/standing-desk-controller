using System;

using System.Text;

using System.Runtime.InteropServices;

namespace keymousespeed01
{
    class winName
    {
        public static string GetActiveWindowTitle()
        {
            const int nChars = 256;
            StringBuilder Buff = new StringBuilder(nChars);
            IntPtr handle = GetForegroundWindow();

            if (GetWindowText(handle, Buff, nChars) > 0)
            {
                return Buff.ToString();
            } else
            { 
                return "...changing...";
            }
        }

        //    http://stackoverflow.com/questions/115868/how-do-i-get-the-title-of-the-current-active-window-using-c
        // ...
        [DllImport("user32.dll")]
        static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll")]
        static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

        // used for private string GetActiveWindowTitle()
    }
}
