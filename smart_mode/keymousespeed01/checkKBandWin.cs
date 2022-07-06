using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace keymousespeed01
{
    class checkKBandWin
    {
        private static String lastWinName = "";
        private static String currentWinName = "";

        private static String lastKBName = "";
        private static String currentKBName = "";

        private static String currentKBLayout = "";

        public static void checkNewKB(System.Windows.Forms.Label ActiveFormKeyboardTypeLabel, System.Windows.Forms.Label KeyboardLayoutLabel)
        {

            currentKBName = keyboardName.getKeyboardName();
            currentKBLayout = keyboardName.getKeyboardLayout();
            ActiveFormKeyboardTypeLabel.Text = currentKBName;
            KeyboardLayoutLabel.Text = currentKBLayout;
            //Console.WriteLine(currentKBName);
            if (!currentKBName.Equals(lastKBName))
            {
                //Console.WriteLine(" Keyboard changed to: " + currentKBName);
                logWriter.write("Keyboard: " + currentKBName + " Layout: " + currentKBLayout, timeFormat.timeStamp());
                lastKBName = currentKBName;
            }

        }

        public static void checkNewWin(System.Windows.Forms.Label ActiveWinLabel, System.Windows.Forms.CheckBox CheckBoxWinPlainText)
        {

            currentWinName = winName.GetActiveWindowTitle();
            ActiveWinLabel.Text = currentWinName;
            if (!currentWinName.Equals(lastWinName))
            {
                //Console.WriteLine(" Forground Window changed to: " + currentWinName);
                if (CheckBoxWinPlainText.Checked == true)
                {
                    logWriter.write("Forground window: " + currentWinName, timeFormat.timeStamp());
                }
                else
                {
                    logWriter.write("Forground window anon: " + convertionFunctions.anonymizeWin(currentWinName), timeFormat.timeStamp());
                }
                lastWinName = currentWinName;
            }

        }
    }
}
