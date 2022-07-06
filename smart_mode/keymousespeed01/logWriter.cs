using System;
using System.IO;


namespace keymousespeed01
{
    class logWriter
    {
        

        public static StreamWriter sw;

        public static void Start(String fileName)
        {
            sw = new StreamWriter(fileName, true);
        }

        public static void stop()
        {
            sw.Close();
        }

        public static void write(String line, String timeMsg ="")
        {    
            sw.WriteLine(timeMsg + line);
        }

        public static void flush()
        {
            sw.Flush();
        }


       

        
    }
}
