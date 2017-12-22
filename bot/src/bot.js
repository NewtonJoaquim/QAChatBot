let env = require('node-env-file');
let filessystem = require('fs');
let os = require('os');
let spawn = require('child_process').spawn;
let request = require('request');
let json = require('jsonify');

env(__dirname + '/.env');

let Botkit = require('botkit');

let controller = Botkit.slackbot({
    clientId: process.env.clientID,
    clientSecret: process.env.clientSecret,
    scopes: ['bot'],
    redirectUri: process.env.redirectUri,
    json_file_store: __dirname + '/.data/db/',
    debug: true,
    interactive_replies: true
});

controller.startTicking();

let bot = controller.spawn({
    token: process.env.token
}).startRTM();


controller.setupWebserver(3000, function (err, webserver) {
// Configure a route to receive webhooks from slack
    controller.createWebhookEndpoints(webserver);
    controller.createOauthEndpoints(webserver);
});

//auxiliar variable to control duplicate replies
let alreadySent = 1;
let command_message = null;

controller.on(['direct_message','direct_mention'], function(bot, message){
   
    let json_text = {
        'data': [
            {
                question: message.text
            }
        ]
    };

    let json_object = json.parse(json.stringify(json_text));

    request({
        url: "http://127.0.0.1:5000/answer",
        method: "POST",
        json: true,   // <--Very important!!!
        body: json_object
    }, function (error, response, body){
        console.log(JSON.stringify(body.data[0]['answer']));
        bot.reply(message, body.data[0]['answer'])
    });

    setTimeout(function(){bot.reply(message, feedback_button())}, 2000);

})

controller.on('interactive_message_callback', function(bot, message){
    let dir = __dirname + '/feedback/' ;
    let subdir_positive = __dirname + '/feedback/positive/';
    let subdir_negative = __dirname + '/feedback/negative/';

    if (!filessystem.existsSync(dir)){
        filessystem.mkdirSync(dir);
        filessystem.mkdirSync(subdir_positive);
        filessystem.mkdirSync(subdir_negative);
    }
    
    switch(message.callback_id){
        case "button_feedback":
            switch(message.actions[0].name){
                case "button_click_no" :
                    bot.reply(message, response1_feedback());
                    break;
                case "button_click_yes" :
                    bot.reply(message, "Obrigado pelo feedback!");

                    let log_text = "texto: " + command_message.text;

                    filessystem.writeFile(__dirname + "/feedback/positive/" + command_message.ts+".txt" , log_text,function(err){
                        if(err) throw err;
                        console.log('success');
                    })
                    break;        
            }
            break;
        case "button_response_feedback":

            let problem, log_text = null;
            let feedback = '';
            switch(message.actions[0].name){
                case "insuf_info" :
                    bot.reply(message, "Obrigado pelo feedback!");

                    log_text = "texto: " + command_message.text + os.EOL;
                    feedback += "informação insuficiente";
                    filessystem.writeFile(__dirname + "/feedback/negative/" + command_message.ts+".txt",log_text + feedback,function(err){
                        if(err) throw err;
                        console.log('success');
                    })
                    break;
                case "wrong_answer" :
                    log_text = "texto: " + command_message.text + os.EOL;
                    problem = "Resposta inesperada" + os.EOL;
                    bot.startPrivateConversation(message, function(err, convo){
                        convo.addQuestion("Qual comando você esperava?", function(response, convo){
                            feedback += "Resposta esperada: " + response.text;
                            filessystem.writeFile(__dirname + "/feedback/negative/" + command_message.ts+".txt",log_text + problem + feedback,function(err){
                                if(err) throw err;
                                console.log('success');
                            })
                            convo.say("sua resposta (" + response.text + ") sera armazenada para analise.");
                            convo.next();
                        },{}, 'default');
                    })
                    break;
                case "other":
                    log_text = "texto: " + command_message.text + os.EOL;
                    problem = "Outro" + os.EOL;
                    bot.startPrivateConversation(message, function(err, convo){
                        convo.addQuestion("Fale-me do seu problema", function(response, convo){
                            feedback += "Problema: " + response.text;
                            filessystem.writeFile(__dirname + "/feedback/negative/" + command_message.ts+".txt",log_text + problem + feedback,function(err){
                                if(err) throw err;
                                console.log('success');
                            })
                            convo.say("sua resposta (" + response.text + ") sera armazenada para analise.");
                            convo.next();
                        }, {}, 'default');
                    })
                    break;
            }
    }
})

function feedback_button(){
    const messageB = {
        "replace_original": true,
        "attachments": [
            {
                "text": "Essa mensagem foi útil?",
                "callback_id": "button_feedback",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "button_click_yes",
                        "text": "sim",
                        "type": "button",
                        "value": "yes"
                    },
                    {
                        "name": "button_click_no",
                        "text": "não",
                        "type": "button",
                        "value": "no"
                    }
                ]
            }
        ]
    };

    return messageB;
}

function response1_feedback(){
    let responseB = {
        "replace_original":true,
        "attachments": [
            {
                "text": "Pode nos informar o problema?",
                "callback_id": "button_response_feedback",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "insuf_info",
                        "text": "Informação insuficiente",
                        "type": "button",
                        "value": "insuf"
                    },
                    {
                        "name": "wrong_answer",
                        "text": "Não era a resposta que eu queria",
                        "type": "button",
                        "value": "wrong"
                    },
                    {
                        "name":"other",
                        "text":"Outro",
                        "type":"button",
                        "value":"other",
                    }
                ]
            }
        ]
    }
    return responseB;
}

function add_question_button(){
    const messageB = {
        "replace_original": true,
        "attachments": [
            {
                "callback_id": "button_add_question",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "button_click_add_question",
                        "text": "Adicionar Pergunta",
                        "type": "button",
                        "value": "yes"
                    }
                ]
            }
        ]
    };
    return responseB;
}