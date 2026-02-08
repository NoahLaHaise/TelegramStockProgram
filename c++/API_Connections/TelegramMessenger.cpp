#include "TelegramMessenger.h"
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <fstream>
#include <iostream>

/*
msg is the message you would to send to telegram
config_file_path is the path to config.json file that has the url endpoint. 
*/
TelegramMessenger::TelegramMessenger(const std::string& msg, const std::string& config_file_path) : message(msg), 
                                                                                          api_url(""),
                                                                                          JSON_CONFIG_PATH(config_file_path)
{
    std::cout << "CONFIG_PATH: " << JSON_CONFIG_PATH << std::endl;
    load_api_info();
}

void TelegramMessenger::load_api_info()
{
    std::ifstream file(JSON_CONFIG_PATH);
    if (file)
    {
        auto config = nlohmann::json::parse(file);

        if (config["TELEGRAM_ENDPOINT"].is_null())
            throw std::runtime_error("CANNOT CONTINUE, NO API URL AVAILABLE FOR TELEGRAM");
        else
            api_url = config["TELEGRAM_ENDPOINT"];
    }
}

bool TelegramMessenger::format_and_send()
{
    CURL* curl = curl_easy_init();

    if(curl)
    {
        char* encoded = curl_easy_escape(curl, message.c_str(), 0);
        std::string url_and_message = api_url + encoded;
        curl_free(encoded);

        curl_easy_setopt(curl, CURLOPT_URL, url_and_message.c_str());
        CURLcode res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);

        if(res == CURLE_OK)     
            return true;

        std::cerr << "curl error: " << curl_easy_strerror(res) << std::endl;

    }

    return false;

}
