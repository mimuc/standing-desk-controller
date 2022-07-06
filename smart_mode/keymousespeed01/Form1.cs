using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.Runtime.InteropServices;
// https://null-byte.wonderhowto.com/how-to/create-simple-hidden-console-keylogger-c-sharp-0132757/
using System.Management;
using System.Management.Instrumentation;

namespace keymousespeed01
{
    public enum MouseMessages
    {
        WM_LBUTTONDOWN = 0x0201,
        WM_LBUTTONUP = 0x0202,
        WM_MOUSEMOVE = 0x0200,
        WM_MOUSEWHEEL = 0x020A,
        WM_RBUTTONDOWN = 0x0204,
        WM_RBUTTONUP = 0x0205
    }

    public enum TrapEventType
    {
        TRAP_key = 1,
        TRAP_mouse = 2
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct POINT
    {
        public int x;
        public int y;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct MSLLHOOKSTRUCT
    {
        public POINT pt;
        public uint mouseData;
        public uint flags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct TRAPEVENT
    {
        public MSLLHOOKSTRUCT hs;
        public MouseMessages ms;
        public Keys ks;
        public TrapEventType ty;
        public string timeStamp;
    }



    public partial class Form1 : Form
    {
        String anomLogFileName = "";
        private static string fileFormat = "MMddyyyyHHmmss";      // Use this format for filename.
        private static DateTime time1;
       
        int j = 0;

 
 
        public Form1()
        {
            InitializeComponent();

            checkBoxKeyEvents.Checked = true;
            checkBoxMouseEvents.Checked = true;

            time1 = DateTime.Now;
            anomLogFileName = "a_" + time1.ToString(fileFormat) + ".log";
            textBoxLogFileName.Text = Application.StartupPath + @"\" + anomLogFileName;
            logWriter.Start(Application.StartupPath + @"\" + anomLogFileName);

            

            timeFormat.Start();

            checkKBandWin.checkNewKB(KeyboardTypeLabel, KeyboardLayoutLabel);
            checkKBandWin.checkNewWin(ActiveWinLabel, CheckBoxWinPlainText);

            timer1.Interval = 5000;
            timer1.Start();

            mouseTrap.Start();
            keyTrap.Start();
            mouseTrap.MouseAction += myEvent;
            keyTrap.KeyAction += myEvent;

           
            this.FormClosing += Form1_FormClosing;
            this.FormClosed += exitButton_Click;

        }

        private void trayIcon_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            this.Show();
            this.WindowState = FormWindowState.Normal;
            //trayIcon.Visible = false;

        }

        

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            //MessageBox.Show("FormClosing... going to sysTray");

            if (e.CloseReason == CloseReason.UserClosing)
            {
                e.Cancel = true;
                ShowInTaskbar = false;
                this.Hide();
                trayIcon.Visible = true;
             }
        }

        private void myEvent(object sender, TRAPEVENT e)
        {
            // Console.Write(e.ty);

           // currentKBName = keyboardName.getKeyboardName();

            

            if (e.ty == TrapEventType.TRAP_mouse && checkBoxMouseEvents.Checked)
            {
                // Console.WriteLine(" MOUSE: x=" + e.hs.pt.x + " y=" + e.hs.pt.y + " code=" + e.ms);
                logWriter.write(" MOUSE: x=" + e.hs.pt.x + " y=" + e.hs.pt.y + " code=" + e.ms, e.timeStamp);

            }
            if (e.ty == TrapEventType.TRAP_key && checkBoxKeyEvents.Checked)
            {
                // Console.WriteLine(" Key " + (Keys)e.ks);

                if (checkBoxPlainText.Checked == true)
                {
                    logWriter.write(" Key  " + (Keys)e.ks, e.timeStamp);
                }
                else
                {
                    logWriter.write(" gKey " + convertionFunctions.convertKeys((Keys)e.ks), e.timeStamp);
                }
            }


           
            
        }





        private void Form1_Load(object sender, EventArgs e)
        {

        }



        private void exitButton_Click(object sender, EventArgs e)
        {
            logWriter.stop();
            Application.Exit();
        }

        private void hideButton_Click(object sender, EventArgs e)
        {
            ShowInTaskbar = false;
            this.Hide();
            trayIcon.Visible = true;
        }

       
        private void timer1_Tick(object sender, EventArgs e)
        {
            checkKBandWin.checkNewKB(KeyboardTypeLabel, KeyboardLayoutLabel);
            checkKBandWin.checkNewWin(ActiveWinLabel, CheckBoxWinPlainText);
            if (timeFormat.checkDiff() > 60000 && timeFormat.checkDiff() < 64500)
            {
                postToServer.run();
            }
          
            logWriter.flush();

            //Visible = true;

            label4.Text = j.ToString();
            j++;
        }

       

    }



}
