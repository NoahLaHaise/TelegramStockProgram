#pragma once
#include <string>

class TelegramMessenger{
public:
    TelegramMessenger(const std::string& msg, const std::string& config);
    std::string message;
    bool format_and_send();

private:
    std::string api_url;
    const std::string JSON_CONFIG_PATH;
    void load_api_info();
};