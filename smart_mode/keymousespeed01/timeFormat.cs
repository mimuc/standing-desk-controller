using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace keymousespeed01
{
    class timeFormat
    {
        private static string anomFormat = "ddd_HH:mm:ss.fffK";   // Use this format in each line.
        private static DateTime time1, time0;
        private static int timeDiff = 0;
        private static string timeMsg = "";


        public static void Start()
        {
            time0 = DateTime.Now;
            time1 = DateTime.Now;
        }

        public static string timeStamp()
        {
            time1 = DateTime.Now;             // Use current time.
            timeDiff = (int)time1.Subtract(time0).TotalMilliseconds;
            timeMsg = time1.ToString(anomFormat) + " " + timeDiff + " ";
            time0 = time1;
            return timeMsg;
        }

        public static int checkDiff()
        {
            time1 = DateTime.Now;             // Use current time.
            timeDiff = (int)time1.Subtract(time0).TotalMilliseconds;
            return timeDiff;
        }

    }
}
