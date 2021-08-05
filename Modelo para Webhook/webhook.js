var alexa = {
    token: null,
    message: null,
    proxy: null,
    parse_mode: null,

    sendmessage: function() {
        var params = {
          "accessCode": alexa.token,
          "notification": alexa.message
        },
        data,
        response,
        request = new CurlHttpRequest(),
        url = 'https://api.notifymyecho.com/v1/NotifyMe';

        if (alexa.parse_mode !== null) {
            params['parse_mode'] = alexa.parse_mode;
        }

        if (alexa.proxy) {
            request.SetProxy(alexa.proxy);
        }

        request.AddHeader('Content-Type: application/json');
        data = JSON.stringify(params);

        // Remove replace() function if you want to see the exposed token in the log file.
        Zabbix.Log(4, '[Alexa Webhook] URL: ' + url.replace(alexa.token, '<TOKEN>'));
        Zabbix.Log(4, '[Alexa Webhook] params: ' + data);
        response = request.Post(url, data);
        Zabbix.Log(4, '[Alexa Webhook] HTTP code: ' + request.Status());

        try {
            response = JSON.parse(response);
        }
        catch (error) {
            response = null;
        }

        if (request.Status() !== 202) {
            if (typeof response.description === 'string') {
                throw response.description;
            }
            else {
                throw 'Unknown error. Check debug log for more information.'
            }
        }
    }
}

try {
    var params = JSON.parse(value);

    if (typeof params.Token === 'undefined') {
        throw 'Incorrect value is given for parameter "Token": parameter is missing';
    }

    alexa.token = params.Token;

    if (params.HTTPProxy) {
        message.proxy = params.HTTPProxy;
    } 
    if (['Markdown', 'HTML', 'MarkdownV2'].indexOf(params.ParseMode) !== -1) {
        Telegram.parse_mode = params.ParseMode;
    }

    alexa.message = params.subject+ '\n' + params.message;
    alexa.sendmessage();

    return 'OK';
}
catch (error) {
    Zabbix.Log(4, '[Alexa Webhook] notification failed: ' + error);
    throw 'Sending failed: ' + error + '.';
}
