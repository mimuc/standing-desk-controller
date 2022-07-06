using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;



namespace keymousespeed01
{
    class postToServer
    {
        private static string serverUrl_post = "http://141.84.8.105:5000/commands/add";
        private static readonly HttpClient client = new HttpClient();


        private static int standCommand = 1;
        private static int userID = 1;
        
        

       
        public static async void run()
        {
            var values = new Dictionary<string, string>
            {
                { "command", "1" },
                { "userid", "1" }
            };


            var content = new FormUrlEncodedContent(values);

          
            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, serverUrl_post);
            request.Content = new StringContent($"{{\"command\": {standCommand},\"userid\":{userID}}}",
                                                Encoding.UTF8,
                                                "application/json");//CONTENT-TYPE header

            var response = await client.SendAsync(request);

                 
            Console.WriteLine("Response: {0}", response);
               

        }
    }
}