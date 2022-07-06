using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Runtime.InteropServices;

namespace keymousespeed01
{
    class convertionFunctions

    {
        public static string convertKeys(Keys realkey)
        {
            char k;
            k = (char)realkey;

            if (char.IsLetter(k))
            {
                return("L");
            }
            else if (char.IsDigit(k))
            {
                return("D");
            }
            else if (realkey == Keys.Back)
            {
                return("Back");
            }
            else if (char.IsWhiteSpace(k))
            {
                return("WhiteSpace");
            }
            else if (char.IsSymbol(k))
            {
                return("Symbol");
            }
            else
            {
                return(realkey.ToString());
            }
        }

        public static string anonymizeWin(string winName)
        {
            if (winName.ToLower().Contains("word"))
            {
                return("WORD");
            }
            else if (winName.ToLower().Contains("excel"))
            {
                return ("EXCEL");
            }
            else if (winName.ToLower().Contains("powerpoint"))
            {
                return ("PPT");
            }
            else if (winName.ToLower().Contains("gmail"))
            {
                return ("GMAIL");
            }
            else if (winName.ToLower().Contains("twitter"))
            {
                return ("TWITTER");
            }
            else if (winName.ToLower().Contains("facebook"))
            {
                return ("FACEBOOK");
            }
            else if (winName.ToLower().Contains("chorme"))
            {
                return ("CHROME");
            }
            else if (winName.ToLower().Contains("firefox"))
            {
                return ("FIREFOX");
            }
            else if (winName.ToLower().Contains("visual studio"))
            {
                return ("VISUAL_STUDIO");
            }
            else if (winName.ToLower().Contains("edge"))
            {
                return("EDGE");
            }
            else
            {
                return("WIN");
            }
        }
    }
}
