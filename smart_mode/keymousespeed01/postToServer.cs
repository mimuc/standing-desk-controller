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
        private static string serverUrl_post = "";
        private static readonly HttpClient client = new HttpClient();


        private static string username = "Bettina";
        
        

       
        public static async void run()
        {

            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, serverUrl_post);

            Console.WriteLine("Request: {0}", request);

            request.Content = new StringContent($"{{\"username\": \"{username}\"}}",
                                                Encoding.UTF8,
                                                "application/json");//CONTENT-TYPE header

            var response = await client.SendAsync(request);

                 
            Console.WriteLine("Response: {0}", response);
               

        }
    }
}